import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main layout and colors */
        .main {
            background-color: #F9F9FB !important;
            padding: 1.5rem !important;
        }
        
        /* Title styling */
        h1, h2 {
            color: #1E1B4B !important;
            font-size: 1.5rem !important;
            margin-bottom: 1.5rem !important;
            font-weight: 600 !important;
        }
        
        /* Input field styling */
        .stTextInput > div > div > input {
            background-color: white !important;
            color: #1E1B4B !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 4px !important;
            padding: 0.75rem !important;
            margin-bottom: 1rem !important;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #1E1B4B !important;
            color: white !important;
            width: 100% !important;
            padding: 0.75rem !important;
            border: none !important;
            border-radius: 4px !important;
            margin: 0.5rem 0 !important;
            cursor: pointer !important;
            font-weight: 500 !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        
        /* Custom paragraph styling */
        p {
            color: #4A5568 !important;
            margin-bottom: 0.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)