from dotenv import load_dotenv
load_dotenv()

import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage

system_prompt = "Act as an AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt):
    
    # Use selected LLM (Groq)
    llm = ChatGroq(model=llm_id)   

    # Optional Tavily Web Search
    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    # Create LangChain agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    # Input messages must be a list of LC-format dicts
    state = {"messages": query}

    response = agent.invoke(state)
    messages = response.get("messages", [])

    ai_messages = [m.content for m in messages if isinstance(m, AIMessage)]

    return ai_messages[-1] if ai_messages else "No response from agent."
