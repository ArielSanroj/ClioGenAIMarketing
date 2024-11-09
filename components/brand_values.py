import streamlit as st

def initialize_brand_values_state():
    """Initialize brand values session state"""
    if 'brand_values' not in st.session_state:
        st.session_state.brand_values = {
            'mission': '',
            'values': [],
            'virtues': [],
            'is_completed': False
        }

def render_brand_values():
    """Render the brand values and virtues form"""
    initialize_brand_values_state()
    
    st.markdown("## Brand Values & Virtues")
    st.markdown("Define your brand's core values and mission to ensure all generated content aligns with your brand identity.")
    
    with st.form(key='brand_values_form', clear_on_submit=False):
        mission = st.text_area(
            "Brand Mission Statement",
            value=st.session_state.brand_values.get('mission', ''),
            help="Define your brand's purpose and goals in a clear, concise statement.",
            height=100
        )
        
        # Convert list to string for text input
        current_values = ', '.join(st.session_state.brand_values.get('values', []))
        values = st.text_area(
            "Core Values",
            value=current_values,
            help="Enter your brand's core values, separated by commas (e.g., Innovation, Integrity, Excellence)",
            height=100
        )
        
        current_virtues = ', '.join(st.session_state.brand_values.get('virtues', []))
        virtues = st.text_area(
            "Brand Virtues",
            value=current_virtues,
            help="Enter your brand's virtues and principles, separated by commas",
            height=100
        )
        
        submit_button = st.form_submit_button("Save Brand Values")
        
        if submit_button:
            if mission and values and virtues:
                # Update session state
                st.session_state.brand_values.update({
                    'mission': mission,
                    'values': [v.strip() for v in values.split(',') if v.strip()],
                    'virtues': [v.strip() for v in virtues.split(',') if v.strip()],
                    'is_completed': True
                })
                st.success("Brand values saved successfully!")
            else:
                st.error("Please fill in all fields before proceeding.")

    # Display current values if completed
    if st.session_state.brand_values.get('is_completed'):
        st.markdown("### Current Brand Profile")
        st.markdown(f"**Mission:** {st.session_state.brand_values['mission']}")
        st.markdown("**Core Values:**")
        for value in st.session_state.brand_values['values']:
            st.markdown(f"- {value}")
        st.markdown("**Brand Virtues:**")
        for virtue in st.session_state.brand_values['virtues']:
            st.markdown(f"- {virtue}")
