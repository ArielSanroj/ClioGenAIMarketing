from typing import Dict, List, Tuple
import streamlit as st

archetype_data = {
    "Autonomous": {
        "Focus on solving the problem": {
            "keywords": ["efficient", "practical", "results", "growth", "achievement"],
            "interpretation": "Consumers with high logical reasoning and organization skills.",
            "neuromarketing_objective": "Highlight product efficiency and functionality. Provide technical data.",
            "consumer_type": "Goal-oriented professionals, leaders, entrepreneurs."
        },
        "Strive and succeed": {
            "keywords": ["growth", "success", "achievement"],
            "interpretation": "Highly motivated, perseverant, and ambitious consumers.",
            "neuromarketing_objective": "Emphasize achievement and personal growth with success stories.",
            "consumer_type": "Entrepreneurs, ambitious professionals, outstanding students."
        }
    },
    "Impulsive": {
        "Tension reduction": {
            "keywords": ["quick", "easy", "instant"],
            "interpretation": "Consumers with low frustration tolerance, seeking immediate gratification.",
            "neuromarketing_objective": "Offer instant satisfaction and ease of use.",
            "consumer_type": "Impulsive buyers, tech enthusiasts, trend seekers."
        },
        "Self-blame": {
            "keywords": ["change", "improve", "growth"],
            "interpretation": "Consumers who tend to blame themselves or others.",
            "neuromarketing_objective": "Use positive messages that boost self-esteem.",
            "consumer_type": "People seeking change and personal development."
        }
    },
    # Add additional archetypes and subscales as necessary
}

def calculate_alignment(brand_values, icp_data, seo_data):
    """Align extracted data with archetypes and subscales."""
    scores = {archetype: 0 for archetype in archetype_data.keys()}
    matches = []

    for archetype, subscales in archetype_data.items():
        for subscale, data in subscales.items():
            matched_keywords = [
                kw for kw in seo_data.get('content', "").split() if kw.lower() in data["keywords"]
            ]
            if matched_keywords:
                scores[archetype] += len(matched_keywords)
                matches.append({"archetype": archetype, "subscale": subscale, "keywords": matched_keywords})

    return scores, matches

def render_archetype_alignment():
    """Render Archetype Alignment component."""
    if not st.session_state['webpage_analysis'].get('is_completed', False):
        st.warning("Please complete the SEO analysis first.")
        return

    st.markdown("## Archetype Alignment")
    st.write("Alignment analysis goes here...")
