import streamlit as st
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import plotly.express as px

# Initialize Session State
def initialize_session_state():
    """Initialize the session state for SEO analyzer."""
    if "webpage_analysis" not in st.session_state:
        st.session_state.webpage_analysis = {
            "url": "",
            "brand_values": {
                "mission": "",
                "values": [],
                "virtues": [],
                "is_completed": False,
            },
            "icp_data": {
                "demographics": {},
                "psychographics": {},
                "is_completed": False,
            },
            "archetype_scores": {},
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
        meta_description = (
            soup.find("meta", {"name": "description"})["content"]
            if soup.find("meta", {"name": "description"})
            else "No Description Found"
        )
        meta_keywords = (
            soup.find("meta", {"name": "keywords"})["content"].split(",")
            if soup.find("meta", {"name": "keywords"})
            else []
        )

        # Extract visible text
        visible_text = " ".join(soup.stripped_strings)[:1000]  # Limit to 1000 chars
        return {
            "title": title,
            "meta_description": meta_description,
            "meta_keywords": meta_keywords,
            "visible_text": visible_text,
        }
    except Exception as e:
        return {"error": f"Error analyzing webpage: {str(e)}"}

# Map Data to Brand Values and ICP
def map_to_brand_values_and_icp(content):
    """Map website content to brand values and ICP."""
    # Extract mission from content and meta description
    mission = content[:100] if content else "Deliver exceptional products and services"
    
    brand_values = {
        "mission": mission,
        "values": ["creativity", "exclusivity", "luxury"],
        "virtues": ["customer-centricity", "high-quality"],
        "is_completed": True,
    }
    icp_data = {
        "demographics": {
            "age_range": "20-40",
            "interests": ["fashion", "elegance", "luxury"],
        },
        "psychographics": {
            "priorities": ["style", "individuality", "comfort"],
            "pain_points": ["need for accessible luxury", "lack of quality options"],
        },
        "is_completed": True,
    }
    return brand_values, icp_data

# Calculate Archetype Alignment
def calculate_archetype_scores(meta_keywords):
    """Match keywords to archetypes and calculate scores."""
    archetypes = {"Autonomous": 0, "Impulsive": 0, "Avoidant": 0}
    keyword_map = {
        "efficiency": "Autonomous",
        "growth": "Autonomous",
        "luxury": "Impulsive",
        "trendy": "Impulsive",
        "comfort": "Avoidant",
        "relaxation": "Avoidant",
    }
    for keyword in meta_keywords:
        keyword = keyword.lower()
        if keyword in keyword_map:
            archetypes[keyword_map[keyword]] += 10

    total = sum(archetypes.values())
    return {
        archetype: round(score / total * 100, 2) if total > 0 else 0
        for archetype, score in archetypes.items()
    }

# Render SEO Analysis
def render_seo_analyzer():
    """Render the SEO analyzer interface."""
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
                    brand_values, icp_data = map_to_brand_values_and_icp(analysis["visible_text"])

                    # Step 3: Calculate archetype alignment
                    archetype_scores = calculate_archetype_scores(analysis["meta_keywords"])

                    # Step 4: Update session state
                    st.session_state.webpage_analysis.update({
                        "url": url,
                        "brand_values": brand_values,
                        "icp_data": icp_data,
                        "archetype_scores": archetype_scores,
                        "is_completed": True,
                    })

                    st.success("SEO Analysis completed successfully!")
                    render_results()

        else:
            st.warning("Please enter a valid URL.")

def render_results():
    """Display the analysis results."""
    st.markdown("### Brand Values Updated")
    st.json(st.session_state.webpage_analysis["brand_values"])

    st.markdown("### ICP Data Updated")
    st.json(st.session_state.webpage_analysis["icp_data"])

    st.markdown("### Archetype Scores")
    scores = st.session_state.webpage_analysis["archetype_scores"]
    st.bar_chart(pd.DataFrame(list(scores.items()), columns=["Archetype", "Score"]))

# Run the App
if __name__ == "__main__":
    render_seo_analyzer()
