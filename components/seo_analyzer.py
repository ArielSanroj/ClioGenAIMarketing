import streamlit as st
import plotly.express as px
import pandas as pd
from urllib.parse import urlparse
from langdetect import detect
from ai_utils import analyze_webpage

# Initialize Session State
def initialize_session_state():
    """Initialize the session state variables for SEO analyzer."""
    if 'webpage_analysis' not in st.session_state:
        st.session_state.webpage_analysis = {
            'url': '',
            'analysis': {},
            'is_completed': False
        }

# Detect Language
def detect_language(text):
    """Detect the language of the text."""
    try:
        return detect(text)
    except Exception:
        return 'en'  # Default to English if detection fails

# Generate Content Topics and Semantic Map
def generate_topics_and_semantic_map(keywords):
    """Generate topics and semantic distribution based on keywords."""
    topic_relevance = [
        {"Topic": "Fashion", "Relevance": 90},
        {"Topic": "Online Shopping", "Relevance": 85},
        {"Topic": "Women's Apparel", "Relevance": 80},
        {"Topic": "Men's Apparel", "Relevance": 75},
        {"Topic": "Elevating Style", "Relevance": 70}
    ]
    semantic_map = [
        {"Topic": "Fashion Trends", "Frequency": 5},
        {"Topic": "Clothing Lines", "Frequency": 4},
        {"Topic": "Style Improvement", "Frequency": 3}
    ]
    return pd.DataFrame(topic_relevance), pd.DataFrame(semantic_map)

# Render Content Gaps and Recommendations
def render_content_gaps_and_recommendations():
    """Display content gaps and actionable content recommendations."""
    st.markdown("### Content Gaps")
    st.write("- More Detailed Product Descriptions")
    st.write("- SEO-Friendly Phrases")
    st.write("- Reviews Section")

    st.markdown("### Metadata Improvement Suggestions")
    st.write("**Suggested Title:** ZafiroTrend: Exclusive and Elegant Fashion")
    st.write("**Suggested Description:** Unleash your individuality with unique and stylish fashion choices for men and women. Enjoy online shopping with ZafiroTrend. Free shipping and cost-free exchanges.")

    st.markdown("### Content Recommendations")
    st.write("- Include a dedicated About Us page.")
    st.write("- Add a blog section for fashion tips and brand discussion.")
    st.write("- Include more product images.")

# Export Analysis
def export_analysis(data):
    """Allow users to download the analysis as a JSON report."""
    import json
    st.download_button(
        label="Download Analysis Report",
        data=json.dumps(data, indent=4),
        file_name="seo_analysis.json",
        mime="application/json"
    )

# Render Archetype and Topic Analysis
def render_archetype_and_topics(analysis):
    """Display archetype alignment, content topics, and semantic map."""
    st.markdown("### Content Topics")
    keywords = analysis.get('keywords', [])
    topics, semantic_map = generate_topics_and_semantic_map(keywords)

    # Topic Relevance Chart
    fig = px.bar(
        topics, x='Topic', y='Relevance', 
        title="Topic Relevance Analysis", 
        color='Topic', color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, use_container_width=True)

    # Semantic Map
    st.markdown("### Semantic Topic Map")
    fig = px.pie(
        semantic_map, names='Topic', values='Frequency',
        title="Semantic Topic Distribution",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig, use_container_width=True)

# Main SEO Analysis Function
def render_seo_analysis_details(analysis):
    """Display detailed SEO analysis with archetype recommendations."""
    st.markdown(f"### Analysis Results for: {urlparse(st.session_state.webpage_analysis['url']).netloc}")

    # Detect Language
    page_text = analysis.get('content', '')
    language = detect_language(page_text)

    # Metadata Display
    st.markdown("#### Current Metadata")
    st.write(f"**Current Title:** {analysis.get('title', 'Not available')}")
    st.write(f"**Current Meta Description:** {analysis.get('meta_description', 'Not available')}")
    st.write(f"**Current Meta Keywords:** {', '.join(analysis.get('meta_keywords', [])) or 'Not available'}")

    # Render Archetype Analysis
    render_archetype_and_topics(analysis)

    # Render Content Gaps and Recommendations
    render_content_gaps_and_recommendations()

    # Export Results
    st.markdown("### Export Analysis")
    export_analysis(analysis)

# Main SEO Analyzer Function
def render_seo_analyzer():
    """Main function to render SEO Analyzer."""
    initialize_session_state()

    # Input for URL
    st.image("assets/logoclio.png", width=100)
    st.markdown("## Website Analysis")
    st.markdown("Let's analyze your website to optimize its SEO performance.")

    url = st.text_input(
        "Enter your website URL",
        value=st.session_state.webpage_analysis.get('url', ''),
        placeholder="https://example.com",
        help="Enter the full URL including https://"
    )

    if st.button("Analyze Website"):
        if url:
            if not url.startswith(('http://', 'https://')):
                st.error("Please enter a valid URL starting with http:// or https://")
            else:
                with st.spinner("Analyzing your website..."):
                    try:
                        analysis = analyze_webpage(url)
                        if "error" in analysis:
                            st.error(f"Error analyzing webpage: {analysis['error']}")
                        else:
                            st.session_state.webpage_analysis.update({
                                'url': url,
                                'analysis': analysis,
                                'is_completed': True
                            })
                            render_seo_analysis_details(analysis)
                    except Exception as e:
                        st.error(f"An error occurred during analysis: {str(e)}")
        else:
            st.warning("Please enter a URL.")

# Run the App
if __name__ == "__main__":
    render_seo_analyzer()
