import json
import pandas as pd
import streamlit as st
from ai_utils import match_archetypes_and_subscales


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
