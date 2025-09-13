import os
import re
import json
import uuid
import tiktoken
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter, TokenTextSplitter

enc = tiktoken.get_encoding("cl100k_base")

def split_on_headings(text:str)->List[str]:
    parts = re.split(r'\*\*[IVXL]+\.[A-Z\s]+\*\*', text)
    return [p.strip() for p in parts if p.strip()]

token_splitter = TokenTextSplitter(
    encoding_name="cl100k_base",
    chunk_size=700,
    chunk_overlap=90,
)

def process_json(fpath: str) -> Dict:
    with open(fpath) as f:
        doc = json.load(f)
        out = []
        # Every key in the json except for "Decisions" which is the bulk of the content
        base = {k: doc.get(k) for k in [
            "Identifier","Title","CaseNumber","Industries","Status",
            "PartyNationalities","Institution","RulesOfArbitration","ApplicableTreaties"
        ]}
        for d_idx, d in enumerate(doc.get("Decisions", [])):
            content = d.get("Content","") or ""
            if not content.strip(): continue
            for sec_idx, sec in enumerate(split_on_headings(content) or [content]):
                for i, piece in enumerate(token_splitter.split_text(sec)):
                    out.append({
                        **base,  # base metadata for the whole json file
                        "DecisionTitle": d.get("Title"),
                        "DecisionType": d.get("Type"),
                        "DecisionDate": d.get("Date"),
                        "Content": piece,
                        "Span": "dec{}_sec{}_chunk{}".format(d_idx, sec_idx, i),
                        "ChunkID": "{}|{}|{}|{}".format(doc["Identifier"], d_idx, sec_idx, i)
                    })
        return out

def process_data(data_dir: str = "cases_20250617") -> List[Dict]:
    chunks = []
    for f in os.listdir(data_dir):
        chunks.extend(process_json(os.path.join(data_dir, f)))
    return chunks