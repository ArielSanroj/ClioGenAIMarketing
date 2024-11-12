import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main layout and colors */
        .main {
            background-color: #FFF8E6;
            padding: 2rem;
        }
        
        /* Centered container */
        .centered-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            text-align: center;
        }
        
        /* Welcome title */
        .welcome-title {
            font-size: 3rem;
            color: #28264D;
            margin-bottom: 1.5rem;
            font-weight: bold;
            text-align: center;
        }
        
        /* Welcome subtitle */
        .welcome-subtitle {
            font-size: 1.2rem;
            color: #4A4867;
            margin-bottom: 3rem;
            text-align: center;
        }
        
        /* Form styling - Updated for better visibility */
        .stTextInput > label, .stTextArea > label, .stSelectbox > label {
            font-size: 1rem;
            color: #28264D;
            font-weight: 600;
            margin-bottom: 0.5rem;
            display: block;
        }
        
        /* Enhanced text input styling */
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div {
            background-color: #FFFFFF !important;
            border: 2px solid #E5E7EB !important;
            border-radius: 8px !important;
            padding: 0.875rem !important;
            font-size: 1rem !important;
            color: #1E1B4B !important;
            width: 100% !important;
            transition: all 0.2s ease-in-out !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
        }

        /* Focus states */
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > div:focus {
            border-color: #1E1B4B !important;
            box-shadow: 0 0 0 2px rgba(30, 27, 75, 0.1) !important;
            outline: none !important;
        }

        /* Placeholder styling */
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {
            color: #9CA3AF !important;
            opacity: 1 !important;
        }

        /* Hover states */
        .stTextInput > div > div > input:hover,
        .stTextArea > div > div > textarea:hover,
        .stSelectbox > div > div > div:hover {
            border-color: #1E1B4B !important;
            background-color: #FAFAFA !important;
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
        
        /* Chat input styling - Enhanced */
        .chat-input {
            width: calc(100% - 50px);
            padding: 0.875rem;
            border: 2px solid #E5E7EB;
            border-radius: 8px;
            outline: none;
            font-size: 16px;
            margin-right: 10px;
            background-color: white;
            color: #1E1B4B;
            transition: all 0.2s ease-in-out;
        }
        
        .chat-input:focus {
            border-color: #1E1B4B;
            box-shadow: 0 0 0 2px rgba(30, 27, 75, 0.1);
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
            margin-bottom: 160px;
            padding: 2rem;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .chat-container {
                left: 1rem;
                right: 1rem;
                bottom: 70px;
            }
            
            .main-content {
                margin-bottom: 140px;
            }
            
            /* Responsive input adjustments */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > div {
                font-size: 16px !important; /* Prevents zoom on mobile */
                padding: 0.75rem !important;
            }
        }
        
        /* Custom styling for specific elements */
        .css-1y4p8pa {  /* Sidebar */
            background-color: #F3F1FF;
            border-right: 1px solid #E5E7EB;
        }
        
        /* Hide sidebar when showing welcome screen */
        .welcome-screen .css-1d391kg {
            display: none;
        }
        
        /* Streamlit default overrides */
        .stApp {
            background-color: #FFF8E6;
        }
        
        .css-1d391kg {
            background-color: #FFF8E6;
        }

        /* Error state for inputs */
        .input-error {
            border-color: #DC2626 !important;
        }

        .error-message {
            color: #DC2626;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }
        </style>
    """, unsafe_allow_html=True)
