import streamlit as st
import pandas as pd

def load_archetype_data():
    """Load data from Excel files"""
    try:
        archetypes_df = pd.read_excel("Consumer Archetype.xlsx")
        subscales_df = pd.read_excel("Consumer Subscales.xlsx")
        return archetypes_df, subscales_df
    except Exception as e:
        st.error(f"Error loading archetype data: {str(e)}")
        return None, None

def render_archetype_card(name, description, color):
    """Render an archetype card with circle icon"""
    st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 8px; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: flex-start;">
                <div style="width: 60px; height: 60px; border-radius: 50%; background-color: {color}; margin-right: 20px; flex-shrink: 0;"></div>
                <div>
                    <h3 style="margin: 0; color: #28264D;">{name}</h3>
                    <p style="color: #4A4867; margin-top: 10px;">{description}</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_subscale_card(title, interpretation, marketing_goal, consumer_type, color):
    """Render a subscale card"""
    st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 8px; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: flex-start;">
                <div style="width: 60px; height: 60px; border-radius: 50%; background-color: {color}; margin-right: 20px; flex-shrink: 0;"></div>
                <div>
                    <h3 style="margin: 0; color: #28264D;">{title}</h3>
                    <p style="color: #4A4867; margin-top: 10px;"><strong>Interpretation:</strong> {interpretation}</p>
                    <p style="color: #4A4867;"><strong>Marketing goal:</strong> {marketing_goal}</p>
                    <p style="color: #4A4867;"><strong>Consumer type:</strong> {consumer_type}</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_consumer_archetypes():
    """Render the consumer archetypes display"""
    # Load data
    archetypes_df, subscales_df = load_archetype_data()
    
    if archetypes_df is None or subscales_df is None:
        st.warning("Unable to load archetype data. Please check the Excel files.")
        return

    # Initialize view state if not exists
    if 'archetype_view' not in st.session_state:
        st.session_state.archetype_view = 'archetypes'

    # Define archetype colors
    archetype_colors = {
        'Autonomous': '#FFE4D6',
        'Impulsive': '#E7D6FF',
        'Isolative': '#FFE4A0',
        'Avoidant': '#FF6B4A'
    }

    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Go back"):
            st.session_state.selected_option = None
            st.rerun()
    
    with col2:
        if st.session_state.archetype_view == 'archetypes':
            if st.button("View subscales"):
                st.session_state.archetype_view = 'subscales'
                st.rerun()

    # Display appropriate view
    if st.session_state.archetype_view == 'archetypes':
        st.markdown("## Archetypes")
        
        # Display archetype cards
        for _, row in archetypes_df.iterrows():
            name = row['Name']
            if name in archetype_colors:
                render_archetype_card(
                    name=name,
                    description=row['Description'],
                    color=archetype_colors[name]
                )
    else:
        st.markdown("## Subscales")
        
        # Display subscale cards
        subscale_titles = {
            'Autonomous': 'Focus on solving the problem - Autonomous',
            'Impulsive': 'Tension reduction - Impulsive',
            'Isolative': 'Keep it to oneself - Isolative',
            'Avoidant': 'Indulge in illusions - Avoidant'
        }

        for archetype, title in subscale_titles.items():
            subscale_data = subscales_df[subscales_df['Category'] == archetype].iloc[0] if not subscales_df[subscales_df['Category'] == archetype].empty else None
            
            if subscale_data is not None:
                render_subscale_card(
                    title=title,
                    interpretation=subscale_data['Description'],
                    marketing_goal=subscale_data.get('Marketing Goal', ''),
                    consumer_type=subscale_data.get('Consumer Type', ''),
                    color=archetype_colors[archetype]
                )

if __name__ == "__main__":
    render_consumer_archetypes()