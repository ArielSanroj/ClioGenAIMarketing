import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main layout and colors */
        .main {
            background-color: #FFFFFF;
            padding: 2rem;
        }
        
        /* Sidebar styles */
        .css-1d391kg {
            background-color: #F3F1FF !important;
        }
        
        /* Sidebar buttons */
        .sidebar-button {
            background-color: #1E1B4B !important;
            color: white !important;
            width: 100% !important;
            text-align: left;
            margin-bottom: 0.5rem;
            border: none !important;
            padding: 0.75rem 1rem !important;
            border-radius: 8px !important;
        }
        
        /* Save and Exit button */
        .save-exit-button {
            background-color: #1E1B4B !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            float: right;
            margin: 1rem;
            border: none !important;
        }
        
        /* Marketing action buttons container */
        .action-buttons-container {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 2rem auto;
            max-width: 800px;
        }
        
        /* Generate Content Marketing button */
        .generate-button {
            background-color: #FFD700 !important;
            color: #1E1B4B !important;
            border: none !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            width: auto !important;
        }
        
        /* Create Marketing Campaign button */
        .campaign-button {
            background-color: white !important;
            color: #1E1B4B !important;
            border: 1px solid #1E1B4B !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            width: auto !important;
        }
        
        /* Chat container */
        .chat-container {
            margin-bottom: 120px;
            padding: 1rem;
            height: calc(100vh - 280px);
            overflow-y: auto;
        }
        
        /* Chat messages */
        .chat-message {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            max-width: 80%;
        }
        
        .user-message {
            background-color: #F3F4F6;
            margin-left: auto;
        }
        
        .bot-message {
            background-color: #E5E7EB;
            margin-right: auto;
        }
        
        /* Chat input area */
        .chat-input-container {
            position: fixed;
            bottom: 60px;
            left: 0;
            right: 0;
            padding: 1rem;
            background-color: white;
            border-top: 1px solid #E5E7EB;
            display: flex;
            align-items: center;
            gap: 1rem;
            z-index: 99;
        }
        
        .chat-input {
            flex-grow: 1;
            padding: 0.875rem;
            border: 2px solid #E5E7EB;
            border-radius: 8px;
            outline: none;
            font-size: 16px;
            background-color: white;
            color: #1E1B4B;
        }
        
        .chat-input:focus {
            border-color: #1E1B4B;
            box-shadow: 0 0 0 2px rgba(30, 27, 75, 0.1);
        }
        
        /* Send button */
        .send-button {
            background-color: #1E1B4B !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.875rem 1.5rem !important;
            margin-left: 0.5rem !important;
        }
        
        /* Footer */
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
        
        /* Footer links and social icons */
        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        .footer-links a {
            color: white;
            text-decoration: none;
            margin: 0 1rem;
        }
        
        .social-icons {
            display: flex;
            gap: 1rem;
        }
        
        .social-icons a {
            color: white;
            text-decoration: none;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)