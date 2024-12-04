import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main layout and colors */
        .main {
            background-color: #FFFFFF !important;
            padding: 0 !important;
        }
        
        /* Sidebar styles */
        section[data-testid="stSidebar"] {
            background-color: #F3F1FF !important;
            padding: 2rem 1rem !important;
            width: 300px !important;
        }
        
        /* Sidebar buttons */
        .stButton button {
            background-color: #1E1B4B !important;
            color: white !important;
            width: 100% !important;
            text-align: left !important;
            padding: 0.75rem 1rem !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            margin-bottom: 0.5rem !important;
            cursor: pointer !important;
        }
        
        /* Save and Exit button */
        .save-exit-btn {
            position: fixed !important;
            top: 1rem !important;
            right: 1rem !important;
            background-color: #1E1B4B !important;
            color: white !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            z-index: 1000 !important;
        }
        
        /* Marketing action buttons */
        .action-buttons {
            display: flex !important;
            justify-content: center !important;
            gap: 1rem !important;
            margin: 2rem auto !important;
            max-width: 800px !important;
            padding: 0 1rem !important;
        }
        
        .generate-btn {
            background-color: #FFD700 !important;
            color: #1E1B4B !important;
            border: none !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            cursor: pointer !important;
        }
        
        .campaign-btn {
            background-color: white !important;
            color: #1E1B4B !important;
            border: 2px solid #1E1B4B !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            cursor: pointer !important;
        }
        
        /* Chat container */
        .chat-container {
            margin: 1rem !important;
            margin-bottom: 120px !important;
            padding: 1rem !important;
            height: calc(100vh - 280px) !important;
            overflow-y: auto !important;
        }
        
        .chat-message {
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
            border-radius: 8px !important;
            max-width: 80% !important;
        }
        
        .user-message {
            background-color: #F3F4F6 !important;
            margin-left: auto !important;
        }
        
        .bot-message {
            background-color: #E5E7EB !important;
            margin-right: auto !important;
        }
        
        /* Chat input */
        .chat-input-container {
            position: fixed !important;
            bottom: 60px !important;
            left: 300px !important;
            right: 0 !important;
            padding: 1rem 2rem !important;
            background-color: white !important;
            border-top: 1px solid #E5E7EB !important;
            display: flex !important;
            align-items: center !important;
            gap: 1rem !important;
            z-index: 100 !important;
        }
        
        .chat-input {
            flex-grow: 1 !important;
            padding: 1rem !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 8px !important;
            font-size: 1rem !important;
        }
        
        .chat-input::placeholder {
            color: #6B7280 !important;
        }
        
        .send-button {
            background-color: #1E1B4B !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        /* Footer */
        .footer {
            position: fixed !important;
            bottom: 0 !important;
            left: 0 !important;
            right: 0 !important;
            background-color: #1E1B4B !important;
            padding: 1rem !important;
            z-index: 1000 !important;
        }
        
        .footer-content {
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            padding: 0 2rem !important;
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        
        .footer-links {
            display: flex !important;
            gap: 2rem !important;
        }
        
        .footer-links a {
            color: white !important;
            text-decoration: none !important;
            font-weight: 500 !important;
        }
        
        .social-icons {
            display: flex !important;
            gap: 1.5rem !important;
        }
        
        .social-icons a {
            color: white !important;
            font-size: 1.25rem !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        </style>
        
        <!-- Font Awesome for icons -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    """, unsafe_allow_html=True)
