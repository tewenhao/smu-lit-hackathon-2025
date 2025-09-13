"""
Agent that takes in a list of mini-concluding statements from the case builder, and formulatses a final concluding statement.
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
    prompt=dedent(
        """
        You are a 'Legal Assistant' agent. Your task is to synthesize the provided mini-concluding statements into a single, coherent, and persuasive final concluding statement. Ensure that the final statement effectively summarizes the key points and arguments presented in the mini-conclusions. The final statement should be concise, clear, and impactful, suitable for use in a legal context.
        """
    )
)

# ---- Using the module ----
def concluder(user_texts: list) -> str:
    """Generate a final concluding statement from the user texts."""
    combined_text = "\n\n".join(user_texts)
    res = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": combined_text
                }
            ]
        }
    )

    result = res['messages'][-1].content
    return result

# ---- Example Run ----
if __name__ == '__main__':
    # import docx

    # def getText(filename):
    #     doc = docx.Document(filename)
    #     fullText = []
    #     for para in doc.paragraphs:
    #         fullText.append(para.text)
    #     return '\n'.join(fullText)

    example_texts = [
        "Issue: Whether Kronos can bootstrap jurisdiction for its environmental counterclaim onto Fenoscadia's validly initiated investment arbitration. Conclusion: Kronos's attempt to transform a contract-based investment dispute into an environmental tort tribunal fundamentally exceeds the parties' original consent to arbitrate. The asymmetrical arbitration clause grants only investors the right to initiate proceedings, creating no reciprocal pathway for state claims. By seeking affirmative relief through an independent USD 150 million counterclaim rather than a defensive set-off, Kronos improperly expands the tribunal's mandate beyond the investment protection framework the parties agreed to. The tribunal must dismiss this jurisdictional overreach to preserve the integrity of consent-based arbitration.",
        "Issue: Whether Kronos has established sufficient evidentiary basis for its USD 150 million environmental damages claim. Conclusion: Kronos's counterclaim collapses under its own evidentiary inadequacy, with the government's own study admittedly failing to 'conclusively prove' the alleged causal link between Fenoscadia's operations and environmental harm. This failure to meet the basic burden of proof for causation renders the entire USD 150 million claim speculative and unsuitable for arbitral determination. Investment arbitration requires concrete, proven damages flowing from established breaches, not conjecture about potential environmental consequences. The tribunal should reject this unfounded attempt to impose retroactive liability based on inconclusive evidence.",
        "Issue: Whether environmental tort claims arising from mining operations fall within the scope of disputes 'arising out of' the investment concession agreement.Conclusion: Kronos's environmental counterclaim represents a fundamental category error that confuses contractual performance with societal impact regulation. While the mining operations occurred under the concession agreement, the alleged environmental damages sound in public tort law rather than contract interpretation or breach. The parties never intended their commercial arbitration clause to establish the tribunal as an environmental regulator with authority over broader societal harm claims. Such claims belong in domestic courts with proper environmental law expertise, not in an investment arbitration forum designed to protect contractual rights and treaty obligations.",
        "Issue: Whether allowing the environmental counterclaim would improperly convert investment arbitration into a general civil liability forum. Conclusion: Permitting Kronos's environmental counterclaim would dangerously transform investment arbitration from a specialized investor protection mechanism into a general forum for any state grievance tangentially related to foreign investment operations. This jurisdictional expansion would fundamentally alter the bilateral investment treaty framework and encourage forum shopping by host states seeking to avoid their own domestic courts' environmental law procedures. Investment tribunals lack both the institutional competence and the parties' consent to adjudicate broad public policy claims that properly belong before domestic environmental courts with appropriate regulatory expertise and remedial powers.",
        "Issue: Whether allowing the environmental counterclaim would improperly convert investment arbitration into a general civil liability forum. Conclusion: Permitting Kronos's environmental counterclaim would dangerously transform investment arbitration from a specialized investor protection mechanism into a general forum for any state grievance tangentially related to foreign investment operations. This jurisdictional expansion would fundamentally alter the bilateral investment treaty framework and encourage forum shopping by host states seeking to avoid their own domestic courts' environmental law procedures. Investment tribunals lack both the institutional competence and the parties' consent to adjudicate broad public policy claims that properly belong before domestic environmental courts with appropriate regulatory expertise and remedial powers."
    ]

    final_conclusion = concluder(example_texts)
    print(final_conclusion)