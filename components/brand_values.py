import streamlit as st
import plotly.express as px
from emotion_engine import EmotionEngine
from utils.session_manager import get_user_state, set_user_state
from typing import Dict, List, Optional 

# Initialize EmotionEngine
emotion_engine = EmotionEngine()

# Get brand values from user input
def get_brand_values() -> dict:
    """Capture brand values from the user using Streamlit widgets."""
    try:
        st.sidebar.header("Define Your Brand Values")
        keywords = st.sidebar.multiselect(
            "Select Keywords That Represent Your Brand",
            options=[
                'efficiency', 'growth', 'trust', 'innovation', 'creativity',
                'comfort', 'security', 'authenticity', 'mastery', 'balance'
            ],
            default=['efficiency', 'growth']
        )
        tone = st.sidebar.slider(
            "Rate Your Brand's Tone (Professional to Casual)",
            0.0, 1.0, 0.7
        )
        return {'keywords': keywords, 'tone': {'professional': tone}}
    except Exception as e:
        st.error(f"Error capturing brand values: {e}")
        return {}

# Calculate archetype compatibility based on brand values
def calculate_compatibility(brand_values: dict) -> Dict[str, float]:
    """Calculate compatibility scores between brand values and archetypes."""
    try:
        return emotion_engine.calculate_archetype_alignment(brand_values)
    except Exception as e:
        st.error(f"Error calculating compatibility: {e}")
        return {}

# Plot compatibility scores as a bar chart
def plot_compatibility_chart(compatibility_scores: dict):
    """Plot a bar chart showing compatibility scores for archetypes."""
    try:
        df = px.data.frame({
            "Archetype": list(compatibility_scores.keys()),
            "Score": list(compatibility_scores.values())
        })
        fig = px.bar(
            df,
            x="Archetype",
            y="Score",
            title="Archetype Compatibility with Brand Values",
            labels={"Score": "Compatibility Score", "Archetype": "Archetype"},
            color="Score",
            color_continuous_scale="Blues",
            text="Score"
        )
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            xaxis_title="Archetype",
            yaxis_title="Compatibility Score",
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error plotting compatibility chart: {e}")

# Show top archetypes and provide recommendations
def show_top_archetypes(compatibility_scores: dict):
    """Display the top recommended archetypes based on compatibility scores."""
    try:
        sorted_scores = sorted(compatibility_scores.items(), key=lambda x: x[1], reverse=True)
        st.subheader("Top Recommended Archetypes")
        for archetype, score in sorted_scores[:2]:
            st.markdown(f"**{archetype.capitalize()}**: {score:.2f}")
            st.write(f"This archetype aligns well with your brand values. "
                     f"Consider focusing on marketing strategies targeting this archetype.")
    except Exception as e:
        st.error(f"Error displaying top archetypes: {e}")

# Display recommendations for aligning brand values with archetypes
def show_brand_recommendations(compatibility_scores: dict, brand_values: dict):
    """Provide actionable recommendations for improving alignment with archetypes."""
    try:
        st.subheader("Brand Alignment Recommendations")
        for archetype, score in compatibility_scores.items():
            if score > 0.5:
                st.markdown(f"**{archetype.capitalize()}**: {score:.2f}")
                st.write(f"To improve alignment with the {archetype.capitalize()} archetype, focus on incorporating "
                         f"keywords like {', '.join(emotion_engine.trigger_mappings[archetype][:3])} into your branding.")
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")

def validate_brand_values(values: Dict) -> bool:
    """Validate the brand values input."""
    required_fields = ['mission', 'vision', 'values', 'tone']
    return all(values.get(field) for field in required_fields)

def render_brand_values():
    """Render the brand values definition component."""
    st.markdown("## Define Your Brand Values")
    st.markdown("Let's start by understanding your brand's core values and personality.")

    # Get current user ID and state
    user_id = st.session_state.get('user_id')
    brand_values = get_user_state(user_id, "brand_values", {})

    with st.form("brand_values_form"):
        # Mission Statement
        mission = st.text_area(
            "What is your brand's mission?",
            value=brand_values.get('mission', ''),
            help="Define your brand's purpose and goals"
        )

        # Vision Statement
        vision = st.text_area(
            "What is your brand's vision?",
            value=brand_values.get('vision', ''),
            help="Describe your brand's aspirational future"
        )

        # Core Values
        values = st.text_area(
            "What are your core brand values?",
            value=brand_values.get('values', ''),
            help="List your brand's fundamental beliefs and principles"
        )

        # Brand Voice/Tone
        tone_options = [
            "Professional", "Friendly", "Casual", "Authoritative",
            "Empathetic", "Innovative", "Traditional", "Playful"
        ]
        tone = st.multiselect(
            "Select your brand's tone of voice",
            options=tone_options,
            default=brand_values.get('tone', []),
            help="Choose the tone that best represents your brand's communication style"
        )

        # Target Keywords
        keywords = st.text_area(
            "Enter target keywords (one per line)",
            value=brand_values.get('keywords', ''),
            help="Keywords that represent your brand and offerings"
        )

        # Form submission
        submitted = st.form_submit_button("Continue")
        if submitted:
            # Process and validate form data
            new_values = {
                'mission': mission,
                'vision': vision,
                'values': values,
                'tone': tone,
                'keywords': [k.strip() for k in keywords.split('\n') if k.strip()],
                'is_completed': True
            }

            if validate_brand_values(new_values):
                # Save to session state
                set_user_state(user_id, "brand_values", new_values)
                st.success("Brand values saved successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields")

    # Skip button outside the form
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Skip"):
            set_user_state(user_id, "brand_values", {'is_completed': True})
            st.rerun()

# Main function
def main():
    """Main function to run the Streamlit application."""
    try:
        st.title("Brand-Archetype Compatibility Analyzer")
        st.write("Analyze how your brand values align with different consumer archetypes and get actionable insights.")

        # Step 1: Get brand values from the user
        brand_values = get_brand_values()

        # Step 2: Calculate archetype compatibility
        compatibility_scores = calculate_compatibility(brand_values)

        # Step 3: Visualize compatibility scores
        if compatibility_scores:
            plot_compatibility_chart(compatibility_scores)

            # Step 4: Show top archetypes and recommendations
            show_top_archetypes(compatibility_scores)
            show_brand_recommendations(compatibility_scores, brand_values)
        else:
            st.write("No compatibility data available. Please define your brand values in the sidebar.")
    except Exception as e:
        st.error(f"Error running the application: {e}")

if __name__ == "__main__":
    main()
