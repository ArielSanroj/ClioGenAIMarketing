import streamlit as st
from ai_utils import generate_marketing_content
from database import db
from emotion_engine import EmotionEngine, EmotionalProfile
import json
import html
import asyncio
from typing import Dict, Optional, Any

class ContentTemplate:
    def __init__(self, archetype: str, tone: str):
        self.archetype = archetype
        self.tone = tone
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """Load content templates based on archetype and tone"""
        return {
            'blog_post': """
            Title: {title}
            
            {introduction}
            
            {main_points}
            
            {conclusion}
            
            Keywords: {keywords}
            Target Audience: {target_audience}
            """,
            'social_post': """
            {headline}
            
            {main_message}
            
            {call_to_action}
            
            {hashtags}
            """,
            'email': """
            Subject: {subject}
            
            {greeting}
            
            {body}
            
            {closing}
            
            {signature}
            """
        }

    def get_template(self, content_type: str) -> str:
        """Get template for specific content type"""
        return self.templates.get(content_type, self.templates['blog_post'])

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'content_form_state' not in st.session_state:
        st.session_state.content_form_state = {
            'story': '',
            'content_type': '',
            'platform': '',
            'tone': '',
            'competitor_insights': '',
            'generated_content': None,
            'performance_metrics': None
        }
    if 'emotion_engine' not in st.session_state:
        st.session_state.emotion_engine = EmotionEngine()

def sanitize_input(text: str) -> str:
    """Sanitize input text to prevent injection and formatting issues"""
    if not text:
        return ""
    sanitized = html.escape(text.strip())
    return ' '.join(sanitized.split())

async def generate_content_async(prompt: str, content_type: str, 
                               emotion_engine: EmotionEngine, 
                               brand_values: dict,
                               audience_data: dict) -> Dict[str, Any]:
    """Generate content asynchronously with emotional optimization"""
    try:
        # Get emotional profile
        emotional_profile = emotion_engine.analyze_emotional_context(
            archetype=audience_data.get('archetype', 'autonomous'),
            brand_values=brand_values,
            audience_data=audience_data
        )
        
        # Generate base content
        content = generate_marketing_content(prompt, content_type)
        
        # Optimize content if emotional profile is available
        if emotional_profile and content.get('content'):
            content['content'] = emotion_engine.optimize_content(
                content['content'],
                emotional_profile
            )
            content['emotional_profile'] = {
                'primary_emotion': emotional_profile.primary_emotion,
                'intensity': emotional_profile.intensity,
                'triggers': emotional_profile.psychological_triggers
            }
        
        return content
    except Exception as e:
        print(f"Error in async content generation: {str(e)}")
        return {
            "error": str(e),
            "title": "Error generating content",
            "content": "An error occurred during content generation.",
            "keywords": [],
            "target_audience": ""
        }

def render_content_generator():
    # Apply custom styles
    st.markdown("""
        <style>
        .main { background-color: #F9F9FB !important; padding-top: 40px !important; }
        .stApp { background-color: #F9F9FB !important; }
        .card-container {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
            height: 100%;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    initialize_session_state()

    # Header with logo
    col1, col2 = st.columns([1, 11])
    with col1:
        st.image("logoclio.png", width=60)
    
    # Main content area with two columns
    col1, col2 = st.columns(2, gap="large")

    # Left column - Input form
    with col1:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        # Form inputs
        story = st.text_area(
            "What would you like to talk about?",
            value=st.session_state.content_form_state['story'],
            placeholder="What is the story you want to tell",
            key="story_input"
        )

        content_type = st.selectbox(
            "Content Type",
            options=["", "Blog Post", "Social Media Post", "Email Newsletter", "Landing Page"],
            key="content_type"
        )

        platform = st.selectbox(
            "Platform",
            options=["", "Website", "LinkedIn", "Twitter", "Instagram", "Facebook"],
            key="platform"
        )

        tone = st.selectbox(
            "Emotional tone",
            options=["", "Professional", "Casual", "Inspirational", "Educational", "Persuasive"],
            key="tone"
        )

        competitor_insights = st.text_area(
            "Competitor Insights",
            value=st.session_state.content_form_state['competitor_insights'],
            placeholder="Add any competitor insights or success strategies",
            key="competitor_insights"
        )
        
        if st.button("Generate Content"):
            # Validate inputs
            if not story.strip():
                st.error("Please enter a story to generate content.")
                return
                
            # Update session state
            st.session_state.content_form_state.update({
                'story': sanitize_input(story),
                'content_type': content_type,
                'platform': platform,
                'tone': tone,
                'competitor_insights': sanitize_input(competitor_insights)
            })
            
            with st.spinner("Generating content..."):
                try:
                    # Prepare the prompt
                    prompt = f"""
                    Story: {st.session_state.content_form_state['story']}
                    Content Type: {content_type}
                    Platform: {platform}
                    Tone: {tone}
                    Competitor Insights: {st.session_state.content_form_state['competitor_insights']}
                    """
                    
                    # Add brand values and ICP data if available
                    brand_values = getattr(st.session_state, 'brand_values', {})
                    icp_data = getattr(st.session_state, 'icp_data', {})
                    
                    # Generate content asynchronously
                    content = asyncio.run(generate_content_async(
                        prompt=prompt,
                        content_type=content_type,
                        emotion_engine=st.session_state.emotion_engine,
                        brand_values=brand_values,
                        audience_data=icp_data
                    ))
                    
                    st.session_state.content_form_state['generated_content'] = content
                    
                    # Save to database if content was generated successfully
                    if content and content.get('content'):
                        db.save_campaign(
                            business_name=st.session_state.content_form_state['story'][:50],
                            campaign_type=content_type,
                            content=content['content'],
                            emotional_profile=content.get('emotional_profile', {})
                        )
                    
                    st.rerun()
                    
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
            
            # Display emotional profile if available
            if content.get('emotional_profile'):
                with st.expander("Emotional Analysis"):
                    st.write("Primary Emotion:", content['emotional_profile']['primary_emotion'])
                    st.write("Emotional Intensity:", f"{content['emotional_profile']['intensity']:.2f}")
                    st.write("Psychological Triggers:", ", ".join(content['emotional_profile']['triggers']))
            
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
            
            # Download button
            if content.get('content'):
                download_content = f"""
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
                    "Export Content",
                    download_content,
                    file_name=f"content_{content.get('title', 'generated').lower().replace(' ', '_')}.txt",
                    mime="text/plain"
                )
        else:
            st.markdown('<p class="generated-content-placeholder">Generated content will appear here...</p>', 
                       unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_content_generator()
