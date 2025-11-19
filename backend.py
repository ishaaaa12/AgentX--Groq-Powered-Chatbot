# ********** Phase-2 (Setup Backend with FastAPI) **************

from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

# ---- FIXED: Message format ----
class Message(BaseModel):
    role: str
    content: str

class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[Message]
    allow_search: bool


# ---- FIXED: Removed OpenAI models ----
ALLOWED_MODEL_NAMES = [
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "llama-3.3-70b-versatile"
]

app = FastAPI(title="LangGraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):

    # Validate model
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid Groq model."}

    llm_id = request.model_name
    query = [msg.model_dump() for msg in request.messages]   # convert pydantic → dict
    allow_search = request.allow_search
    system_prompt = request.system_prompt

    # ---- FIXED: No provider needed ----
    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt)
    
    return response


# Run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)
