import streamlit as st
from utils.session_manager import get_user_state, set_user_state, get_current_user_id

def initialize_brand_values_state():
    """Initialize brand values session state"""
    user_id = get_current_user_id()
    if not get_user_state(user_id, "brand_values"):
        set_user_state(user_id, "brand_values", {
            'mission': '',
            'values': [],
            'virtues': [],
            'is_completed': False
        })

def render_brand_values():
    """Render the brand values and virtues form"""
    initialize_brand_values_state()
    user_id = get_current_user_id()
    
    # Add centered container
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    
    # Logo
    st.image("logoclio.png", width=100)
    
    # Welcome message
    st.markdown('<h1 class="welcome-title">Welcome to Clio</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="welcome-subtitle">Please tell us about your company to personalize your experience</p>',
        unsafe_allow_html=True
    )
    
    with st.form(key='brand_values_form', clear_on_submit=False):
        mission = st.text_area(
            "What is your company's mission?",
            value=get_user_state(user_id, "brand_values").get('mission', ''),
            height=100,
            help="Define your company's purpose and goals in a clear, concise statement."
        )
        
        st.markdown("### What are the virtues and values of your brand?")
        
        # Convert list to string for text input
        current_values = ', '.join(get_user_state(user_id, "brand_values").get('values', []))
        values = st.text_area(
            "Core Values",
            value=current_values,
            help="Enter your brand's core values, separated by commas (e.g., Innovation, Integrity, Excellence)",
            height=100
        )
        
        current_virtues = ', '.join(get_user_state(user_id, "brand_values").get('virtues', []))
        virtues = st.text_area(
            "Brand Virtues",
            value=current_virtues,
            help="Enter your brand's virtues and principles, separated by commas",
            height=100
        )
        
        submit_button = st.form_submit_button("Save and Continue")
        
        if submit_button:
            if mission and values and virtues:
                # Update session state using session manager
                brand_values = {
                    'mission': mission,
                    'values': [v.strip() for v in values.split(',') if v.strip()],
                    'virtues': [v.strip() for v in virtues.split(',') if v.strip()],
                    'is_completed': True
                }
                set_user_state(user_id, "brand_values", brand_values)
                st.success("Brand values saved successfully!")
                st.rerun()
            else:
                st.error("Please fill in all fields before proceeding.")
    
    # Add skip button after the form
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Skip", type="secondary"):
            # Update session state to skip brand values
            brand_values = {
                'mission': '',
                'values': [],
                'virtues': [],
                'is_completed': True  # Mark as completed even though skipped
            }
            set_user_state(user_id, "brand_values", brand_values)
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="footer">
            <div>
                <a href="#">Contact Us</a>
                <a href="#">Privacy Policy</a>
            </div>
            <div>
                <a href="#"><i class="fab fa-facebook"></i></a>
                <a href="#"><i class="fab fa-instagram"></i></a>
                <a href="#"><i class="fab fa-youtube"></i></a>
                <a href="#"><i class="fab fa-twitter"></i></a>
                <a href="#"><i class="fab fa-whatsapp"></i></a>
                <a href="#"><i class="fab fa-linkedin"></i></a>
            </div>
        </div>
    """, unsafe_allow_html=True)
