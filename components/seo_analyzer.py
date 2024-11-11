import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from ai_utils import generate_seo_recommendations, analyze_webpage
import pandas as pd
from utils.webpage_analysis import display_webpage_analysis

def initialize_session_state():
    """Initialize the session state variables for SEO analyzer"""
    if 'webpage_analysis' not in st.session_state:
        st.session_state.webpage_analysis = {
            'url': '',
            'analysis': {},
            'is_completed': False
        }

def render_seo_analyzer():
    """Render the SEO analyzer component"""
    initialize_session_state()
    
    # Center align the content
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    
    # Show logo
    st.image("logoclio.png", width=100)
    
    st.markdown("## Website Analysis")
    st.markdown("Let's analyze your website to optimize its SEO performance")
    
    # URL input with example and validation
    url = st.text_input(
        "Enter your website URL",
        value=st.session_state.webpage_analysis.get('url', ''),
        placeholder="https://example.com",
        help="Enter the full URL including https://"
    )
    
    # Analysis button
    if st.button("Analyze Website", type="primary"):
        if url:
            if not url.startswith(('http://', 'https://')):
                st.error("Please enter a valid URL starting with http:// or https://")
            else:
                with st.spinner("Analyzing your website..."):
                    try:
                        webpage_analysis = analyze_webpage(url)
                        
                        if "error" in webpage_analysis:
                            st.error(f"Error analyzing webpage: {webpage_analysis['error']}")
                        else:
                            # Save analysis results in session state
                            st.session_state.webpage_analysis.update({
                                'url': url,
                                'analysis': webpage_analysis,
                                'is_completed': True
                            })
                            
                            # Display analysis results
                            display_webpage_analysis(webpage_analysis)
                            
                            # Show completion button
                            if st.button("Complete Analysis", type="primary"):
                                st.rerun()
                    except Exception as e:
                        st.error(f"An error occurred during analysis: {str(e)}")
        else:
            st.warning("Please enter a valid URL")
    
    # Show sample analysis option
    with st.expander("🔍 Want to see a sample analysis?"):
        if st.button("Run Sample Analysis"):
            sample_url = "https://example.com"
            with st.spinner("Generating sample analysis..."):
                try:
                    sample_analysis = {
                        "url": sample_url,
                        "domain": "example.com",
                        "title": "Example Website",
                        "meta_description": "A sample website for demonstration",
                        "meta_keywords": "example, demo, sample",
                        "analysis": {
                            "topics": ["Sample Topic 1", "Sample Topic 2", "Sample Topic 3"],
                            "traffic_potential": {
                                "estimated_monthly_visits": 1000,
                                "engagement_metrics": {
                                    "avg_time_on_page": "2:30",
                                    "bounce_rate": "45%"
                                }
                            },
                            "content_gaps": ["Missing About page", "No blog section"],
                            "keyword_suggestions": ["sample keyword 1", "sample keyword 2"],
                            "meta_suggestions": {
                                "title": "Example Website - Your Sample Site",
                                "description": "An improved meta description for the sample website."
                            },
                            "content_recommendations": [
                                "Add more detailed product descriptions",
                                "Include customer testimonials"
                            ],
                            "estimated_word_count": 500,
                            "readability_score": 85
                        }
                    }
                    display_webpage_analysis(sample_analysis)
                except Exception as e:
                    st.error(f"Error generating sample analysis: {str(e)}")
    
    # Skip button
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Skip", type="secondary"):
            st.session_state.webpage_analysis['is_completed'] = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
