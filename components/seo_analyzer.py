
import streamlit as st
from urllib.parse import urlparse
from utils.session_manager import initialize_session_state
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from collections import Counter
import re

# Initialize NLTK components
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)

class DynamicContentAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def extract_key_topics(self, text, num_topics=5):
        try:
            tfidf_matrix = self.vectorizer.fit_transform([text])
            feature_names = self.vectorizer.get_feature_names_out()
            scores = zip(feature_names, tfidf_matrix.toarray()[0])
            sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
            return [term for term, score in sorted_scores[:num_topics]]
        except:
            return []

    def analyze_content_structure(self, soup):
        structure = {
            'main_sections': [],
            'key_elements': [],
            'interaction_points': [],
            'value_propositions': []
        }
        
        for tag in soup.find_all(['h1', 'h2', 'h3']):
            text = tag.get_text(strip=True)
            if text:
                context = " ".join([s.get_text() for s in tag.find_all_next(['p', 'div'])[:2]])
                sentiment = TextBlob(text + " " + context).sentiment
                structure['main_sections'].append({
                    'text': text,
                    'sentiment': sentiment.polarity,
                    'importance': sentiment.subjectivity
                })

        for elem in soup.find_all(['p', 'div']):
            text = elem.get_text(strip=True)
            if len(text) > 50:
                sentiment = TextBlob(text).sentiment
                if abs(sentiment.polarity) > 0.3:
                    structure['key_elements'].append({
                        'text': text,
                        'sentiment': sentiment.polarity,
                        'importance': sentiment.subjectivity
                    })

        return structure

    def extract_semantic_relationships(self, text):
        relationships = []
        sentences = sent_tokenize(text)
        
        for sentence in sentences:
            doc = TextBlob(sentence)
            if doc.sentiment.polarity != 0:
                relationships.append({
                    'text': sentence,
                    'sentiment': doc.sentiment.polarity,
                    'concepts': self.extract_key_topics(sentence, 2)
                })
        
        return relationships

