import streamlit as st
from components.seo_analyzer import render_seo_analyzer
from components.data_input import render_data_input
from components.archetype_alignment import render_archetype_alignment
from components.marketing_recommendations import render_marketing_recommendations
from auth import is_authenticated
from auth_pages import render_auth_pages  # Import from correct module

from components.recommendation_executor import render_recommendation_executor

def main():
    """Main function for the AI Marketing Assistant."""
    st.set_page_config(
        page_title="AI Marketing Assistant",
        page_icon="assets/logoclio.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Check if user is authenticated
    if not is_authenticated():
        render_auth_pages()  # Show login/registration pages
        return  # Exit the app if not authenticated

    # Sidebar Navigation
    st.sidebar.title("AI Marketing Assistant")
    options = [
        "SEO Analyzer",
        "Data Input",
        "Archetype Alignment",
        "Marketing Recommendations"
    ]
    choice = st.sidebar.radio("Navigation", options)

    # Route based on user selection
    if choice == "SEO Analyzer":
        render_seo_analyzer()
        if 'webpage_analysis' in st.session_state and st.session_state.webpage_analysis.get("is_completed"):
            render_recommendation_executor()
    elif choice == "Data Input":
        render_data_input()
    elif choice == "Archetype Alignment":
        render_archetype_alignment()
    elif choice == "Marketing Recommendations":
        render_marketing_recommendations()

if __name__ == "__main__":
    main()
