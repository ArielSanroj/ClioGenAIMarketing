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
    """Render the chat interface with suggested actions based on analyzed data"""
    st.markdown("### 💬 Chat with Clio AI")
    
    # Display suggested actions based on analyzed data
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
    
    # Chat input
    render_chat_input()

def main():
    st.set_page_config(
        page_title="AI Marketing Assistant",
        page_icon="assets/logo.svg",
        layout="wide"
    )
    
    apply_custom_styles()
    
    # Initialize session state
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
        
    if 'analyzed_data' not in st.session_state:
        st.session_state.analyzed_data = True  # Default value for demonstration purposes
        
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False  # Added to manage chat visibility

    # Render sidebar
    selected_sidebar_option = render_sidebar()
    if selected_sidebar_option:
        st.session_state.selected_option = selected_sidebar_option
    
    # Main content area with proper spacing for chat input
    main_container = st.container()
    
    with main_container:
        st.title("AI Marketing Assistant")
        
        # Show analyzer component initially
        if not st.session_state.get('show_chat', False):
            render_analyzer()
        
        # Show chat interface after analysis
        if st.session_state.get('show_chat', False):
            render_chat_interface()
            
            # Render selected component based on chat actions
            if st.session_state.selected_option == "content":
                render_content_generator()
            elif st.session_state.selected_option == "social":
                render_social_media_campaign()
            elif st.session_state.selected_option == "audience":
                render_audience_analyzer()
            elif st.session_state.selected_option == "seo":
                render_seo_analyzer()
    
    # Render chat input if show_chat is true
    if st.session_state.get('show_chat', False):
        render_chat_input()

if __name__ == "__main__":
    main()