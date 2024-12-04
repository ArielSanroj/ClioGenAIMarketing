import streamlit as st
from utils.session_manager import get_user_state, get_current_user_id, set_user_state

def render_chat_interface():
    """Render the marketing chat interface."""
    user_id = get_current_user_id()
    chat_history = get_user_state(user_id, "chat_history", [])

    # Save and Exit button
    st.markdown(
        '<button class="save-exit-btn" onclick="window.location.href=\'/\'">Save and Exit</button>',
        unsafe_allow_html=True
    )

    # Sidebar
    with st.sidebar:
        # Logo
        st.image("assets/logoclio.png", width=100)
        
        # Navigation buttons
        st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
        if st.button("New Chat", key="new_chat", help="Start a new chat", use_container_width=True,
                    type="secondary", args=({'className': 'sidebar-btn'},)):
            set_user_state(user_id, "chat_history", [])
            st.rerun()
            
        if st.button("Chats history", key="chat_history", help="View previous chats", use_container_width=True,
                    type="secondary", args=({'className': 'sidebar-btn'},)):
            # Handle chat history navigation
            pass

    # Marketing action buttons
    st.markdown(
        '<div class="action-buttons">'
        '<button class="generate-btn" onclick="handleGenerateContent()">Generate Content Marketing</button>'
        '<button class="campaign-btn" onclick="handleCreateCampaign()">Create Marketing Campaign</button>'
        '</div>',
        unsafe_allow_html=True
    )

    # Chat messages container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in chat_history:
        message_class = "user-message" if message["role"] == "user" else "bot-message"
        st.markdown(
            f'<div class="chat-message {message_class}">{message["content"]}</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input and send button
    st.markdown(
        '<div class="chat-input-container">'
        '<input type="text" class="chat-input" placeholder="Message Clio AI">'
        '<button class="send-btn"><i class="fas fa-paper-plane"></i></button>'
        '</div>',
        unsafe_allow_html=True
    )

    # Footer
    st.markdown(
        '<div class="footer">'
        '<div class="footer-content">'
        '<div class="footer-links">'
        '<a href="/contact">Contact Us</a>'
        '<a href="/privacy">Privacy Policy</a>'
        '</div>'
        '<div class="social-icons">'
        '<a href="#" target="_blank"><i class="fab fa-facebook"></i></a>'
        '<a href="#" target="_blank"><i class="fab fa-instagram"></i></a>'
        '<a href="#" target="_blank"><i class="fab fa-youtube"></i></a>'
        '<a href="#" target="_blank"><i class="fab fa-twitter"></i></a>'
        '<a href="#" target="_blank"><i class="fab fa-whatsapp"></i></a>'
        '<a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # Add JavaScript for button handlers
    st.markdown("""
        <script>
        function handleGenerateContent() {
            // Handle Generate Content Marketing button click
            console.log('Generate Content Marketing clicked');
        }

        function handleCreateCampaign() {
            // Handle Create Marketing Campaign button click
            console.log('Create Marketing Campaign clicked');
        }
        </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_chat_interface()
