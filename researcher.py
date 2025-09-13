import re, json, math, numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from chunker import process_data
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm
import torch
import os

def normalize_text(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def build_tfidf(chunks: List[Dict], min_df=2, max_df=0.9) -> Tuple[TfidfVectorizer, np.ndarray, List[str], List[Dict]]:
    """
    chunks: list of dicts with at least {'ChunkID','Content', ...}
    Returns: fitted vectorizer, TF-IDF csr matrix (docs x vocab), chunk_ids, metas (WITHOUT Content)
    """
    texts = [normalize_text(c["Content"]) for c in chunks]
    vec = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1,2),
        min_df=min_df, max_df=max_df,
        token_pattern=r"(?u)\b\w+\b",
        stop_words="english"
    )
    X = vec.fit_transform(texts)
    chunk_ids = [c["ChunkID"] for c in chunks]
    metas = [{k:v for k,v in c.items() if k!="Content"} for c in chunks]
    return vec, X, chunk_ids, metas

def tfidf_search(vec, X, query: str, topk=20) -> List[int]:
    q_vec = vec.transform([normalize_text(query)])
    scores = (X @ q_vec.T).toarray().ravel()
    if topk >= len(scores): 
        return np.argsort(-scores).tolist()
    part = np.argpartition(-scores, topk)[:topk]
    return part[np.argsort(-scores[part])].tolist()

class NLIStance:
    def __init__(self, model_name="ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tok = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(self.device).eval()
        self.idx2lbl = {0:"contradiction", 1:"neutral", 2:"entailment"}

    def score_pair(self, premise: str, hypothesis: str) -> Dict[str,float]:
        enc = self.tok(premise, hypothesis, truncation=True, max_length=512, return_tensors="pt").to(self.device)
        with torch.no_grad():
            logits = self.model(**enc).logits[0]
        probs = torch.softmax(logits, dim=-1).detach().cpu().numpy().tolist()
        return {"contradiction": probs[0], "neutral": probs[1], "entailment": probs[2]}

    def score_long(self, text: str, hypothesis: str, max_tokens=200):
        sents = [s.strip() for s in re.split(r'(?<=[\.\?!])\s+', text) if s.strip()]
        windows, cur = [], ""
        for s in sents:
            tlen = len(self.tok.tokenize((cur+" "+s).strip()))
            if tlen > max_tokens and cur:
                windows.append(cur); cur = s
            else:
                cur = (cur + " " + s).strip()
        if cur: windows.append(cur)
        best_e, best_c, snip_e, snip_c = 0.0, 0.0, "", ""
        for w in windows or [text]:
            sc = self.score_pair(w, hypothesis)
            if sc["entailment"] > best_e: best_e, snip_e = sc["entailment"], w[:500]
            if sc["contradiction"] > best_c: best_c, snip_c = sc["contradiction"], w[:500]
        neutral = max(0.0, 1.0 - max(best_e, best_c))
        return {"entailment": best_e, "contradiction": best_c, "neutral": neutral,
                "support_snippet": snip_e, "oppose_snippet": snip_c}

def label(ent, con, thr=0.6, margin=0.05):
    if ent >= thr and ent >= con + margin: return "support"
    if con >= thr and con >= ent + margin: return "oppose"
    return "neutral"

def issue_search_and_label(chunks: List[Dict], issue_prompt: str, stance_text: str,
                           id2name: Dict[str, str],
                           topk_retrieval=150, topn_return=40) -> Dict[str, List[Dict]]:
    vec, X, ids, metas = build_tfidf(chunks)
    idxs = tfidf_search(vec, X, issue_prompt, topk=topk_retrieval)

    nli = NLIStance()
    results = []
    for i in tqdm(idxs):
        c = chunks[i]
        sc = nli.score_long(c["Content"], stance_text)
        results.append({
            **metas[i],
            "fname": id2name[metas[i]["Identifier"]],
            "ChunkID": ids[i],
            "support_conf": round(sc["entailment"],4),
            "oppose_conf": round(sc["contradiction"],4),
            "stance_label": label(sc["entailment"], sc["contradiction"]),
            "support_snippet": sc["support_snippet"],
            "oppose_snippet": sc["oppose_snippet"]
        })

    support = sorted([r for r in results if r["stance_label"]=="support"], key=lambda x: x["support_conf"], reverse=True)[:topn_return]
    oppose  = sorted([r for r in results if r["stance_label"]=="oppose"],  key=lambda x: x["oppose_conf"],   reverse=True)[:topn_return]
    neutral = [r for r in results if r["stance_label"]=="neutral"][:topn_return]
    return {"support": support, "oppose": oppose, "neutral": neutral}

def reverse_map(data_dir: str = "cases_20250617") -> Dict:
    """
    Map the case identifier to the filename
    """
    mapping = {}
    for fname in os.listdir(data_dir):
        with open(os.path.join(data_dir, fname)) as f:
            data = json.load(f)
            mapping[data["Identifier"]] = fname
    return mapping


if __name__ == "__main__":
    chunks = process_data()
    id2name = reverse_map()
    issue_prompt = "Whether the arbitral tribunal has jurisdication over an environmental counterclaim brought by the host state (Kronos) under the relevant arbitration clause."
    stance = "Fenoscadia has not consented to arbitrate claims brought by Kronos."
    resp = issue_search_and_label(chunks, issue_prompt, stance, id2name)
    print(resp)
