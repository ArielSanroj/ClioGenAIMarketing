import streamlit as st
import plotly.express as px
from ai_utils import analyze_audience

def render_audience_analyzer():
    st.markdown("## Target Audience Analysis")
    
    business_info = st.text_area("Tell us about your business and current audience")
    
    if st.button("Analyze Audience") and business_info:
        with st.spinner("Analyzing audience..."):
            analysis = analyze_audience(business_info)
            
            # Display demographics
            st.markdown("### Demographics")
            demographics = analysis['demographics']
            
            # Age distribution chart
            age_data = {'Age Group': demographics['age_groups'],
                       'Percentage': [20, 35, 25, 15, 5]}  # Mock percentages
            fig_age = px.pie(age_data, values='Percentage', names='Age Group',
                           title='Age Distribution')
            st.plotly_chart(fig_age)
            
            # Interests word cloud
            st.markdown("### Key Interests")
            for interest in demographics['interests']:
                st.markdown(f"- {interest}")
            
            # Locations
            st.markdown("### Top Locations")
            for location in demographics['locations']:
                st.markdown(f"- {location}")
            
            # Psychographics
            st.markdown("### Psychographic Profile")
            for trait in analysis['psychographics']:
                st.markdown(f"- {trait}")
            
            # Export option
            export_data = f"""
            Audience Analysis Report
            
            Demographics:
            {demographics}
            
            Psychographics:
            {analysis['psychographics']}
            
            Pain Points:
            {analysis['pain_points']}
            
            Recommendations:
            {analysis['recommendations']}
            """
            
            st.download_button(
                "Export Analysis",
                export_data,
                file_name="audience_analysis.txt",
                mime="text/plain"
            )
