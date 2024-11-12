import streamlit as st
from components.sidebar import render_sidebar
from components.content_generator import render_content_generator
from components.social_media import render_social_media_campaign
from components.seo_analyzer import render_seo_analyzer
from components.brand_values import render_brand_values
from components.icp_definition import render_icp_definition
from components.consumer_archetypes import render_consumer_archetypes
from styles import apply_custom_styles

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
        st.session_state.selected_option = None  # Default to home view
    if 'show_icp_questionnaire' not in st.session_state:
        st.session_state.show_icp_questionnaire = False
    if 'archetype_view' not in st.session_state:
        st.session_state.archetype_view = 'archetypes'

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

def render_chat_input():
    """Render the chat input component"""
    st.markdown('''
        <div class="chat-input-container">
            <input type="text" class="chat-input" placeholder="Message Clio AI">
            <button class="send-button">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M22 2L11 13" stroke="currentColor" stroke-width="2"/>
                    <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2"/>
                </svg>
            </button>
        </div>
    ''', unsafe_allow_html=True)

def render_dashboard():
    """Render the main dashboard after onboarding is completed"""
    # Render sidebar and get selected option
    selected_option = render_sidebar()
    
    if selected_option:
        st.session_state.selected_option = selected_option
    
    # Main content area
    if st.session_state.selected_option is None:
        # Home chat view with buttons
        st.markdown('''
            <div style="display: flex; flex-direction: column; gap: 1rem; max-width: 600px; margin: 2rem auto;">
                <button class="nav-option" onclick="window.location.href='#content'">
                    Generate Content Marketing
                </button>
                <button class="nav-option" onclick="window.location.href='#social'">
                    Create Social Media Campaign
                </button>
                <button class="nav-option" onclick="window.location.href='#seo'">
                    Generate SEO recommendations
                </button>
            </div>
        ''', unsafe_allow_html=True)
        
        # Chat input at bottom
        st.markdown('''
            <div class="chat-input-container">
                <input type="text" class="chat-input" placeholder="Message Clio AI">
                <button class="send-button">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M22 2L11 13" stroke="currentColor" stroke-width="2"/>
                        <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2"/>
                    </svg>
                </button>
            </div>
        ''', unsafe_allow_html=True)
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
        render_dashboard()

if __name__ == "__main__":
    main()
