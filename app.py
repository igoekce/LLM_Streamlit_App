import os
from dotenv import load_dotenv
import streamlit as st
import openai
import toml

# Load secrets from secrets.toml
secrets = toml.load("secrets.toml")

# Set OpenAI API key from secrets file
openai_api_key = secrets["general"]["OPENAI_API_KEY"]
openai.api_key = openai_api_key

st.title("OpenAI Chatbot")
st.write("Ask me anything!")

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Create a text input for the user
user_input = st.text_input("You: ", "")

if st.button("Send") and user_input:
    # Add user input to conversation history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Instantiate the OpenAI client
    client = openai.OpenAI(api_key=openai_api_key)

    # Get response from OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=st.session_state.messages
    )

    # Extract the text from the response
    output = response.choices[0].message.content.strip()

    # Add assistant response to conversation history
    st.session_state.messages.append({"role": "assistant", "content": output})

# Display conversation history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"You: {message['content']}")
    elif message["role"] == "assistant":
        st.write(f"Chatbot: {message['content']}")

if st.button('Clear Chat'):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
