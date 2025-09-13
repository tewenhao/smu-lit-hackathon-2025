from typing import Union
import json
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


origins = [
        "http://localhost:3000",  # Example: your frontend application
        "https://yourfrontenddomain.com",
        # You can add more origins here
]
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# {
#       thought: "Analyzing the case scenario for applicable legal precedents, relevant arbitration rules, and similar dispute outcomes. Examining jurisdictional requirements, procedural timelines, and evidentiary standards that will govern this arbitration proceeding.",
#       output: "**Key Legal Precedents Found:**\n\n• *International Trading Co. v. Manufacturing Corp* (2022) - Similar breach of contract scenario with 85% damages awarded\n• *Construction Alliance v. Development Ltd* (2023) - Precedent for delay-based damages in commercial disputes\n• **Applicable Rules:** UNCITRAL Arbitration Rules, ICC Rules Art. 25 (document production)\n\n**Jurisdictional Analysis:**\n• Arbitration clause appears valid and enforceable\n• Estimated timeline: 6-8 months for full proceedings\n• Success rate for similar cases: 73% favorable outcomes for claimants"
#     },
#     // Case Builder Analysis  
#     {
#       thought: "Structuring the legal arguments by identifying the strongest claims, organizing supporting evidence chronologically, and developing a compelling narrative that establishes clear liability, causation, and quantifiable damages.",
#       output: "**Primary Legal Arguments:**\n\n1. **Material Breach of Contract**\n   - Clear violation of delivery timelines (Section 4.2)\n   - Failure to meet quality specifications\n   - Non-compliance with notification requirements\n\n2. **Causation & Damages Framework**\n   - Direct losses: $125,000 in additional costs\n   - Consequential damages: Lost profits $85,000\n   - Mitigation expenses: $15,000\n\n3. **Evidence Portfolio**\n   - 47 supporting documents organized by category\n   - Email correspondence establishing timeline\n   - Expert witness testimony on industry standards"
#     },
#     // Weakness Identifier Analysis
#     {
#       thought: "Examining potential vulnerabilities in our position, anticipating counterarguments from opposing counsel, and identifying areas where additional evidence or different strategic approaches might strengthen the case.",
#       output: "**Critical Vulnerabilities Identified:**\n\n⚠️ **High Risk Issues:**\n• Client's 45-day delay in formal breach notice may limit damages recovery\n• Email suggesting acceptance of modified delivery terms could undermine breach claim\n• Force majeure clause (Section 9.3) provides defendant strong defense\n\n⚠️ **Medium Risk Concerns:**\n• Damage calculations rely heavily on projected profits (speculative)\n• Incomplete documentation for Q3 2024 period\n• Potential contributory negligence in vendor selection\n\n**Recommended Mitigation:**\n• Gather evidence of continuing breach doctrine applicability\n• Strengthen damages with industry comparables and expert analysis\n• Document all good faith mitigation efforts undertaken"
#     },
#     // Concluder Analysis
#     {
#       thought: "Synthesizing all team inputs to provide strategic recommendations, assess overall case viability, estimate probable outcomes, and suggest optimal procedural approaches for achieving client objectives.",
#       output: "**Strategic Assessment & Recommendations:**\n\n🎯 **Overall Case Strength: 7.5/10**\n• Strong liability case with solid precedential support\n• Damages well-documented but some vulnerability to reduction\n• Procedural compliance generally sound\n\n**Recommended Strategy:**\n1. **Pre-Arbitration:** Attempt structured settlement ($150-180K range)\n2. **Arbitration Track:** Request expedited proceedings (4-6 month timeline)\n3. **Evidence Focus:** Prioritize continuing breach narrative, strengthen damages calculation\n\n**Probable Outcomes:**\n• 75% chance of favorable liability finding\n• Expected damages recovery: $165-220K (65-85% of claim)\n• Estimated total costs: $85-125K\n• **Recommendation:** Proceed with arbitration while remaining open to reasonable settlement above $160K"
#     }



