import streamlit as st


def render_archetype_card(name, data):
    """
    Render an archetype card with a circle icon and profile information.
    """
    card_html = f"""
    <div style="background: white; border-radius: 12px; margin: 1.5rem 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);">
        <div style="padding: 2rem;">
            <div style="display: flex; align-items: flex-start; gap: 1.5rem;">
                <div style="width: 4.5rem; height: 4.5rem; border-radius: 50%; background-color: {data['color']}; flex-shrink: 0;"></div>
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


def render_subscale_card(name, data):
    """
    Render a subscale card with details about interpretation, goals, and consumer type.
    """
    card_html = f"""
    <div style="background: white; border-radius: 12px; margin: 1.5rem 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);">
        <div style="padding: 2rem;">
            <div style="display: flex; align-items: flex-start; gap: 1.5rem;">
                <div style="width: 4.5rem; height: 4.5rem; border-radius: 50%; background-color: {data['color']}; flex-shrink: 0;"></div>
                <div style="flex-grow: 1;">
                    <h3 style="margin: 0; color: #1E1B4B; font-size: 1.5rem; font-weight: 600; line-height: 1.2;">{name}</h3>
                    <div style="margin-top: 1.25rem;">
                        <div style="margin-bottom: 1.25rem;">
                            <h4 style="font-size: 1rem; font-weight: 500; margin: 0 0 0.5rem; color: #1E1B4B;">Interpretation:</h4>
                            <p style="margin: 0; line-height: 1.6; color: #4A4867;">{data['interpretation']}</p>
                        </div>
                        <div style="margin-bottom: 1.25rem;">
                            <h4 style="font-size: 1rem; font-weight: 500; margin: 0 0 0.5rem; color: #1E1B4B;">Marketing Goal:</h4>
                            <p style="margin: 0; line-height: 1.6; color: #4A4867;">{data['objective']}</p>
                        </div>
                        <div>
                            <h4 style="font-size: 1rem; font-weight: 500; margin: 0 0 0.5rem; color: #1E1B4B;">Consumer Type:</h4>
                            <p style="margin: 0; line-height: 1.6; color: #4A4867;">{data['consumer_type']}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_consumer_archetypes():
    """
    Render the consumer archetypes display with view toggles for archetypes and subscales.
    """
    st.markdown("""
        <style>
        .stApp {
            background-color: #F9F9FB;
        }
        </style>
    """, unsafe_allow_html=True)

    st.image("assets/logoclio.png", width=100)

    # Header with toggle buttons
    st.markdown("""
        <h2 style="color: #1E1B4B; font-size: 2rem; margin-top: 1rem;">Consumer Archetypes</h2>
    """, unsafe_allow_html=True)

    # View state for toggling
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = 'archetypes'

    col1, col2 = st.columns([4, 1])
    with col2:
        if st.session_state.view_mode == 'archetypes':
            if st.button("View Subscales", key="subscale_toggle"):
                st.session_state.view_mode = 'subscales'
                st.experimental_rerun()
        else:
            if st.button("Back to Archetypes", key="archetype_toggle"):
                st.session_state.view_mode = 'archetypes'
                st.experimental_rerun()

    # Data for archetypes and subscales
    archetypes_data = load_archetypes_data()
    subscales_data = load_subscales_data()

    # Render cards based on the view state
    if st.session_state.view_mode == 'archetypes':
        for name, data in archetypes_data.items():
            render_archetype_card(name, data)
    else:
        for name, data in subscales_data.items():
            render_subscale_card(name, data)


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


def load_subscales_data():
    """
    Load subscales data for display.
    """
    return {
        'Focus Problem': {
            'interpretation': 'Clients with high logical reasoning.',
            'objective': 'Provide technical data and efficiency-focused solutions.',
            'consumer_type': 'Goal-oriented professionals.',
            'color': '#FFE4D6'
        },
        'Tension Reduction': {
            'interpretation': 'Clients seeking quick solutions.',
            'objective': 'Promote ease of use and instant gratification.',
            'consumer_type': 'Impulsive buyers.',
            'color': '#E6E6FA'
        },
        'Keep to Oneself': {
            'interpretation': 'Clients valuing autonomy and privacy.',
            'objective': 'Highlight independent and private solutions.',
            'consumer_type': 'Privacy-conscious consumers.',
            'color': '#FFD700'
        },
        'Indulge Illusions': {
            'interpretation': 'Clients seeking escape and dreams.',
            'objective': 'Focus on immersive and aspirational experiences.',
            'consumer_type': 'Dreamers and entertainment consumers.',
            'color': '#FF6B6B'
        }
    }


if __name__ == "__main__":
    render_consumer_archetypes()
