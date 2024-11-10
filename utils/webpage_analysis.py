import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def display_webpage_analysis(analysis):
    """Display webpage analysis results with improved styling"""
    st.markdown(f"### Analysis Results for: {analysis['domain']}")
    
    # Progress indicator
    st.progress(1.0)
    
    # Current metadata
    with st.expander("Current Metadata", expanded=True):
        st.markdown(f"**Current Title:** {analysis['title']}")
        st.markdown(f"**Current Meta Description:** {analysis['meta_description']}")
        st.markdown(f"**Current Meta Keywords:** {analysis['meta_keywords']}")
    
    # Topics and semantic analysis
    st.markdown("### Content Topics")
    topics_df = pd.DataFrame({
        'Topic': analysis['analysis']['topics'],
        'Relevance': [90, 85, 80, 75, 70][:len(analysis['analysis']['topics'])]
    })
    
    fig = px.bar(topics_df, x='Topic', y='Relevance',
                title='Topic Relevance Analysis',
                color='Relevance',
                color_continuous_scale='viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    # Content gaps and recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Content Gaps")
        for gap in analysis['analysis']['content_gaps']:
            st.markdown(f"- {gap}")
    
    with col2:
        st.markdown("### Keyword Suggestions")
        for keyword in analysis['analysis']['keyword_suggestions']:
            st.markdown(f"- {keyword}")
    
    # Meta suggestions
    st.markdown("### Metadata Improvement Suggestions")
    meta_suggestions = analysis['analysis']['meta_suggestions']
    st.markdown(f"**Suggested Title:** {meta_suggestions['title']}")
    st.markdown(f"**Suggested Description:** {meta_suggestions['description']}")
    
    # Content recommendations
    st.markdown("### Content Recommendations")
    for recommendation in analysis['analysis']['content_recommendations']:
        st.markdown(f"- {recommendation}")
    
    # Content metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Estimated Word Count", analysis['analysis']['estimated_word_count'])
    with col2:
        st.metric("Readability Score", f"{analysis['analysis']['readability_score']}/100")