class Payload(BaseModel):
    context: str
    prompt: str 
    tone: str

@app.post("/generate/result")
def read_item(payload: Payload):
    # Calls workflow.py
    print(payload)

    return {
        "user_context": "User context", 
        "user_prompt": "user prompt",
        "thoughts": {
            "researcher": {
                "thought": "Analyzing the case scenario for applicable legal precedents, relevant arbitration rules, and similar dispute outcomes. Examining jurisdictional requirements, procedural timelines, and evidentiary standards that will govern this arbitration proceeding.",
                "output": "**Key Legal Precedents Found:**\n\n• *International Trading Co. v. Manufacturing Corp* (2022) - Similar breach of contract scenario with 85% damages awarded\n• *Construction Alliance v. Development Ltd* (2023) - Precedent for delay-based damages in commercial disputes\n• **Applicable Rules:** UNCITRAL Arbitration Rules, ICC Rules Art. 25 (document production)\n\n**Jurisdictional Analysis:**\n• Arbitration clause appears valid and enforceable\n• Estimated timeline: 6-8 months for full proceedings\n• Success rate for similar cases: 73% favorable outcomes for claimants"
            }, 
            "case_builder": {
                "thought": "Structuring the legal arguments by identifying the strongest claims, organizing supporting evidence chronologically, and developing a compelling narrative that establishes clear liability, causation, and quantifiable damages.",
                "output": "**Primary Legal Arguments:**\n\n1. **Material Breach of Contract**\n   - Clear violation of delivery timelines (Section 4.2)\n   - Failure to meet quality specifications\n   - Non-compliance with notification requirements\n\n2. **Causation & Damages Framework**\n   - Direct losses: $125,000 in additional costs\n   - Consequential damages: Lost profits $85,000\n   - Mitigation expenses: $15,000\n\n3. **Evidence Portfolio**\n   - 47 supporting documents organized by category\n   - Email correspondence establishing timeline\n   - Expert witness testimony on industry standards"
            }, 
            "concluder": {
                "thought": "Synthesizing all team inputs to provide strategic recommendations, assess overall case viability, estimate probable outcomes, and suggest optimal procedural approaches for achieving client objectives.",
                "output": "**Strategic Assessment & Recommendations:**\n\n🎯 **Overall Case Strength: 7.5/10**\n• Strong liability case with solid precedential support\n• Damages well-documented but some vulnerability to reduction\n• Procedural compliance generally sound\n\n**Recommended Strategy:**\n1. **Pre-Arbitration:** Attempt structured settlement ($150-180K range)\n2. **Arbitration Track:** Request expedited proceedings (4-6 month timeline)\n3. **Evidence Focus:** Prioritize continuing breach narrative, strengthen damages calculation\n\n**Probable Outcomes:**\n• 75% chance of favorable liability finding\n• Expected damages recovery: $165-220K (65-85% of claim)\n• Estimated total costs: $85-125K\n• **Recommendation:** Proceed with arbitration while remaining open to reasonable settlement above $160K" 
            },
            "weakness identifier": {
                "thought": "Examining potential vulnerabilities in our position, anticipating counterarguments from opposing counsel, and identifying areas where additional evidence or different strategic approaches might strengthen the case.",
                "output": "**Critical Vulnerabilities Identified:**\n\n⚠️ **High Risk Issues:**\n• Client's 45-day delay in formal breach notice may limit damages recovery\n• Email suggesting acceptance of modified delivery terms could undermine breach claim\n• Force majeure clause (Section 9.3) provides defendant strong defense\n\n⚠️ **Medium Risk Concerns:**\n• Damage calculations rely heavily on projected profits (speculative)\n• Incomplete documentation for Q3 2024 period\n• Potential contributory negligence in vendor selection\n\n**Recommended Mitigation:**\n• Gather evidence of continuing breach doctrine applicability\n• Strengthen damages with industry comparables and expert analysis\n• Document all good faith mitigation efforts undertaken"
            }, 
        }, 
        "final_report": "final report"
    }
