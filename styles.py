import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main layout and colors */
        .main {
            background-color: #F9F9FB !important;
            padding: 2rem !important;
        }
        
        /* Title styling */
        h1 {
            color: #1E1B4B !important;
            font-size: 2rem !important;
            margin-bottom: 2rem !important;
        }
        
        /* Input field styling */
        .stTextInput > div > div > input {
            background-color: #1E1B4B !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            margin-bottom: 1rem !important;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #1E1B4B !important;
            color: white !important;
            width: 100% !important;
            padding: 1rem !important;
            border: none !important;
            border-radius: 8px !important;
            margin-bottom: 1rem !important;
            cursor: pointer !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        </style>
    """, unsafe_allow_html=True)