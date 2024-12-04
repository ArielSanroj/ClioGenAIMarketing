import streamlit as st

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
        .custom-box {
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            padding: 1rem;
            text-align: center;
            box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
        }
        .custom-box:hover {
            border-color: #3e2a5e;
        }
        .sidebar {
            background-color: #f0e6ff;
            padding: 1rem;
        }
        .main-area {
            background-color: #fffbf0;
            padding: 2rem;
        }
        .footer {
            text-align: center;
            font-size: 12px;
            color: #aaa;
            padding: 1rem;
        }
        .footer a {
            text-decoration: none;
            color: #3e2a5e;
        }
        .stTextInput input {
            border-radius: 8px;
            padding: 0.5rem;
            border: 1px solid #e0e0e0;
        }
        .send-button {
            background-color: #1f1937;
            color: white;
            border-radius: 8px;
            border: none;
            font-size: 16px;
            cursor: pointer;
            padding: 0.5rem 1rem;
        }
        .send-button:hover {
            background-color: #3e2a5e;
        }
        </style>
    """, unsafe_allow_html=True)

# Main Interface Function
def render_chat_interface():
    """Render the marketing chat interface."""
    st.set_page_config(layout="wide", page_title="Gen AI Marketing Chat")

    # Load custom CSS
    load_custom_css()

    # Layout: Sidebar and Main Area
    col_sidebar, col_main = st.columns([1, 4])

    # Sidebar
    with col_sidebar:
        st.image("assets/logoclio.png", width=100)
        st.write("")  # Spacing
        st.button("New Chat", use_container_width=True)
        st.button("Chats History", use_container_width=True)

    # Main Area
    with col_main:
        # Top row for Save and Exit
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("Save and Exit", use_container_width=True):
                st.write("Save and Exit clicked!")

        # Centered Action Buttons
        st.write("")
        col_action1, col_action2 = st.columns([1, 1], gap="large")
        with col_action1:
            if st.button("Generate Content Marketing", use_container_width=True):
                st.write("Generate Content Marketing clicked!")
        with col_action2:
            if st.button("Create Marketing Campaign", use_container_width=True):
                st.write("Create Marketing Campaign clicked!")

        # Footer and Input Box
        st.markdown("---")
        col_input, col_send = st.columns([4, 1])
        with col_input:
            user_input = st.text_input(
                "Message Clio AI",
                placeholder="Type your message here...",
                key="chat_input",
                label_visibility="collapsed"
            )
        with col_send:
            if st.button("Send", use_container_width=True):
                if user_input:
                    st.write(f"User Input: {user_input}")
                else:
                    st.error("Please enter a message before sending.")

    # Footer Links
    st.markdown(
        """
        <div class="footer">
            <a href="#">Contact Us</a> | <a href="#">Privacy Policy</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Run the app
if __name__ == "__main__":
    render_interface()
