import streamlit as st
from components.sidebar import render_sidebar
from components.content_generator import render_content_generator
from components.social_media import render_social_media_campaign
from components.audience_analyzer import render_audience_analyzer
from components.seo_analyzer import render_seo_analyzer
from styles import apply_custom_styles
from database import db

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

def main():
    st.set_page_config(
        page_title="AI Marketing Assistant",
        page_icon="assets/logo.svg",
        layout="wide"
    )
    
    apply_custom_styles()
    
    # Render sidebar
    selected_option = render_sidebar()
    
    # Add container for main content to add proper spacing for chat input
    main_container = st.container()
    
    with main_container:
        st.title("AI Marketing Assistant")
        
        # Navigation buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("Generate Content Marketing"):
                selected_option = "content"
        with col2:
            if st.button("Create Social Media Campaign"):
                selected_option = "social"
        with col3:
            if st.button("Analyze Target Audience"):
                selected_option = "audience"
        with col4:
            if st.button("Generate SEO recommendations"):
                selected_option = "seo"
        
        # Render selected component
        if selected_option == "content":
            render_content_generator()
        elif selected_option == "social":
            render_social_media_campaign()
        elif selected_option == "audience":
            render_audience_analyzer()
        elif selected_option == "seo":
            render_seo_analyzer()
        else:
            # Default view - Quick start guide
            st.markdown("""
            ## 👋 Welcome to Clio AI Marketing Assistant!
            
            Get started by selecting one of the following options:
            
            1. **Generate Content Marketing** - Create engaging blog posts, social media content, and more
            2. **Create Social Media Campaign** - Design comprehensive social media campaigns
            3. **Analyze Target Audience** - Get insights about your target market
            4. **Generate SEO Recommendations** - Optimize your content for search engines
            
            Select an option above to begin!
            """)
    
    # Render chat input at the bottom
    render_chat_input()

if __name__ == "__main__":
    main()
