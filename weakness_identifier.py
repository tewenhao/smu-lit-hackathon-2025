"""
Agent which takes in a closing statement and identifies potential weaknesses in the argument.
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
    # if possible, add in what lawyers actually look out for and attack
    prompt="You are a 'Legal Assistant' agent. Your sole task is to analyze the provided closing statement and identify potential weaknesses in the argument. Present these weaknesses as a continuous paragraph. Do not use bullet points. Do not classify them as themes. Do not include any other text, analysis, or preamble. Your entire response must be just the list of weaknesses.",
    name="weakness_identifier_agent"
)

# ---- Helper functions ----
def get_weaknesses(result: str) -> list[str]:
    """Extract weaknesses from the agent's result string."""
    lines = result.split("\n")
    weaknesses = [line.strip("* ").strip() for line in lines if line.startswith("*")]
    return weaknesses


# ---- Using the module ----
def weakness_identifier(user_text: str) -> list[str]:
    """Identify weaknesses in the user text."""
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
    # weaknesses = get_weaknesses(result)
    # return weaknesses
    return result

# this is a version of weakness identifier which returns the agent itself
def weakness_identifier_agent() -> ChatGoogleGenerativeAI:
    """Return the agent for external use."""
    return agent

# ---- Example Run ----
if __name__ == '__main__':
    import docx

    def getText(filename):
        doc = docx.Document(filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    
    # text = getText('temp-files/closing_statement_sample.docx')
    text = getText('temp-files/sample_case_builder_document.docx')
    results = weakness_identifier(text)
    print(results)
