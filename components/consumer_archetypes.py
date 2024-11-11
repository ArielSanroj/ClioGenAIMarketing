import streamlit as st
import pandas as pd

def load_archetype_data():
    """Load data from Excel files"""
    try:
        archetypes_df = pd.read_excel("Consumer Archetype.xlsx", engine='openpyxl')
        subscales_df = pd.read_excel("Consumer Subscales.xlsx", engine='openpyxl')
        return archetypes_df, subscales_df
    except Exception as e:
        st.error(f"Error loading archetype data: {str(e)}")
        return None, None

def render_archetype_card(name, description, bullets, color):
    """Render an archetype card with circle icon"""
    st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: flex-start;">
                <div style="width: 60px; height: 60px; border-radius: 50%; background-color: {color}; margin-right: 20px; flex-shrink: 0;"></div>
                <div style="width: 100%;">
                    <h3 style="margin: 0; color: #28264D; font-size: 20px;">{name}</h3>
                    <p style="color: #4A4867; margin: 10px 0;">{description}</p>
                    {"".join([f'<p style="color: #4A4867; margin: 5px 0;">• {bullet}</p>' for bullet in bullets])}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_subscale_card(title, interpretation, marketing_goal, consumer_type, color):
    """Render a subscale card"""
    st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: flex-start;">
                <div style="width: 60px; height: 60px; border-radius: 50%; background-color: {color}; margin-right: 20px; flex-shrink: 0;"></div>
                <div style="width: 100%;">
                    <h3 style="margin: 0; color: #28264D; font-size: 20px;">{title}</h3>
                    <div style="margin-top: 15px;">
                        <p style="color: #4A4867; margin: 5px 0;"><strong>Interpretation:</strong> {interpretation}</p>
                        <p style="color: #4A4867; margin: 5px 0;"><strong>Marketing goal:</strong> {marketing_goal}</p>
                        <p style="color: #4A4867; margin: 5px 0;"><strong>Consumer type:</strong> {consumer_type}</p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_consumer_archetypes():
    """Render the consumer archetypes display"""
    st.markdown('<div style="padding: 20px;">', unsafe_allow_html=True)
    
    # Logo
    st.image("logoclio.png", width=100)
    
    # Initialize view state if not exists
    if 'archetype_view' not in st.session_state:
        st.session_state.archetype_view = 'archetypes'

    # Define archetype colors to match screenshots
    archetype_colors = {
        'Autonomous': '#FFE4D6',  # Peach
        'Impulsive': '#E7D6FF',   # Light Purple
        'Isolative': '#FFE4A0',   # Light Yellow
        'Avoidant': '#FF6B4A'     # Coral Red
    }

    # Navigation buttons with correct styling
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Go back", type="secondary"):
            st.session_state.selected_option = None
            st.rerun()
    
    with col2:
        if st.session_state.archetype_view == 'archetypes':
            if st.button("View subscales", type="primary"):
                st.session_state.archetype_view = 'subscales'
                st.rerun()
        else:
            if st.button("View archetypes", type="primary"):
                st.session_state.archetype_view = 'archetypes'
                st.rerun()

    # Display title based on view
    st.markdown(
        f"<h2 style='color: #28264D; margin: 20px 0;'>{st.session_state.archetype_view.title()}</h2>",
        unsafe_allow_html=True
    )

    # Display appropriate view
    if st.session_state.archetype_view == 'archetypes':
        archetype_data = {
            'Autonomous': {
                'description': "Clients who seek effective solutions and focus on quick results. Ideal for products that emphasize efficiency, performance, and autonomy.",
                'bullets': [
                    "Clients who frequently search for detailed information, download whitepapers, attend webinars.",
                    "Campaigns that showcase success stories, concrete data on product ROI, and use cases focused on results."
                ]
            },
            'Impulsive': {
                'description': "Clients with reactive behaviors and difficulty managing emotions. Products that provide emotional support, quick solutions to unexpected problems, or stability would be attractive.",
                'bullets': [
                    "Clients who respond to limited-time offers, make unplanned purchases, participate in contests.",
                    "Use emotional messages highlighting the product's speed and ease, including trust-building testimonials."
                ]
            },
            'Isolative': {
                'description': "Clients who seek enjoyment and want to avoid discomfort. Marketing that emphasizes simplicity, pleasure, and well-being can resonate with this profile.",
                'bullets': [
                    "Clients interested in content related to well-being, relaxation, easy-to-use products.",
                    "Content that conveys comfort and joy, highlighting the stress-free benefits the product provides."
                ]
            },
            'Avoidant': {
                'description': "Clients who value independence and prefer discreet, personal solutions. Offers prioritizing privacy and gradual connection would be ideal.",
                'bullets': [
                    "Clients who prefer online interactions, avoid phone calls, value personalization.",
                    "Offers of personalized services, emphasizing privacy and long-term support."
                ]
            }
        }
        
        for name, data in archetype_data.items():
            render_archetype_card(
                name=name,
                description=data['description'],
                bullets=data['bullets'],
                color=archetype_colors[name]
            )
    else:
        subscale_data = {
            'Focus on solving the problem - Autonomous': {
                'interpretation': 'Consumers with high logical reasoning and organization skills. They seek practical and efficient solutions to their problems.',
                'marketing_goal': 'Highlight product efficiency and functionality. - Provide detailed information and technical data. - Show how the product solves specific problems.',
                'consumer_type': 'Goal-oriented professionals, leaders, entrepreneurs. - Value effectiveness and performance. - Want tools to optimize their productivity.',
                'color': archetype_colors['Autonomous']
            },
            'Tension reduction - Impulsive': {
                'interpretation': 'Consumers with low frustration tolerance, seeking immediate gratification and quick solutions.',
                'marketing_goal': 'Offer instant satisfaction and ease of use. - Promote limited-time offers and immediate rewards. - Highlight product speed and simplicity.',
                'consumer_type': 'Impulsive buyers, tech enthusiasts, trend seekers. - Value immediacy and convenience in their purchases.',
                'color': archetype_colors['Impulsive']
            },
            'Keep it to oneself - Isolative': {
                'interpretation': 'Consumers who prefer to handle problems independently and may feel lonely.',
                'marketing_goal': 'Offer autonomous and private solutions. - Promote products that can be used alone. - Ensure product privacy and discretion.',
                'consumer_type': 'Introverts, independent individuals, privacy-concerned consumers. - Value control and autonomy in their experiences.',
                'color': archetype_colors['Isolative']
            },
            'Indulge in illusions - Avoidant': {
                'interpretation': 'Consumers who may detach from reality, avoiding difficult situations.',
                'marketing_goal': 'Offer products that enable dreaming and escape. - Promote immersive or aspirational experiences. - Use storytelling that inspires and motivates.',
                'consumer_type': 'Dreamers, fantasy fans, entertainment consumers. - Seek products that let them explore new realities.',
                'color': archetype_colors['Avoidant']
            }
        }
        
        for title, data in subscale_data.items():
            render_subscale_card(
                title=title,
                interpretation=data['interpretation'],
                marketing_goal=data['marketing_goal'],
                consumer_type=data['consumer_type'],
                color=data['color']
            )

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_consumer_archetypes()
