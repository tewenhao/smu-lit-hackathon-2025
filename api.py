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
            "case_builder": {
                "output": "**Primary Legal Arguments:**\n\n1. **Material Breach of Contract**\n   - Clear violation of delivery timelines (Section 4.2)\n   - Failure to meet quality specifications\n   - Non-compliance with notification requirements\n\n2. **Causation & Damages Framework**\n   - Direct losses: $125,000 in additional costs\n   - Consequential damages: Lost profits $85,000\n   - Mitigation expenses: $15,000\n\n3. **Evidence Portfolio**\n   - 47 supporting documents organized by category\n   - Email correspondence establishing timeline\n   - Expert witness testimony on industry standards"
            }, 
            "concluder": {
                "output": "**Strategic Assessment & Recommendations:**\n\n🎯 **Overall Case Strength: 7.5/10**\n• Strong liability case with solid precedential support\n• Damages well-documented but some vulnerability to reduction\n• Procedural compliance generally sound\n\n**Recommended Strategy:**\n1. **Pre-Arbitration:** Attempt structured settlement ($150-180K range)\n2. **Arbitration Track:** Request expedited proceedings (4-6 month timeline)\n3. **Evidence Focus:** Prioritize continuing breach narrative, strengthen damages calculation\n\n**Probable Outcomes:**\n• 75% chance of favorable liability finding\n• Expected damages recovery: $165-220K (65-85% of claim)\n• Estimated total costs: $85-125K\n• **Recommendation:** Proceed with arbitration while remaining open to reasonable settlement above $160K" 
            },
            "weakness identifier": {

                "output": "**Critical Vulnerabilities Identified:**\n\n⚠️ **High Risk Issues:**\n• Client's 45-day delay in formal breach notice may limit damages recovery\n• Email suggesting acceptance of modified delivery terms could undermine breach claim\n• Force majeure clause (Section 9.3) provides defendant strong defense\n\n⚠️ **Medium Risk Concerns:**\n• Damage calculations rely heavily on projected profits (speculative)\n• Incomplete documentation for Q3 2024 period\n• Potential contributory negligence in vendor selection\n\n**Recommended Mitigation:**\n• Gather evidence of continuing breach doctrine applicability\n• Strengthen damages with industry comparables and expert analysis\n• Document all good faith mitigation efforts undertaken"
            }, 
        }, 
        "final_report": """
        
### STATE THE CORE ISSUE

The central, fatal flaw in Kronos’s strategy is this: **The arbitral tribunal has absolutely no jurisdiction to hear this environmental counterclaim.** The State’s consent to arbitration under the investment treaty is a shield for the investor, not a sword for the State. Kronos is attempting to twist a dispute resolution mechanism designed to protect foreign investment into a forum to litigate its domestic tort claims. We will not allow it.

### BRIEF RECAP OF OUR CASE THEME

Our theme is simple and aggressive: **This counterclaim is an illegitimate, bad-faith litigation tactic designed to intimidate and offset liability for an illegal expropriation.** Kronos expropriated our asset using a flimsy environmental pretext, and now that they're facing a massive damages award, they've manufactured a counterclaim to muddy the waters. It's a procedural ambush, and we're going to expose it as a flagrant abuse of the arbitral process. We will argue that the tribunal lacks jurisdiction, that the claim is inadmissible as an abuse of process, and that, on the merits, it is utterly baseless.

### EMPHASISE STRONGEST EVIDENCE: THE JURISDICTIONAL ASSAULT

This is where we land the killing blow. Jurisdiction is not a suggestion; it is a hard-line requirement, and Kronos fails to meet it. Our argument is built on the fundamental principle of consent in arbitration.

**1. Lack of Consent is Fatal to Jurisdiction**

Arbitration is a creature of consent. No party can be forced into it. Where did Fenoscadia consent to be hauled into an international tribunal to answer for alleged domestic environmental torts? It didn’t. The arbitration clause in the concession agreement and the underlying treaty is a unilateral offer of consent *from Kronos to Fenoscadia*. It allows the *investor* to bring claims against the *State* for breaches of the treaty. It is not a two-way street. By filing its Request for Arbitration, Fenoscadia accepted Kronos's offer to arbitrate *Fenoscadia's claims*. It did not, by any stretch of legal logic, issue an open invitation for Kronos to sue it back.

**2. The Asymmetry of the Arbitration Clause**

The case law you’ve pulled is perfect for this. We will hammer the reasoning implicit in *Unión Fenosa Gas v. Egypt*. That case arose under the same Spain-Egypt BIT as the *Cementos* case, a model often replicated. Article 11 of that treaty states that a dispute "shall be submitted, **at the choice of the investor**."

This language is our primary weapon. It’s not ambiguous. It frames the entire dispute resolution process around the investor’s initiative. The investor chooses the forum. The investor brings the claim. The State’s role is that of a respondent, nothing more. This asymmetrical structure is the bedrock of investor-state arbitration. To allow a host-state counterclaim of this nature would be to rewrite the treaty, an act this tribunal has no power to do. Kronos is a respondent, and it should act like one. Its attempt to become a claimant is a jurisdictional overreach that must be shut down immediately.

**3. The Counterclaim Falls Outside the Jurisdictional Grant**

Even if the tribunal were to entertain the fantasy that it could hear a counterclaim, it must be inextricably linked to the primary claim and fall within the treaty's definition of a dispute "arising directly out of an investment." Kronos’s claim doesn’t.

*   **This is a Domestic Tort Claim:** Kronos is alleging environmental damage, public health costs, and water purification needs. These are classic domestic tort claims based on alleged breaches of Kronos's own environmental laws. The proper forum for such claims is the domestic courts of Kronos, where Fenoscadia would be subject to the full procedural rights and obligations of that system. This tribunal was not constituted to interpret and apply Kronos’s domestic environmental regulatory framework.
*   **No "Nexus" to the Expropriation Claim:** Our claim is that Kronos illegally expropriated our concession. Their counterclaim is that our operations caused environmental damage. While they used the *pretext* of environmental concerns for the expropriation, their claim for monetary damages is a separate legal issue. It is not a defense to expropriation; it is an independent claim for damages that must stand on its own feet in the proper forum. The nexus is tenuous at best and contrived for litigation purposes.

We will argue that the tribunal must narrowly construe its jurisdiction, and this counterclaim is squarely outside of it. Do not let them get away with arguments of "procedural economy." Procedural economy cannot create jurisdiction where none exists.

### SECONDARY ARGUMENTS: ADMISSIBILITY AND MERITS

If the tribunal shows any weakness on jurisdiction, we pivot immediately to admissibility and merits.

**1. Admissibility: This is a Clear Abuse of Process**

Kronos operated with Fenoscadia for years. If these environmental concerns were so dire, where were the administrative actions? Where were the fines? Where were the court orders? They didn't exist. Instead, Kronos waited until it needed a pretext for expropriation, funded a "study" that conveniently supported its goal without proving anything, and then terminated an 80-year concession.

Filing this counterclaim now, only after we've brought our claim for compensation, is a textbook case of abuse of process. It is a retaliatory measure, not a genuine legal claim. It should be dismissed as inadmissible to protect the integrity of this arbitration.

**2. Merits: Demolish Their "Evidence"**

On the off-chance this claim survives the jurisdictional and admissibility challenges, we will tear it apart on the merits.
*   **Burden of Proof:** The burden rests entirely on Kronos. They must prove, with clear and convincing evidence, that Fenoscadia's specific actions directly caused the specific damages claimed.
*   **The Inconclusive Study:** Their entire case rests on a study that "didn’t conclusively prove" the link. We will hire the world's best experts to dismantle this study, expose its flawed methodologies, its unproven assumptions, and its biased conclusions. We will show it for what it is: junk science commissioned to justify a political decision.
*   **Compliance:** We will prove that Fenoscadia complied with every applicable environmental law and standard in Kronos during its operations. If Kronos now wants to apply new, retroactive standards, that is in itself a violation of the fair and equitable treatment standard.

### DAMAGES AND RELIEF SOUGHT

Our position is unwavering. We demand the following:

1.  A declaration that the tribunal **lacks jurisdiction** over the environmental counterclaim.
2.  In the alternative, a declaration that the counterclaim is **inadmissible** as an abuse of process.
3.  In the further alternative, a **complete dismissal** of the counterclaim on the merits with prejudice.
4.  An order that Kronos bear **100% of the costs** incurred by Fenoscadia in defending against this frivolous and vexatious counterclaim, including all legal fees, expert fees, and administrative costs.

### CONCLUSION

Make no mistake: this counterclaim is a desperate gamble by a State that knows it is liable for a massive expropriation award. It is procedurally improper, jurisdictionally baseless, and factually unsubstantiated. We will not be distracted or intimidated. We will force the tribunal to confront the fundamental limits of its authority. The consent to arbitrate flows one way in this context. We will dismantle Kronos’s jurisdictional arguments brick by brick, expose their claim as a sham, and ensure it is dismissed with the contempt it deserves. Now get back to work and make it happen.        """
    }
