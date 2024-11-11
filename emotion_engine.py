from typing import Dict, List, Optional
import numpy as np
from dataclasses import dataclass
import json

@dataclass
class EmotionalProfile:
    primary_emotion: str
    intensity: float
    secondary_emotions: List[str]
    psychological_triggers: List[str]
    content_tone: Dict[str, float]

class EmotionEngine:
    def __init__(self):
        # Initialize emotion vectors for different archetypes
        self.emotion_vectors = {
            'autonomous': np.array([0.8, 0.2, 0.1, 0.7]),  # Logic, Independence, Control, Achievement
            'impulsive': np.array([0.3, 0.9, 0.7, 0.2]),  # Excitement, Urgency, Desire, Spontaneity
            'isolative': np.array([0.6, 0.2, 0.8, 0.3]),  # Safety, Privacy, Comfort, Reflection
            'avoidant': np.array([0.2, 0.1, 0.9, 0.4])    # Security, Distance, Protection, Peace
        }
        
        # Psychological trigger mappings
        self.trigger_mappings = {
            'autonomous': [
                'achievement', 'control', 'efficiency', 'mastery',
                'independence', 'competence', 'growth', 'recognition'
            ],
            'impulsive': [
                'urgency', 'excitement', 'novelty', 'pleasure',
                'instant gratification', 'social proof', 'fomo', 'status'
            ],
            'isolative': [
                'safety', 'comfort', 'privacy', 'peace',
                'reflection', 'authenticity', 'simplicity', 'harmony'
            ],
            'avoidant': [
                'security', 'protection', 'stability', 'predictability',
                'certainty', 'familiarity', 'trust', 'reliability'
            ]
        }
        
        # Content tone mappings
        self.tone_mappings = {
            'autonomous': {
                'professional': 0.8,
                'authoritative': 0.7,
                'direct': 0.9,
                'analytical': 0.8
            },
            'impulsive': {
                'energetic': 0.9,
                'persuasive': 0.8,
                'urgent': 0.7,
                'exciting': 0.8
            },
            'isolative': {
                'calm': 0.8,
                'reassuring': 0.7,
                'authentic': 0.9,
                'empathetic': 0.6
            },
            'avoidant': {
                'gentle': 0.8,
                'supportive': 0.7,
                'non-threatening': 0.9,
                'encouraging': 0.6
            }
        }

    def analyze_emotional_context(self, 
                                archetype: str, 
                                brand_values: dict,
                                audience_data: dict) -> Optional[EmotionalProfile]:
        """
        Analyze emotional context based on archetype, brand values, and audience data
        """
        try:
            # Get base emotional vector for archetype
            base_vector = self.emotion_vectors.get(archetype.lower())
            if base_vector is None:
                return None

            # Calculate emotional intensity based on audience data
            intensity = self._calculate_emotional_intensity(base_vector, audience_data)
            
            # Get psychological triggers
            triggers = self._get_psychological_triggers(archetype, brand_values)
            
            # Get content tone mapping
            tone = self._get_content_tone(archetype, brand_values)
            
            # Get secondary emotions
            secondary_emotions = self._get_secondary_emotions(archetype, intensity)
            
            return EmotionalProfile(
                primary_emotion=archetype,
                intensity=intensity,
                secondary_emotions=secondary_emotions,
                psychological_triggers=triggers,
                content_tone=tone
            )
        except Exception as e:
            print(f"Error in emotional context analysis: {str(e)}")
            return None

    def _calculate_emotional_intensity(self, base_vector: np.ndarray, audience_data: dict) -> float:
        """Calculate emotional intensity based on audience data and base vector"""
        try:
            # Extract relevant metrics from audience data
            engagement = audience_data.get('engagement_rate', 0.5)
            sentiment = audience_data.get('sentiment_score', 0.5)
            
            # Calculate weighted intensity
            intensity = np.mean(base_vector) * engagement * sentiment
            return float(np.clip(intensity, 0.1, 1.0))
        except Exception:
            return 0.5

    def _get_psychological_triggers(self, archetype: str, brand_values: dict) -> List[str]:
        """Get psychological triggers based on archetype and brand values"""
        base_triggers = self.trigger_mappings.get(archetype.lower(), [])
        brand_keywords = brand_values.get('keywords', [])
        
        # Combine and prioritize triggers that align with brand values
        combined_triggers = []
        for trigger in base_triggers:
            if any(keyword in trigger for keyword in brand_keywords):
                combined_triggers.insert(0, trigger)
            else:
                combined_triggers.append(trigger)
        
        return combined_triggers[:5]  # Return top 5 most relevant triggers

    def _get_content_tone(self, archetype: str, brand_values: dict) -> Dict[str, float]:
        """Get content tone mapping based on archetype and brand values"""
        base_tone = self.tone_mappings.get(archetype.lower(), {})
        brand_tone = brand_values.get('tone', {})
        
        # Combine and adjust tone weights based on brand values
        combined_tone = base_tone.copy()
        for tone, weight in brand_tone.items():
            if tone in combined_tone:
                combined_tone[tone] = (combined_tone[tone] + float(weight)) / 2
        
        return combined_tone

    def _get_secondary_emotions(self, archetype: str, intensity: float) -> List[str]:
        """Get secondary emotions based on archetype and intensity"""
        emotion_sets = {
            'autonomous': ['confident', 'determined', 'focused', 'ambitious'],
            'impulsive': ['excited', 'passionate', 'energetic', 'enthusiastic'],
            'isolative': ['peaceful', 'content', 'mindful', 'balanced'],
            'avoidant': ['cautious', 'careful', 'measured', 'reserved']
        }
        
        base_emotions = emotion_sets.get(archetype.lower(), [])
        # Return more secondary emotions for higher intensity
        return base_emotions[:max(2, int(intensity * len(base_emotions)))]

    def optimize_content(self, content: str, emotional_profile: EmotionalProfile) -> str:
        """Optimize content based on emotional profile"""
        try:
            # Apply tone adjustments
            optimized_content = self._adjust_tone(content, emotional_profile.content_tone)
            
            # Insert psychological triggers
            optimized_content = self._insert_triggers(
                optimized_content, 
                emotional_profile.psychological_triggers
            )
            
            return optimized_content
        except Exception as e:
            print(f"Error in content optimization: {str(e)}")
            return content

    def _adjust_tone(self, content: str, tone_mapping: Dict[str, float]) -> str:
        """Adjust content tone based on tone mapping"""
        # This is a placeholder for tone adjustment logic
        # In a real implementation, this would use NLP to modify sentence structures
        return content

    def _insert_triggers(self, content: str, triggers: List[str]) -> str:
        """Insert psychological triggers into content"""
        # This is a placeholder for trigger insertion logic
        # In a real implementation, this would strategically place triggers
        return content
