
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

def detect_language(text):
    try:
        return detect(text)
    except:
        return 'en'  # Default to English if detection fails

def get_stopwords(language):
    if language == 'es':
        return {
            "y", "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "para", 
            "por", "con", "sin", "sobre", "entre", "detrás", "después", "esto", "esta", "que"
        }
    else:  # English default
        return {
            "and", "the", "for", "with", "from", "this", "that", "your", "our", "their",
            "we", "are", "has", "have", "been", "would", "could", "should", "will"
        }

def analyze_webpage(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        visible_text = " ".join([text for text in soup.stripped_strings 
                               if any(c.isalpha() for c in text)])[:3000]
        language = detect_language(visible_text)
        title = soup.title.string if soup.title else ""
        meta_description = soup.find("meta", {"name": "description"})
        meta_description = meta_description["content"] if meta_description else ""

        meta_keywords = []
        keywords_meta = soup.find("meta", {"name": re.compile(r"keywords", re.I)})
        if keywords_meta and keywords_meta.get("content"):
            meta_keywords = [k.strip() for k in keywords_meta["content"].split(",")]

        headings = []
        for tag in soup.find_all(re.compile("^h[1-6]$")):
            text = tag.get_text(strip=True)
            if text and any(c.isalpha() for c in text):
                headings.append(text)

        return {
            "title": title,
            "meta_description": meta_description,
            "meta_keywords": meta_keywords,
            "headings": headings,
            "visible_text": visible_text,
            "language": language
        }
    except Exception as e:
        return {"error": f"Error analyzing webpage: {str(e)}"}

def get_pain_point_indicators(language):
    if language == 'es':
        return ["sin", "falta", "necesita", "difícil", "problema", "busca", "quiere"]
    else:
        return ["without", "lack", "need", "difficult", "problem", "looking", "want"]

def get_keyword_map(language):
    if language == 'es':
        return {
            "eficiencia": "Autonomous",
            "calidad": "Autonomous",
            "profesional": "Autonomous",
            "lujo": "Impulsive",
            "elegancia": "Impulsive",
            "exclusivo": "Impulsive",
            "comodidad": "Avoidant",
            "fácil": "Avoidant",
            "simple": "Avoidant"
        }
    else:
        return {
            "efficiency": "Autonomous",
            "quality": "Autonomous",
            "professional": "Autonomous",
            "luxury": "Impulsive",
            "elegance": "Impulsive",
            "exclusive": "Impulsive",
            "comfort": "Avoidant",
            "easy": "Avoidant",
            "simple": "Avoidant"
        }

def map_to_brand_values_and_icp(content, meta_description, headings, language):
    stopwords = get_stopwords(language)
    words = re.findall(r'\w+', content.lower())
    filtered_words = [word for word in words if word not in stopwords and len(word) > 3]
    word_freq = Counter(filtered_words)
    mission = meta_description if meta_description else (headings[0] if headings else "")
    values = [word for word, _ in word_freq.most_common(5) if word not in stopwords][:3]

    if language == 'es':
        virtue_keywords = ["calidad", "diseño", "estilo", "elegancia"]
        default_virtues = ["Calidad Premium", "Diseño Exclusivo"]
        default_interests = ["moda", "estilo", "tendencias"]
    else:
        virtue_keywords = ["quality", "design", "style", "elegance"]
        default_virtues = ["Premium Quality", "Exclusive Design"]
        default_interests = ["fashion", "style", "trends"]

    virtues = []
    for heading in headings:
        if any(word in heading.lower() for word in virtue_keywords):
            virtues.append(heading)
    if not virtues:
        virtues = default_virtues

    demographics = {
        "age_range": "25-45",
        "interests": values[:3] if values else default_interests
    }

    psychographics = {
        "priorities": virtues[:3],
        "pain_points": extract_pain_points(content, language)
    }

    return {
        "brand_values": {
            "mission": mission,
            "values": values,
            "virtues": virtues[:2],
            "is_completed": True
        },
        "icp_data": {
            "demographics": demographics,
            "psychographics": psychographics,
            "is_completed": True
        }
    }

def extract_pain_points(content, language):
    pain_indicators = get_pain_point_indicators(language)
    pain_points = []

    for sentence in content.split("."):
        if any(indicator in sentence.lower() for indicator in pain_indicators):
            cleaned = sentence.strip()
            if len(cleaned) > 10:
                pain_points.append(cleaned)

    if not pain_points:
        return ["No specific pain points detected"] if language == 'en' else ["No se detectaron puntos de dolor específicos"]

    return pain_points[:3]

def calculate_archetype_scores(meta_keywords, content, language):
    keyword_map = get_keyword_map(language)
    archetypes = {"Autonomous": 0, "Impulsive": 0, "Avoidant": 0}

    words = re.findall(r'\w+', content.lower())
    for word in words:
        if word in keyword_map:
            archetypes[keyword_map[word]] += 1

    for keyword in meta_keywords:
        keyword = keyword.lower().strip()
        if keyword in keyword_map:
            archetypes[keyword_map[keyword]] += 2

    total = sum(archetypes.values()) or 1
    return {k: round(v / total * 100, 2) for k, v in archetypes.items()}

def generate_recommendations(archetype_scores, language):
    if language == 'es':
        recommendations = []
        if archetype_scores.get("Autonomous", 0) > 30:
            recommendations.append("Destaca la funcionalidad y calidad premium ('Diseñado para la Excelencia').")
        if archetype_scores.get("Impulsive", 0) > 30:
            recommendations.append("Resalta la exclusividad y el lujo a través de historias aspiracionales ('Elegancia Moderna para Ti').")
        if archetype_scores.get("Avoidant", 0) > 30:
            recommendations.append("Enfócate en la comodidad y facilidad de compra ('Experiencia de Compra Sin Complicaciones').")
        return recommendations or ["Personaliza tu estrategia de marketing basada en los valores de marca identificados."]
    else:
        recommendations = []
        if archetype_scores.get("Autonomous", 0) > 30:
            recommendations.append("Highlight functionality and premium quality ('Designed for Excellence').")
        if archetype_scores.get("Impulsive", 0) > 30:
            recommendations.append("Emphasize exclusivity and luxury through aspirational storytelling ('Modern Elegance for You').")
        if archetype_scores.get("Avoidant", 0) > 30:
            recommendations.append("Focus on comfort and easy shopping experience ('Hassle-Free Shopping Experience').")
        return recommendations or ["Customize your marketing strategy based on identified brand values."]

def render_archetype_chart(archetype_scores):
    df_archetypes = pd.DataFrame({
        'Archetype': list(archetype_scores.keys()),
        'Score': list(archetype_scores.values())
    })
    
    fig = px.bar(df_archetypes, 
                x='Archetype', 
                y='Score',
                title='Archetype Distribution',
                color='Score',
                color_continuous_scale='Viridis')
    
    fig.update_layout(
        height=400,
        margin=dict(t=30, b=0, l=0, r=0)
    )
    
    return fig

def render_brand_values_card(brand_values):
    st.markdown("### 🎯 Brand Values")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Mission:**")
        st.info(brand_values.get("mission", "N/A"))
        
    with col2:
        st.markdown("**Core Values:**")
        for value in brand_values.get("values", []):
            st.markdown(f"- {value}")
            
    if brand_values.get("virtues"):
        st.markdown("**Brand Virtues:**")
        for virtue in brand_values.get("virtues", []):
            st.markdown(f"- {virtue}")

def render_icp_card(icp_data):
    st.markdown("### 👥 Ideal Customer Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Demographics:**")
        st.markdown(f"Age Range: {icp_data['demographics'].get('age_range', 'N/A')}")
        
        st.markdown("**Interests:**")
        for interest in icp_data['demographics'].get('interests', []):
            st.markdown(f"- {interest}")
            
    with col2:
        st.markdown("**Psychographics:**")
        
        st.markdown("*Priorities:*")
        for priority in icp_data['psychographics'].get('priorities', []):
            st.markdown(f"- {priority}")
            
        st.markdown("*Pain Points:*")
        for point in icp_data['psychographics'].get('pain_points', []):
            st.markdown(f"- {point}")

def render_recommendations_card(recommendations):
    st.markdown("### 💡 Strategic Recommendations")
    
    for idx, rec in enumerate(recommendations, 1):
        st.markdown(f"""
        <div style='padding: 10px; border-left: 3px solid #8e44ad; margin: 10px 0; background-color: #f8f9fa;'>
            {idx}. {rec}
        </div>
        """, unsafe_allow_html=True)

def render_results():
    if st.session_state.webpage_analysis["is_completed"]:
        st.markdown("## 📊 Analysis Results")
        
        tab1, tab2, tab3 = st.tabs(["Brand & Audience", "Detailed Analysis", "Raw Data"])
        
        with tab1:
            st.plotly_chart(
                render_archetype_chart(st.session_state.webpage_analysis["archetype_scores"]),
                use_container_width=True
            )
            
            col1, col2 = st.columns(2)
            with col1:
                render_brand_values_card(st.session_state.webpage_analysis["brand_values"])
            with col2:
                render_icp_card(st.session_state.webpage_analysis["icp_data"])
            
            render_recommendations_card(st.session_state.webpage_analysis["recommendations"])
            
        with tab2:
            st.subheader("Brand Values")
            st.json(st.session_state.webpage_analysis["brand_values"])
            
            st.subheader("Ideal Customer Profile")
            st.json(st.session_state.webpage_analysis["icp_data"])
            
            st.subheader("Archetype Scores")
            st.json(st.session_state.webpage_analysis["archetype_scores"])
        
        with tab3:
            st.subheader("Raw Analysis Data")
            st.json(st.session_state.webpage_analysis)

def render_seo_analyzer():
    initialize_session_state()
    st.image("assets/logoclio.png", width=100)
    st.markdown("## Website Analysis")
    st.markdown("Analyze your website to optimize its SEO performance and gather insights for Brand Values and ICP.")

    url = st.text_input("Enter your website URL", placeholder="https://example.com")
    if st.button("Analyze Website"):
        if url and urlparse(url).scheme in ["http", "https"]:
            with st.spinner("Analyzing your website..."):
                analysis = analyze_webpage(url)
                if "error" in analysis:
                    st.error(analysis["error"])
                else:
                    language = analysis.get("language", "en")
                    results = map_to_brand_values_and_icp(
                        analysis["visible_text"], 
                        analysis["meta_description"], 
                        analysis["headings"],
                        language
                    )
                    archetype_scores = calculate_archetype_scores(
                        analysis["meta_keywords"], 
                        analysis["visible_text"],
                        language
                    )
                    recommendations = generate_recommendations(archetype_scores, language)

                    st.session_state.webpage_analysis.update({
                        "url": url,
                        "brand_values": results["brand_values"],
                        "icp_data": results["icp_data"],
                        "archetype_scores": archetype_scores,
                        "recommendations": recommendations,
                        "is_completed": True
                    })

                    st.success("SEO Analysis completed successfully!")
                    render_results()
        else:
            st.warning("Please enter a valid URL.")
