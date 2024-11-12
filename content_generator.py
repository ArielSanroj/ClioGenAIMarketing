import streamlit as st
from ai_utils import generate_marketing_content
from database import db
from emotion_engine import EmotionEngine, EmotionalProfile, BehavioralPattern
from ai_system import EnhancedAISystem, ContentOrchestrator, PersonalizationEngine
from marketing_campaign_system import FeedbackLoop
import json
import html
import asyncio
from typing import Dict, Optional, Any
from datetime import datetime

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
    if 'content_orchestrator' not in st.session_state:
        st.session_state.content_orchestrator = ContentOrchestrator()
    if 'personalization_engine' not in st.session_state:
        st.session_state.personalization_engine = PersonalizationEngine({
            'model_config': {'temperature': 0.7},
            'optimization_config': {'real_time': True}
        })
    if 'feedback_loop' not in st.session_state:
        st.session_state.feedback_loop = FeedbackLoop()

async def generate_content_for_all_archetypes(story: str, content_type: str, platform: str, tone: str) -> Dict[str, Any]:
    """Generate content for all archetypes using enhanced AI system with emotional intelligence"""
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
    tasks = []
    
    for archetype, traits in archetypes.items():
        # Create behavioral pattern for each archetype
        behavioral_pattern = BehavioralPattern(
            interaction_history=[],
            engagement_scores={},
            conversion_points=[],
            attention_spans={},
            device_preferences={},
            time_sensitivity={},
            content_affinity={}
        )
        
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
        
        # Create task for async content generation
        task = st.session_state.content_orchestrator.create_campaign(
            target_profiles=[{
                'archetype': archetype,
                'behavioral_pattern': behavioral_pattern,
                'traits': traits
            }],
            campaign_objectives={
                'story': prompt,
                'content_type': content_type,
                'platform': platform,
                'tone': tone
            }
        )
        tasks.append((archetype, task))
    
    # Execute all tasks concurrently
    for archetype, task in tasks:
        try:
            campaign_result = await task
            
            if campaign_result.get('error'):
                results[archetype] = {
                    'error': campaign_result['error'],
                    'content': None
                }
                continue
            
            # Process and personalize content
            personalized_content = await st.session_state.personalization_engine.generate_personalized_content(
                user_profile={'archetype': archetype},
                context={'campaign': campaign_result},
                content_type=content_type
            )
            
            # Track performance metrics
            await st.session_state.feedback_loop.process_interaction({
                'archetype': archetype,
                'content_type': content_type,
                'platform': platform,
                'timestamp': datetime.utcnow(),
                'content': personalized_content
            })
            
            results[archetype] = {
                'content': personalized_content['content'],
                'emotional_profile': personalized_content['metadata']['emotional_context'],
                'behavioral_insights': personalized_content['metadata']['behavioral_insights'],
                'performance_metrics': personalized_content['metadata']['optimization_metrics']
            }
            
        except Exception as e:
            results[archetype] = {
                'error': str(e),
                'content': f"Error generating content for {archetype}"
            }
    
    return results

[Previous content_generator.py code continues from line 99 onwards...]
