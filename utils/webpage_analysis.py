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
    topics = analysis['analysis']['topics']
    # Generate relevance scores dynamically based on number of topics
    relevance_scores = [90 - (i * 5) for i in range(len(topics))]
    
    topics_df = pd.DataFrame({
        'Topic': topics,
        'Relevance': relevance_scores
    })
    
    fig = px.bar(topics_df, x='Topic', y='Relevance',
                title='Topic Relevance Analysis',
                color='Relevance',
                color_continuous_scale='viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    # Traffic Potential Metrics
    st.markdown("### Traffic & Engagement Metrics")
    col1, col2, col3 = st.columns(3)
    
    traffic_potential = analysis['analysis'].get('traffic_potential', {})
    with col1:
        st.metric("Est. Monthly Visits", 
                 traffic_potential.get('estimated_monthly_visits', 0))
    with col2:
        st.metric("Avg. Time on Page", 
                 traffic_potential.get('engagement_metrics', {}).get('avg_time_on_page', '0:00'))
    with col3:
        st.metric("Bounce Rate", 
                 traffic_potential.get('engagement_metrics', {}).get('bounce_rate', '0%'))
    
    # Market Trends Analysis
    st.markdown("### Market Trends")
    market_trends = analysis['analysis'].get('market_trends', {})
    
    # Search Volume Trend
    if 'search_volume' in market_trends:
        search_data = market_trends['search_volume']
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=search_data.get('data', [0]*12),
            mode='lines+markers',
            name='Search Volume'
        ))
        fig.update_layout(title='Monthly Search Volume Trend',
                         xaxis_title='Month',
                         yaxis_title='Search Volume')
        st.plotly_chart(fig, use_container_width=True)
    
    # Regional Popularity Heatmap
    if 'regional_popularity' in market_trends:
        regional_data = market_trends['regional_popularity']
        region_df = pd.DataFrame({
            'Region': regional_data.get('top_regions', []),
            'Score': regional_data.get('scores', [])
        })
        
        fig = px.choropleth(region_df,
                          locations='Region',
                          locationmode='country names',
                          color='Score',
                          title='Regional Popularity Distribution',
                          color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    # Competition Analysis
    st.markdown("### Competition Analysis")
    if 'competition' in market_trends:
        competition = market_trends['competition']
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Competition Level:** {competition.get('level', 'N/A')}")
        with col2:
            st.markdown(f"**Analysis:** {competition.get('analysis', 'N/A')}")
    
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
    
    # Export Analysis
    st.markdown("### Export Analysis")
    export_data = pd.DataFrame([{
        'url': analysis['url'],
        'analysis_date': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        'analysis_results': json.dumps(analysis['analysis'])
    }])
    
    st.download_button(
        "Download Analysis Report",
        data=export_data.to_csv(index=False),
        file_name=f"seo_analysis_{analysis['domain']}.csv",
        mime="text/csv"
    )
