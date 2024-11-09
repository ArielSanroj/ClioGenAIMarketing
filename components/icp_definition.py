import streamlit as st
import pandas as pd

def initialize_icp_state():
    """Initialize ICP session state"""
    if 'icp_data' not in st.session_state:
        st.session_state.icp_data = {
            'demographics': {},
            'psychographics': {},
            'archetype': '',
            'pain_points': [],
            'goals': [],
            'is_completed': False
        }

def render_icp_definition():
    """Render the ICP definition form"""
    initialize_icp_state()
    
    st.markdown("## Ideal Customer Profile (ICP)")
    st.markdown("Define your ideal customer profile to ensure targeted and effective content generation.")
    
    with st.form(key='icp_form', clear_on_submit=False):
        # Demographics
        st.subheader("Demographics")
        col1, col2 = st.columns(2)
        
        with col1:
            age_range = st.selectbox(
                "Age Range",
                ["18-24", "25-34", "35-44", "45-54", "55+"],
                index=0 if not st.session_state.icp_data['demographics'].get('age_range') else 
                ["18-24", "25-34", "35-44", "45-54", "55+"].index(st.session_state.icp_data['demographics'].get('age_range'))
            )
            
            income_range = st.selectbox(
                "Income Range",
                ["Under $30k", "$30k-$50k", "$50k-$100k", "$100k-$150k", "$150k+"],
                index=0 if not st.session_state.icp_data['demographics'].get('income_range') else
                ["Under $30k", "$30k-$50k", "$50k-$100k", "$100k-$150k", "$150k+"].index(st.session_state.icp_data['demographics'].get('income_range'))
            )
        
        with col2:
            education = st.selectbox(
                "Education Level",
                ["High School", "Bachelor's", "Master's", "Ph.D.", "Other"],
                index=0 if not st.session_state.icp_data['demographics'].get('education') else
                ["High School", "Bachelor's", "Master's", "Ph.D.", "Other"].index(st.session_state.icp_data['demographics'].get('education'))
            )
            
            location = st.text_input(
                "Primary Location/Market",
                value=st.session_state.icp_data['demographics'].get('location', '')
            )
        
        # Consumer Archetype
        st.subheader("Consumer Archetype")
        archetype = st.radio(
            "Select the primary consumer archetype that best matches your ICP:",
            ["Autonomous - Independent decision-makers who value control and efficiency",
             "Impulsive - Spontaneous buyers who make quick, emotion-driven decisions",
             "Isolative - Careful researchers who prefer self-guided purchasing journeys",
             "Avoidant - Risk-averse consumers who need extensive validation"],
            index=0 if not st.session_state.icp_data.get('archetype') else
            ["Autonomous", "Impulsive", "Isolative", "Avoidant"].index(st.session_state.icp_data.get('archetype'))
        )
        
        # Pain Points and Goals
        st.subheader("Pain Points & Goals")
        pain_points = st.text_area(
            "Key Pain Points",
            value=', '.join(st.session_state.icp_data.get('pain_points', [])),
            help="Enter the main challenges and pain points your ICP faces, separated by commas"
        )
        
        goals = st.text_area(
            "Primary Goals",
            value=', '.join(st.session_state.icp_data.get('goals', [])),
            help="Enter the main goals and aspirations of your ICP, separated by commas"
        )
        
        submit_button = st.form_submit_button("Save ICP Definition")
        
        if submit_button:
            if all([age_range, income_range, education, location, archetype, pain_points, goals]):
                # Update session state
                st.session_state.icp_data.update({
                    'demographics': {
                        'age_range': age_range,
                        'income_range': income_range,
                        'education': education,
                        'location': location
                    },
                    'archetype': archetype.split(' - ')[0],  # Store just the archetype name
                    'pain_points': [p.strip() for p in pain_points.split(',') if p.strip()],
                    'goals': [g.strip() for g in goals.split(',') if g.strip()],
                    'is_completed': True
                })
                st.success("ICP definition saved successfully!")
            else:
                st.error("Please fill in all fields before proceeding.")

    # Display current ICP if completed
    if st.session_state.icp_data.get('is_completed'):
        st.markdown("### Current ICP Profile")
        st.markdown("**Demographics:**")
        for key, value in st.session_state.icp_data['demographics'].items():
            st.markdown(f"- {key.replace('_', ' ').title()}: {value}")
        
        st.markdown(f"**Consumer Archetype:** {st.session_state.icp_data['archetype']}")
        
        st.markdown("**Pain Points:**")
        for point in st.session_state.icp_data['pain_points']:
            st.markdown(f"- {point}")
            
        st.markdown("**Goals:**")
        for goal in st.session_state.icp_data['goals']:
            st.markdown(f"- {goal}")
