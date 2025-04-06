# chat_ui.py
import streamlit as st
import time
from src.mdl.agent.agent import get_bot_response

def initialize_chat_ui():
    """Initialize chat history if it doesn't exist in session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_messages():
    """Display all messages from the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

def add_message_to_history(role, content):
    """Add a new message to the chat history."""
    st.session_state.messages.append({"role": role, "content": content})

def display_user_message(message):
    """Display the user's message in the chat UI."""
    with st.chat_message("user", avatar="👤"):
        st.markdown(message)

def get_and_display_assistant_response(user_input):
    """Display the assistant's response with a streaming effect."""
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            for chunk in get_bot_response(user_input):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.01)  # Small delay for visual effect
            
            # Final display without cursor
            message_placeholder.markdown(full_response)
            return full_response
        except Exception as e:
            error_message = f"Error: {str(e)}"
            st.error(error_message)
            full_response = "I'm sorry, but I encountered an error while processing your request. Please try again."
            message_placeholder.markdown(full_response)
            return full_response

def handle_user_input():
    """Process user input and generate assistant response."""
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add and display user message
        add_message_to_history("user", user_input)
        display_user_message(user_input)
        
        # Get and display assistant response
        full_response = get_and_display_assistant_response(user_input)
        
        # Add assistant response to history
        add_message_to_history("assistant", full_response)