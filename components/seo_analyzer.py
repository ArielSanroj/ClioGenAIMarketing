import streamlit as st
import plotly.express as px
import pandas as pd
from langdetect import detect
from ai_utils import analyze_webpage
from urllib.parse import urlparse
import langdetect
# Removed circular import

# Initialize Session State
def initialize_session_state():
    """Initialize the session state variables for SEO analyzer."""
    if 'webpage_analysis' not in st.session_state:
        st.session_state.webpage_analysis = {
            'url': '',
            'analysis': {},
            'is_completed': False
        }
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False

# Archetype and Subscale Mapping
def map_archetypes_and_subscales(keywords, language):
    """Map keywords to archetypes and subscales in English and Spanish."""
    archetype_data = {
        'Autonomous': {
            'Focus on solving the problem': {
                'keywords': ['efficient', 'practical', 'results', 'eficiente', 'práctico', 'resultados'],
                'objective': {
                    'en': 'Highlight product efficiency and functionality. Provide detailed information and technical data.',
                    'es': 'Destaca la eficiencia y funcionalidad del producto. Proporciona información técnica detallada.'
                },
                'profile': {
                    'en': 'Goal-oriented professionals, leaders, entrepreneurs.',
                    'es': 'Profesionales orientados a objetivos, líderes, emprendedores.'
                }
            },
            'Strive and succeed': {
                'keywords': ['growth', 'achievement', 'success', 'crecimiento', 'logro', 'éxito'],
                'objective': {
                    'en': 'Emphasize achievement and personal growth. Use success stories and case studies.',
                    'es': 'Enfatiza los logros y el crecimiento personal. Usa historias de éxito y estudios de caso.'
                },
                'profile': {
                    'en': 'Entrepreneurs, ambitious professionals, outstanding students.',
                    'es': 'Emprendedores, profesionales ambiciosos, estudiantes destacados.'
                }
            }
        },
        'Impulsive': {
            'Tension reduction': {
                'keywords': ['instant', 'fast', 'easy', 'quick', 'instantáneo', 'rápido', 'fácil'],
                'objective': {
                    'en': 'Promote speed and simplicity. Highlight immediate rewards.',
                    'es': 'Promueve la rapidez y simplicidad. Resalta recompensas inmediatas.'
                },
                'profile': {
                    'en': 'Impulsive buyers, tech enthusiasts, trend seekers.',
                    'es': 'Compradores impulsivos, entusiastas tecnológicos, buscadores de tendencias.'
                }
            }
        }
    }

    archetype_scores = {archetype: 0 for archetype in archetype_data.keys()}
    recommendations = []

    for archetype, subscales in archetype_data.items():
        for subscale, data in subscales.items():
            matched_keywords = [kw for kw in keywords if kw in data['keywords']]
            if matched_keywords:
                archetype_scores[archetype] += len(matched_keywords)
                recommendations.append({
                    'archetype': archetype,
                    'subscale': subscale,
                    'objective': data['objective'][language],
                    'profile': data['profile'][language],
                    'matched_keywords': matched_keywords,
                    'missing_keywords': list(set(data['keywords']) - set(matched_keywords))
                })

    return archetype_scores, recommendations

# Detect Language
def detect_language(text):
    """Detect the language of the text."""
    try:
        return detect(text)
    except Exception:
        return 'en'  # Default to English if detection fails

def render_chat_interface():
    """Render the chat interface."""
    st.markdown("## Chat Interface")
    # Add chat interface components
    st.text_input("Ask a question about your analysis:", key="chat_input")
    if st.button("Send"):
        # Add chat logic here
        st.write("Bot: Thank you for your question! [Add response logic here]")

    # Add a button to go back to analysis
    if st.button("Back to Analysis"):
        st.session_state.show_chat = False
        st.rerun()

# Render Archetype Analysis
def render_archetype_analysis(keywords, language):
    """Render archetype alignment and improvement recommendations."""
    archetype_scores, recommendations = map_archetypes_and_subscales(keywords, language)

    # Display Archetype Scores
    st.markdown("### Archetype Alignment Analysis")
    archetype_data = pd.DataFrame({
        'Archetype': archetype_scores.keys(),
        'Alignment Score': archetype_scores.values()
    }).sort_values(by="Alignment Score", ascending=False)

    fig = px.bar(
        archetype_data, x='Archetype', y='Alignment Score',
        title='Archetype Alignment Based on Webpage Content',
        color='Archetype', color_discrete_sequence=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig, use_container_width=True)

    # Display Recommendations
    st.markdown("### Recommendations for Improvement")
    for rec in recommendations:
        st.markdown(f"#### {rec['archetype']} - {rec['subscale']}")
        st.write(f"**Objective:** {rec['objective']}")
        st.write(f"**Consumer Profile:** {rec['profile']}")
        st.write(f"**Matched Keywords:** {', '.join(rec['matched_keywords'])}")
        st.write(f"**Suggested Keywords to Add:** {', '.join(rec['missing_keywords'])}")

# Render SEO Analysis Details
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
    render_archetype_analysis(analysis.get('keywords', []), language)

    # Content Recommendations
    st.markdown("### Content Recommendations")
    for rec in analysis.get("content_recommendations", []):
        st.write(f"- {rec}")

# Main SEO Analyzer Function
def render_seo_analyzer():
    """Main function to render SEO Analyzer."""
    initialize_session_state()

    if st.session_state.show_chat:
        render_chat_interface()
        return

    # Input for URL
    st.image("assets/logoclio.png", width=100)
    st.markdown("## Website Analysis")
    st.markdown("Analyze your website's alignment with consumer archetypes and objectives.")

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

    # Continue button to chat interface
    if st.button("Continue to Chat"):
        if st.session_state.webpage_analysis.get('is_completed', False):
            st.success("Moving to chat interface...")
            st.session_state.show_chat = True
            st.rerun()
        else:
            st.warning("Please complete the website analysis first before continuing to chat.")

# Run the App
if __name__ == "__main__":
    render_seo_analyzer()