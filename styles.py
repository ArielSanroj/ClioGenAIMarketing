import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main layout and colors */
        .main {
            background-color: #FFF8E6;
            padding: 2rem;
        }
        
        /* Navigation options */
        .nav-option {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: left;
            font-size: 1rem;
            color: #1E1B4B;
            cursor: pointer;
            transition: all 0.2s;
            width: 100%;
            max-width: 600px;
            margin: 0 auto 1rem;
            position: relative;
            overflow: hidden;
        }
        
        .nav-option:hover {
            border-color: #1E1B4B;
            transform: translateY(-1px);
            background-color: #F9FAFB;
        }
        
        /* Chat input container */
        .chat-input-container {
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 800px;
            background-color: white;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            display: flex;
            align-items: center;
            gap: 1rem;
            z-index: 1000;
        }
        
        .chat-input {
            flex: 1;
            padding: 0.75rem 1rem;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            font-size: 1rem;
            color: #1E1B4B;
            outline: none;
            transition: border-color 0.2s;
        }
        
        .chat-input:focus {
            border-color: #1E1B4B;
        }
        
        .send-button {
            background-color: transparent;
            border: none;
            padding: 0.5rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #1E1B4B;
            transition: color 0.2s;
        }
        
        .send-button:hover {
            color: #2D2A5C;
        }
        
        /* Chat messages */
        .chat-message {
            margin-bottom: 1rem;
            display: flex;
            align-items: flex-start;
            gap: 1rem;
        }
        
        .chat-message.user {
            flex-direction: row-reverse;
        }
        
        .message-content {
            background-color: white;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            max-width: 70%;
        }
        
        .chat-message.user .message-content {
            background-color: #1E1B4B;
            color: white;
        }
        
        /* Rest of the existing styles */
        .centered-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            text-align: center;
        }
        
        .welcome-title {
            font-size: 3rem;
            color: #28264D;
            margin-bottom: 1.5rem;
            font-weight: bold;
            text-align: center;
        }
        
        .welcome-subtitle {
            font-size: 1.2rem;
            color: #4A4867;
            margin-bottom: 3rem;
            text-align: center;
        }
        
        /* Form styling */
        .stTextInput > label, .stTextArea > label {
            font-size: 1rem;
            color: #28264D;
            font-weight: 500;
        }
        
        .stTextInput > div > div > input, .stTextArea > div > textarea {
            background-color: white;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 0.75rem;
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
        
        /* Enhanced AI System UI Elements */
        .emotional-analysis {
            background-color: #F3F4F6;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .emotional-metric {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        .emotional-metric-label {
            font-weight: 500;
            color: #1E1B4B;
            min-width: 120px;
        }
        
        .emotional-metric-value {
            color: #4B5563;
        }
        
        .behavioral-insights {
            background-color: #F8F9FA;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
        }
        
        .insight-card {
            background-color: white;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.5rem;
        }
        
        .insight-title {
            font-weight: 600;
            color: #1E1B4B;
            margin-bottom: 0.5rem;
        }
        
        .insight-value {
            color: #4B5563;
            font-size: 0.9rem;
        }
        </style>
    """, unsafe_allow_html=True)