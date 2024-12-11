import streamlit as st
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from collections import Counter

# Initialize Session State
def initialize_session_state():
    """Initialize the session state for SEO analyzer."""
    if "webpage_analysis" not in st.session_state:
        st.session_state.webpage_analysis = {
            "url": "",
            "brand_values": {"mission": "", "values": [], "virtues": [], "is_completed": False},
            "icp_data": {"demographics": {}, "psychographics": {}, "is_completed": False},
            "archetype_scores": {},
            "recommendations": [],
            "is_completed": False,
        }

# Extract Website Data
def analyze_webpage(url):
    """Scrape the website and extract metadata and content."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract metadata
        title = soup.title.string if soup.title else "No Title Found"
        meta_description = soup.find("meta", {"name": "description"})
        meta_description = meta_description["content"] if meta_description else "No Description Found"
        meta_keywords = soup.find("meta", {"name": "keywords"})
        meta_keywords = meta_keywords["content"].split(",") if meta_keywords else []

        # Extract headings for semantic relevance
        headings = [h.get_text(strip=True) for h in soup.find_all(re.compile("^h[1-6]$"))]

        # Extract visible text
        visible_text = " ".join(soup.stripped_strings)[:2000]  # Limit to 2000 chars
        return {
            "title": title,
            "meta_description": meta_description,
            "meta_keywords": meta_keywords,
            "headings": headings,
            "visible_text": visible_text,
        }
    except Exception as e:
        return {"error": f"Error analyzing webpage: {str(e)}"}

# Map Data to Brand Values and ICP
def map_to_brand_values_and_icp(content, meta_description, headings):
    """Map website content to dynamic brand values and ICP."""
    # Tokenize and clean words
    words = re.findall(r'\w+', content.lower())
    stopwords = {"and", "the", "for", "with", "from", "this", "that", "your", "como"}
    filtered_words = [word for word in words if word not in stopwords and len(word) > 3]
    word_freq = Counter(filtered_words)

    # Extract mission from meta description or headings
    mission = meta_description if meta_description != "No Description Found" else " ".join(headings[:3])

    # Get top keywords
    top_keywords = [word for word, count in word_freq.most_common(5)]

    # Derive priorities and pain points from content
    priorities = [heading for heading in headings[:3]]
    pain_points = []
    negative_indicators = ["without", "lacks", "needs", "problem", "difficult"]
    for indicator in negative_indicators:
        if indicator in content.lower():
            idx = content.lower().find(indicator)
            pain_points.append(content[idx:idx+50].strip())

    brand_values = {
        "mission": mission,
        "values": top_keywords[:3],
        "virtues": priorities[:2],
        "is_completed": True,
    }

    icp_data = {
        "demographics": {
            "age_range": "25-45",
            "interests": top_keywords[:3],
        },
        "psychographics": {
            "priorities": priorities,
            "pain_points": pain_points if pain_points else ["No clear pain points detected"],
        },
        "is_completed": True,
    }
    
    return brand_values, icp_data

# Generate Recommendations
def generate_recommendations(archetype_scores):
    """Generate campaign ideas and recommendations."""
    recommendations = []
    if archetype_scores.get("Autonomous", 0) > 30:
        recommendations.append("Promote functionality and achievement-oriented branding ('Tailored for Growth').")
    if archetype_scores.get("Impulsive", 0) > 30:
        recommendations.append("Highlight exclusivity and luxury through aspirational storytelling ('Modern Elegance for Everyone').")
    if archetype_scores.get("Avoidant", 0) > 30:
        recommendations.append("Focus on relaxation and convenience ('Hassle-Free Shopping Experience').")
    return recommendations

# Render Results
def render_results():
    """Display the analysis results."""
    st.markdown("### Brand Values Updated")
    st.json(st.session_state.webpage_analysis["brand_values"])

    st.markdown("### ICP Data Updated")
    st.json(st.session_state.webpage_analysis["icp_data"])

    st.markdown("### Archetype Scores")
    scores = st.session_state.webpage_analysis["archetype_scores"]
    st.bar_chart(pd.DataFrame(list(scores.items()), columns=["Archetype", "Score"]))

    st.markdown("### Recommendations")
    recommendations = st.session_state.webpage_analysis["recommendations"]
    for rec in recommendations:
        st.write(f"- {rec}")

# Main SEO Analyzer Function
def render_seo_analyzer():
    """Main function to render SEO Analyzer."""
    initialize_session_state()

    st.image("assets/logoclio.png", width=100)
    st.markdown("## Website Analysis")
    st.markdown("Analyze your website to optimize its SEO performance and gather insights for Brand Values and ICP.")

    url = st.text_input("Enter your website URL", placeholder="https://example.com")

    if st.button("Analyze Website"):
        if url and urlparse(url).scheme in ["http", "https"]:
            with st.spinner("Analyzing your website..."):
                # Step 1: Extract website data
                analysis = analyze_webpage(url)
                if "error" in analysis:
                    st.error(analysis["error"])
                else:
                    # Step 2: Map data to Brand Values and ICP
                    brand_values, icp_data = map_to_brand_values_and_icp(
                        analysis["visible_text"],
                        analysis["meta_description"],
                        analysis["headings"],
                    )

                    # Step 3: Calculate archetype alignment
                    archetype_scores = calculate_archetype_scores(analysis["meta_keywords"], analysis["visible_text"])

                    # Step 4: Generate recommendations
                    recommendations = generate_recommendations(archetype_scores)

                    # Step 5: Update session state
                    st.session_state.webpage_analysis.update({
                        "url": url,
                        "brand_values": brand_values,
                        "icp_data": icp_data,
                        "archetype_scores": archetype_scores,
                        "recommendations": recommendations,
                        "is_completed": True,
                    })

                    st.success("SEO Analysis completed successfully!")
                    render_results()
        else:
            st.warning("Please enter a valid URL.")

# Run the App
if __name__ == "__main__":
    render_seo_analyzer()
