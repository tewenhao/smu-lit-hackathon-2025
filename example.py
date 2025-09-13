from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---- LLM Setup ----
from langchain_google_genai import ChatGoogleGenerativeAI

# create LLM class
llm = ChatGoogleGenerativeAI(
    model= "gemini-2.5-pro",
    temperature=1.0,
    max_retries=2,
    google_api_key=GEMINI_API_KEY,
)

# tool binding if needed
# xyz tools

# ---- Agent Setup ----
from langgraph.prebuilt import create_react_agent

def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    model=llm,  
    tools=[get_weather],  
    prompt="You are a helpful assistant"  
)

# Run the agent
res = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(res)