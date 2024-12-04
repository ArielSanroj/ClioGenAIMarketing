import streamlit as st
import plotly.express as px
from ai_utils import analyze_audience, map_audience_to_archetypes


def render_audience_analyzer():
    """
    Render the audience analyzer interface with demographic, psychographic, and archetype insights.
    """
    st.markdown("## Target Audience Analysis")

    # User input for business information
    business_info = st.text_area("Tell us about your business and current audience")

    # Button to analyze audience
    if st.button("Analyze Audience") and business_info:
        with st.spinner("Analyzing audience..."):
            # Get analysis results
            analysis = analyze_audience(business_info)

            # Display demographics
            st.markdown("### Demographics")
            demographics = analysis.get('demographics', {})
            if demographics:
                # Age distribution chart
                age_data = {
                    'Age Group': demographics.get('age_groups', []),
                    'Percentage': demographics.get('percentages', [])
                }
                if age_data['Age Group']:
                    fig_age = px.pie(
                        age_data,
                        values='Percentage',
                        names='Age Group',
                        title='Age Distribution'
                    )
                    st.plotly_chart(fig_age)
                else:
                    st.write("No age group data available.")

                # Key interests
                st.markdown("### Key Interests")
                interests = demographics.get('interests', [])
                if interests:
                    for interest in interests:
                        st.markdown(f"- {interest}")
                else:
                    st.write("No interests data available.")

                # Top locations
                st.markdown("### Top Locations")
                locations = demographics.get('locations', [])
                if locations:
                    for location in locations:
                        st.markdown(f"- {location}")
                else:
                    st.write("No location data available.")

            # Display psychographics
            st.markdown("### Psychographic Profile")
            psychographics = analysis.get('psychographics', [])
            if psychographics:
                for trait in psychographics:
                    st.markdown(f"- {trait}")
            else:
                st.write("No psychographic data available.")

            # Map audience to archetypes
            st.markdown("### Archetype Mapping")
            archetype_mapping = map_audience_to_archetypes(analysis)
            if archetype_mapping:
                for archetype, details in archetype_mapping.items():
                    st.markdown(f"**{archetype.capitalize()} Archetype:**")
                    st.write(f"- Engagement Platform: {details['platform']}")
                    st.write(f"- Best Time to Engage: {details['time']}")
                    st.write(f"- Content Strategy: {details['content_strategy']}")

            # Display pain points
            st.markdown("### Pain Points")
            pain_points = analysis.get('pain_points', [])
            if pain_points:
                for point in pain_points:
                    st.markdown(f"- {point}")
            else:
                st.write("No pain points data available.")

            # Display recommendations
            st.markdown("### Recommendations")
            recommendations = analysis.get('recommendations', [])
            if recommendations:
                for rec in recommendations:
                    st.markdown(f"- {rec}")
            else:
                st.write("No recommendations available.")

            # Export option
            export_data = f"""
            Audience Analysis Report

            Demographics:
            {demographics}

            Psychographics:
            {psychographics}

            Pain Points:
            {pain_points}

            Archetype Mapping:
            {archetype_mapping}

            Recommendations:
            {recommendations}
            """
            st.download_button(
                "Export Analysis",
                export_data,
                file_name="audience_analysis.txt",
                mime="text/plain"
            )


# Utility to map audience data to archetypes (in ai_utils.py or locally defined here)
def map_audience_to_archetypes(audience_data):
    """
    Map audience insights to relevant archetypes with strategies.
    """
    # Mocked archetype mapping logic; replace with real analysis
    demographics = audience_data.get('demographics', {})
    interests = demographics.get('interests', [])
    archetype_mapping = {}

    if "efficiency" in interests or "growth" in interests:
        archetype_mapping['autonomous'] = {
            'platform': 'LinkedIn',
            'time': '8am-11am',
            'content_strategy': 'Case studies, ROI-focused reports, and professional blogs.'
        }
    if "emotions" in interests or "trending topics" in interests:
        archetype_mapping['impulsive'] = {
            'platform': 'Instagram',
            'time': '7pm-10pm',
            'content_strategy': 'Flash sales, emotional storytelling, and vibrant visuals.'
        }
    if "privacy" in interests or "simplicity" in interests:
        archetype_mapping['isolative'] = {
            'platform': 'Email',
            'time': '9am-12pm',
            'content_strategy': 'Personalized, empathetic content focused on simplicity and privacy.'
        }
    if "escape" in interests or "relaxation" in interests:
        archetype_mapping['avoidant'] = {
            'platform': 'YouTube',
            'time': '6pm-9pm',
            'content_strategy': 'Immersive videos, aspirational stories, and calming visuals.'
        }

    return archetype_mapping


if __name__ == "__main__":
    render_audience_analyzer()
