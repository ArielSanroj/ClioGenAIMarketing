import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from ai_utils import generate_seo_recommendations, analyze_webpage
import pandas as pd

def render_seo_analyzer():
    st.markdown("## SEO Recommendations")
    
    # Create tabs for direct content and webpage analysis
    tab1, tab2 = st.tabs(["Content Analysis", "Webpage Analysis"])
    
    with tab1:
        content = st.text_area("Paste your content for SEO analysis", height=200)
        
        if st.button("Generate SEO Recommendations") and content:
            with st.spinner("Analyzing content..."):
                seo_analysis = generate_seo_recommendations(content)
                display_seo_analysis(seo_analysis)

    with tab2:
        url = st.text_input("Enter webpage URL for analysis", placeholder="https://example.com")
        
        if st.button("Analyze Webpage") and url:
            with st.spinner("Analyzing webpage..."):
                webpage_analysis = analyze_webpage(url)
                
                if "error" in webpage_analysis:
                    st.error(f"Error analyzing webpage: {webpage_analysis['error']}")
                else:
                    display_webpage_analysis(webpage_analysis)

def display_seo_analysis(analysis):
    """Display SEO analysis results"""
    # Keywords visualization
    st.markdown("### Keyword Recommendations")
    keywords_df = pd.DataFrame({
        'Keyword': analysis['keywords'],
        'Score': [85, 75, 70, 65, 60][:len(analysis['keywords'])]  # Mock scores
    })
    
    fig = px.bar(keywords_df, x='Keyword', y='Score',
                title='Keyword Relevance Score',
                color='Score',
                color_continuous_scale='viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    # Meta description
    st.markdown("### Meta Description")
    st.text_area("Suggested meta description",
                analysis['meta_description'],
                height=100)
    
    # Title suggestions
    st.markdown("### Title Suggestions")
    for title in analysis['title_suggestions']:
        st.markdown(f"- {title}")
    
    # Content improvements
    st.markdown("### Content Improvement Suggestions")
    for improvement in analysis['content_improvements']:
        st.markdown(f"- {improvement}")
    
    # Technical suggestions
    st.markdown("### Technical SEO Suggestions")
    for suggestion in analysis['technical_suggestions']:
        st.markdown(f"- {suggestion}")

def display_webpage_analysis(analysis):
    """Display webpage analysis results"""
    st.markdown(f"### Analysis Results for: {analysis['domain']}")
    
    # Current metadata
    with st.expander("Current Metadata", expanded=True):
        st.markdown(f"**Current Title:** {analysis['title']}")
        st.markdown(f"**Current Meta Description:** {analysis['meta_description']}")
        st.markdown(f"**Current Meta Keywords:** {analysis['meta_keywords']}")
    
    # Topics and semantic analysis
    st.markdown("### Content Topics")
    topics_df = pd.DataFrame({
        'Topic': analysis['analysis']['topics'],
        'Relevance': [90, 85, 80, 75, 70][:len(analysis['analysis']['topics'])]  # Mock scores
    })
    
    fig = px.bar(topics_df, x='Topic', y='Relevance',
                title='Topic Relevance Analysis',
                color='Relevance',
                color_continuous_scale='viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    # Semantic topics visualization
    st.markdown("### Semantic Topic Map")
    semantic_topics = analysis['analysis']['semantic_topics']
    if semantic_topics:
        fig = go.Figure(data=[go.Sunburst(
            labels=[item for sublist in [[topic, *[f"{topic}-{i}" for i in range(3)]] 
                    for topic in semantic_topics] for item in sublist],
            parents=['' if '-' not in label else label.split('-')[0] 
                    for sublist in [[topic, *[topic for i in range(3)]] 
                    for topic in semantic_topics] for label in sublist],
            values=[10 if '-' not in label else 5 
                   for sublist in [[topic, *[f"{topic}-{i}" for i in range(3)]] 
                   for topic in semantic_topics] for label in sublist],
        )])
        fig.update_layout(title="Semantic Topic Distribution")
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
    
    # Export options
    st.markdown("### Export Analysis")
    export_data = {
        "url": analysis['url'],
        "analysis_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis_results": analysis['analysis']
    }
    
    st.download_button(
        "Download Analysis Report",
        data=pd.DataFrame([export_data]).to_csv(index=False),
        file_name=f"seo_analysis_{analysis['domain']}.csv",
        mime="text/csv"
    )
