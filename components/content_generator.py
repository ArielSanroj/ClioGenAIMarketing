import streamlit as st
from ai_utils import generate_marketing_content
from database import db
from emotion_engine import EmotionEngine, EmotionalProfile
from ai_system import EnhancedAISystem
import json
import html
import asyncio
from typing import Dict, Optional, Any

def generate_content_for_all_archetypes(story: str, content_type: str, platform: str, tone: str) -> Dict[str, Any]:
    """Generate content for all archetypes using enhanced AI system"""
    archetypes = {
        'autonomous': {
            'tone': 'professional and data-driven',
            'focus': 'efficiency and results',
            'style': 'detailed and analytical'
        },
        'impulsive': {
            'tone': 'urgent and emotional',
            'focus': 'immediate benefits',
            'style': 'dynamic and engaging'
        },
        'avoidant': {
            'tone': 'gentle and reassuring',
            'focus': 'comfort and simplicity',
            'style': 'clear and comforting'
        },
        'isolated': {
            'tone': 'respectful and private',
            'focus': 'independence and control',
            'style': 'detailed and personal'
        }
    }
    
    results = {}
    
    for archetype, traits in archetypes.items():
        try:
            # Create enhanced prompt with emotional intelligence
            prompt = f"""
            Story: {story}
            Content Type: {content_type}
            Platform: {platform}
            Base Tone: {tone}
            
            Archetype: {archetype}
            Archetype Tone: {traits['tone']}
            Content Focus: {traits['focus']}
            Writing Style: {traits['style']}
            """
            
            # Generate content using enhanced AI system
            content = st.session_state.ai_system.generate_content(
                story=prompt,
                archetype=archetype,
                content_type=content_type,
                platform=platform,
                tone=tone
            )
            
            if content.get('error'):
                results[archetype] = {
                    'error': content['error'],
                    'content': None
                }
                continue
            
            # Process the enhanced content
            processed_content = generate_marketing_content(prompt, content_type)
            processed_content['emotional_profile'] = content['emotional_profile']
            
            results[archetype] = processed_content
            
        except Exception as e:
            results[archetype] = {
                'error': str(e),
                'content': f"Error generating content for {archetype}"
            }
    
    return results

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
    if 'emotion_engine' not in st.session_state:
        st.session_state.emotion_engine = EmotionEngine()
    if 'ai_system' not in st.session_state:
        st.session_state.ai_system = EnhancedAISystem()

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
            padding: 40px !important;
        }
        .stApp { 
            background-color: #F9F9FB !important; 
        }
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding: 0 2rem;
        }
        .logo {
            width: 60px;
            height: auto;
        }
        .button-container {
            display: flex;
            gap: 1rem;
        }
        .nav-btn {
            background-color: #1E1B4B;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 500;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
        }
        .nav-btn:hover {
            background-color: #2D2A5C;
            transform: translateY(-1px);
        }
        .card-container {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
            height: 100%;
            margin-bottom: 2rem;
        }
        .label-text {
            color: #1E1B4B !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.75rem !important;
            display: block !important;
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: white !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            color: #1E1B4B !important;
            min-height: 150px !important;
            box-shadow: none !important;
            margin-bottom: 24px !important;
            transition: border-color 0.2s ease-in-out !important;
        }
        .stTextInput>div>div>input:hover, .stTextArea>div>div>textarea:hover {
            border-color: #1E1B4B !important;
        }
        .stSelectbox>div>div>div {
            background-color: white !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            color: #1E1B4B !important;
            height: 56px !important;
            margin-bottom: 24px !important;
            transition: border-color 0.2s ease-in-out !important;
        }
        .stSelectbox>div>div>div:hover {
            border-color: #1E1B4B !important;
        }
        .stButton>button {
            background-color: #1E1B4B !important;
            color: white !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 12px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease-in-out !important;
        }
        .stButton>button:hover {
            background-color: #2D2A5C !important;
            transform: translateY(-1px) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    initialize_session_state()

    # Header with logo and navigation buttons
    st.markdown('''
        <div class="header-container">
            <img src="logoclio.png" alt="Logo" class="logo">
            <div class="button-container">
                <button class="nav-btn" onclick="window.location.href='#'" id="new-chat-btn">New Chat</button>
                <button class="nav-btn" onclick="window.location.href='#'" id="go-back-btn">Go back</button>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Add button click handlers
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("New Chat", key="new_chat"):
            st.session_state.selected_option = "content"
            st.rerun()
    with col2:
        if st.button("Go back", key="go_back"):
            st.session_state.selected_option = "content"
            st.rerun()

    # Main content area with two columns
    col1, col2 = st.columns(2, gap="large")

    # Left column - Input form
    with col1:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        st.markdown('<p class="label-text">What would you like to talk about?</p>', unsafe_allow_html=True)
        story = st.text_area(
            "Story Input",
            value=st.session_state.content_form_state['story'],
            placeholder="What is the story you want to tell",
            label_visibility="collapsed"
        )

        st.markdown('<p class="label-text">Content Type</p>', unsafe_allow_html=True)
        content_type = st.selectbox(
            "Content Type",
            options=["", "Blog Post", "Social Media Post", "Email Newsletter", "Landing Page"],
            key="content_type",
            label_visibility="collapsed"
        )

        st.markdown('<p class="label-text">Platform</p>', unsafe_allow_html=True)
        platform = st.selectbox(
            "Platform",
            options=["", "Website", "LinkedIn", "Twitter", "Instagram", "Facebook"],
            key="platform",
            label_visibility="collapsed"
        )

        st.markdown('<p class="label-text">Emotional tone</p>', unsafe_allow_html=True)
        tone = st.selectbox(
            "Emotional tone",
            options=["", "Professional", "Casual", "Inspirational", "Educational", "Persuasive"],
            key="tone",
            label_visibility="collapsed"
        )

        st.markdown('<p class="label-text">Competitor Insights</p>', unsafe_allow_html=True)
        competitor_insights = st.text_area(
            "Competitor Insights",
            value=st.session_state.content_form_state['competitor_insights'],
            placeholder="Add any competitor insights or success strategies",
            label_visibility="collapsed"
        )
        
        if st.button("Generate Content"):
            if not story:
                st.error("Please enter a story to generate content.")
                return
                
            with st.spinner("Generating content..."):
                try:
                    # Generate content for all archetypes
                    all_content = generate_content_for_all_archetypes(
                        story=sanitize_input(story),
                        content_type=content_type,
                        platform=platform,
                        tone=tone
                    )
                    
                    st.session_state.content_form_state['generated_content'] = all_content
                    
                    # Save to database with proper error handling
                    for archetype, content in all_content.items():
                        if content and content.get('content'):
                            try:
                                db.save_campaign(
                                    business_name=f"{story[:50]}_{archetype}",
                                    campaign_type=content_type,
                                    content=content['content'],
                                    emotional_profile=content.get('emotional_profile', {})
                                )
                            except Exception as e:
                                st.warning(f"Could not save {archetype} content to database: {str(e)}")
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error generating content: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Right column - Display all generated content
    with col2:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown("<h2>Content Marketing Generator</h2>", unsafe_allow_html=True)
        
        if st.session_state.content_form_state.get('generated_content'):
            tabs = st.tabs([
                "Autonomous", "Impulsive", "Avoidant", "Isolated"
            ])
            
            archetypes = ["autonomous", "impulsive", "avoidant", "isolated"]
            
            for tab, archetype in zip(tabs, archetypes):
                with tab:
                    content = st.session_state.content_form_state['generated_content'].get(archetype, {})
                    if not content:
                        st.info(f"No content generated for {archetype} archetype yet.")
                        continue
                        
                    if content.get('error'):
                        st.error(content['error'])
                        continue
                        
                    # Display emotional profile
                    if content.get('emotional_profile'):
                        with st.expander("Emotional Analysis"):
                            st.write("Primary Emotion:", 
                                   content['emotional_profile']['primary_emotion'])
                            st.write("Emotional Intensity:", 
                                   f"{content['emotional_profile']['intensity']:.2f}")
                            st.write("Psychological Triggers:", 
                                   ", ".join(content['emotional_profile']['triggers']))
                    
                    # Display content sections
                    if content.get('title'):
                        st.markdown(f"### {content['title']}")
                        st.markdown("---")
                    
                    if content.get('content'):
                        st.markdown("### Content")
                        st.markdown(content['content'])
                        st.markdown("---")
                    
                    if content.get('keywords'):
                        st.markdown("### Keywords")
                        st.markdown(", ".join(content['keywords']))
                        st.markdown("---")
                    
                    if content.get('target_audience'):
                        st.markdown("### Target Audience")
                        st.markdown(content['target_audience'])
                    
                    # Download button for this archetype
                    if content.get('content'):
                        download_content = f"""
                        Archetype: {archetype.upper()}
                        
                        Title: {content.get('title', '')}
                        
                        Content:
                        {content.get('content', '')}
                        
                        Keywords:
                        {', '.join(content.get('keywords', []))}
                        
                        Target Audience:
                        {content.get('target_audience', '')}
                        
                        Emotional Analysis:
                        Primary Emotion: {content.get('emotional_profile', {}).get('primary_emotion', 'N/A')}
                        Emotional Intensity: {content.get('emotional_profile', {}).get('intensity', 'N/A')}
                        Psychological Triggers: {', '.join(content.get('emotional_profile', {}).get('triggers', []))}
                        """
                        
                        st.download_button(
                            f"Export {archetype.capitalize()} Content",
                            download_content,
                            file_name=f"{archetype}_{content.get('title', 'generated').lower().replace(' ', '_')}.txt",
                            mime="text/plain"
                        )
        else:
            st.markdown('<p class="generated-content-placeholder">Generated content will appear here...</p>', 
                       unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_content_generator()