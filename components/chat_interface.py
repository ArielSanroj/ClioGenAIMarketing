import streamlit as st
from utils.session_manager import get_user_state, get_current_user_id, set_user_state

def load_custom_css():
    """Load custom CSS for styling the Streamlit app."""
    st.markdown("""
        <style>
        .stButton button {
            background-color: #1f1937;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            border: none;
        }
        .stButton button:hover {
            background-color: #3e2a5e;
            color: #ffeeb3;
        }
        .chat-interface {
            margin-bottom: 60px;
        }
        .chat-message {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            max-width: 80%;
        }
        .user-message {
            background-color: #f3f4f6;
            margin-left: auto;
        }
        .bot-message {
            background-color: #e5e7eb;
            margin-right: auto;
        }
        .action-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 2rem 0;
        }
        .action-button {
            background-color: #ffeeb3 !important;
            color: #1f1937 !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_chat_interface():
    """Render the marketing chat interface."""
    st.set_page_config(layout="wide", page_title="Gen AI Marketing Chat")
    
    # Load custom CSS
    load_custom_css()
    
    # Get user state
    user_id = get_current_user_id()
    chat_history = get_user_state(user_id, "chat_history", [])
    
    # Layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.image("assets/logoclio.png", width=100)
        st.button("New Chat", use_container_width=True)
        st.button("Chats history", use_container_width=True)
    
    with col2:
        # Top action buttons
        with st.container():
            col_exit, = st.columns([1])
            with col_exit:
                st.button("Save and Exit", use_container_width=True)
        
        # Marketing action buttons
        st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
        col_action1, col_action2 = st.columns(2)
        with col_action1:
            if st.button("Generate Content Marketing", key="gen_content", use_container_width=True):
                set_user_state(user_id, "selected_option", "content")
        with col_action2:
            if st.button("Create Marketing Campaign", key="create_campaign", use_container_width=True):
                set_user_state(user_id, "selected_option", "campaign")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat messages
        st.markdown('<div class="chat-interface">', unsafe_allow_html=True)
        for message in chat_history:
            message_class = "user-message" if message["role"] == "user" else "bot-message"
            st.markdown(
                f'<div class="chat-message {message_class}">{message["content"]}</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input area
        with st.container():
            input_col, button_col = st.columns([4, 1])
            with input_col:
                user_input = st.text_input(
                    "Message Clio AI",
                    key="chat_input",
                    label_visibility="collapsed"
                )
            with button_col:
                if st.button("Send", use_container_width=True):
                    if user_input:
                        # Add user message to chat history
                        chat_history.append({"role": "user", "content": user_input})
                        set_user_state(user_id, "chat_history", chat_history)
                        # Clear input (will be implemented through session state)
                        st.session_state.chat_input = ""
    
    # Footer
    st.markdown("""
        <div style="position: fixed; bottom: 0; left: 0; right: 0; background-color: #1f1937; padding: 1rem; text-align: center;">
            <a href="#" style="color: white; text-decoration: none; margin: 0 1rem;">Contact Us</a>
            <a href="#" style="color: white; text-decoration: none; margin: 0 1rem;">Privacy Policy</a>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_chat_interface()
