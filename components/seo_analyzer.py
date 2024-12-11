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
        return 'en'

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

def map_to_brand_values_and_icp(content, meta_description, headings, language='en'):
    stopwords = {"and", "the", "for", "with", "from", "this", "that", "your"} if language == 'en' else \
                {"y", "el", "la", "los", "las", "un", "una", "para", "con"}

    words = re.findall(r'\w+', content.lower())
    filtered_words = [word for word in words if word not in stopwords and len(word) > 3]
    word_freq = Counter(filtered_words)

    mission = meta_description if meta_description else (headings[0] if headings else "")
    values = [word for word, _ in word_freq.most_common(5)][:3]

    return {
        "brand_values": {
            "mission": mission,
            "values": values,
            "virtues": headings[:2] if headings else ["Quality", "Innovation"],
            "is_completed": True
        },
        "icp_data": {
            "demographics": {
                "age_range": "25-45",
                "interests": values[:3]
            },
            "psychographics": {
                "priorities": headings[:3] if headings else [],
                "pain_points": ["No specific pain points detected"]
            },
            "is_completed": True
        }
    }

def calculate_archetype_scores(meta_keywords, content):
    archetypes_data = {
        'Autonomous': {
            'keywords': ['efficiency', 'professional', 'optimization', 'results', 'performance'],
            'weight': 1.2
        },
        'Impulsive': {
            'keywords': ['new', 'exclusive', 'limited', 'offer', 'now', 'instant'],
            'weight': 1.0
        },
        'Isolative': {
            'keywords': ['private', 'independent', 'personal', 'individual', 'unique'],
            'weight': 0.8
        },
        'Avoidant': {
            'keywords': ['escape', 'relax', 'comfort', 'easy', 'simple', 'secure'],
            'weight': 0.8
        }
    }

    scores = {archetype: 0 for archetype in archetypes_data.keys()}

    # Process content
    words = re.findall(r'\w+', content.lower())
    for word in words:
        for archetype, data in archetypes_data.items():
            if word in data['keywords']:
                scores[archetype] += data['weight']

    # Process meta keywords
    for keyword in meta_keywords:
        keyword = keyword.lower().strip()
        for archetype, data in archetypes_data.items():
            if keyword in data['keywords']:
                scores[archetype] += data['weight'] * 2

    # Normalize scores
    total = sum(scores.values()) or 1
    normalized_scores = {k: round((v / total) * 100) for k, v in scores.items()}

    # Filter out zero scores
    return {k: v for k, v in normalized_scores.items() if v > 0}

def generate_recommendations(archetype_scores):
    recommendations = []

    if archetype_scores.get("Autonomous", 0) > 30:
        recommendations.append("Focus on efficiency and ROI-driven messaging")
    if archetype_scores.get("Impulsive", 0) > 30:
        recommendations.append("Implement urgency-based campaigns and exclusive offers")
    if archetype_scores.get("Isolative", 0) > 30:
        recommendations.append("Highlight privacy features and personal control")
    if archetype_scores.get("Avoidant", 0) > 30:
        recommendations.append("Emphasize comfort and stress-free experiences")

    return recommendations

