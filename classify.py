import re, math
from typing import List, Dict, Optional
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class StanceNLI:
    def __init__(self, model_name: str = "microsoft/deberta-v3-large-mnli"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tok = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(self.device).eval()
        self.idx2lbl = {0:"contradiction", 1:"neutral", 2:"entailment"}

    def _score_pair(self, premise: str, hypothesis: str) -> Dict[str, float]:
        enc = self.tok(premise, hypothesis, truncation=True, max_length=512, return_tensors="pt").to(self.device)
        with torch.no_grad():
            logits = self.model(**enc).logits[0]
        probs = torch.softmax(logits, dim=-1).detach().cpu().tolist()
        return {self.idx2lbl[i]: float(p) for i, p in enumerate(probs)}

    def score_long_premise(self, text: str, hypothesis: str, max_tokens: int = 450) -> Dict[str, object]:
        sents = [s.strip() for s in re.split(r'(?<=[\.\?!])\s+', text) if s.strip()]
        windows, cur = [], ""
        for s in sents:
            tok_len = len(self.tok.tokenize(cur + " " + s))
            if tok_len > max_tokens and cur:
                windows.append(cur.strip()); cur = s
            else:
                cur = (cur + " " + s).strip()
        if cur: windows.append(cur)

        best_e = best_c = 0.0
        best_e_snip = best_c_snip = ""
        for w in windows or [text]:
            sc = self._score_pair(w, hypothesis)
            if sc["entailment"] > best_e:
                best_e, best_e_snip = sc["entailment"], w[:500]
            if sc["contradiction"] > best_c:
                best_c, best_c_snip = sc["contradiction"], w[:500]

        return {
            "entailment": best_e,
            "contradiction": best_c,
            "neutral": max(0.0, 1.0 - max(best_e, best_c)),
            "best_support_snippet": best_e_snip,
            "best_oppose_snippet": best_c_snip,
        }

def label_from_probs(ent: float, con: float, thr: float = 0.6, margin: float = 0.05) -> str:
    if ent >= thr and ent >= con + margin:
        return "support"
    if con >= thr and con >= ent + margin:
        return "oppose"
    return "neutral"

def stance_search_and_classify(idx, stance: str, topk_retrieval: int = 80, topn_return: int = 30,
                               nli_model: Optional[StanceNLI] = None) -> Dict[str, List[Dict]]:
    nli = nli_model or StanceNLI()

    hits = idx.search(stance, k_ann=200, k_bm25=200, topn=topk_retrieval)

    labeled = []
    for h in hits:
        txt = h.get("Content") or h.get("Snippet") or ""
        sc = nli.score_long_premise(txt, stance)
        lbl = label_from_probs(sc["entailment"], sc["contradiction"])
        h2 = h.copy()
        h2.update({
            "stance_label": lbl,
            "support_conf": round(sc["entailment"], 4),
            "oppose_conf": round(sc["contradiction"], 4),
            "support_snippet": sc["best_support_snippet"],
            "oppose_snippet": sc["best_oppose_snippet"],
        })
        labeled.append(h2)

    support = sorted([d for d in labeled if d["stance_label"] == "support"],
                     key=lambda x: x["support_conf"], reverse=True)[:topn_return]
    oppose  = sorted([d for d in labeled if d["stance_label"] == "oppose"],
                     key=lambda x: x["oppose_conf"], reverse=True)[:topn_return]
    neutral = [d for d in labeled if d["stance_label"] == "neutral"][:topn_return]

    return {"support": support, "oppose": oppose, "neutral": neutral}
