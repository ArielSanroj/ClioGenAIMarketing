import streamlit as st
from utils.session_manager import get_user_state, get_current_user_id, set_user_state

def render_sidebar():
    """Render the sidebar navigation"""
    user_id = get_current_user_id()
    
    # Initialize ICP state if not exists
    if not get_user_state(user_id, "icp_data"):
        set_user_state(user_id, "icp_data", {
            'knowledge_level': '',
            'current_question': 1,
            'demographics': {},
            'psychographics': {},
            'archetype': '',
            'pain_points': [],
            'goals': [],
            'answers': {},
            'is_completed': False
        })
    
    with st.sidebar:
        st.markdown("""
            <style>
            .css-1d391kg {
                background-color: #FFFFFF;
            }
            section[data-testid="stSidebar"] {
                background-color: #FFFFFF;
                border-right: 1px solid #E5E7EB;
                display: flex;
                flex-direction: column;
                min-height: 100vh;
            }
            .stButton>button {
                width: 100%;
                text-align: left;
                padding: 0.75rem 1rem;
                background: transparent;
                color: #1E1B4B;
                border: none;
                font-size: 1rem;
                font-weight: 500;
            }
            .stButton>button:hover {
                background-color: #F3F4F6;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.image("assets/logoclio.png", width=100)
        
        st.markdown("### Navigation")
        
        menu_options = {
            "View my ICP": "icp",
            "Market analysis": "market_analysis",
            "Consumer Archetypes": "archetypes",
            "New Chat": "new_chat",
            "Chats history": "history"
        }
        
        selected_option = None
        
        # Handle ICP view button specially
        if st.button("View my ICP", key=f"menu_icp"):
            icp_data = get_user_state(user_id, "icp_data") or {}
            if not icp_data.get('is_completed', False):
                set_user_state(user_id, "selected_option", "icp_questionnaire")
                selected_option = "icp_questionnaire"
            else:
                set_user_state(user_id, "selected_option", "icp_summary")
                selected_option = "icp_summary"
        
        # Handle other navigation buttons
        for label, value in menu_options.items():
            if label not in ["View my ICP"]:
                if st.button(label, key=f"menu_{value}"):
                    if value == "new_chat":
                        # Reset chat state when clicking "New Chat"
                        set_user_state(user_id, "chat_history", [])
                        set_user_state(user_id, "current_chat_id", None)
                        set_user_state(user_id, "selected_option", "home")
                        set_user_state(user_id, "content_form_state", {
                            'story': '',
                            'content_type': '',
                            'platform': '',
                            'tone': '',
                            'competitor_insights': '',
                            'generated_content': None
                        })
                    elif value == "archetypes":
                        set_user_state(user_id, "archetype_view", 'archetypes')
                    
                    set_user_state(user_id, "selected_option", value)
                    selected_option = value
                    st.rerun()
        
        # Add spacer to push logout button to bottom
        st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)
        
        # Add logout button at bottom
        if st.button("Log out", key="logout_button"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        return selected_option
