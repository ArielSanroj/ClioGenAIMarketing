import streamlit as st
from datetime import datetime
import re

def generate_dynamic_content(brand_values, archetype_scores, icp_data, language='es'):
    """Dynamically generate content based on actual analysis results"""

    # Extract key elements from the analysis
    mission = brand_values.get('mission', '')
    core_values = brand_values.get('values', [])
    virtues = brand_values.get('virtues', [])
    priorities = icp_data.get('psychographics', {}).get('priorities', [])
    pain_points = icp_data.get('psychographics', {}).get('pain_points', [])

    # Determine the dominant archetype
    dominant_archetype = max(archetype_scores.items(), key=lambda x: x[1])[0]

    def get_content_style():
        """Define content style based on dominant archetype"""
        styles = {
            'Autonomous': {
                'tone': 'professional and authoritative',
                'focus': 'functionality and efficiency',
                'keywords': ['calidad', 'profesional', 'excelencia']
            },
            'Impulsive': {
                'tone': 'aspirational and emotional',
                'focus': 'exclusivity and lifestyle',
                'keywords': ['exclusivo', 'elegancia', 'lujo']
            },
            'Avoidant': {
                'tone': 'reassuring and simple',
                'focus': 'comfort and reliability',
                'keywords': ['confianza', 'simplicidad', 'comodidad']
            }
        }
        return styles.get(dominant_archetype, styles['Autonomous'])

    def generate_headlines():
        """Generate headlines based on brand values and style"""
        style = get_content_style()
        headlines = []

        # Use actual brand values to create headlines
        if core_values:
            headlines.append(f"Descubre {core_values[0].title()}: {virtues[0] if virtues else ''}")

        # Use mission statement to create headline
        if mission:
            # Extract key phrases from mission
            key_phrases = re.findall(r'([^,.;]+)[,.;]', mission)
            if key_phrases:
                headlines.append(f"Tu {style['focus'].title()}: {key_phrases[0].strip()}")

        # Use psychographics to create headline
        if priorities:
            headlines.append(f"{priorities[0]} - {style['keywords'][0].title()}")

        return headlines or [f"Descubre la Excelencia en {core_values[0].title() if core_values else 'Cada Detalle'}"]

    def generate_main_content():
        """Generate main content using actual analysis data"""
        style = get_content_style()

        # Build content sections using real data
        content_sections = []

        # Mission-based content
        if mission:
            content_sections.append(mission)

        # Value proposition based on core values
        if core_values:
            value_prop = f"Nuestra colección {', '.join(core_values)} representa:"
            content_sections.append(value_prop)

        # Benefits based on virtues and priorities
        benefits = []
        if virtues:
            benefits.extend(virtues)
        if priorities:
            benefits.extend(priorities)

        if benefits:
            benefits_text = " • ".join(benefits)
            content_sections.append(benefits_text)

        # Address pain points if available
        if pain_points:
            solutions = f"Soluciones diseñadas para: {' • '.join(pain_points)}"
            content_sections.append(solutions)

        return "\n\n".join(content_sections)

    def generate_social_media_content():
        """Generate social media content based on analysis"""
        style = get_content_style()

        # Create hashtags from core values and keywords
        hashtags = [f"#{value.replace(' ', '')}" for value in core_values]
        hashtags.extend([f"#{keyword.replace(' ', '')}" for keyword in style['keywords']])

        posts = []

        # Create posts using actual brand elements
        if mission:
            posts.append({
                "caption": f"{mission}",
                "hashtags": hashtags[:3],
                "content_type": "Brand Story",
                "call_to_action": "Descubre Más"
            })

        if core_values:
            posts.append({
                "caption": f"Experimenta {core_values[0].title()}: {virtues[0] if virtues else ''}",
                "hashtags": hashtags[2:5],
                "content_type": "Product Feature",
                "call_to_action": "Explora Ahora"
            })

        return posts

    return {
        "headlines": generate_headlines(),
        "main_content": generate_main_content(),
        "social_media": generate_social_media_content(),
        "style": get_content_style()
    }

def render_recommendation_executor():
    """Render the recommendation implementation interface"""
    if not st.session_state.webpage_analysis["is_completed"]:
        st.warning("Por favor, realiza primero el análisis del sitio web.")
        return

    st.markdown("## 🚀 Implementación de Recomendaciones Estratégicas")

    # Get analysis data
    brand_values = st.session_state.webpage_analysis["brand_values"]
    archetype_scores = st.session_state.webpage_analysis["archetype_scores"]
    icp_data = st.session_state.webpage_analysis["icp_data"]

    # Generate dynamic content
    content = generate_dynamic_content(brand_values, archetype_scores, icp_data)

    # Display content in tabs
    tab1, tab2, tab3 = st.tabs(["Contenido Premium", "Storytelling", "Campaña Social"])

    with tab1:
        st.markdown("### 💎 Contenido Premium")

        st.markdown("**Titulares Sugeridos:**")
        for headline in content["headlines"]:
            st.markdown(f"• {headline}")

        st.markdown("**Contenido Principal:**")
        st.markdown(content["main_content"])

        if st.button("Guardar Contenido Premium"):
            save_generated_content("premium", content)
            st.success("Contenido guardado exitosamente!")

    with tab2:
        st.markdown("### ✨ Storytelling")
        display_storytelling(content, brand_values)

    with tab3:
        st.markdown("### 📱 Campaña Social")
        display_social_campaign(content["social_media"])

def save_generated_content(content_type, content):
    """Save generated content to session state"""
    if "generated_content" not in st.session_state:
        st.session_state.generated_content = {}

    st.session_state.generated_content[content_type] = {
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "url": st.session_state.webpage_analysis["url"]
    }

def display_storytelling(content, brand_values):
    """Display storytelling content"""
    story_angles = [
        f"La Historia de {value.title()}" for value in brand_values.get('values', [])[:2]
    ]
    for angle in story_angles:
        st.markdown(f"• {angle}")
    st.markdown(content["main_content"])

def display_social_campaign(social_content):
    """Display social media campaign content"""
    for idx, post in enumerate(social_content, 1):
        st.markdown(f"**Post {idx}**")
        st.markdown(f"Caption: {post['caption']}")
        st.markdown(f"Hashtags: {' '.join(post['hashtags'])}")
        st.markdown(f"CTA: {post['call_to_action']}")
        st.markdown("---")