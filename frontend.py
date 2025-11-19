# ********* Phase-3 (Setup FrontEnd) ***************

import streamlit as st
import requests

# Page Settings
st.set_page_config(page_title="LangGraph Agent UI", layout="centered")
st.header("Agentic AI Chatbot Application")
st.write("Create and Interact with the AI Agents!")

# Sidebar
st.sidebar.title("Agentic AI Chatbot")
st.sidebar.image(
    "https://miro.medium.com/v2/resize:fit:1400/1*hdd2IGtXs3E8rsa98m-kCg.png",
    caption="Your Agentic AI Assistant",
    use_container_width=True
)

st.sidebar.title("Instructions 📜")
st.sidebar.markdown("""
1. Enter a persona or system prompt.  
2. Select your Groq model.  
3. Optional: enable web search.  
4. Enter your query.  
5. Ask the agent!  
""")

# Input Fields
system_prompt = st.text_area(
    "Define your AI Agent:", 
    height=70, 
    placeholder="Type your system prompt here..."
)

MODEL_NAMES_GROQ = [
    "llama-3.3-70b-versatile",
    "mixtral-8x7b-32768"
]

# Removed provider since backend is now Groq-only
selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)

allow_web_search = st.checkbox("Allow Web Search")

user_query = st.text_area("Enter your query:", height=150, placeholder="Ask Anything!")

API_URL = "http://127.0.0.1:9999/chat"

# Button
if st.button("Ask Agent!"):
    if user_query.strip():
        
        # FIXED: messages must be list of dicts
        payload = {
            "model_name": selected_model,
            "system_prompt": system_prompt,
            "messages": [
                {"role": "user", "content": user_query}
            ],
            "allow_search": allow_web_search
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            response_data = response.json()

            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                st.write(response_data)
        else:
            st.error("Backend error. Check FastAPI console for details.")
