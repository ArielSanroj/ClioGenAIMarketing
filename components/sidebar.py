import streamlit as st
from utils.session_manager import get_user_state, get_current_user_id, set_user_state

def render_sidebar():
    """Render the sidebar navigation with proper styling."""
    user_id = get_current_user_id()
    
    with st.sidebar:
        st.markdown("""
            <style>
            section[data-testid="stSidebar"] {
                background-color: #F3F1FF !important;
                width: 300px !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Logo at top
        st.image("assets/logoclio.png", width=100)
        
        # Navigation buttons with proper styling
        st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
        
        # Handle ICP view button
        if st.button("View my ICP", key="menu_icp", use_container_width=True):
            icp_data = get_user_state(user_id, "icp_data") or {}
            if not icp_data.get('is_completed', False):
                set_user_state(user_id, "selected_option", "icp_questionnaire")
                selected_option = "icp_questionnaire"
            else:
                set_user_state(user_id, "selected_option", "icp_summary")
                selected_option = "icp_summary"
        
        # Other navigation buttons
        menu_options = {
            "Market analysis": "market_analysis",
            "Consumer Archetypes": "archetypes",
            "New Chat": "new_chat",
            "Chats history": "history"
        }
        
        for label, value in menu_options.items():
            if st.button(label, key=f"menu_{value}", use_container_width=True):
                if value == "new_chat":
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
                st.rerun()
        
        # Add spacer to push logout to bottom
        st.markdown('<div style="flex-grow: 1;"></div>', unsafe_allow_html=True)
        
        # Logout button at bottom
        if st.button("Log out", key="logout_button", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    return get_user_state(user_id, "selected_option")