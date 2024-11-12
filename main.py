import streamlit as st
from components.sidebar import render_sidebar
from components.content_generator import render_content_generator
from components.social_media import render_social_media_campaign
from components.seo_analyzer import render_seo_analyzer
from components.brand_values import render_brand_values
from components.icp_definition import render_icp_definition
from components.consumer_archetypes import render_consumer_archetypes
from styles import apply_custom_styles
from auth import is_authenticated
from auth_pages import render_auth_pages
from utils.session_manager import get_user_state, get_current_user_id, set_user_state

def render_dashboard():
    """Render the home chat interface"""
    user_id = get_current_user_id()
    
    # Apply styles for centered layout
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    
    # Show logo
    st.image("logoclio.png", width=100)
    
    # Add the two action buttons in a centered layout
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Content Marketing"):
            set_user_state(user_id, "selected_option", "content")
            st.rerun()
    with col2:
        if st.button("Create Social Media Campaign"):
            set_user_state(user_id, "selected_option", "social")
            st.rerun()
    
    # Add chat input at the bottom
    st.markdown('''
        <div style="position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); width: 80%; max-width: 800px;">
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <input type="text" placeholder="Message Clio AI" style="width: 100%; padding: 0.75rem; border: 1px solid #E5E7EB; border-radius: 8px;">
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_icp_summary():
    """Render the ICP summary view"""
    user_id = get_current_user_id()
    icp_data = get_user_state(user_id, "icp_data")
    
    st.markdown("### Your ICP Profile")
    st.markdown(f"**Knowledge Level:** {icp_data['knowledge_level']}")
    
    st.markdown("**Your Answers:**")
    for q_num in range(1, 6):
        answer = icp_data['answers'].get(f"q{q_num}", "Not answered")
        st.markdown(f"**Question {q_num}**")
        if isinstance(answer, list):
            for item in answer:
                st.markdown(f"- {item}")
        else:
            st.markdown(f"{answer}")

def main():
    st.set_page_config(
        page_title="AI Marketing Assistant",
        page_icon="assets/logo.svg",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom styles
    apply_custom_styles()
    
    # Check authentication
    if not is_authenticated():
        render_auth_pages()
        return
    
    user_id = get_current_user_id()
    
    # Main flow condition
    if not get_user_state(user_id, "brand_values").get('is_completed', False):
        st.markdown('<div class="welcome-screen">', unsafe_allow_html=True)
        render_brand_values()
        st.markdown('</div>', unsafe_allow_html=True)
    elif not get_user_state(user_id, "icp_data").get('is_completed', False):
        st.markdown('<div class="welcome-screen">', unsafe_allow_html=True)
        render_icp_definition()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Render sidebar and get selected option
        selected_option = render_sidebar()
        
        # Handle navigation from sidebar
        if selected_option:
            set_user_state(user_id, "selected_option", selected_option)
        
        # Main content area
        current_option = get_user_state(user_id, "selected_option")
        if current_option == "home":
            render_dashboard()
        elif current_option == "content":
            render_content_generator()
        elif current_option == "social":
            render_social_media_campaign()
        elif current_option == "market_analysis":
            render_seo_analyzer()
        elif current_option == "archetypes":
            render_consumer_archetypes()
        elif current_option == "icp_questionnaire":
            render_icp_definition()
        elif current_option == "icp_summary":
            render_icp_summary()

if __name__ == "__main__":
    main()