import os 
from langgraph.prebuilt import create_react_agent
from langgraph.graph.message import add_messages # helper function to add messages to the state
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json 

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

issue = f""" 
Whether the arbitral tribunal has jurisdiction over an environmental counterclaim brought by the host state under the relevant arbitration clause.
"""
og_prompt = f"""
    I’m working on a case representing Fenoscadia Limited, a mining company from Ticadia that was operating in Kronos under an 80-year concession to extract lindoro, a rare earth metal. In 2016, Kronos passed a decree that revoked Fenoscadia’s license and terminated the concession agreement, citing environmental concerns. The government had funded a study that suggested lindoro mining contaminated the Rhea River and caused health issues, although the study didn’t conclusively prove this. Kronos is now filing an environmental counterclaim in the ongoing arbitration, seeking at least USD 150 million for environmental damage, health costs, and water purification.
    Can you help me analyze how to challenge Kronos’s environmental counterclaim, especially in terms of jurisdiction, admissibility, and merits?
"""

cases = {
    "supporting":  ["cases_20250617/234.json"], 
    "opposing":  ["cases_20250617/254.json"]
}

def pull_cases(cases):
    res =  {
       "supporting":{}, 
       "opposing": {}
    }

    for case in cases["supporting"]: 
        with open(case, 'r') as f:
            data = json.load(f)
            res["supporting"]=data

    for case in cases["opposing"]: 
        with open(case, 'r') as f:
            data = json.load(f)
            res["opposing"]=data 
            
    return res




def case_builder(issue, og_prompt, cases) -> str: 
    
    system_prompt = f"""
        You are a lawyer that specialises in arbitration case building with regards to {issue}
    """
    prompt = f"""
        Your colleague came to you with this problem: '{og_prompt}' and wants to tackle it in the context of this issue: '{issue}'. He has pulled out the relevant cases that support or oppose the arguement: '{pull_cases(cases)}'. 
        
        Your goal is to build a case that your colleague can use to argue his point with regards to the issue.

        You are free to determine what sections should be in your case. But your case should minimally have the following sections: 
        - State the core issue
        - Breifly recap your case theme
        - Emphasise strongest evidence
        - Damages and relief sought
        - Conclusion
    """
    # Create LLM class
    llm = ChatGoogleGenerativeAI(
        model= "gemini-2.5-pro",
        temperature=1.0,
        max_retries=2,
        google_api_key=api_key,
    )

    # Test the model with tools
    agent = create_react_agent(
        model=llm,  
        tools=[],
        prompt=system_prompt
    )

    # Call agent
    res=agent.invoke({
        "messages": [
            {"role": "user", 
                "content": prompt
            }
        ]
    })

    return res["messages"][-1].content


res = case_builder(issue, og_prompt, cases)
print(res)