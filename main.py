import streamlit as st
from components.sidebar import render_sidebar
from components.content_generator import render_content_generator
from components.social_media import render_social_media_campaign
from components.seo_analyzer import render_seo_analyzer
from components.brand_values import render_brand_values
from components.consumer_archetypes import render_consumer_archetypes
from styles import apply_custom_styles
from auth import is_authenticated
from auth_pages import render_auth_pages
from utils.session_manager import get_user_state, get_current_user_id, set_user_state
from plotly import express as px
from components.icp_definition import render_icp_questionnaire
from components.chat_interface import render_chat_interface


def initialize_state(user_id):
    """Initialize default states for all components."""
    default_states = {
        "brand_values": {"is_completed": False},
        "icp_data": {"is_completed": False},
        "seo_analyzer": {"is_completed": False},
        "content_generator": {"is_completed": False},
    }
    for key, default in default_states.items():
        if not get_user_state(user_id, key):
            set_user_state(user_id, key, default)


def next_incomplete_stage(user_id):
    """Determine the next incomplete stage in the user flow."""
    stages = ["brand_values", "icp_data", "seo_analyzer", "content_generator"]
    for stage in stages:
        if not get_user_state(user_id, stage).get('is_completed', False):
            return stage
    return None


def render_dashboard():
    """Render the home dashboard with metrics and insights."""
    user_id = get_current_user_id()

    st.markdown("## Marketing Dashboard")

    # Example Metrics
    alignment_data = {
        'Archetype': ['Autonomous', 'Impulsive', 'Avoidant', 'Isolated'],
        'Alignment Score': [85, 70, 60, 90]  # Example scores
    }
    fig_alignment = px.bar(
        alignment_data,
        x='Archetype',
        y='Alignment Score',
        title='Archetype-Brand Alignment',
        color='Archetype',
        text='Alignment Score'
    )
    fig_alignment.update_layout(xaxis_title="Archetype", yaxis_title="Alignment Score")
    st.plotly_chart(fig_alignment)

    st.markdown("### Campaign Performance by Archetype")
    campaign_data = {
        'Archetype': ['Autonomous', 'Impulsive', 'Avoidant', 'Isolated'],
        'CTR': [8.5, 5.2, 3.9, 7.8],  # Click-through rates
        'Conversions': [120, 80, 50, 100]
    }
    fig_campaign = px.scatter(
        campaign_data,
        x='CTR',
        y='Conversions',
        size='Conversions',
        color='Archetype',
        hover_name='Archetype',
        title='Campaign Performance by Archetype'
    )
    fig_campaign.update_layout(xaxis_title="Click-Through Rate (%)", yaxis_title="Conversions")
    st.plotly_chart(fig_campaign)

    st.markdown("### Engagement Trends by Time and Platform")
    trend_data = pd.DataFrame({
        'Time': ['8am', '10am', '12pm', '2pm', '4pm', '6pm'],
        'LinkedIn': [120, 140, 130, 150, 160, 170],
        'Instagram': [200, 230, 210, 250, 270, 300],
    })
    fig_trends = px.line(
        trend_data,
        x='Time',
        y=['LinkedIn', 'Instagram'],
        title='Engagement Trends by Time and Platform',
        labels={'value': 'Engagement', 'variable': 'Platform'}
    )
    fig_trends.update_layout(xaxis_title="Time", yaxis_title="Engagement")
    st.plotly_chart(fig_trends)


def main():
    st.set_page_config(
        page_title="AI Marketing Assistant",
        page_icon="assets/logoclio.png",
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
    initialize_state(user_id)

    try:
        # Determine the next stage in the onboarding process
        next_stage = next_incomplete_stage(user_id)
        if next_stage == "brand_values":
            st.markdown('<div class="welcome-screen">', unsafe_allow_html=True)
            render_brand_values()
            st.markdown('</div>', unsafe_allow_html=True)
        elif next_stage == "icp_data":
            st.markdown('<div class="welcome-screen">', unsafe_allow_html=True)
            render_icp_questionnaire()
            st.markdown('</div>', unsafe_allow_html=True)
        elif next_stage == "seo_analyzer":
            st.markdown('<div class="welcome-screen">', unsafe_allow_html=True)
            render_seo_analyzer()
            st.markdown('</div>', unsafe_allow_html=True)
        elif next_stage == "content_generator":
            st.markdown('<div class="welcome-screen">', unsafe_allow_html=True)
            render_content_generator()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Render sidebar and dashboard if all stages are completed
            selected_option = render_sidebar()
            current_option = get_user_state(user_id, "selected_option")
            if selected_option:
                set_user_state(user_id, "selected_option", selected_option)

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
                render_icp_questionnaire()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.write("Please refresh the page or contact support.")


if __name__ == "__main__":
    main()
