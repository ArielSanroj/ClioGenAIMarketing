from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
import asyncio
from emotion_engine import EmotionEngine, EmotionalProfile

@dataclass
class MarketingGoal:
    name: str
    target_metrics: Dict[str, float]
    current_metrics: Dict[str, float] = None
    deadline: datetime = None
    status: str = "pending"

@dataclass
class BuyerPersona:
    name: str
    demographics: Dict[str, str]
    interests: List[str]
    pain_points: List[str]
    preferred_channels: List[str]
    archetype: str
    emotional_profile: Optional[EmotionalProfile] = None

@dataclass
class ContentPiece:
    title: str
    content_type: str
    target_persona: str
    emotional_tone: str
    keywords: List[str]
    content_body: str
    created_at: datetime
    emotional_profile: Optional[Dict] = None
    performance_metrics: Optional[Dict[str, float]] = None
    engagement_data: Optional[Dict[str, Any]] = None

class MarketingCampaignSystem:
    def __init__(self):
        self.emotion_engine = EmotionEngine()
        self.goals: List[MarketingGoal] = []
        self.buyer_personas: List[BuyerPersona] = []
        self.content_pieces: List[ContentPiece] = []
        self.performance_history: List[Dict] = []

    async def create_campaign(self, 
                            name: str,
                            goals: List[MarketingGoal],
                            personas: List[BuyerPersona],
                            brand_values: Dict) -> Dict:
        """Create a new marketing campaign with emotional intelligence"""
        try:
            campaign_data = {
                'name': name,
                'created_at': datetime.utcnow(),
                'goals': goals,
                'content_pieces': [],
                'performance_metrics': {},
                'emotional_insights': {}
            }

            # Process each persona
            for persona in personas:
                # Analyze emotional context
                emotional_profile = self.emotion_engine.analyze_emotional_context(
                    archetype=persona.archetype,
                    brand_values=brand_values,
                    audience_data={'demographics': persona.demographics}
                )
                
                if emotional_profile:
                    persona.emotional_profile = emotional_profile
                    campaign_data['emotional_insights'][persona.name] = {
                        'primary_emotion': emotional_profile.primary_emotion,
                        'triggers': emotional_profile.psychological_triggers,
                        'content_tone': emotional_profile.content_tone
                    }

            self.buyer_personas.extend(personas)
            return campaign_data

        except Exception as e:
            print(f"Error creating campaign: {str(e)}")
            return {'error': str(e)}

    async def generate_campaign_content(self, 
                                     campaign_data: Dict,
                                     content_types: List[str]) -> List[ContentPiece]:
        """Generate content for campaign asynchronously"""
        try:
            content_pieces = []
            tasks = []

            for persona in self.buyer_personas:
                for content_type in content_types:
                    task = self._generate_content_piece(
                        persona=persona,
                        content_type=content_type,
                        campaign_data=campaign_data
                    )
                    tasks.append(task)

            # Execute content generation tasks concurrently
            results = await asyncio.gather(*tasks)
            content_pieces.extend([r for r in results if r is not None])
            
            self.content_pieces.extend(content_pieces)
            return content_pieces

        except Exception as e:
            print(f"Error generating campaign content: {str(e)}")
            return []

    async def _generate_content_piece(self,
                                    persona: BuyerPersona,
                                    content_type: str,
                                    campaign_data: Dict) -> Optional[ContentPiece]:
        """Generate a single content piece with emotional optimization"""
        try:
            # Generate content using emotion engine
            emotional_profile = persona.emotional_profile
            if not emotional_profile:
                return None

            # Create content piece
            content_piece = ContentPiece(
                title=f"{content_type} for {persona.name}",
                content_type=content_type,
                target_persona=persona.name,
                emotional_tone=list(emotional_profile.content_tone.keys())[0],
                keywords=[],  # To be filled by content generation
                content_body="",  # To be filled by content generation
                created_at=datetime.utcnow(),
                emotional_profile={
                    'primary_emotion': emotional_profile.primary_emotion,
                    'intensity': emotional_profile.intensity,
                    'triggers': emotional_profile.psychological_triggers
                }
            )

            return content_piece

        except Exception as e:
            print(f"Error generating content piece: {str(e)}")
            return None

    async def track_campaign_performance(self, campaign_id: str) -> Dict:
        """Track campaign performance metrics"""
        try:
            performance_metrics = {
                'engagement_rate': self._calculate_engagement_rate(),
                'conversion_rate': self._calculate_conversion_rate(),
                'emotional_resonance': self._calculate_emotional_resonance(),
                'content_performance': self._analyze_content_performance()
            }

            self.performance_history.append({
                'timestamp': datetime.utcnow(),
                'metrics': performance_metrics
            })

            return performance_metrics

        except Exception as e:
            print(f"Error tracking campaign performance: {str(e)}")
            return {}

    def _calculate_engagement_rate(self) -> float:
        """Calculate overall engagement rate"""
        if not self.content_pieces:
            return 0.0
        
        total_engagement = sum(
            piece.performance_metrics.get('engagement_rate', 0)
            for piece in self.content_pieces
            if piece.performance_metrics
        )
        return total_engagement / len(self.content_pieces)

    def _calculate_conversion_rate(self) -> float:
        """Calculate overall conversion rate"""
        if not self.content_pieces:
            return 0.0
        
        total_conversion = sum(
            piece.performance_metrics.get('conversion_rate', 0)
            for piece in self.content_pieces
            if piece.performance_metrics
        )
        return total_conversion / len(self.content_pieces)

    def _calculate_emotional_resonance(self) -> Dict:
        """Calculate emotional resonance scores"""
        resonance_scores = {}
        for piece in self.content_pieces:
            if piece.emotional_profile and piece.performance_metrics:
                emotion = piece.emotional_profile['primary_emotion']
                score = piece.performance_metrics.get('engagement_rate', 0) * \
                       piece.emotional_profile.get('intensity', 1.0)
                resonance_scores[emotion] = resonance_scores.get(emotion, 0) + score
        return resonance_scores

    def _analyze_content_performance(self) -> Dict:
        """Analyze performance of different content types"""
        performance_by_type = {}
        for piece in self.content_pieces:
            if piece.performance_metrics:
                content_type = piece.content_type
                if content_type not in performance_by_type:
                    performance_by_type[content_type] = {
                        'count': 0,
                        'total_engagement': 0,
                        'total_conversion': 0
                    }
                
                metrics = piece.performance_metrics
                performance_by_type[content_type]['count'] += 1
                performance_by_type[content_type]['total_engagement'] += \
                    metrics.get('engagement_rate', 0)
                performance_by_type[content_type]['total_conversion'] += \
                    metrics.get('conversion_rate', 0)
        
        # Calculate averages
        for content_type, data in performance_by_type.items():
            count = data['count']
            if count > 0:
                data['avg_engagement'] = data['total_engagement'] / count
                data['avg_conversion'] = data['total_conversion'] / count
                
        return performance_by_type
