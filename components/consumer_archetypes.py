import streamlit as st
import pandas as pd

def render_archetype_card(name, data):
    """Render an archetype card with circle icon and profile information"""
    st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: flex-start; gap: 1rem;">
                <div style="width: 4rem; height: 4rem; border-radius: 50%; background-color: {data['color']}; flex-shrink: 0;"></div>
                <div style="flex-grow: 1;">
                    <h3 style="margin: 0; color: #28264D; font-size: 1.25rem; font-weight: 600;">{name}</h3>
                    
                    <div style="margin-top: 1rem; color: #4A4867;">
                        <p style="margin-bottom: 0.75rem;">{data['description']}</p>
                        <p style="margin-bottom: 0.75rem;">{data['client_type']}</p>
                        <p style="margin-bottom: 0.75rem;">{data['campaign_strategy']}</p>
                    </div>

                    <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #E5E7EB;">
                        <h4 style="font-size: 1rem; font-weight: 500; margin-bottom: 0.5rem;">Profile Example:</h4>
                        <p style="color: #4A4867; margin: 0;">
                            {data['profile']['name']}, {data['profile']['occupation']}, {data['profile']['age']} years old
                        </p>
                        <p style="color: #4A4867; margin-top: 0.25rem;">
                            {data['profile']['needs']}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_subscale_card(title, interpretation, marketing_goal, consumer_type, color):
    """Render a subscale card with matching styling"""
    st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: flex-start; gap: 1rem;">
                <div style="width: 4rem; height: 4rem; border-radius: 50%; background-color: {color}; flex-shrink: 0;"></div>
                <div style="flex-grow: 1;">
                    <h3 style="margin: 0; color: #28264D; font-size: 1.25rem; font-weight: 600;">{title}</h3>
                    
                    <div style="margin-top: 1rem; color: #4A4867;">
                        <p style="margin-bottom: 0.75rem;"><strong>Interpretation:</strong> {interpretation}</p>
                        <p style="margin-bottom: 0.75rem;"><strong>Marketing goal:</strong> {marketing_goal}</p>
                        <p style="margin-bottom: 0.75rem;"><strong>Consumer type:</strong> {consumer_type}</p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_consumer_archetypes():
    """Render the consumer archetypes display"""
    st.markdown('<div style="padding: 1.5rem; max-width: 64rem; margin: 0 auto;">', unsafe_allow_html=True)
    
    # Logo
    st.image("logoclio.png", width=100)
    
    # Initialize view state if not exists
    if 'archetype_view' not in st.session_state:
        st.session_state.archetype_view = 'archetypes'

    # Navigation buttons with correct styling
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Go back", type="secondary", key="go_back"):
            st.session_state.selected_option = None
            st.rerun()
    
    with col2:
        if st.session_state.archetype_view == 'archetypes':
            if st.button("View subscales", type="primary", key="view_subscales"):
                st.session_state.archetype_view = 'subscales'
                st.rerun()
        else:
            if st.button("View archetypes", type="primary", key="view_archetypes"):
                st.session_state.archetype_view = 'archetypes'
                st.rerun()

    # Display title based on view
    st.markdown(
        f"<h2 style='color: #28264D; margin: 1.5rem 0; font-size: 2rem;'>{st.session_state.archetype_view.title()}</h2>",
        unsafe_allow_html=True
    )

    # Display appropriate view
    if st.session_state.archetype_view == 'archetypes':
        archetype_data = {
            'autonomous': {
                'name': 'Autonomous',
                'description': 'This archetype is aimed at clients who seek effective solutions and focus on quick results. Ideal for products that emphasize efficiency, performance, and autonomy.',
                'client_type': 'Clients who frequently search for detailed information, download whitepapers, attend webinars.',
                'campaign_strategy': 'Campaigns that showcase success stories, concrete data on product ROI, and use cases focused on results.',
                'color': '#FFE4D6',
                'profile': {
                    'name': 'María',
                    'age': 35,
                    'occupation': 'Project Manager',
                    'needs': 'Seeks tools that optimize her time and give her full control'
                }
            },
            'impulsive': {
                'name': 'Impulsive',
                'description': 'Applies to clients with reactive behaviors and difficulty managing emotions. Products that provide emotional support, quick solutions to unexpected problems, or stability would be attractive.',
                'client_type': 'Clients who respond to limited-time offers, make unplanned purchases, participate in contests.',
                'campaign_strategy': 'Use emotional messages highlighting the product\'s speed and ease, including trust-building testimonials.',
                'color': '#E7D6FF',
                'profile': {
                    'name': 'Juan',
                    'age': 22,
                    'occupation': 'University Student',
                    'needs': 'Attracted to the latest trends and flash offers'
                }
            },
            'isolative': {
                'name': 'Isolative',
                'description': 'Suited to clients who seek enjoyment and want to avoid discomfort. Marketing that emphasizes simplicity, pleasure, and well-being can resonate with this profile.',
                'client_type': 'Clients interested in content related to well-being, relaxation, easy-to-use products.',
                'campaign_strategy': 'Content that conveys comfort and joy, highlighting the stress-free benefits the product provides.',
                'color': '#FFE4A0',
                'profile': {
                    'name': 'Carlos',
                    'age': 45,
                    'occupation': 'Independent Writer',
                    'needs': 'Prefers personalized solutions and values privacy'
                }
            },
            'avoidant': {
                'name': 'Avoidant',
                'description': 'This archetype fits clients who value independence and prefer discreet, personal solutions. Offers prioritizing privacy and gradual connection would be ideal.',
                'client_type': 'Clients who prefer online interactions, avoid phone calls, value personalization.',
                'campaign_strategy': 'Offers of personalized services, emphasizing privacy and long-term support.',
                'color': '#FF6B4A',
                'profile': {
                    'name': 'Laura',
                    'age': 40,
                    'occupation': 'Health Professional',
                    'needs': 'Seeks products that offer comfort and reduce stress'
                }
            }
        }
        
        for id, data in archetype_data.items():
            render_archetype_card(data['name'], data)
    else:
        subscale_data = {
            'Focus on solving the problem - Autonomous': {
                'interpretation': 'Consumers with high logical reasoning and organization skills. They seek practical and efficient solutions to their problems.',
                'marketing_goal': 'Highlight product efficiency and functionality. - Provide detailed information and technical data. - Show how the product solves specific problems.',
                'consumer_type': 'Goal-oriented professionals, leaders, entrepreneurs. - Value effectiveness and performance. - Want tools to optimize their productivity.',
                'color': '#FFE4D6'
            },
            'Tension reduction - Impulsive': {
                'interpretation': 'Consumers with low frustration tolerance, seeking immediate gratification and quick solutions.',
                'marketing_goal': 'Offer instant satisfaction and ease of use. - Promote limited-time offers and immediate rewards. - Highlight product speed and simplicity.',
                'consumer_type': 'Impulsive buyers, tech enthusiasts, trend seekers. - Value immediacy and convenience in their purchases.',
                'color': '#E7D6FF'
            },
            'Keep it to oneself - Isolative': {
                'interpretation': 'Consumers who prefer to handle problems independently and may feel lonely.',
                'marketing_goal': 'Offer autonomous and private solutions. - Promote products that can be used alone. - Ensure product privacy and discretion.',
                'consumer_type': 'Introverts, independent individuals, privacy-concerned consumers. - Value control and autonomy in their experiences.',
                'color': '#FFE4A0'
            },
            'Indulge in illusions - Avoidant': {
                'interpretation': 'Consumers who may detach from reality, avoiding difficult situations.',
                'marketing_goal': 'Offer products that enable dreaming and escape. - Promote immersive or aspirational experiences. - Use storytelling that inspires and motivates.',
                'consumer_type': 'Dreamers, fantasy fans, entertainment consumers. - Seek products that let them explore new realities.',
                'color': '#FF6B4A'
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
