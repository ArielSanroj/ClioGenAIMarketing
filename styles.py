import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        .stButton > button {
            background-color: #28264D;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            border: none;
            width: 100%;
        }
        .stTextInput > div > div > input {
            border-radius: 8px;
        }
        .sidebar-content {
            background-color: #F5F3FF;
            padding: 1rem;
            border-radius: 8px;
        }
        .main-content {
            padding: 2rem;
            background-color: white;
            border-radius: 12px;
            margin: 1rem 0;
        }
        .card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
