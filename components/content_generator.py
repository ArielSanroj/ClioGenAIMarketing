import streamlit as st
from ai_utils import generate_marketing_content
from database import db
import json

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'content_form_state' not in st.session_state:
        st.session_state.content_form_state = {
            'story': '',
            'content_type': 'Blog Post',
            'platform': 'Website',
            'tone': 'Professional',
            'competitor_insights': '',
            'generated_content': None
        }

def render_content_generator():
    # Apply custom styles
    st.markdown("""
        <style>
        .main {
            background-color: #F9F9FB;
            padding: 2rem;
        }
        .card-container {
            background-color: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            height: 100%;
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: white !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
            font-size: 1rem !important;
            color: #1E1B4B !important;
        }
        .stSelectbox>div>div>div {
            background-color: white !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
            color: #1E1B4B !important;
        }
        .stButton>button {
            border-radius: 8px !important;
            padding: 0.75rem 1.5rem !important;
            background-color: #1E1B4B !important;
            color: white !important;
            font-weight: 500 !important;
            border: none !important;
            transition: all 0.2s !important;
            margin-top: 1rem !important;
        }
        .stButton>button:hover {
            background-color: #2D2A5C !important;
            transform: translateY(-1px) !important;
        }
        .go-back {
            position: absolute;
            top: 2rem;
            right: 2rem;
        }
        h1, h2, h3 {
            color: #1E1B4B !important;
            font-weight: 600 !important;
            margin-bottom: 1.5rem !important;
        }
        .label-text {
            color: #1E1B4B !important;
            font-weight: 500 !important;
            margin-bottom: 0.5rem !important;
            font-size: 1rem !important;
        }
        .output-container {
            background-color: white;
            border-radius: 12px;
            padding: 2rem;
            height: calc(100vh - 12rem);
            overflow-y: auto;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    initialize_session_state()

    # Header with logo
    col1, col2 = st.columns([1, 11])
    with col1:
        st.image("logoclio.png", width=60)
    
    # Go back button
    st.markdown(
        """
        <div class="go-back">
            <button class="stButton" onclick="window.history.back()">Go back</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Main content area with two columns
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        st.markdown('<p class="label-text">What would you like to talk about?</p>', unsafe_allow_html=True)
        story = st.text_area(
            "",
            value=st.session_state.content_form_state['story'],
            placeholder="What is the story you want to tell",
            label_visibility="collapsed",
            height=100
        )

        st.markdown('<p class="label-text">Content Type</p>', unsafe_allow_html=True)
        content_type = st.selectbox(
            "",
            options=["Blog Post", "Social Media Post", "Email Newsletter", "Landing Page"],
            key="content_type",
            label_visibility="collapsed"
        )

        st.markdown('<p class="label-text">Platform</p>', unsafe_allow_html=True)
        platform = st.selectbox(
            "",
            options=["Website", "LinkedIn", "Twitter", "Instagram", "Facebook"],
            key="platform",
            label_visibility="collapsed"
        )

        st.markdown('<p class="label-text">Emotional tone</p>', unsafe_allow_html=True)
        tone = st.selectbox(
            "",
            options=["Professional", "Casual", "Inspirational", "Educational", "Persuasive"],
            key="tone",
            label_visibility="collapsed"
        )

        st.markdown('<p class="label-text">Competitor Insights</p>', unsafe_allow_html=True)
        competitor_insights = st.text_area(
            "",
            value=st.session_state.content_form_state['competitor_insights'],
            placeholder="Add any competitor insights or success strategies",
            label_visibility="collapsed",
            height=120
        )
        
        # Generate button at the bottom of the form
        if st.button("Generate Content", type="primary"):
            st.session_state.content_form_state.update({
                'story': story,
                'content_type': content_type,
                'platform': platform,
                'tone': tone,
                'competitor_insights': competitor_insights
            })
            
            with st.spinner("Generating content..."):
                try:
                    prompt = f"""
                    Story: {story}
                    Content Type: {content_type}
                    Platform: {platform}
                    Tone: {tone}
                    Competitor Insights: {competitor_insights}
                    Brand Values: {json.dumps(st.session_state.brand_values)}
                    ICP Data: {json.dumps(st.session_state.icp_data)}
                    """
                    
                    content = generate_marketing_content(prompt, content_type)
                    st.session_state.content_form_state['generated_content'] = content
                    
                    # Save to database
                    db.save_campaign(
                        business_name=story[:50],
                        campaign_type=content_type,
                        content=content['content']
                    )
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error generating content: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown("<h2>Content Marketing Generator</h2>", unsafe_allow_html=True)
        
        if st.session_state.content_form_state.get('generated_content'):
            content = st.session_state.content_form_state['generated_content']
            st.success("Content generated successfully!")
            st.markdown(f"**Title:** {content['title']}")
            st.markdown("**Content:**")
            st.markdown(content['content'])
            
            # Export button
            st.download_button(
                "Export Content",
                content['content'],
                file_name=f"content_{st.session_state.content_form_state['content_type'].lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
        else:
            st.markdown("Generated content will appear here...")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_content_generator()
