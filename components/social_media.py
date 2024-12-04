import streamlit as st
import plotly.express as px
from ai_utils import generate_marketing_content

# Platform-specific recommendations
platform_recommendations = {
    'LinkedIn': "Use a professional tone, focus on data and ROI to appeal to professionals.",
    'Instagram': "Leverage vibrant visuals, emotional stories, and hashtags for quick engagement.",
    'Twitter': "Keep posts concise, use trending hashtags, and focus on real-time relevance.",
    'Facebook': "Create community-driven posts, share relatable stories, and encourage discussions.",
    'YouTube': "Create short, engaging explainer videos or behind-the-scenes content."
}

def render_social_media_campaign():
    """
    Render the social media campaign creator interface with platform-specific content suggestions.
    """
    st.markdown("## Social Media Campaign Creator")

    # Select platforms
    platforms = ["Instagram", "Twitter", "LinkedIn", "Facebook", "YouTube"]
    selected_platforms = st.multiselect("Select Platforms", platforms)

    # Campaign details
    campaign_objective = st.text_area("Campaign Objective", placeholder="What is the main goal of this campaign?")
    target_audience = st.text_input("Target Audience", placeholder="Who are you targeting with this campaign?")

    if st.button("Create Campaign") and selected_platforms and campaign_objective:
        with st.spinner("Generating campaign content..."):
            for platform in selected_platforms:
                # Generate content
                platform_guidance = platform_recommendations.get(platform, "No specific guidance available.")
                content_prompt = (
                    f"Platform: {platform}\n"
                    f"Campaign Objective: {campaign_objective}\n"
                    f"Target Audience: {target_audience}\n"
                    f"Guidance: {platform_guidance}"
                )
                content = generate_marketing_content(content_prompt, f"{platform} post")

                # Display content
                with st.expander(f"{platform} Content"):
                    st.markdown(f"### Post for {platform}")
                    st.markdown(f"**Content:**\n{content.get('content', 'No content generated.')}")
                    st.markdown(f"**Platform Guidance:** {platform_guidance}")

                    if content.get('keywords'):
                        st.markdown("**Suggested Hashtags:**")
                        st.markdown(", ".join(content['keywords']))

                    # Create mock engagement predictions
                    engagement_data = {
                        'Metric': ['Likes', 'Comments', 'Shares'],
                        'Predicted': [100, 20, 15]  # Replace with dynamic predictions if available
                    }
                    fig = px.bar(
                        engagement_data, 
                        x='Metric', 
                        y='Predicted',
                        title=f'Predicted Engagement for {platform}'
                    )
                    st.plotly_chart(fig)


if __name__ == "__main__":
    render_social_media_campaign()
