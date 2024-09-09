import streamlit as st
import openai
from chatbot import get_response

import streamlit as st

def set_background():
    st.markdown(
        """
        <style>
        /* Full app background */
        .stApp {
            background-image: url("https://www.aliah.ac.in/images/slider-3.webp");
            background-size: cover;
            background-attachment: fixed;
        }

        /* Main content area - adjust the selector as needed */
        .main .block-container {
            background-color: white; /* Ensures the chat area is white */
            position: fixed; /* Keeps the position fixed */
            top: 50px; /* Adjust based on your header or needs */
            left: 50%; /* Centers the container */
            transform: translateX(-50%); /* Adjusts the positioning to the center */
            width: 80%; /* Adjust the width as needed */
            height: 80vh; /* Use viewport height to control the area */
            z-index: 10; /* Ensures it is above the background */
            padding: 20px; /* Adds some padding */
            overflow-y: auto; /* Ensures the area is scrollable if content exceeds height */
            border-radius: 10px; /* Rounds the corners */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
set_background()



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
