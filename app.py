import streamlit as st
import requests
import json

# FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000"

# Initialize session state for chat
if "current_session" not in st.session_state:
    st.session_state.current_session = []  # Store current chat session messages
if "selected_session" not in st.session_state:
    st.session_state.selected_session = None  # Track selected past session

# Sidebar: Past chat sessions
st.sidebar.title("Chat Sessions")
st.sidebar.markdown("Click a session to load it.")

try:
    # Fetch past chats from backend
    response = requests.get(f"{BACKEND_URL}/chats")
    if response.status_code == 200:
        past_chats = response.json()  # Assuming response is a list of session objects
        for i, chat in enumerate(past_chats):
            # Display past session in the sidebar with a preview of the first user input
            preview_text = chat['messages'][0]['text'][:20] if chat['messages'] else "No input"
            if st.sidebar.button(f"Session {i+1}: {preview_text}..."):
                # Select past session and load its chat history
                st.session_state.selected_session = chat
                st.session_state.current_session = chat.get("messages", [])
    else:
        st.sidebar.error("Failed to fetch past chats.")
except Exception as e:
    st.sidebar.error(f"Error: {e}")

# Button to start a new session (clear current session and reset selection)
if st.sidebar.button("Start New Session"):
    st.session_state.current_session = []
    st.session_state.selected_session = None

# Main chat interface
st.title("ChatGPT-like Chat Interface")

# Display selected session's chat history
if st.session_state.selected_session:
    st.subheader("Selected Session")
else:
    st.subheader("New Session")

# Chat messages container (display chat history)
for message in st.session_state.current_session:
    if message["role"] == "user":
        st.markdown(
            f"""
            <div style='text-align: right; margin: 10px; padding: 10px; background-color: #d1e7dd; border-radius: 10px;'>
                <strong>You:</strong> {message['text']}
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif message["role"] == "bot":
        st.markdown(
            f"""
            <div style='text-align: left; margin: 10px; padding: 10px; background-color: #f8d7da; border-radius: 10px;'>
                <strong>Bot:</strong> {message['text']}
            </div>
            """,
            unsafe_allow_html=True,
        )

# Input box for user prompt
user_input = st.text_input("Your message", key="input_box")

# Send button (send message to backend)
if st.button("Send"):
    if user_input:
        # Add user input to the chat
        st.session_state.current_session.append({"role": "user", "text": user_input})
        st.markdown(
            f"""
            <div style='text-align: right; margin: 10px; padding: 10px; background-color: #d1e7dd; border-radius: 10px;'>
                <strong>You:</strong> {user_input}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Send user input to backend (Gemini API or any other model)
        payload = {"prompt": user_input, "model": "gemini"}  # Change model as needed
        try:
            with st.spinner("Generating response..."):  # Spinner wraps the backend call
                response = requests.post(f"{BACKEND_URL}/chat", json=payload)
                if response.status_code == 200:
                    bot_response = response.json().get("response", "No response")
                    # Add bot response to the chat
                    st.session_state.current_session.append({"role": "bot", "text": bot_response})
                    st.markdown(
                        f"""
                        <div style='text-align: left; margin: 10px; padding: 10px; background-color: #f8d7da; border-radius: 10px;'>
                            <strong>Bot:</strong> {bot_response}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.error("Failed to get a response from the backend.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a message.")
