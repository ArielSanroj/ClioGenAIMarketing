import streamlit as st
from ai_utils import generate_marketing_content
from database import db
import json
import html

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'content_form_state' not in st.session_state:
        st.session_state.content_form_state = {
            'story': '',
            'content_type': '',
            'platform': '',
            'tone': '',
            'competitor_insights': '',
            'generated_content': None
        }

def sanitize_input(text: str) -> str:
    """Sanitize input text to prevent injection and formatting issues"""
    if not text:
        return ""
    sanitized = html.escape(text.strip())
    return ' '.join(sanitized.split())

def render_content_generator():
    # Apply custom styles
    st.markdown("""
        <style>
        .main {
            background-color: #F9F9FB !important;
            padding-top: 40px !important;
        }
        .stApp {
            background-color: #F9F9FB !important;
        }
        .card-container {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
            height: 100%;
            margin-bottom: 2rem;
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: white !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            font-size: 1rem !important;
            color: #1E1B4B !important;
            min-height: 150px !important;
            box-shadow: none !important;
            margin-bottom: 24px !important;
            transition: all 0.2s ease !important;
        }
        .stTextInput>div>div>input:hover, .stTextArea>div>div>textarea:hover {
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
            border-color: #D1D5DB !important;
        }
        .stTextInput>div>div>input::placeholder, .stTextArea>div>div>textarea::placeholder {
            color: #6B7280 !important;
            opacity: 1 !important;
            font-size: 1rem !important;
        }
        .stSelectbox>div>div>div {
            background-color: white !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            color: #1E1B4B !important;
            font-size: 1rem !important;
            height: 56px !important;
            min-height: 56px !important;
            display: flex !important;
            align-items: center !important;
            cursor: pointer !important;
            margin-bottom: 24px !important;
            transition: all 0.2s ease !important;
        }
        .stSelectbox>div>div>div:hover {
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
            border-color: #D1D5DB !important;
        }
        .stSelectbox>div>div>div::after {
            content: '';
            border-style: solid;
            border-width: 2px 2px 0 0;
            display: inline-block;
            padding: 3px;
            transform: rotate(135deg);
            position: absolute;
            right: 1.5rem;
            top: 50%;
            margin-top: -4px;
            color: #1E1B4B !important;
        }
        /* Remove default selectbox arrow */
        .stSelectbox select {
            -webkit-appearance: none !important;
            -moz-appearance: none !important;
            appearance: none !important;
        }
        .go-back {
            position: absolute;
            top: 2rem;
            right: 2rem;
            z-index: 1000;
        }
        .go-back button {
            background-color: #1E1B4B !important;
            color: white !important;
            border: none !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.2s !important;
            font-size: 1rem !important;
        }
        .go-back button:hover {
            background-color: #2D2A5C !important;
            transform: translateY(-1px) !important;
        }
        h1, h2, h3 {
            color: #1E1B4B !important;
            font-weight: 700 !important;
            margin-bottom: 2rem !important;
            font-size: 24px !important;
            line-height: 1.2 !important;
            letter-spacing: -0.025em !important;
        }
        .label-text {
            color: #1E1B4B !important;
            font-weight: 600 !important;
            margin-bottom: 1rem !important;
            font-size: 1rem !important;
            display: block !important;
            line-height: 1.5 !important;
            margin-top: 1.5rem !important;
            letter-spacing: -0.01em !important;
        }
        .stButton>button {
            background-color: #1E1B4B !important;
            color: white !important;
            border: none !important;
            padding: 1rem 1.5rem !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            width: 100% !important;
            margin-top: 2rem !important;
            transition: all 0.2s !important;
            font-size: 1rem !important;
            letter-spacing: 0.025em !important;
            height: 56px !important;
        }
        .stButton>button:hover {
            background-color: #2D2A5C !important;
            transform: translateY(-1px) !important;
        }
        .generated-content-placeholder {
            color: #6B7280 !important;
            font-style: italic !important;
            margin-top: 1rem !important;
            line-height: 1.6 !important;
            font-size: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    initialize_session_state()

    # Header with logo and Go back button
    col1, col2 = st.columns([1, 11])
    with col1:
        st.image("logoclio.png", width=60)
    
    # Go back button
    st.markdown(
        """
        <div class="go-back">
            <button onclick="window.history.back()">Go back</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Main content area with two equal columns
    col1, col2 = st.columns(2, gap="large")

    # Left column - Input form
    with col1:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        st.markdown('<p class="label-text">What would you like to talk about?</p>', unsafe_allow_html=True)
        story = st.text_area(
            label="Story Input",
            value=st.session_state.content_form_state['story'],
            placeholder="What is the story you want to tell",
            label_visibility="collapsed",
            height=150
        )

        st.markdown('<p class="label-text">Content Type</p>', unsafe_allow_html=True)
        content_type = st.selectbox(
            label="Content Type Selection",
            options=["", "Blog Post", "Social Media Post", "Email Newsletter", "Landing Page"],
            key="content_type",
            label_visibility="collapsed"
        )

        st.markdown('<p class="label-text">Platform</p>', unsafe_allow_html=True)
        platform = st.selectbox(
            label="Platform Selection",
            options=["", "Website", "LinkedIn", "Twitter", "Instagram", "Facebook"],
            key="platform",
            label_visibility="collapsed"
        )

        st.markdown('<p class="label-text">Emotional tone</p>', unsafe_allow_html=True)
        tone = st.selectbox(
            label="Tone Selection",
            options=["", "Professional", "Casual", "Inspirational", "Educational", "Persuasive"],
            key="tone",
            label_visibility="collapsed"
        )

        st.markdown('<p class="label-text">Competitor Insights</p>', unsafe_allow_html=True)
        competitor_insights = st.text_area(
            label="Competitor Insights Input",
            value=st.session_state.content_form_state['competitor_insights'],
            placeholder="Add any competitor insights or success strategies",
            label_visibility="collapsed",
            height=150
        )
        
        # Generate button
        if st.button("Generate Content"):
            # Sanitize inputs
            sanitized_story = sanitize_input(story or "")
            sanitized_insights = sanitize_input(competitor_insights or "")
            
            if not sanitized_story:
                st.error("Please enter a story to generate content.")
                return
                
            st.session_state.content_form_state.update({
                'story': sanitized_story,
                'content_type': content_type,
                'platform': platform,
                'tone': tone,
                'competitor_insights': sanitized_insights
            })
            
            with st.spinner("Generating content..."):
                try:
                    prompt = f"""
                    Story: {sanitized_story}
                    Content Type: {content_type}
                    Platform: {platform}
                    Tone: {tone}
                    Competitor Insights: {sanitized_insights}
                    """
                    
                    if hasattr(st.session_state, 'brand_values'):
                        prompt += f"\nBrand Values: {json.dumps(st.session_state.brand_values)}"
                    if hasattr(st.session_state, 'icp_data'):
                        prompt += f"\nICP Data: {json.dumps(st.session_state.icp_data)}"
                    
                    try:
                        content = generate_marketing_content(prompt, content_type)
                        st.session_state.content_form_state['generated_content'] = content
                        
                        if content and content.get('content'):
                            db.save_campaign(
                                business_name=sanitized_story[:50],
                                campaign_type=content_type,
                                content=content['content']
                            )
                        
                        st.rerun()
                        
                    except json.JSONDecodeError:
                        st.error("Error parsing generated content. Please try again.")
                        
                except Exception as e:
                    st.error(f"Error generating content: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Right column - Generated content
    with col2:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown("<h2>Content Marketing Generator</h2>", unsafe_allow_html=True)
        
        if st.session_state.content_form_state.get('generated_content'):
            content = st.session_state.content_form_state['generated_content']
            st.success("Content generated successfully!")
            st.markdown(f"**Title:** {content['title']}")
            st.markdown("**Content:**")
            st.markdown(content['content'])
            
            if content.get('keywords'):
                st.markdown("**Keywords:**")
                st.markdown(", ".join(content['keywords']))
            
            if content.get('target_audience'):
                st.markdown("**Target Audience:**")
                st.markdown(content['target_audience'])
            
            # Export button
            st.download_button(
                "Export Content",
                content['content'],
                file_name=f"content_{content_type.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
        else:
            st.markdown('<p class="generated-content-placeholder">Generated content will appear here...</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_content_generator()
