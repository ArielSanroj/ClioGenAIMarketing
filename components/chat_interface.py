import streamlit as st
from utils.session_manager import get_user_state, get_current_user_id, set_user_state

def render_chat_interface():
    """Render the marketing chat interface with the exact design implementation."""
    user_id = get_current_user_id()
    chat_history = get_user_state(user_id, "chat_history", [])

    # Save and Exit button
    st.markdown(
        '<button class="save-exit-btn">Save and Exit</button>',
        unsafe_allow_html=True
    )

    # Sidebar content
    with st.sidebar:
        # Logo at top
        st.image("assets/logoclio.png", width=100)
        
        # Navigation buttons
        st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
        if st.button("New Chat", key="new_chat", use_container_width=True):
            set_user_state(user_id, "chat_history", [])
            st.rerun()
        
        if st.button("Chats history", key="chats_history", use_container_width=True):
            # Handle chats history
            pass

    # Marketing action buttons
    st.markdown(
        """
        <div class="action-buttons">
            <button class="generate-btn">Generate Content Marketing</button>
            <button class="campaign-btn">Create Marketing Campaign</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in chat_history:
        message_class = "user-message" if message["role"] == "user" else "bot-message"
        st.markdown(
            f'<div class="chat-message {message_class}">{message["content"]}</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input
    st.markdown(
        """
        <div class="chat-input-container">
            <input type="text" class="chat-input" placeholder="Message Clio AI">
            <button class="send-button">
                <i class="fas fa-paper-plane"></i>
            </button>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Footer with social icons
    st.markdown(
        """
        <div class="footer">
            <div class="footer-content">
                <div class="footer-links">
                    <a href="#">Contact Us</a>
                    <a href="#">Privacy Policy</a>
                </div>
                <div class="social-icons">
                    <a href="#"><i class="fab fa-facebook"></i></a>
                    <a href="#"><i class="fab fa-instagram"></i></a>
                    <a href="#"><i class="fab fa-youtube"></i></a>
                    <a href="#"><i class="fab fa-twitter"></i></a>
                    <a href="#"><i class="fab fa-whatsapp"></i></a>
                    <a href="#"><i class="fab fa-linkedin"></i></a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add JavaScript for handling button clicks
    st.markdown(
        """
        <script>
            document.querySelectorAll('.generate-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    // Handle generate content click
                    console.log('Generate Content clicked');
                });
            });

            document.querySelectorAll('.campaign-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    // Handle create campaign click
                    console.log('Create Campaign clicked');
                });
            });

            document.querySelector('.send-button').addEventListener('click', () => {
                const input = document.querySelector('.chat-input');
                if (input.value.trim()) {
                    // Handle send message
                    console.log('Message:', input.value);
                    input.value = '';
                }
            });
        </script>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    render_chat_interface()
