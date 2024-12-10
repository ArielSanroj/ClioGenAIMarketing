import streamlit as st
from utils.session_manager import get_user_state, get_current_user_id, set_user_state

def render_chat_interface():
    """Render the simplified chat interface exactly matching the design."""
    # Apply custom styles for the chat interface
    st.markdown("""
        <style>
        .stApp {
            background-color: #F9F9FB !important;
        }
        .stButton > button {
            background-color: #1E1B4B !important;
            color: white !important;
            width: 100% !important;
            padding: 0.75rem !important;
            margin: 0.5rem 0 !important;
        }
        .stTextInput > div > div > input {
            border: 1px solid #E2E8F0 !important;
            border-radius: 4px !important;
            padding: 0.75rem !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title with proper styling
    st.markdown("<h2 style='color: #1E1B4B; margin-bottom: 2rem;'>Chat Interface</h2>", unsafe_allow_html=True)
    
    # Question label
    st.markdown("<p style='color: #4A5568; margin-bottom: 0.5rem;'>Ask a question about your analysis:</p>", unsafe_allow_html=True)
    
    # Question input field
    user_id = get_current_user_id()
    question = st.text_input("", key="chat_input", label_visibility="collapsed")
    
    # Send button
    if st.button("Send", type="primary", use_container_width=True):
        if question.strip():
            chat_history = get_user_state(user_id, "chat_history", [])
            chat_history.append({"role": "user", "content": question})
            set_user_state(user_id, "chat_history", chat_history)
            st.rerun()
    
    # Back to Analysis button
    if st.button("Back to Analysis", type="primary", use_container_width=True):
        set_user_state(user_id, "selected_option", "home")
        st.rerun()

if __name__ == "__main__":
    render_chat_interface()