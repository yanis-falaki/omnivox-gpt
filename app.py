from main import run_llm
import streamlit as st
from streamlit_chat import message
from langchain.memory import ConversationBufferMemory

# sets streamlit to wide mode
st.set_page_config(layout="wide")

st.header("Omnivox Digital Assistant")

prompt = st.text_input("Prompt", placeholder="Enter your prompt here...")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "agent_memory" not in st.session_state:
    st.session_state["agent_memory"] =  ConversationBufferMemory(memory_key="chat_history", return_messages=True)


if prompt:
    with st.spinner("Generating Response"):
        generated_response = run_llm(
            question=prompt, memory=st.session_state["agent_memory"]
        )
        st.session_state["chat_history"].append((prompt, generated_response))


if st.session_state["chat_history"]:
    for prompt, generated_response in st.session_state["chat_history"]:
        message(prompt, is_user=True)
        message(generated_response, is_user=False)