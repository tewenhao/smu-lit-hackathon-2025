import os, json, math, hashlib
from pathlib import Path
from typing import List, Dict, Tuple
from tqdm import tqdm
from chunk import process_data

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

class Paths:
    def __init__(self, index_dir: str):
        self.dir = Path(index_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.meta_jsonl = self.dir / "meta.jsonl"      # one JSON per line (stores Content + metadata)
        self.id_map_json = self.dir / "rowid_to_chunkid.json"  # ["ChunkID0","ChunkID1",...]
        self.config_json = self.dir / "config.json"    # model name etc.
        self.faiss_index = self.dir / "faiss.index"
        self.bm25_tokens_json = self.dir / "bm25_tokens.json"  # tokenized docs to avoid re-tokenizing on load

def _tokenize(text: str) -> List[str]:
    return text.lower().split()

def _hash_dict(d: dict) -> str:
    return hashlib.sha1(json.dumps(d, sort_keys=True).encode("utf-8")).hexdigest()

def build_index_from_chunks(chunks: List[Dict], index_dir: str, model_name="sentence-transformers/all-mpnet-base-v2"):
    P = Paths(index_dir)

    seen = set()
    clean_chunks = []
    for c in chunks:
        cid = c["ChunkID"]
        if cid not in seen:
            seen.add(cid)
            clean_chunks.append(c)

    with P.meta_jsonl.open("w", encoding="utf-8") as f:
        for c in clean_chunks:
            meta = {k: v for k, v in c.items() if k == "ChunkID"}
            f.write(json.dumps(meta, ensure_ascii=False) + "\n")

    model = SentenceTransformer(model_name)
    texts = [c["Content"] for c in clean_chunks]
    embs = model.encode(texts, normalize_embeddings=True)
    embs = np.asarray(embs, dtype="float32")

    dim = embs.shape[1]
    index = faiss.IndexHNSWFlat(dim, 32)
    index.hnsw.efConstruction = 200
    index.add(embs)
    faiss.write_index(index, str(P.faiss_index))

    row_to_id = [c["ChunkID"] for c in clean_chunks]
    P.id_map_json.write_text(json.dumps(row_to_id, ensure_ascii=False), encoding="utf-8")

    tokenized = [ _tokenize(t) for t in texts ]
    P.bm25_tokens_json.write_text(json.dumps(tokenized), encoding="utf-8")

    cfg = {"model_name": model_name, "num_docs": len(clean_chunks), "dim": int(dim)}
    P.config_json.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

    print(f"Built index in {P.dir}  |  docs={len(clean_chunks)}  dim={dim}")

class LocalHybridIndex:
    def __init__(self, index_dir: str):
        self.P = Paths(index_dir)
        if not self.P.faiss_index.exists() or not self.P.id_map_json.exists() or not self.P.meta_jsonl.exists():
            raise FileNotFoundError()

        self.cfg = json.loads(self.P.config_json.read_text(encoding="utf-8"))
        self.model = SentenceTransformer(self.cfg["model_name"])
        self.faiss = faiss.read_index(str(self.P.faiss_index))
        self.row_to_id = json.loads(self.P.id_map_json.read_text(encoding="utf-8"))

        tokenized = json.loads(self.P.bm25_tokens_json.read_text(encoding="utf-8"))
        self.bm25 = BM25Okapi(tokenized)

        self._offsets = {}
        with self.P.meta_jsonl.open("rb") as f:
            pos = 0
            for line in f:
                obj = json.loads(line)
                self._offsets[obj["ChunkID"]] = (pos, len(line))
                pos += len(line)

    def _get_meta(self, chunk_id: str) -> Dict:
        start, length = self._offsets[chunk_id]
        with self.P.meta_jsonl.open("rb") as f:
            f.seek(start)
            line = f.read(length)
            return json.loads(line)

    def search(self, query: str, k_ann=200, k_bm25=200, topn=25, rrf_k=60) -> List[Dict]:
        q = self.model.encode(query, normalize_embeddings=True).astype("float32")[None, :]
        sims, idxs = self.faiss.search(q, k_ann)
        ann = []
        for j, row_id in enumerate(idxs[0]):
            if row_id == -1: continue
            ann.append( (self.row_to_id[row_id], float(sims[0][j])) )

        bm_scores = self.bm25.get_scores(_tokenize(query))
        top_rows = np.argpartition(-bm_scores, min(k_bm25, len(bm_scores)-1))[:k_bm25]
        bm = [(self.row_to_id[int(i)], float(bm_scores[int(i)])) for i in top_rows]
        bm.sort(key=lambda x: x[1], reverse=True)

        def rrf(lst):
            return {doc_id: 1.0/(rrf_k+rank) for rank,(doc_id,_) in enumerate(lst, start=1)}

        ann_rrf = rrf(ann)
        bm_rrf  = rrf(bm)
        fused = {}
        for d,s in ann_rrf.items(): fused[d] = fused.get(d,0.0) + s
        for d,s in bm_rrf.items():  fused[d] = fused.get(d,0.0) + s

        top_ids = sorted(fused.keys(), key=lambda k: fused[k], reverse=True)[:topn]
        results = [self._get_meta(cid) | {"_score": fused[cid]} for cid in top_ids]
        return results

    def add_chunks(self, new_chunks: List[Dict]):
        existing = set(self.row_to_id)
        new_chunks = [c for c in new_chunks if c["ChunkID"] not in existing]
        if not new_chunks:
            print("No new chunks to add.")
            return

        with self.P.meta_jsonl.open("a", encoding="utf-8") as f:
            for c in new_chunks:
                meta = {k: v for k, v in c.items() if k == "ChunkID"}
                f.write(json.dumps(meta, ensure_ascii=False) + "\n")

        texts = [c["Content"] for c in new_chunks]
        new_embs = self.model.encode(texts, normalize_embeddings=True)
        new_embs = np.asarray(new_embs, dtype="float32")
        self.faiss.add(new_embs)
        faiss.write_index(self.faiss, str(self.P.faiss_index))

        self.row_to_id.extend([c["ChunkID"] for c in new_chunks])
        self.P.id_map_json.write_text(json.dumps(self.row_to_id, ensure_ascii=False), encoding="utf-8")

        tokenized = json.loads(self.P.bm25_tokens_json.read_text(encoding="utf-8"))
        tokenized.extend([ _tokenize(t) for t in texts ])
        self.P.bm25_tokens_json.write_text(json.dumps(tokenized), encoding="utf-8")
        self.bm25 = BM25Okapi(tokenized)

        self.cfg["num_docs"] = len(self.row_to_id)
        self.P.config_json.write_text(json.dumps(self.cfg, indent=2), encoding="utf-8")

        print(f"Added {len(new_chunks)} chunks. New total: {len(self.row_to_id)}")

if __name__ == "__main__":
    chunks = process_data()

    # Build once
    build_index_from_chunks(chunks, index_dir=os.path.join(os.getcwd(), "case_index"))

    # Load & search
    # idx = LocalHybridIndex("my_index")
    # hits = idx.search("Contamination of water bodies due to asbestos", topn=5)
    # for h in hits:
    #     print(h["ChunkID"], round(h["_score"], 4))
    #     print(h["Content"][:200].replace("\n"," "), "...\n")
