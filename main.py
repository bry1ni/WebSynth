import streamlit as st
import random
import time

from src.agent import get_bot_response

# Set page configuration
st.set_page_config(page_title="WebSynth", page_icon="🤖")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat title
st.title("💬 WebSynth")
st.markdown("Your first station for subject familiarity.")

# Display chat messages using st.chat_message
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])


# Input field for user message
user_input = st.chat_input("Type your message here...")

# Process user input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # Create a placeholder for the assistant's response
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Get bot response with streaming enabled
        try:
            # Generate bot response with streaming
            for chunk in get_bot_response(user_input, stream=True):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.01)  # Small delay for visual effect
            
            # Final display without cursor
            message_placeholder.markdown(full_response)
        except Exception as e:
            error_message = f"Error: {str(e)}"
            st.error(error_message)
            full_response = f"I'm sorry, but I encountered an error while processing your request. Please try again."
            message_placeholder.markdown(full_response)
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
