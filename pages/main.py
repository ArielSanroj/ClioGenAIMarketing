import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

import streamlit as st
from components.sidebar import render_sidebar
from components.content_generator import render_content_generator
from components.social_media import render_social_media_campaign
from components.audience_analyzer import render_audience_analyzer
from components.seo_analyzer import render_seo_analyzer
from components.analyzer import render_analyzer
from styles import apply_custom_styles

def render_chat_input():
    st.markdown("""
        <div class="chat-container">
            <form id="chat-form" onsubmit="return false;">
                <div style="display: flex; align-items: center;">
                    <input type="text" class="chat-input" placeholder="Message Clio AI" id="chat-input">
                    <button type="submit" class="send-button" onclick="handleSubmit()">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
            </form>
        </div>
        
        <script>
        function handleSubmit() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            if (message) {
                // Clear input
                input.value = '';
                // Send message to Streamlit
                window.parent.postMessage({
                    type: 'streamlit:message',
                    chat_message: message
                }, '*');
            }
            return false;
        }
        
        // Add event listener for Enter key
        document.getElementById('chat-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                handleSubmit();
            }
        });
        </script>
    """, unsafe_allow_html=True)

def render_chat_interface():
    """Render the chat interface with suggested actions"""
    st.markdown("### 💬 Chat with Clio AI")
    
    # Display action buttons
    if st.session_state.analyzed_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("Generate Content Marketing", key="chat_content"):
                st.session_state.selected_option = "content"
                st.rerun()
        
        with col2:
            if st.button("Create Social Media Campaign", key="chat_social"):
                st.session_state.selected_option = "social"
                st.rerun()
        
        with col3:
            if st.button("Analyze Target Audience", key="chat_audience"):
                st.session_state.selected_option = "audience"
                st.rerun()
        
        with col4:
            if st.button("Generate SEO recommendations", key="chat_seo"):
                st.session_state.selected_option = "seo"
                st.rerun()

    # Chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know about the analysis?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Add AI response here
        response = "I understand you're asking about " + prompt
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    st.set_page_config(
        page_title="Clio - Marketing GenAI Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    apply_custom_styles()
    
    # Initialize session states
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'analyzer'
    if 'analyzed_data' not in st.session_state:
        st.session_state.analyzed_data = True  # Default value for demonstration purposes
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
            
    # Render sidebar
    selected_sidebar_option = render_sidebar()
    if selected_sidebar_option:
        st.session_state.selected_option = selected_sidebar_option
    
    # Main content area
    st.title("Clio - Marketing GenAI Assistant")
    
    # Navigation handling
    if st.session_state.get('show_chat', False) and st.session_state.get('current_page') == 'chat':
        # Coming from analyzer, show chat interface
        render_chat_interface()
        if st.session_state.selected_option:
            # Show selected component based on chat actions
            if st.session_state.selected_option == "content":
                render_content_generator()
            elif st.session_state.selected_option == "social":
                render_social_media_campaign()
            elif st.session_state.selected_option == "audience":
                render_audience_analyzer()
            elif st.session_state.selected_option == "seo":
                render_seo_analyzer()
    else:
        # Show analyzer component
        render_analyzer()
    
    # Render chat input if show_chat is true
    if st.session_state.get('show_chat', False):
        render_chat_input()

if __name__ == "__main__":
    main()