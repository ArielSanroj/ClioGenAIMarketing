
import json
import pandas as pd
import streamlit as st
from ai_utils import match_archetypes_and_subscales, calculate_archetype_probabilities, generate_archetype_recommendations

class ArchetypeAnalyzer:
    def __init__(self):
        self.scores = {}
        self.recommendations = []
        self.campaign_suggestions = []

    def analyze_content(self, content: str):
        # Calculate archetype probabilities
        self.scores = calculate_archetype_probabilities(
            brand_values={"keywords": self._extract_keywords(content)},
            icp_data={},
            seo_analysis={}
        )
        
        # Generate recommendations
        recommendations = generate_archetype_recommendations(self.scores)
        self.recommendations = []
        self.campaign_suggestions = []
        
        for archetype, data in recommendations.items():
            if "campaign_ideas" in data:
                self.recommendations.extend(data["campaign_ideas"])
                self.campaign_suggestions.append({
                    "archetype": archetype,
                    "tone": "Professional" if archetype == "Autonomous" else "Emotional",
                    "channels": ["Website", "Email", "LinkedIn"] if archetype == "Autonomous" else ["Social Media", "Blog"],
                    "content_types": ["Case Studies", "Whitepapers"] if archetype == "Autonomous" else ["Stories", "Videos"],
                    "example_messages": data["campaign_ideas"]
                })
        
        return self

    def _extract_keywords(self, content: str) -> list:
        # Simple keyword extraction
        words = content.lower().split()
        keywords = []
        important_words = ["efficiency", "growth", "creativity", "comfort", "security", "trust"]
        return [word for word in words if word in important_words]

def render_archetype_analysis():
    """Render archetype and subscale analysis results."""
    st.markdown("## Archetype and Subscale Analysis")

    # Fetch data from session state
    brand_values = st.session_state.get('brand_values', {})
    icp_data = st.session_state.get('icp_data', {})
    seo_data = st.session_state.get('webpage_analysis', {}).get('analysis', {})

    # Match archetypes and subscales
    archetype_scores, subscale_matches = match_archetypes_and_subscales(brand_values, icp_data, seo_data)

    # Display Archetype Scores
    st.markdown("### Archetype Scores")
    st.bar_chart(pd.DataFrame.from_dict(archetype_scores, orient='index', columns=['Score']))

    # Display Subscale Matches
    st.markdown("### Subscale Matches")
    for match in subscale_matches:
        st.markdown(f"#### {match['archetype']} - {match['subscale']}")
        st.write(f"**Interpretation:** {match['interpretation']}")
        st.write(f"**Neuromarketing Objective:** {match['neuromarketing_objective']}")
        st.write(f"**Consumer Type:** {match['consumer_type']}")
        st.write(f"**Matched Keywords:** {', '.join(match['matched_keywords'])}")
        st.write(f"**Missing Keywords:** {', '.join(match['missing_keywords'])}")

    # Export Results
    st.markdown("### Export Analysis")
    st.download_button(
        label="Download Full Report",
        data=json.dumps({"archetypes": archetype_scores, "subscales": subscale_matches}, indent=4),
        file_name="archetype_analysis.json",
        mime="application/json"
    )