def analyze_webpage(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        analyzer = DynamicContentAnalyzer()
        
        text_content = " ".join([text for text in soup.stripped_strings 
                               if any(c.isalpha() for c in text)])
        
        # Extract key topics
        key_topics = analyzer.extract_key_topics(text_content)
        
        # Analyze content structure
        structure = analyzer.analyze_content_structure(soup)
        
        # Extract semantic relationships
        relationships = analyzer.extract_semantic_relationships(text_content)
        
        # Calculate dynamic archetype scores
        archetype_scores = calculate_dynamic_archetypes(structure, relationships)
        
        # Generate brand values and ICP data
        brand_values = generate_brand_values(key_topics, structure, relationships)
        icp_data = generate_icp_data(structure, relationships, key_topics)
        
        # Generate recommendations
        recommendations = generate_recommendations(brand_values, archetype_scores, structure)
        
        return {
            "url": url,
            "brand_values": brand_values,
            "icp_data": icp_data,
            "archetype_scores": archetype_scores,
            "recommendations": recommendations,
            "is_completed": True
        }
        
    except Exception as e:
        return {"error": f"Error analyzing webpage: {str(e)}"}

def calculate_dynamic_archetypes(structure, relationships):
    scores = {"Autonomous": 0, "Impulsive": 0, "Avoidant": 0}
    
    # Analyze content sentiment and structure
    for element in structure['key_elements']:
        if element['sentiment'] > 0.3:
            scores["Autonomous"] += 1
        elif element['sentiment'] < -0.3:
            scores["Avoidant"] += 1
        else:
            scores["Impulsive"] += 0.5
    
    # Analyze semantic relationships
    for rel in relationships:
        if rel['sentiment'] > 0.3:
            scores["Autonomous"] += 0.5
        elif rel['sentiment'] < -0.3:
            scores["Avoidant"] += 0.5
    
    total = sum(scores.values()) or 1
    return {k: round(v/total * 100, 2) for k, v in scores.items()}

def generate_brand_values(key_topics, structure, relationships):
    positive_elements = [elem for elem in structure['key_elements'] 
                        if elem['sentiment'] > 0]
    
    mission = positive_elements[0]['text'] if positive_elements else ""
    values = key_topics[:3]
    virtues = [elem['text'] for elem in sorted(positive_elements, 
                                             key=lambda x: x['importance'], 
                                             reverse=True)[:2]]
    
    return {
        "mission": mission,
        "values": values,
        "virtues": virtues,
        "is_completed": True
    }

def generate_icp_data(structure, relationships, key_topics):
    pain_points = [elem['text'] for elem in structure['key_elements'] 
                  if elem['sentiment'] < -0.2][:3]
    
    priorities = [rel['text'] for rel in relationships 
                 if rel['sentiment'] > 0.2][:3]
    
    return {
        "demographics": {
            "age_range": "25-45",
            "interests": key_topics[:3]
        },
        "psychographics": {
            "priorities": priorities,
            "pain_points": pain_points
        },
        "is_completed": True
    }

def generate_recommendations(brand_values, archetype_scores, structure):
    recommendations = []
    
    # Generate recommendations based on content analysis
    if archetype_scores["Autonomous"] > 30:
        recommendations.append(
            f"Enhance thought leadership content around {', '.join(brand_values['values'][:2])}"
        )
    
    if archetype_scores["Impulsive"] > 30:
        recommendations.append(
            "Create emotional storytelling content highlighting unique value propositions"
        )
    

def render_brand_values_card(brand_values):
    """Render a card displaying brand values"""
    st.markdown("### 🎯 Brand Values")
    
    if brand_values.get("mission"):
        st.markdown("**Mission:**")
        st.write(brand_values["mission"])
    
    if brand_values.get("values"):
        st.markdown("**Core Values:**")
        st.write(", ".join(brand_values["values"]))
        
    if brand_values.get("virtues"):
        st.markdown("**Brand Virtues:**")
        st.write(", ".join(brand_values["virtues"]))

def render_icp_card(icp_data, archetype_scores=None):
    """Render a card displaying ICP data"""
    st.markdown("### 👥 Ideal Customer Profile")
    
    recommendations = []
    
    if "demographics" in icp_data:
        st.markdown("**Demographics:**")
        st.write(f"Age Range: {icp_data['demographics']['age_range']}")
        st.write(f"Interests: {', '.join(icp_data['demographics']['interests'])}")
    
    if "psychographics" in icp_data:
        st.markdown("**Psychographics:**")
        if icp_data["psychographics"].get("priorities"):
            st.write("Priorities:", ", ".join(icp_data["psychographics"]["priorities"]))
        if icp_data["psychographics"].get("pain_points"):
            st.write("Pain Points:", ", ".join(icp_data["psychographics"]["pain_points"]))

    if archetype_scores and archetype_scores.get("Avoidant", 0) > 30:
        recommendations.append(
            "Focus on simplifying content and emphasizing reliability"
        )
    
    return recommendations if recommendations else [
        "Customize your marketing strategy based on the identified content patterns"
    ]

def render_results():
    if st.session_state.webpage_analysis["is_completed"]:
        st.markdown("## 📊 Analysis Results")
        
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

def render_overview():
    col1, col2 = st.columns(2)
    with col1:
        render_brand_values_card(st.session_state.webpage_analysis["brand_values"])
    with col2:
        render_icp_card(st.session_state.webpage_analysis["icp_data"], st.session_state.webpage_analysis["archetype_scores"])
    
    st.plotly_chart(
        render_archetype_chart(st.session_state.webpage_analysis["archetype_scores"]),
        use_container_width=True
    )

def render_semantic_analysis():
    st.markdown("### 🔍 Semantic Analysis")
    analyzer = DynamicContentAnalyzer()
    
    if "webpage_analysis" in st.session_state:
        analysis = st.session_state.webpage_analysis
        
        # Display key topics
        st.markdown("#### Key Topics")
        st.write(analysis["brand_values"]["values"])
        
        # Display sentiment distribution
        st.markdown("#### Content Sentiment")
        if "key_elements" in analysis:
            sentiments = [elem["sentiment"] for elem in analysis["key_elements"]]
            fig = px.histogram(sentiments, title="Content Sentiment Distribution")
            st.plotly_chart(fig)

def render_industry_insights():
    st.markdown("### 🎯 Industry Insights")
    if "webpage_analysis" in st.session_state:
        analysis = st.session_state.webpage_analysis
        
        # Display value propositions
        st.markdown("#### Value Propositions")
        st.write(analysis["brand_values"]["virtues"])
        
        # Display market positioning
        st.markdown("#### Market Positioning")
        st.write(analysis["recommendations"])

def render_competitive_analysis():
    st.markdown("### 📊 Competitive Analysis")
    if "webpage_analysis" in st.session_state:
        analysis = st.session_state.webpage_analysis
        
        # Display archetype comparison
        st.markdown("#### Archetype Distribution")
        st.plotly_chart(
            render_archetype_chart(analysis["archetype_scores"]),
            use_container_width=True
        )

def render_technical_details():
    st.markdown("### 🔧 Technical Details")
    if "webpage_analysis" in st.session_state:
        st.json(st.session_state.webpage_analysis)

def render_seo_analyzer():
    initialize_session_state()
    st.image("assets/logoclio.png", width=100)
    st.markdown("## Website Analysis")
    st.markdown("Dynamic content analysis for SEO optimization and brand insights.")

    url = st.text_input("Enter your website URL", placeholder="https://example.com")
    
    if st.button("Analyze Website"):
        if url and urlparse(url).scheme in ["http", "https"]:
            with st.spinner("Analyzing your website..."):
                analysis = analyze_webpage(url)
                if "error" in analysis:
                    st.error(analysis["error"])
                else:
                    st.session_state.webpage_analysis.update(analysis)
                    st.success("Analysis completed successfully!")
                    render_results()
        else:
            st.warning("Please enter a valid URL.")
