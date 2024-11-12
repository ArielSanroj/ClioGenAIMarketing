from typing import Dict, List, Optional, Any
import numpy as np
from dataclasses import dataclass
from datetime import datetime
import asyncio
from emotion_engine import EmotionEngine, EmotionalProfile, BehavioralPattern

@dataclass
class ContentStrategy:
    tone_of_voice: str
    key_messages: List[str]
    emotional_triggers: List[str]
    content_structure: Dict[str, Any]
    distribution_channels: List[str]
    performance_metrics: Optional[Dict[str, float]] = None
    behavioral_insights: Optional[Dict[str, Any]] = None

class ChannelOptimizer:
    """Optimizes content delivery across multiple channels"""
    
    def __init__(self):
        self.channel_performance = {}
        self.audience_preferences = {}
    
    async def get_optimal_channels(self, profile: Dict[str, Any]) -> List[tuple]:
        """Get optimal channels for content delivery"""
        return [
            ('social_media', 'text'),
            ('email', 'text'),
            ('website', 'text')
        ]
    
    async def create_strategy(self, profile: Dict[str, Any], content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create optimal delivery strategy"""
        return {
            'channels': await self.get_optimal_channels(profile),
            'timing': self._get_optimal_timing(profile),
            'frequency': self._get_optimal_frequency(profile)
        }
    
    def _get_optimal_timing(self, profile: Dict[str, Any]) -> Dict[str, List[datetime]]:
        """Calculate optimal timing for content delivery"""
        return {'best_times': [datetime.utcnow()]}
    
    def _get_optimal_frequency(self, profile: Dict[str, Any]) -> Dict[str, float]:
        """Calculate optimal posting frequency"""
        return {'posts_per_day': 2.0}

class ContentOrchestrator:
    """Orchestrates content generation and delivery across channels"""
    
    def __init__(self):
        self.emotion_engine = EmotionEngine()
        self.channel_optimizer = ChannelOptimizer()
        self.performance_cache = {}
    
    async def create_campaign(
        self,
        target_profiles: List[Dict[str, Any]],
        campaign_objectives: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a multi-channel personalized campaign"""
        try:
            campaigns = []
            
            for profile in target_profiles:
                # Get emotional profile
                emotional_profile = self.emotion_engine.analyze_emotional_context(
                    archetype=profile['archetype'],
                    brand_values=campaign_objectives.get('brand_values', {}),
                    audience_data=profile
                )
                
                # Get optimal channels
                channels = await self.channel_optimizer.get_optimal_channels(profile)
                
                # Generate content for each channel
                channel_content = await asyncio.gather(*[
                    self._generate_channel_content(
                        profile=profile,
                        emotional_profile=emotional_profile,
                        channel=channel,
                        content_type=content_type,
                        objectives=campaign_objectives
                    )
                    for channel, content_type in channels
                ])
                
                campaigns.append({
                    'profile': profile,
                    'content': channel_content,
                    'delivery_strategy': await self.channel_optimizer.create_strategy(
                        profile, channel_content
                    )
                })
            
            return {
                'campaigns': campaigns,
                'metadata': {
                    'optimization_metrics': await self._aggregate_optimization_metrics(campaigns),
                    'emotional_resonance': self._calculate_emotional_resonance(campaigns),
                    'behavioral_patterns': self._extract_behavioral_patterns(campaigns)
                }
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _generate_channel_content(
        self,
        profile: Dict[str, Any],
        emotional_profile: EmotionalProfile,
        channel: str,
        content_type: str,
        objectives: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate content for specific channel"""
        try:
            content = await self._generate_base_content(
                profile, emotional_profile, objectives
            )
            
            optimized_content = self.emotion_engine.optimize_content(
                content=content,
                emotional_profile=emotional_profile
            )
            
            return {
                'channel': channel,
                'content': optimized_content,
                'emotional_profile': {
                    'primary_emotion': emotional_profile.primary_emotion,
                    'intensity': emotional_profile.intensity,
                    'triggers': emotional_profile.psychological_triggers
                }
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _generate_base_content(
        self,
        profile: Dict[str, Any],
        emotional_profile: EmotionalProfile,
        objectives: Dict[str, Any]
    ) -> str:
        """Generate base content with emotional intelligence"""
        story = objectives.get('story', '')
        return story  # This would typically call OpenAI API
    
    async def _aggregate_optimization_metrics(
        self,
        campaigns: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Aggregate optimization metrics across campaigns"""
        return {
            'emotional_resonance': np.mean([
                self._calculate_campaign_resonance(c)
                for c in campaigns
            ]),
            'behavioral_alignment': np.mean([
                self._calculate_behavioral_alignment(c)
                for c in campaigns
            ])
        }
    
    def _calculate_emotional_resonance(
        self,
        campaigns: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate emotional resonance scores"""
        return {
            'overall_resonance': np.mean([
                self._calculate_campaign_resonance(c)
                for c in campaigns
            ])
        }
    
    def _calculate_campaign_resonance(self, campaign: Dict[str, Any]) -> float:
        """Calculate resonance score for a single campaign"""
        return 0.8  # Placeholder for actual calculation
    
    def _calculate_behavioral_alignment(self, campaign: Dict[str, Any]) -> float:
        """Calculate behavioral alignment score"""
        return 0.7  # Placeholder for actual calculation
    
    def _extract_behavioral_patterns(
        self,
        campaigns: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Extract behavioral patterns from campaigns"""
        return {
            'engagement_patterns': self._analyze_engagement_patterns(campaigns),
            'conversion_patterns': self._analyze_conversion_patterns(campaigns)
        }
    
    def _analyze_engagement_patterns(
        self,
        campaigns: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze engagement patterns"""
        return {'average_engagement': 0.75}  # Placeholder
    
    def _analyze_conversion_patterns(
        self,
        campaigns: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze conversion patterns"""
        return {'average_conversion': 0.25}  # Placeholder

class EnhancedAISystem:
    def __init__(self):
        self.emotion_engine = EmotionEngine()
        self.content_cache = {}
        self.content_orchestrator = ContentOrchestrator()
        
    async def generate_content(self,
                             story: str,
                             archetype: str,
                             content_type: str,
                             platform: str,
                             tone: str) -> Dict[str, Any]:
        """Generate content with emotional intelligence"""
        try:
            # Get emotional profile
            emotional_profile = self.emotion_engine.analyze_emotional_context(
                archetype=archetype,
                brand_values={},  # Get from session state
                audience_data={'archetype': archetype}
            )
            
            if not emotional_profile:
                raise ValueError(f"Could not generate emotional profile for {archetype}")
            
            # Create content strategy
            strategy = self._create_content_strategy(
                archetype=archetype,
                emotional_profile=emotional_profile,
                content_type=content_type,
                platform=platform,
                tone=tone
            )
            
            # Generate base content
            content = self._generate_base_content(
                story=story,
                strategy=strategy,
                emotional_profile=emotional_profile
            )
            
            # Optimize content
            optimized_content = self.emotion_engine.optimize_content(
                content=content,
                emotional_profile=emotional_profile
            )
            
            return {
                'content': optimized_content,
                'emotional_profile': {
                    'primary_emotion': emotional_profile.primary_emotion,
                    'intensity': emotional_profile.intensity,
                    'triggers': emotional_profile.psychological_triggers,
                    'tone': emotional_profile.content_tone
                },
                'strategy': strategy
            }
            
        except Exception as e:
            print(f"Error in enhanced content generation: {str(e)}")
            return {
                'error': str(e),
                'content': None,
                'emotional_profile': None,
                'strategy': None
            }
    
    def _create_content_strategy(self,
                               archetype: str,
                               emotional_profile: EmotionalProfile,
                               content_type: str,
                               platform: str,
                               tone: str) -> ContentStrategy:
        """Create a content strategy based on emotional profile"""
        return ContentStrategy(
            tone_of_voice=tone,
            key_messages=self._extract_key_messages(emotional_profile),
            emotional_triggers=emotional_profile.psychological_triggers,
            content_structure=self._get_content_structure(content_type, platform),
            distribution_channels=[platform]
        )
    
    def _extract_key_messages(self, profile: EmotionalProfile) -> List[str]:
        """Extract key messages based on emotional profile"""
        base_messages = {
            'autonomous': [
                'Efficiency and results',
                'Professional excellence',
                'Strategic advantage'
            ],
            'impulsive': [
                'Immediate benefits',
                'Exciting opportunities',
                'Limited time offers'
            ],
            'avoidant': [
                'Safety and security',
                'Peace of mind',
                'Reliable solutions'
            ],
            'isolated': [
                'Personal control',
                'Privacy protection',
                'Independent decision-making'
            ]
        }
        
        return base_messages.get(profile.primary_emotion.lower(), [])
    
    def _get_content_structure(self, content_type: str, platform: str) -> Dict[str, Any]:
        """Get content structure based on type and platform"""
        structures = {
            'Blog Post': {
                'sections': ['intro', 'main_points', 'examples', 'conclusion'],
                'word_count': 1000,
                'tone': 'informative'
            },
            'Social Media Post': {
                'sections': ['hook', 'value_prop', 'cta'],
                'word_count': 280,
                'tone': 'engaging'
            },
            'Email Newsletter': {
                'sections': ['subject', 'greeting', 'body', 'cta', 'signature'],
                'word_count': 500,
                'tone': 'personal'
            }
        }
        
        return structures.get(content_type, {})
    
    async def _generate_base_content(self,
                             story: str,
                             strategy: ContentStrategy,
                             emotional_profile: EmotionalProfile) -> str:
        """Generate base content using the strategy and emotional profile"""
        # This would typically call the OpenAI API with the enhanced prompt
        # For now, return a placeholder
        return story