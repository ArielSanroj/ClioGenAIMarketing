import streamlit as st
import plotly.express as px
from ai_utils import generate_seo_recommendations

def render_seo_analyzer():
    st.markdown("## SEO Recommendations")
    
    content = st.text_area("Paste your content for SEO analysis")
    
    if st.button("Generate SEO Recommendations") and content:
        with st.spinner("Analyzing content..."):
            seo_analysis = generate_seo_recommendations(content)
            
            # Display keyword recommendations
            st.markdown("### Keyword Recommendations")
            keywords_df = {
                'Keyword': seo_analysis['keywords'],
                'Score': [85, 75, 70, 65, 60]  # Mock scores
            }
            fig = px.bar(keywords_df, x='Keyword', y='Score',
                        title='Keyword Relevance Score')
            st.plotly_chart(fig)
            
            # Meta description
            st.markdown("### Meta Description")
            st.text_area("Suggested meta description",
                        seo_analysis['meta_description'],
                        height=100)
            
            # Title suggestions
            st.markdown("### Title Suggestions")
            for title in seo_analysis['title_suggestions']:
                st.markdown(f"- {title}")
            
            # Content improvements
            st.markdown("### Content Improvement Suggestions")
            for improvement in seo_analysis['content_improvements']:
                st.markdown(f"- {improvement}")
            
            # Technical suggestions
            st.markdown("### Technical SEO Suggestions")
            for suggestion in seo_analysis['technical_suggestions']:
                st.markdown(f"- {suggestion}")
            
            # Export recommendations
            st.download_button(
                "Export SEO Recommendations",
                str(seo_analysis),
                file_name="seo_recommendations.txt",
                mime="text/plain"
            )
