import streamlit as st
import requests

st.title("💬 Llama 3.1 Chatbot on Hugging Face (Token Embedded)")
st.write(
    "This chatbot uses Meta's Llama 3.1 8B Instruct model hosted on Hugging Face's Inference API. "
    "The API token is pre-configured in the code."
)

# Hardcoded API Token (Replace with your actual token)
api_token = st.secrets["huggingface"]["api_token"]
model_id = "meta-llama/Llama-3.1-8B-Instruct"
api_url = f"https://api-inference.huggingface.co/models/{model_id}"

headers = {"Authorization": f"Bearer {api_token}"}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build chat history in Llama format
    chat_history = ""
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        chat_history += f"{role}: {msg['content']}\n"
    chat_history += "Assistant:"

    # Call Hugging Face Inference API
    payload = {"inputs": chat_history, "parameters": {"max_new_tokens": 512, "temperature": 0.7}}
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        generated_text = result[0]["generated_text"]
        assistant_reply = generated_text.split("Assistant:")[-1].strip()

        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
