import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.image("logoclio.png", width=100)
        
        st.markdown("### Navigation")
        
        menu_options = {
            "View my ICP": "icp",
            "Market analysis": "market_analysis",
            "Consumer Archetypes": "archetypes",
            "Social Media Sentiment": "sentiment",
            "New Chat": "new_chat",
            "Chats history": "history"
        }
        
        selected_option = None
        for label, value in menu_options.items():
            if st.button(label, key=f"menu_{value}"):
                selected_option = value
                
        return selected_option
