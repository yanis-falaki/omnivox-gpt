from main import run_llm
import streamlit as st
from streamlit_chat import message

# sets streamlit to wide mode
st.set_page_config(layout="wide")

st.header("Omnivox Digital Assistant")

prompt = st.text_input("Prompt", placeholder="Enter your prompt here...")

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answer_history" not in st.session_state:
    st.session_state["chat_answer_history"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


if prompt:
    with st.spinner("Generating Response"):
        generated_response = run_llm(
            question=prompt#, chat_history=st.session_state["chat_history"]
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answer_history"].append(generated_response)
        st.session_state["chat_history"].append((prompt, generated_response))


if st.session_state["chat_answer_history"]:
    for generated_response, prompt in zip(
        st.session_state["chat_answer_history"], st.session_state["user_prompt_history"]
    ):
        message(prompt, is_user=True)
        message(generated_response, is_user=False)