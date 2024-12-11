
def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'webpage_analysis' not in st.session_state:
        st.session_state.webpage_analysis = {
            'url': '',
            'brand_values': {},
            'icp_data': {},
            'archetype_scores': {},
            'recommendations': [],
            'is_completed': False
        }


import streamlit as st
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
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

        # Extract all text content
        visible_text = " ".join([text for text in soup.stripped_strings 
                               if any(c.isalpha() for c in text)])[:3000]

        # Detect language from visible text
        language = detect_language(visible_text)

        # Extract metadata
        title = soup.title.string if soup.title else ""
        meta_description = soup.find("meta", {"name": "description"})
        meta_description = meta_description["content"] if meta_description else ""

        # Extract meta keywords
        meta_keywords = []
        keywords_meta = soup.find("meta", {"name": re.compile(r"keywords", re.I)})
        if keywords_meta and keywords_meta.get("content"):
            meta_keywords = [k.strip() for k in keywords_meta["content"].split(",")]

        # Extract headings
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

    # Extract meaningful words
    words = re.findall(r'\w+', content.lower())
    filtered_words = [word for word in words if word not in stopwords and len(word) > 3]
    word_freq = Counter(filtered_words)

    # Set mission from meta description or first heading
    mission = meta_description if meta_description else (headings[0] if headings else "")

    # Extract top keywords and values
    values = [word for word, _ in word_freq.most_common(5) 
             if word not in stopwords][:3]

    # Extract virtues based on language
    if language == 'es':
        virtue_keywords = ["calidad", "diseño", "estilo", "elegancia"]
        default_virtues = ["Calidad Premium", "Diseño Exclusivo"]
    else:
        virtue_keywords = ["quality", "design", "style", "elegance"]
        default_virtues = ["Premium Quality", "Exclusive Design"]

    virtues = []
    for heading in headings:
        if any(word in heading.lower() for word in virtue_keywords):
            virtues.append(heading)
    if not virtues:
        virtues = default_virtues

    # Define demographics and psychographics
    if language == 'es':
        default_interests = ["moda", "estilo", "tendencias"]
    else:
        default_interests = ["fashion", "style", "trends"]

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

    # Process content
    words = re.findall(r'\w+', content.lower())
    for word in words:
        if word in keyword_map:
            archetypes[keyword_map[word]] += 1

    # Process meta keywords
    for keyword in meta_keywords:
        keyword = keyword.lower().strip()
        if keyword in keyword_map:
            archetypes[keyword_map[keyword]] += 2

    # Normalize scores
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

# Update the render_seo_analyzer function to pass language to all relevant functions
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

def render_results():
    """Display the analysis results."""
    if st.session_state.webpage_analysis["is_completed"]:
        # Display Brand Values
        st.subheader("Brand Values")
        st.json(st.session_state.webpage_analysis["brand_values"])
        
        # Display ICP Data
        st.subheader("Ideal Customer Profile")
        st.json(st.session_state.webpage_analysis["icp_data"])
        
        # Display Archetype Scores
        st.subheader("Archetype Scores")
        st.json(st.session_state.webpage_analysis["archetype_scores"])
        
        # Display Recommendations
        st.subheader("Recommendations")
        for rec in st.session_state.webpage_analysis["recommendations"]:
            st.write("•", rec)