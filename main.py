import streamlit as st
from components.sidebar import render_sidebar
from components.content_generator import render_content_generator
from components.social_media import render_social_media_campaign
from components.audience_analyzer import render_audience_analyzer
from components.seo_analyzer import render_seo_analyzer
from styles import apply_custom_styles
from database import db

def main():
    st.set_page_config(
        page_title="AI Marketing Assistant",
        page_icon="assets/logo.svg",
        layout="wide"
    )
    
    apply_custom_styles()
    
    # Render sidebar
    selected_option = render_sidebar()
    
    # Main content area
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
        ## 👋 Welcome to AI Marketing Assistant!
        
        Get started by selecting one of the following options:
        
        1. **Generate Content Marketing** - Create engaging blog posts, social media content, and more
        2. **Create Social Media Campaign** - Design comprehensive social media campaigns
        3. **Analyze Target Audience** - Get insights about your target market
        4. **Generate SEO Recommendations** - Optimize your content for search engines
        
        Select an option above to begin!
        """)

if __name__ == "__main__":
    main()
