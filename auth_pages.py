import streamlit as st
from auth import register_user, authenticate_user

def render_login_page():
    """Render the login page"""
    st.markdown("""
        <style>
        .main {
            background-color: #FFF8E6;
        }
        .stButton>button {
            background-color: #1E1B4B;
            color: white;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            width: 100%;
        }
        .form-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.image("logoclio.png", width=100)
    st.markdown("<h1 style='text-align: center;'>Welcome to Clio AI</h1>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Log In"):
            if email and password:
                result = authenticate_user(email, password)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.session_state.user_id = result["user_id"]
                    st.session_state.user_email = result["email"]
                    st.session_state.access_token = result["access_token"]
                    st.rerun()
            else:
                st.error("Please fill in all fields")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Don't have an account?"):
            st.session_state.show_register = True
            st.rerun()
    with col2:
        if st.button("Forgot password?"):
            st.session_state.show_reset = True
            st.rerun()

def render_registration_page():
    """Render the registration page"""
    st.image("logoclio.png", width=100)
    st.markdown("<h1 style='text-align: center;'>Create Account</h1>", unsafe_allow_html=True)
    
    with st.form("registration_form"):
        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")
        name = st.text_input("Name")
        surname = st.text_input("Surname")
        cellphone = st.text_input("Cellphone")
        purpose = st.selectbox(
            "How can we help you?",
            ["", "For Education - Personalized Learning", "For Human Resources", "For Marketing - Personalized Ads"]
        )
        
        if st.form_submit_button("Sign Up"):
            if all([email, password, name, surname, cellphone, purpose]):
                result = register_user(email, password, name, surname, cellphone, purpose)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(result["message"])
                    # Set session state for automatic login
                    st.session_state.user_id = result["user_id"]
                    st.session_state.user_email = result["email"]
                    st.session_state.access_token = result["access_token"]
                    st.rerun()
            else:
                st.error("Please fill in all fields")
    
    if st.button("Already have an account? Log in"):
        st.session_state.show_register = False
        st.rerun()

def render_auth_pages():
    """Main function to render authentication pages"""
    if "show_register" not in st.session_state:
        st.session_state.show_register = False
    if "show_reset" not in st.session_state:
        st.session_state.show_reset = False
    
    if st.session_state.show_register:
        render_registration_page()
    else:
        render_login_page()