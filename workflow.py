"""Workflow which strings everything together"""

from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- LLM Setup ---
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.2,
    max_retries=2,
    api_key=GEMINI_API_KEY)

# --- Define State Graph ---
from typing import TypedDict

# class State(TypedDict):
#     """The state of the workflow"""

#     # initial inputs
#     context: str
#     user_prompt: str
#     tone: str

#     # decomposer states
#     sub_issues: list[str]

#     # issues states
#     issue_datadump: dict[str, dict[str, str]]

#     # concluder states
#     final_output: str

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
    print(resp)

def case_builder_node(issue: str, original_prompt: str, cases: dict[str, list[dict]], tone: str) -> str:
    """Build a case for the given issue"""
    from case_builder import case_builder_agent
    from weakness_identifier import weakness_identifier_agent
    from langgraph_supervisor import create_supervisor

    case_builder_agent = case_builder_agent(issue, original_prompt, cases, tone)
    weakness_identifier_agent = weakness_identifier_agent()

    supervisor = create_supervisor(
        model=llm,
        agents=[case_builder_agent, weakness_identifier_agent],
        prompt="You are a supervisor agent. Your task is to first use the Case Builder agent to construct a detailed case for the given issue, incorporating relevant cases and adhering to the specified tone. After the case is built, you will then use the Weakness Identifier agent to analyze the constructed case and identify any potential weaknesses in the argument. Then, regenerate the case to address these weaknesses, ensuring a robust and well-rounded argument. You will regenerate the case atmost three times. Your final output should be a comprehensive and persuasive case that effectively addresses the issue at hand.",
    ).compile()

    final_case = supervisor.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"Build a case for the issue: '{issue}' with the original prompt: '{original_prompt}'. These are the relevant cases: '{cases}'. Use a {tone} tone."
            }
        ]
    })

    print(final_case)

# --- Define workflow ---
def workflow(context: str, user_prompt: str, tone: str) -> str:
    """Main workflow function"""

    state = {
        "context": context,
        "user_prompt": user_prompt,
        "tone": tone,
    }

    state["sub_issues"] = decomposer_node(state["context"], state["user_prompt"])
    
    for issue in state["sub_issues"]:
        researcher_node(issue)
        break

if __name__ == "__main__":
    workflow("context", "user_prompt", "tone")
    # issue = f""" 
    # Whether the arbitral tribunal has jurisdiction over an environmental counterclaim brought by the host state under the relevant arbitration clause.
    # """
    # og_prompt = f"""
    #     I’m working on a case representing Fenoscadia Limited, a mining company from Ticadia that was operating in Kronos under an 80-year concession to extract lindoro, a rare earth metal. In 2016, Kronos passed a decree that revoked Fenoscadia’s license and terminated the concession agreement, citing environmental concerns. The government had funded a study that suggested lindoro mining contaminated the Rhea River and caused health issues, although the study didn’t conclusively prove this. Kronos is now filing an environmental counterclaim in the ongoing arbitration, seeking at least USD 150 million for environmental damage, health costs, and water purification.
    #     Can you help me analyze how to challenge Kronos’s environmental counterclaim, especially in terms of jurisdiction, admissibility, and merits?
    # """

    # cases = {
    #     "supporting":  ["cases_20250617/cases_20250617/234.json"], 
    #     "opposing":  ["cases_20250617/cases_20250617/254.json"]
    # }
    # case_builder_node(issue, og_prompt, cases, "formal")