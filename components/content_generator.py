import streamlit as st
from ai_utils import generate_marketing_content
from database import db
from emotion_engine import EmotionEngine, EmotionalProfile
import json
import html
import asyncio
from typing import Dict, Optional, Any, List

# Define archetype behaviors with detailed attributes
archetype_behaviors = {
    'autonomous': {
        'platforms': ['LinkedIn', 'Twitter', 'Medium'],
        'content_focus': 'Efficiency, performance, and professional growth',
        'preferred_tone': 'Professional and data-driven',
        'engagement_time': '8am-11am'
    },
    'impulsive': {
        'platforms': ['Instagram', 'TikTok', 'Facebook'],
        'content_focus': 'Urgency, excitement, and instant gratification',
        'preferred_tone': 'Dynamic and engaging',
        'engagement_time': '7pm-10pm'
    },
    'avoidant': {
        'platforms': ['YouTube', 'Pinterest', 'Instagram'],
        'content_focus': 'Relaxation, simplicity, and emotional connection',
        'preferred_tone': 'Gentle and reassuring',
        'engagement_time': '6pm-9pm'
    },
    'isolated': {
        'platforms': ['Email', 'LinkedIn', 'Reddit'],
        'content_focus': 'Privacy, autonomy, and introspection',
        'preferred_tone': 'Respectful and private',
        'engagement_time': '9am-12pm'
    }
}

# Define platform-specific recommendations with details
platform_recommendations = {
    'LinkedIn': {
        'best_for': 'Professional audiences and B2B marketing',
        'content_tips': 'Share case studies, ROI-focused reports, and industry insights.',
        'engagement_tips': 'Post during weekdays, especially mornings.'
    },
    'Twitter': {
        'best_for': 'Real-time updates and thought leadership',
        'content_tips': 'Use concise, impactful posts with trending hashtags.',
        'engagement_tips': 'Engage in conversations and share breaking news.'
    },
    'Medium': {
        'best_for': 'Long-form content and storytelling',
        'content_tips': 'Publish in-depth articles and thought pieces.',
        'engagement_tips': 'Focus on niche topics and use strategic tagging.'
    },
    'Instagram': {
        'best_for': 'Visual storytelling and brand awareness',
        'content_tips': 'Leverage vibrant visuals, stories, and short videos.',
        'engagement_tips': 'Use interactive features like polls and reels.'
    },
    'TikTok': {
        'best_for': 'Short, engaging video content for younger audiences',
        'content_tips': 'Create trends, challenges, and entertaining clips.',
        'engagement_tips': 'Post frequently and follow platform trends.'
    },
    'Facebook': {
        'best_for': 'Community building and wide audience reach',
        'content_tips': 'Share relatable stories, events, and group-driven content.',
        'engagement_tips': 'Focus on visuals and short captions.'
    },
    'YouTube': {
        'best_for': 'Longer video content and tutorials',
        'content_tips': 'Create explainer videos, behind-the-scenes, and educational content.',
        'engagement_tips': 'Post consistently and use attention-grabbing thumbnails.'
    },
    'Pinterest': {
        'best_for': 'Inspirational and lifestyle-focused content',
        'content_tips': 'Share visually appealing pins with actionable ideas.',
        'engagement_tips': 'Focus on keywords and seasonal trends.'
    },
    'Email': {
        'best_for': 'Direct and personalized communication',
        'content_tips': 'Use clear CTAs and segmented campaigns for personalization.',
        'engagement_tips': 'Send during mid-week mornings for higher open rates.'
    },
    'Reddit': {
        'best_for': 'Niche communities and in-depth discussions',
        'content_tips': 'Participate in relevant subreddits and offer value-driven content.',
        'engagement_tips': 'Engage genuinely and avoid overt promotion.'
    }
}


# Archetype-specific content templates
TEMPLATES = {
    'autonomous': "Highlight efficiency and results with data-driven visuals.",
    'impulsive': "Focus on urgency with dynamic calls-to-action.",
    'avoidant': "Emphasize comfort and simplicity with reassuring messages.",
    'isolated': "Promote independence and control with private solutions."
}

def generate_content_for_all_archetypes(story: str, content_type: str, platform: str, tone: str) -> Dict[str, Any]:
    """Generate content for all archetypes simultaneously"""
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

            for platform in archetype_behaviors[archetype]['platforms']:
                recommended_content = platform_recommendations[platform]
                
            # Retrieve template for the archetype
            template = TEMPLATES.get(archetype, "No specific template available.")

            # Create prompt for this archetype
            prompt = f"""
            Story: {story}
            Content Type: {content_type}
            Platform: {platform}
            Base Tone: {tone}

            Archetype: {archetype}
            Archetype Tone: {traits['tone']}
            Content Focus: {traits['focus']}
            Writing Style: {traits['style']}
            Template Guidance: {template}
            """

            # Generate content with proper error handling
            try:
                content = generate_marketing_content(prompt, content_type)
            except Exception as e:
                content = {
                    'error': f"Content generation error: {str(e)}",
                    'title': f"Error - {archetype}",
                    'content': None,
                    'keywords': [],
                    'target_audience': ''
                }

            # Get emotional profile with proper error handling
            try:
                emotional_profile = st.session_state.emotion_engine.analyze_emotional_context(
                    archetype=archetype,
                    brand_values=getattr(st.session_state, 'brand_values', {}),
                    audience_data={'archetype': archetype}
                )

                if emotional_profile:
                    content['emotional_profile'] = {
                        'primary_emotion': emotional_profile.primary_emotion,
                        'intensity': emotional_profile.intensity,
                        'triggers': emotional_profile.psychological_triggers
                    }
            except Exception as e:
                content['emotional_profile'] = {
                    'primary_emotion': archetype,
                    'intensity': 0.5,
                    'triggers': []
                }

            results[archetype] = content

        except Exception as e:
            results[archetype] = {
                'error': f"Error processing {archetype}: {str(e)}",
                'content': None,
                'emotional_profile': None
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
        .go-back-btn {
            background-color: #1E1B4B;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.2s ease-in-out;
        }
        .go-back-btn:hover {
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
        .stSelectbox [data-baseweb="select"] {
            height: 56px !important;
            background-color: white !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            margin-bottom: 1.5rem;
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 0.75rem 1.25rem;
            border-radius: 8px;
            background-color: #F3F4F6;
            color: #4B5563;
            font-weight: 500;
            border: none;
            transition: all 0.2s ease-in-out;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1E1B4B !important;
            color: white !important;
        }
        .stButton>button {
            background-color: #1E1B4B !important;
            color: white !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 12px !important;
            font-weight: 500 !important;
            width: 100% !important;
            height: 56px !important;
            margin-top: 1rem !important;
            transition: all 0.2s ease-in-out !important;
        }
        .stButton>button:hover {
            background-color: #2D2A5C !important;
            transform: translateY(-1px) !important;
        }
        .generated-content-placeholder {
            color: #6B7280 !important;
            font-style: italic !important;
            text-align: center !important;
            margin-top: 2rem !important;
        }
        h2 {
            color: #1E1B4B !important;
            font-size: 24px !important;
            font-weight: 600 !important;
            margin-bottom: 1.5rem !important;
        }
        ::placeholder {
            color: #6B7280 !important;
            opacity: 1 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    initialize_session_state()

    # Header with logo and go back button
    st.markdown("""
        <div class="header-container">
            <img src="assets/logoclio.png" alt="Logo" class="logo">
            <a href="#" class="go-back-btn">Go back</a>
        </div>
    """, unsafe_allow_html=True)
    
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
                
            with st.spinner("Generating content for all archetypes..."):
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
