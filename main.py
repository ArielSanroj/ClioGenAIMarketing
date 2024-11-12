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

def initialize_session_state():
    """Initialize the session state variables"""
    if 'brand_values' not in st.session_state:
        st.session_state.brand_values = {
            'mission': 'Example mission',
            'values': ['value1', 'value2'],
            'virtues': ['virtue1', 'virtue2'],
            'is_completed': True
        }
    if 'icp_data' not in st.session_state:
        st.session_state.icp_data = {
            'knowledge_level': 'I know my ICP',
            'current_question': 1,
            'demographics': {},
            'psychographics': {},
            'archetype': '',
            'pain_points': [],
            'goals': [],
            'answers': {},
            'is_completed': True
        }
    if 'webpage_analysis' not in st.session_state:
        st.session_state.webpage_analysis = {
            'url': '',
            'analysis': {},
            'is_completed': False
        }
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = 'content'
    if 'show_icp_questionnaire' not in st.session_state:
        st.session_state.show_icp_questionnaire = False
    if 'archetype_view' not in st.session_state:
        st.session_state.archetype_view = 'archetypes'
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_chat_id' not in st.session_state:
        st.session_state.current_chat_id = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

def render_dashboard():
    """Render the home chat interface"""
    # Apply styles for centered layout
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    
    # Show logo
    st.image("logoclio.png", width=100)
    
    # Add the two action buttons in a centered layout
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Content Marketing"):
            st.session_state.selected_option = "content"
            st.rerun()
    with col2:
        if st.button("Create Social Media Campaign"):
            st.session_state.selected_option = "social"
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
    st.markdown("### Your ICP Profile")
    st.markdown(f"**Knowledge Level:** {st.session_state.icp_data['knowledge_level']}")
    
    st.markdown("**Your Answers:**")
    for q_num in range(1, 6):
        answer = st.session_state.icp_data['answers'].get(f"q{q_num}", "Not answered")
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
    
    # Initialize session state
    initialize_session_state()
    
    # Apply custom styles
    apply_custom_styles()
    
    # Check authentication
    if not is_authenticated():
        render_auth_pages()
        return
    
    # Main flow condition
    if not st.session_state.brand_values.get('is_completed', False):
        st.markdown('<div class="welcome-screen">', unsafe_allow_html=True)
        render_brand_values()
        st.markdown('</div>', unsafe_allow_html=True)
    elif not st.session_state.icp_data.get('is_completed', False):
        st.markdown('<div class="welcome-screen">', unsafe_allow_html=True)
        render_icp_definition()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Render sidebar and get selected option
        selected_option = render_sidebar()
        
        # Handle navigation from sidebar
        if selected_option:
            st.session_state.selected_option = selected_option
        
        # Main content area
        if st.session_state.selected_option == "home":
            render_dashboard()
        elif st.session_state.selected_option == "content":
            render_content_generator()
        elif st.session_state.selected_option == "social":
            render_social_media_campaign()
        elif st.session_state.selected_option == "market_analysis":
            render_seo_analyzer()
        elif st.session_state.selected_option == "archetypes":
            render_consumer_archetypes()
        elif st.session_state.selected_option == "icp_questionnaire":
            render_icp_definition()
        elif st.session_state.selected_option == "icp_summary":
            render_icp_summary()

if __name__ == "__main__":
    main()
