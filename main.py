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
            'is_completed': True  # Set to True to bypass welcome screen
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
            'is_completed': True  # Set to True to bypass ICP questionnaire
        }
    if 'webpage_analysis' not in st.session_state:
        st.session_state.webpage_analysis = {
            'url': '',
            'analysis': {},
            'is_completed': False
        }
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = 'archetypes'  # Set default to archetypes view
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
    chat_container = st.container()
    with chat_container:
        st.markdown("""
            <div class="chat-container">
                <div style="display: flex; align-items: center;">
                    <input type="text" class="chat-input" placeholder="Message Clio AI">
                    <button class="send-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
            </div>
        """, unsafe_allow_html=True)

def render_dashboard():
    """Render the main dashboard after onboarding is completed"""
    # Render sidebar and get selected option
    selected_option = render_sidebar()
    
    # Handle navigation from sidebar
    if selected_option:
        st.session_state.selected_option = selected_option
        if selected_option == "archetypes":
            render_consumer_archetypes()
            return
    
    # Main content area
    main_container = st.container()
    
    with main_container:
        # Handle other views
        if st.session_state.selected_option == "icp_questionnaire":
            render_icp_definition()
            return
        elif st.session_state.selected_option == "icp_summary":
            render_icp_summary()
            return
        elif st.session_state.selected_option == "market_analysis":
            if st.session_state.webpage_analysis.get('is_completed'):
                from utils.webpage_analysis import display_webpage_analysis
                display_webpage_analysis(st.session_state.webpage_analysis['analysis'])
            else:
                render_seo_analyzer()
            return
        elif st.session_state.selected_option == "archetypes":
            render_consumer_archetypes()
            return
        
        # Default dashboard content
        st.title("AI Marketing Assistant")
        
        # Navigation buttons - Updated to use 3 columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Generate Content Marketing", type="primary"):
                st.session_state.selected_option = "content"
        with col2:
            if st.button("Create Social Media Campaign"):
                st.session_state.selected_option = "social"
        with col3:
            if st.button("Generate SEO recommendations"):
                st.session_state.selected_option = "seo"
        
        # Render selected component
        if st.session_state.selected_option == "content":
            render_content_generator()
        elif st.session_state.selected_option == "social":
            render_social_media_campaign()
        elif st.session_state.selected_option == "seo":
            render_seo_analyzer()
        else:
            # Default welcome view
            st.markdown("""
            ## 👋 Welcome to Clio AI Marketing Assistant!
            
            Get started by selecting one of the following options:
            
            1. **Generate Content Marketing** - Create engaging blog posts, social media content, and more
            2. **Create Social Media Campaign** - Design comprehensive social media campaigns
            3. **Generate SEO Recommendations** - Optimize your content for search engines
            
            Select an option above to begin!
            """)
        
        # Render chat input at the bottom
        render_chat_input()

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
        # Add class to body for welcome screen styling
        st.markdown('<div class="welcome-screen">', unsafe_allow_html=True)
        render_brand_values()
        st.markdown('</div>', unsafe_allow_html=True)
    elif not st.session_state.icp_data.get('is_completed', False):
        # Show ICP questionnaire after brand values are completed
        st.markdown('<div class="welcome-screen">', unsafe_allow_html=True)
        render_icp_definition()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Show main dashboard after all steps are completed
        render_dashboard()

if __name__ == "__main__":
    main()
