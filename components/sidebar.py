import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("""
            <style>
            .css-1d391kg {
                background-color: #FFFFFF;
            }
            section[data-testid="stSidebar"] {
                background-color: #FFFFFF;
                border-right: 1px solid #E5E7EB;
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
        
        st.image("logoclio.png", width=100)
        
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
            if not st.session_state.icp_data.get('is_completed', False):
                st.session_state.show_icp_questionnaire = True
                selected_option = "icp_questionnaire"
            else:
                selected_option = "icp_summary"
        
        # Handle other navigation buttons
        for label, value in menu_options.items():
            if label not in ["View my ICP"]:
                if st.button(label, key=f"menu_{value}"):
                    selected_option = value
                    st.session_state.selected_option = value
                    # Reset chat state when clicking "New Chat"
                    if value == "new_chat":
                        st.session_state.chat_history = []
                        st.session_state.current_chat_id = None
                        st.session_state.selected_option = "home"  # Changed to "home"
                        st.session_state.content_form_state = {  # Reset content form state
                            'story': '',
                            'content_type': '',
                            'platform': '',
                            'tone': '',
                            'competitor_insights': '',
                            'generated_content': None
                        }
                    elif value == "archetypes":
                        st.session_state.archetype_view = 'archetypes'
                    st.rerun()
        
        return selected_option
