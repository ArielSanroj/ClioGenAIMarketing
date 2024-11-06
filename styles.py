import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main layout and colors */
        .main {
            background-color: #F3F1FF;
            padding: 2rem;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #F3F1FF;
        }
        
        /* Button styles */
        .stButton > button {
            background-color: #1E1B4B;
            color: white;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            border: none;
            width: 100%;
            transition: background-color 0.2s;
        }
        
        .stButton > button:hover {
            background-color: #2d2a5c;
        }
        
        /* Action buttons */
        .action-button {
            background-color: white !important;
            color: #1E1B4B !important;
            border: 1px solid #E5E7EB !important;
        }
        
        .highlight-button {
            background-color: #FFF8E6 !important;
            border: 1px solid #FFE4A0 !important;
        }
        
        /* Fixed footer */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #1E1B4B;
            color: white;
            padding: 1rem;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        /* Chat input */
        .chat-input-container {
            position: fixed;
            bottom: 60px;
            left: 300px;
            right: 2rem;
            background-color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            z-index: 99;
        }
        
        .chat-input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            outline: none;
        }
        
        /* Sidebar navigation */
        .sidebar-nav {
            padding: 1rem;
        }
        
        .sidebar-nav button {
            text-align: left;
            margin-bottom: 0.5rem;
        }
        
        /* Main content area */
        .main-content {
            margin-bottom: 120px;  /* Space for fixed footer and chat input */
            padding: 2rem;
        }
        
        /* Responsive columns */
        .row-widget.stHorizontal {
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .row-widget.stHorizontal > div {
            flex: 1 1 200px;
        }
        
        /* Custom styling for specific elements */
        .css-1y4p8pa {  /* Sidebar */
            background-color: #F3F1FF;
            border-right: 1px solid #E5E7EB;
        }
        
        .css-1vq4p4l {  /* Main content */
            padding: 2rem;
        }
        
        </style>
    """, unsafe_allow_html=True)