def render_results():
    if not hasattr(st.session_state, 'webpage_analysis'):
        st.warning("Please analyze a webpage first.")
        return

    st.markdown("""
        <style>
        .stApp {
            background-color: #F9F9FB;
        }
        </style>
    """, unsafe_allow_html=True)

    archetype_scores = st.session_state.webpage_analysis["archetype_scores"]
    archetypes_data = load_archetypes_data()

    # Header
    st.markdown("""
        <h2 style="color: #1E1B4B; font-size: 2rem; margin-top: 1rem;">Analysis Results</h2>
    """, unsafe_allow_html=True)

    # Render scores chart
    st.markdown("### Archetype Distribution")
    chart_data = pd.DataFrame(list(archetype_scores.items()), columns=["Archetype", "Score"])
    st.bar_chart(chart_data.set_index("Archetype"))

    # Render archetype cards for scores > 0
    st.markdown("### Detected Archetypes")
    for name, score in archetype_scores.items():
        if score > 0 and name in archetypes_data:
            data = archetypes_data[name]
            card_html = f"""
            <div style="background: white; border-radius: 12px; margin: 1.5rem 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);">
                <div style="padding: 2rem;">
                    <div style="display: flex; align-items: flex-start; gap: 1.5rem;">
                        <div style="width: 4.5rem; height: 4.5rem; border-radius: 50%; background-color: {data['color']}; flex-shrink: 0; display: flex; align-items: center; justify-content: center;">
                            <span style="font-weight: bold; color: #1E1B4B;">{score}%</span>
                        </div>
                        <div style="flex-grow: 1;">
                            <h3 style="margin: 0; color: #1E1B4B; font-size: 1.5rem; font-weight: 600; line-height: 1.2;">{name}</h3>
                            <div style="margin-top: 1.25rem; color: #4A4867;">
                                <p style="margin: 0 0 1rem; line-height: 1.6;">{data['segment']}</p>
                                <p style="margin: 0 0 1rem; line-height: 1.6;"><b>Client Type:</b> {data['client_type']}</p>
                                <p style="margin: 0; line-height: 1.6;"><b>Campaign Strategy:</b> {data['campaign']}</p>
                            </div>
                            <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #E5E7EB;">
                                <h4 style="font-size: 1rem; font-weight: 500; margin: 0 0 0.75rem; color: #1E1B4B;">Profile Example:</h4>
                                <p style="color: #4A4867; margin: 0; line-height: 1.6;">{data['profile']}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

    # Render recommendations
    if st.session_state.webpage_analysis["recommendations"]:
        st.markdown("### Strategic Recommendations")
        recs_html = """
        <div style="background: white; border-radius: 12px; padding: 2rem; margin: 1.5rem 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <h4 style="color: #1E1B4B; margin: 0 0 1rem;">Based on your audience profile:</h4>
            <ul style="color: #4A4867; margin: 0; padding-left: 1.5rem;">
        """
        for rec in st.session_state.webpage_analysis["recommendations"]:
            recs_html += f'<li style="margin-bottom: 0.75rem;">{rec}</li>'
        recs_html += "</ul></div>"
        st.markdown(recs_html, unsafe_allow_html=True)

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
                    results = map_to_brand_values_and_icp(
                        analysis["visible_text"],
                        analysis["meta_description"],
                        analysis["headings"],
                        analysis.get("language", "en")
                    )

                    archetype_scores = calculate_archetype_scores(
                        analysis["meta_keywords"],
                        analysis["visible_text"]
                    )

                    recommendations = generate_recommendations(archetype_scores)

                    st.session_state.webpage_analysis.update({
                        "url": url,
                        "brand_values": results["brand_values"],
                        "icp_data": results["icp_data"],
                        "archetype_scores": archetype_scores,
                        "recommendations": recommendations,
                        "is_completed": True,
                    })

                    st.success("Analysis completed successfully!")
                    render_results()
        else:
            st.warning("Please enter a valid URL.")

def load_archetypes_data():
    """
    Load archetypes data for display.
    """
    return {
        'Autonomous': {
            'segment': 'Clients seeking efficiency and autonomy.',
            'client_type': 'Professionals and entrepreneurs.',
            'campaign': 'Case studies and ROI-focused campaigns.',
            'color': '#FFE4D6',
            'profile': 'María, Project Manager, 35 years old. Values tools for time optimization.'
        },
        'Impulsive': {
            'segment': 'Clients driven by urgency and emotional triggers.',
            'client_type': 'Tech enthusiasts and trend seekers.',
            'campaign': 'Emotional messaging with flash sales.',
            'color': '#E6E6FA',
            'profile': 'Juan, University Student, 22 years old. Attracted to flash sales.'
        },
        'Isolative': {
            'segment': 'Clients valuing simplicity and privacy.',
            'client_type': 'Introverts, privacy-focused individuals.',
            'campaign': 'Highlight autonomy and stress-free experiences.',
            'color': '#FFD700',
            'profile': 'Carlos, Independent Writer, prefers personal solutions.'
        },
        'Avoidant': {
            'segment': 'Clients seeking escape and security.',
            'client_type': 'Dreamers and fantasy seekers.',
            'campaign': 'Aspirational, storytelling-based campaigns.',
            'color': '#FF6B6B',
            'profile': 'Laura, Health Professional, values relaxation tools.'
        }
    }

def initialize_session_state():
    if "webpage_analysis" not in st.session_state:
        st.session_state.webpage_analysis = {
            "url": "",
            "brand_values": {"mission": "", "values": [], "virtues": [], "is_completed": False},
            "icp_data": {"demographics": {}, "psychographics": {}, "is_completed": False},
            "archetype_scores": {},
            "recommendations": [],
            "is_completed": False,
        }

if __name__ == "__main__":
    render_seo_analyzer()