import streamlit as st
import openai
from chatbot import get_response

import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []


st.markdown("<h3><center>VidyaSarthi - Guiding Steps, Expanding Knowledge</center></h3>",
            unsafe_allow_html=True)

with st.chat_message("assistant"):
    st.markdown(
        "Namaste নমস্কার :pray: Welcome to Aliah University. I am `VidyaSarthi`, your virtual assistant :robot_face:. How may I assist you with information from our university brochure today?")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if query := st.chat_input("Enter your query here to chatbot."):
    st.session_state.messages.append({"role": "user", "content": query})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = get_response(query=query)
        st.markdown(response)
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
