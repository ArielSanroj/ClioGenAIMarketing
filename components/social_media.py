import streamlit as st
import plotly.express as px
from ai_utils import generate_marketing_content

def render_social_media_campaign():
    st.markdown("## Social Media Campaign Creator")
    
    platforms = ["Instagram", "Twitter", "LinkedIn", "Facebook"]
    selected_platforms = st.multiselect("Select Platforms", platforms)
    
    campaign_objective = st.text_area("Campaign Objective")
    target_audience = st.text_input("Target Audience")
    
    if st.button("Create Campaign") and selected_platforms and campaign_objective:
        with st.spinner("Generating campaign content..."):
            for platform in selected_platforms:
                content = generate_marketing_content(
                    f"Campaign Objective: {campaign_objective}\nTarget Audience: {target_audience}",
                    f"{platform} post"
                )
                
                with st.expander(f"{platform} Content"):
                    st.markdown(f"**Post:**\n{content['content']}")
                    st.markdown("**Suggested Hashtags:**")
                    st.markdown(", ".join(content['keywords']))
                    
                    # Create mock engagement predictions
                    engagement_data = {
                        'Metric': ['Likes', 'Comments', 'Shares'],
                        'Predicted': [100, 20, 15]
                    }
                    fig = px.bar(engagement_data, x='Metric', y='Predicted',
                                title=f'Predicted Engagement for {platform}')
                    st.plotly_chart(fig)
