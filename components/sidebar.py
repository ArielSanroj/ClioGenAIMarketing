import streamlit as st

def render_sidebar():
    with st.sidebar:
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
                # If ICP not completed, set state to trigger questionnaire
                st.session_state.show_icp_questionnaire = True
                selected_option = "icp_questionnaire"
            else:
                # If completed, show summary
                selected_option = "icp_summary"
        
        # Handle other navigation buttons
        for label, value in menu_options.items():
            if label not in ["View my ICP"] and st.button(label, key=f"menu_{value}"):
                selected_option = value
                st.session_state.selected_option = value
                if value == "archetypes":
                    st.session_state.archetype_view = 'archetypes'
                st.rerun()
        
        return selected_option
