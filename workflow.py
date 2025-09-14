"""Workflow which strings everything together"""

from dotenv import load_dotenv
import os
from textwrap import dedent
from pprint import pp

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- LLM Setup ---
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.2,
    max_retries=2,
    api_key=GEMINI_API_KEY)

# --- Define Nodes ---
def decomposer_node(context: str, user_prompt: str) -> list[str]:
    """Decompose the user prompt into sub-issues"""
    from decomposer import decomposer

    # combine context and user_prompt
    combined_prompt = f"<context>\n{context}</context>\n\n<user_prompt>\n{user_prompt}\n</user_prompt>"
    sub_issues = decomposer(combined_prompt)

    return sub_issues

# insert researcher and sorter nodes here
def researcher_node(issue: str, stance: str = "Fenoscadia has not consented to arbitrate claims brought by Kronos."):
    from researcher import process_data, issue_search_and_label, reverse_map

    chunks = process_data()
    id2name = reverse_map()
    resp = issue_search_and_label(chunks, issue, stance, id2name)
    return resp

def case_builder_node(issue: str, og_prompt: str, cases: dict[str, list[dict]], tone: str) -> str:
    """Build a case for the given issue"""
    from case_builder import case_builder
    final_case = case_builder(issue, og_prompt, cases, tone)
    return final_case

def concluder_node(all_conclusions: list[str]) -> str:
    """Conclude the final output from all conclusions"""
    from concluder import concluder

    final_output = concluder(all_conclusions)
    return final_output

# add weakness identifier node here
def weakness_identifier_node(user_text: str) -> list[str]:
    """Identify weaknesses in the user text"""
    from weakness_identifier import weakness_identifier

    weaknesses = weakness_identifier(user_text)
    return weaknesses

# --- Define workflow ---
def workflow(context: str, user_prompt: str, tone: str) -> str:
    """Main workflow function"""

    state = {
        "context": context,
        "user_prompt": user_prompt,
        "tone": tone,
    }

    print('Setting up decomposition')
    state["sub_issues"] = decomposer_node(state["context"], state["user_prompt"])
    
    for issue in state["sub_issues"]:
        state[issue] = {}
        print('Setting up research for issue:', issue)
        state[issue]['case'] = researcher_node(issue)
        print("Setting up conclusion for issue:", issue)
        state[issue]['conclusion'] = case_builder_node(issue, state["user_prompt"], state[issue]['case'], state["tone"])

    print("Setting up conclusion")
    state["all_conclusions"] = [state[issue]['conclusion'] for issue in state["sub_issues"]]

    print("Final output")
    state["final_output"] = concluder_node(state["all_conclusions"])
    state["weaknesses"] = weakness_identifier_node(state["final_output"])

    with open('output.txt', 'w') as file:
        file.write(str(state))

    return state["final_output"]

if __name__ == "__main__":
    context = dedent("""
    You are assisting a legal team representing the Fenoscadia Limited, a large mining company doing its activities in Republic of Kronos. Fenoscadia and Kronos have signed a concession agreement allowing it to exploit a site in Kronos for 80 years.

    In 2015, Kronos passed a new Environmental Act (KEA), requiring companies to protect local waters from toxic waste. In 2016, following a government-funded university study suggesting that Fenoscadia's work may have contaminated the Rhea River (Kronos' main water source), Kronos issued Presidential Decree No. 2424. This decree revoked Fenoscadia's license, terminated the concession agreement, and banned lindoro exploitation altogether.

    A dispute arose.

    Fast forward to the middle of the arbitration proceedings, Kronos is seeking to file an environmental counterclaim against Fenoscadia during arbitration proceedings, alleging:

    Contamination of the Rhea River due to graspel, a toxic component released during mining;

    Health impacts, including increased cardiovascular disease rates;

    Costs of cleanup, alternative water supplies, and healthcare, estimated at USD 150 million.

    An environmental counterclaim is essentially the host state's legal response claiming that the investor caused environmental damage, such as pollution or deforestation. The state uses this counterclaim to avoid paying compensation for the investor's original claims of unfair treatment and losses.

    The legal team's mission is to prepare a closing statement for Fenoscadia, aimed at persuading the tribunal to reject the environmental counterclaim.
    """)
    user_prompt = dedent("""I'm working on a case representing Fenoscadia Limited, a mining company from Ticadia that was operating in Kronos under an 80-year concession to extract lindoro, a rare earth metal. In 2016, Kronos passed a decree that revoked Fenoscadia's license and terminated the concession agreement, citing environmental concerns. The government had funded a study that suggested lindoro mining contaminated the Rhea River and caused health issues, although the study didn't conclusively prove this. Kronos is now filing an environmental counterclaim in the ongoing arbitration, seeking at least USD 150 million for environmental damage, health costs, and water purification.

    Can you help me analyze how to challenge Kronos's environmental counterclaim, especially in terms of jurisdiction, admissibility, and merits?""")
    tone = "aggressive"
    print(workflow(context, user_prompt, tone))