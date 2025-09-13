"""
Agent which takes in a problem statement and decomposes it into smaller subissues for further processing.

Note to frontend dev:
- between `context_example` and `context_detailed`, `context_detailed` performs better
- so need to have 2 inputs, one for the prompt itself, and one for the detailed context, then we just concatenate them together
"""

from dotenv import load_dotenv
import os
from textwrap import dedent

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---- LLM Setup ----
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model= "gemini-2.5-pro",
    temperature=0.3,
    max_retries=2,
    google_api_key=GEMINI_API_KEY,
)

# ---- Agent Setup ----
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=llm,
    tools=[],
    prompt="You are a 'Legal Assistant' agent. Your sole task is to analyze the provided problem statement and identify the specific legal sub-issues. Present these sub-issues as a list. Do not classify them as themes. Do not include any other text, analysis, or preamble. Your entire response must be just the list of legal sub-issues."
)

# ---- Helper functions ----
def get_subissues(result: str) -> list[str]:
    """Extract sub-issues from the agent's result string."""
    lines = result.split("\n")
    subissues = [line.strip("* ").strip() for line in lines if line.startswith("*")]
    return subissues

# ---- Using the module ----
def decomposer(user_text: str) -> list[str]:
    """Decompose the user text into sub-issues."""
    res = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        }
    )

    result = res['messages'][-1].content
    subissues = get_subissues(result)
    return subissues

# ---- Example Run ----
if __name__ == "__main__":
    # context_example = dedent("""
    # I’m working on a case representing Fenoscadia Limited, a mining company from Ticadia that was operating in Kronos under an 80-year concession to extract lindoro, a rare earth metal. In 2016, Kronos passed a decree that revoked Fenoscadia’s license and terminated the concession agreement, citing environmental concerns. The government had funded a study that suggested lindoro mining contaminated the Rhea River and caused health issues, although the study didn’t conclusively prove this. Kronos is now filing an environmental counterclaim in the ongoing arbitration, seeking at least USD 150 million for environmental damage, health costs, and water purification.

    # Can you help me analyze how to challenge Kronos’s environmental counterclaim, especially in terms of jurisdiction, admissibility, and merits?
    # """)

    context_detailed = dedent("""
    <context>
    You are assisting a legal team representing the Fenoscadia Limited, a large mining company doing its activities in Republic of Kronos. Fenoscadia and Kronos have signed a concession agreement allowing it to exploit a site in Kronos for 80 years.

    In 2015, Kronos passed a new Environmental Act (KEA), requiring companies to protect local waters from toxic waste. In 2016, following a government-funded university study suggesting that Fenoscadia’s work may have contaminated the Rhea River (Kronos' main water source), Kronos issued Presidential Decree No. 2424. This decree revoked Fenoscadia’s license, terminated the concession agreement, and banned lindoro exploitation altogether.

    A dispute arose.

    Fast forward to the middle of the arbitration proceedings, Kronos is seeking to file an environmental counterclaim against Fenoscadia during arbitration proceedings, alleging:

    Contamination of the Rhea River due to graspel, a toxic component released during mining;

    Health impacts, including increased cardiovascular disease rates;

    Costs of cleanup, alternative water supplies, and healthcare, estimated at USD 150 million.

    An environmental counterclaim is essentially the host state’s legal response claiming that the investor caused environmental damage, such as pollution or deforestation. The state uses this counterclaim to avoid paying compensation for the investor’s original claims of unfair treatment and losses.

    👉 The legal team’s mission is to prepare a closing statement for Fenoscadia, aimed at persuading the tribunal to reject the environmental counterclaim.
    </context>

    <user prompt>
    I’m working on a case representing Fenoscadia Limited, a mining company from Ticadia that was operating in Kronos under an 80-year concession to extract lindoro, a rare earth metal. In 2016, Kronos passed a decree that revoked Fenoscadia’s license and terminated the concession agreement, citing environmental concerns. The government had funded a study that suggested lindoro mining contaminated the Rhea River and caused health issues, although the study didn’t conclusively prove this. Kronos is now filing an environmental counterclaim in the ongoing arbitration, seeking at least USD 150 million for environmental damage, health costs, and water purification.

    Can you help me analyze how to challenge Kronos’s environmental counterclaim, especially in terms of jurisdiction, admissibility, and merits?
    </user prompt>
    """)

    # context_detailed = dedent("""
    # You are a legal advisor for Triton Spire Industries, a multinational energy company specializing in deep-sea resource extraction. In 2012, Triton Spire signed a 50-year agreement with the Republic of Aethelgard to build and operate a massive floating platform to harvest rare-earth minerals from a deep-ocean trench within Aethelgard's exclusive economic zone.

    # In 2020, Aethelgard passed a new Marine Heritage and Preservation Act (MHPA), which designated certain marine habitats as protected zones. Shortly after, a government-sponsored scientific expedition discovered a unique species of bioluminescent coral near Triton Spire’s platform. Following this, the President of Aethelgard issued a decree, Presidential Edict No. 1991, revoking Triton Spire's permits, terminating the concession agreement, and prohibiting all deep-sea resource extraction in its waters.

    # A dispute arose, leading to an international arbitration.

    # Fast forward to the arbitration proceedings. Aethelgard has filed a counterclaim against Triton Spire, alleging:

    # Destruction of a pristine marine ecosystem and an uncatalogued species of coral due to Triton Spire's sonic drilling operations.

    # Irreversible damage to the ocean floor, impacting the entire food chain in the region.

    # Costs for a 20-year ecological restoration project, including a scientific research fund and reparations to local fishing communities, estimated at USD 250 million.

    # This environmental counterclaim is a legal maneuver by the host state to argue that the investor's actions caused significant ecological damage. By doing so, the state aims to avoid paying compensation for the investor’s original claims, such as wrongful termination of the contract and lost profits.

    # 👉 Your legal team’s mission is to prepare a persuasive closing statement for Triton Spire, arguing that the tribunal should reject Aethelgard's environmental counterclaim.

    # Example Prompt for the AI:
    # I'm advising Triton Spire Industries, an energy company from the Federated Republics of Valerion, on an arbitration case against the Republic of Aethelgard. We had a 50-year agreement to extract deep-sea minerals, but Aethelgard terminated it with Presidential Edict No. 1991, citing environmental concerns over a newly discovered bioluminescent coral. Aethelgard's government claims our sonic drilling operations destroyed the ecosystem and is now seeking a USD 250 million counterclaim for restoration and research.

    # Can you help me analyze how to challenge Aethelgard’s environmental counterclaim, specifically by focusing on issues of jurisdiction, admissibility, and the merits of their claims?
    # """)

    for i in range(5):
        print("\n\n\n")
        print(f"======== Iteration {i+1} ========")
        res = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": context_detailed
                    }
                ]
            }
        )

        result = res['messages'][-1].content
        subissues = get_subissues(result)
        print(subissues)