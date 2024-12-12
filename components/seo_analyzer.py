
import streamlit as st
from urllib.parse import urlparse
import requests
from utils.session_manager import initialize_session_state
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter
from langdetect import detect
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from textblob import TextBlob
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('averaged_perceptron_tagger')
    nltk.data.find('maxent_ne_chunker')
    nltk.data.find('words')
except LookupError:
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    nltk.download('stopwords')

def render_overview():
    """Render overview section with basic metrics"""
    analysis = st.session_state.webpage_analysis
    st.subheader("📊 Overview")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Industry", analysis['industry']['primary_industry'].title())
        st.metric("Content Type", analysis['content_category']['primary_category'].title())
    with col2:
        st.metric("Language", analysis['language'].upper())
        readability = analysis['semantic_analysis']['readability']
        st.metric("Readability", f"{readability['level']} ({readability['score']})")

def render_semantic_analysis():
    """Render semantic analysis results"""
    analysis = st.session_state.webpage_analysis
    semantic = analysis['semantic_analysis']
    
    st.subheader("🔍 Semantic Analysis")
    
    # Key Phrases
    st.write("**Key Phrases**")
    phrases_df = pd.DataFrame(semantic['key_phrases'], columns=['Phrase'])
    st.dataframe(phrases_df)
    
    # Sentiment Analysis
    sentiment = semantic['sentiment']
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sentiment", f"{sentiment['sentiment']:.2f}")
    with col2:
        st.metric("Subjectivity", f"{sentiment['subjectivity']:.2f}")
    
    # Named Entities
    st.write("**Named Entities**")
    for entity_type, entities in semantic['entities'].items():
        st.write(f"{entity_type}: {', '.join(entities)}")

def render_industry_insights():
    """Render industry analysis insights"""
    analysis = st.session_state.webpage_analysis
    industry = analysis['industry']
    
    st.subheader("🏢 Industry Analysis")
    
    # Industry scores chart
    scores_df = pd.DataFrame({
        'Industry': list(industry['scores'].keys()),
        'Score': list(industry['scores'].values())
    })
    
    fig = px.bar(scores_df, 
                 x='Industry', 
                 y='Score',
                 title='Industry Classification Scores')
    st.plotly_chart(fig)

def render_competitive_analysis():
    """Render competitive analysis results"""
    analysis = st.session_state.webpage_analysis
    competitors = analysis['competitors']
    
    st.subheader("🔄 Competitive Analysis")
    
    if competitors:
        for comp in competitors:
            with st.expander(f"Competitor: {comp['url']}"):
                st.write(f"**Title:** {comp['title']}")
                st.write("**Key Features:**")
                for feature in comp['main_features']:
                    st.write(f"- {feature}")
                st.write("**Keywords:**")
                st.write(", ".join(comp['keywords']))
    else:
        st.info("No competitor data available")

def render_technical_details():
    """Render technical SEO details"""
    analysis = st.session_state.webpage_analysis
    
    st.subheader("⚙️ Technical Details")
    st.json({
        'url': analysis['url'],
        'language': analysis['language'],
        'content_category': analysis['content_category'],
        'readability_score': analysis['semantic_analysis']['readability']['score']
    })

def render_seo_analyzer():
    """Main SEO analyzer interface"""
    st.title("🔍 SEO Analyzer")
    
    # URL input
    url = st.text_input("Enter URL to analyze:")
    
    if st.button("Analyze"):
        if url:
            with st.spinner("Analyzing webpage..."):
                from Pasted import analyze_webpage
                analysis = analyze_webpage(url)
                if 'error' not in analysis:
                    st.session_state.webpage_analysis = {
                        **analysis,
                        'is_completed': True
                    }
                else:
                    st.error(analysis['error'])
    
    # Render results if analysis is complete
    if "webpage_analysis" in st.session_state and st.session_state.webpage_analysis.get("is_completed"):
        tabs = st.tabs([
            "Overview", 
            "Semantic Analysis", 
            "Industry Insights", 
            "Competition",
            "Technical Details"
        ])
        
        with tabs[0]:
            render_overview()
        with tabs[1]:
            render_semantic_analysis()
        with tabs[2]:
            render_industry_insights()
        with tabs[3]:
            render_competitive_analysis()
        with tabs[4]:
            render_technical_details()
