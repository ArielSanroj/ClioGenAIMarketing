import streamlit as st
from utils.session_manager import get_user_state, get_current_user_id

def render_chat_interface():
    """Render the simplified chat interface exactly matching the design."""
    # Set page config
    st.set_page_config(page_title="Chat Interface", layout="wide")
    
    # Apply background color
    st.markdown("""
        <style>
        .stApp {
            background-color: #F9F9FB;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown("## Chat Interface")
    
    # Ask a question input
    st.markdown("Ask a question about your analysis:")
    
    # Question input field
    question = st.text_input("", label_visibility="collapsed")
    
    # Send button
    if st.button("Send", type="primary", use_container_width=True):
        if question:
            # Handle sending the question
            pass
    
    # Back to Analysis button
    if st.button("Back to Analysis", type="primary", use_container_width=True):
        # Handle going back to analysis
        pass

if __name__ == "__main__":
    render_chat_interface()