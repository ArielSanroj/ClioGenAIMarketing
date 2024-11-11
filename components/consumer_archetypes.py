import streamlit as st
import pandas as pd

def render_archetype_card(name, data):
    """Render an archetype card with circle icon and profile information"""
    st.markdown(
        f"""
        <div style="background: white; border-radius: 12px; margin: 1.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); overflow: hidden;">
            <div style="padding: 1.5rem;">
                <div style="display: flex; align-items: flex-start; gap: 1.25rem;">
                    <div style="width: 4rem; height: 4rem; border-radius: 50%; background-color: {data['color']}; flex-shrink: 0;"></div>
                    <div style="flex-grow: 1;">
                        <h3 style="margin: 0; color: #1E1B4B; font-size: 1.25rem; font-weight: 600;">{name}</h3>
                        <div style="margin-top: 1rem;">
                            <p style="margin: 0 0 1rem; line-height: 1.6; color: #4B5563;">{data['segment']}</p>
                            <p style="margin: 0 0 1rem; line-height: 1.6; color: #4B5563;">{data['client_type']}</p>
                            <p style="margin: 0; line-height: 1.6; color: #4B5563;">{data['campaign']}</p>
                        </div>
                        <div style="margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid #E5E7EB;">
                            <h4 style="font-size: 1rem; font-weight: 500; margin: 0 0 0.75rem; color: #1E1B4B;">Profile:</h4>
                            <p style="color: #4B5563; margin: 0; line-height: 1.6;">{data['profile']}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_subscale_card(name, data):
    """Render a subscale card with matching styling"""
    st.markdown(
        f"""
        <div style="background: white; border-radius: 12px; margin: 1.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); overflow: hidden;">
            <div style="padding: 1.5rem;">
                <div style="display: flex; align-items: flex-start; gap: 1.25rem;">
                    <div style="width: 4rem; height: 4rem; border-radius: 50%; background-color: {data['color']}; flex-shrink: 0;"></div>
                    <div style="flex-grow: 1;">
                        <h3 style="margin: 0; color: #1E1B4B; font-size: 1.25rem; font-weight: 600;">{name}</h3>
                        <div style="margin-top: 1rem;">
                            <div style="margin-bottom: 1rem;">
                                <h4 style="font-size: 1rem; font-weight: 500; margin: 0 0 0.5rem; color: #1E1B4B;">Interpretation:</h4>
                                <p style="margin: 0; line-height: 1.6; color: #4B5563;">{data['interpretation']}</p>
                            </div>
                            <div style="margin-bottom: 1rem;">
                                <h4 style="font-size: 1rem; font-weight: 500; margin: 0 0 0.5rem; color: #1E1B4B;">Marketing goal:</h4>
                                <p style="margin: 0; line-height: 1.6; color: #4B5563;">{data['objective']}</p>
                            </div>
                            <div>
                                <h4 style="font-size: 1rem; font-weight: 500; margin: 0 0 0.5rem; color: #1E1B4B;">Consumer type:</h4>
                                <p style="margin: 0; line-height: 1.6; color: #4B5563;">{data['consumer_type']}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_consumer_archetypes():
    """Render the consumer archetypes display"""
    st.markdown("""
        <style>
        .stApp {
            background-color: #F9F9FB;
        }
        .stButton>button[kind="primary"] {
            background-color: #1E1B4B;
            color: white;
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            border: none;
            width: auto;
            min-width: 120px;
            transition: background-color 0.2s;
        }
        .stButton>button[kind="primary"]:hover {
            background-color: #2D2A5C;
        }
        .stButton>button[kind="secondary"] {
            background-color: white;
            color: #1E1B4B;
            border: 1px solid #1E1B4B;
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            width: auto;
            min-width: 120px;
            transition: background-color 0.2s;
        }
        .stButton>button[kind="secondary"]:hover {
            background-color: #F3F4F6;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="padding: 1.5rem 2rem; max-width: 64rem; margin: 0 auto;">', unsafe_allow_html=True)
    
    st.image("logoclio.png", width=100)
    
    if 'archetype_view' not in st.session_state:
        st.session_state.archetype_view = 'archetypes'

    col1, col2 = st.columns([1, 11])
    with col1:
        if st.button("Go back", type="secondary"):
            st.session_state.selected_option = None
            st.rerun()
    
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 1.5rem 0;">
            <h2 style="font-size: 1.5rem; font-weight: 600; color: #1E1B4B; margin: 0;">
                {st.session_state.archetype_view.capitalize()}
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.archetype_view == 'archetypes':
        col1, col2 = st.columns([10, 2])
        with col2:
            if st.button("View subscales", type="primary"):
                st.session_state.archetype_view = 'subscales'
                st.rerun()

    if st.session_state.archetype_view == 'archetypes':
        archetype_data = {
            'autonomous': {
                'name': 'Autonomous',
                'segment': 'This archetype is aimed at clients who seek effective solutions and focus on quick results. Ideal for products that emphasize efficiency, performance, and autonomy.',
                'client_type': 'Clients who frequently search for detailed information, download whitepapers, attend webinars.',
                'campaign': 'Campaigns that showcase success stories, concrete data on product ROI, and use cases focused on results.',
                'color': '#FFE4D6',
                'profile': 'María, project manager, 35 years old, seeks tools that optimize her time and give her full control.'
            },
            'impulsive': {
                'name': 'Impulsive',
                'segment': 'Applies to clients with reactive behaviors and difficulty managing emotions. Products that provide emotional support, quick solutions to unexpected problems, or stability would be attractive.',
                'client_type': 'Clients who respond to limited-time offers, make unplanned purchases, participate in contests.',
                'campaign': 'Use emotional messages highlighting the product\'s speed and ease, including trust-building testimonials.',
                'color': '#E6E6FA',
                'profile': 'Juan, university student, 22 years old, attracted to the latest trends and flash offers.'
            },
            'isolative': {
                'name': 'Isolative',
                'segment': 'Suited to clients who seek enjoyment and want to avoid discomfort. Marketing that emphasizes simplicity, pleasure, and well-being can resonate with this profile.',
                'client_type': 'Clients interested in content related to well-being, relaxation, easy-to-use products.',
                'campaign': 'Content that conveys comfort and joy, highlighting the stress-free benefits the product provides.',
                'color': '#FFD700',
                'profile': 'Carlos, independent writer, 45 years old, prefers personalized solutions and values privacy.'
            },
            'avoidant': {
                'name': 'Avoidant',
                'segment': 'This archetype fits clients who value independence and prefer discreet, personal solutions. Offers prioritizing privacy and gradual connection would be ideal.',
                'client_type': 'Clients who prefer online interactions, avoid phone calls, value personalization.',
                'campaign': 'Offers of personalized services, emphasizing privacy and long-term support.',
                'color': '#FF6B6B',
                'profile': 'Laura, health professional, 40 years old, seeks products that offer comfort and reduce stress.'
            }
        }
        
        for id, data in archetype_data.items():
            render_archetype_card(data['name'], data)
    else:
        subscale_data = {
            'focus-problem': {
                'name': 'Focus on solving the problem - Autonomous',
                'interpretation': 'Consumers with high logical reasoning and organization skills. They seek practical and efficient solutions to their problems.',
                'objective': 'Highlight product efficiency and functionality. - Provide detailed information and technical data. - Show how the product solves specific problems.',
                'consumer_type': 'Goal-oriented professionals, leaders, entrepreneurs. - Value effectiveness and performance. - Want tools to optimize their productivity.',
                'color': '#FFE4D6'
            },
            'tension-reduction': {
                'name': 'Tension reduction - Impulsive',
                'interpretation': 'Consumers with low frustration tolerance, seeking immediate gratification and quick solutions.',
                'objective': 'Offer instant satisfaction and ease of use. - Promote limited-time offers and immediate rewards. - Highlight product speed and simplicity.',
                'consumer_type': 'Impulsive buyers, tech enthusiasts, trend seekers. - Value immediacy and convenience in their purchases.',
                'color': '#E6E6FA'
            },
            'keep-to-oneself': {
                'name': 'Keep it to oneself - Isolative',
                'interpretation': 'Consumers who prefer to handle problems independently and may feel lonely.',
                'objective': 'Offer autonomous and private solutions. - Promote products that can be used alone. - Ensure product privacy and discretion.',
                'consumer_type': 'Introverts, independent individuals, privacy-concerned consumers. - Value control and autonomy in their experiences.',
                'color': '#FFD700'
            },
            'indulge-illusions': {
                'name': 'Indulge in illusions - Avoidant',
                'interpretation': 'Consumers who may detach from reality, avoiding difficult situations.',
                'objective': 'Offer products that enable dreaming and escape. - Promote immersive or aspirational experiences. - Use storytelling that inspires and motivates.',
                'consumer_type': 'Dreamers, fantasy fans, entertainment consumers. - Seek products that let them explore new realities.',
                'color': '#FF6B6B'
            }
        }
        
        for id, data in subscale_data.items():
            render_subscale_card(data['name'], data)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_consumer_archetypes()
