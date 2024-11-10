import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from ai_utils import generate_seo_recommendations, analyze_webpage
import pandas as pd
from utils.webpage_analysis import display_webpage_analysis

def render_seo_analyzer():
    """Render the SEO analyzer component"""
    # Center align the content
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    
    # Show logo
    st.image("logoclio.png", width=100)
    
    st.markdown("## Website Analysis")
    st.markdown("Let's analyze your website to optimize its SEO performance")
    
    # URL input
    url = st.text_input(
        "Enter your website URL",
        value=st.session_state.webpage_analysis.get('url', ''),
        placeholder="https://example.com"
    )
    
    # Analysis button
    if st.button("Analyze Website", type="primary"):
        if url:
            with st.spinner("Analyzing your website..."):
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
        else:
            st.warning("Please enter a valid URL")
    
    # Skip button
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Skip", type="secondary"):
            st.session_state.webpage_analysis['is_completed'] = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
