import os
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Tuple
import requests
from openai import OpenAI

# Initialize OpenAI API
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Archetype Data
archetype_data = {
    "Autonomous": {
        "Focus on solving the problem": {
            "keywords": ["efficient", "practical", "results", "growth", "achievement"],
            "interpretation": "Consumers with high logical reasoning and organization skills.",
            "neuromarketing_objective": "Highlight product efficiency and functionality. Provide technical data.",
            "consumer_type": "Goal-oriented professionals, leaders, entrepreneurs."
        },
        "Strive and succeed": {
            "keywords": ["growth", "success", "achievement"],
            "interpretation": "Highly motivated, perseverant, and ambitious consumers.",
            "neuromarketing_objective": "Emphasize achievement and personal growth with success stories.",
            "consumer_type": "Entrepreneurs, ambitious professionals, outstanding students."
        }
    },
    "Impulsive": {
        "Tension reduction": {
            "keywords": ["quick", "easy", "instant"],
            "interpretation": "Consumers with low frustration tolerance, seeking immediate gratification.",
            "neuromarketing_objective": "Offer instant satisfaction and ease of use.",
            "consumer_type": "Impulsive buyers, tech enthusiasts, trend seekers."
        },
        "Self-blame": {
            "keywords": ["change", "improve", "growth"],
            "interpretation": "Consumers who tend to blame themselves or others.",
            "neuromarketing_objective": "Use positive messages that boost self-esteem.",
            "consumer_type": "People seeking change and personal development."
        }
    },
    # Add additional archetypes and subscales as necessary
}

# Function Definitions
def validate_inputs(story: str, content_type: str) -> bool:
    """Validate input parameters before generating content."""
    return bool(story and story.strip() and content_type and content_type.strip())

def generate_marketing_content(prompt: str, content_type: str) -> Dict:
    """Generate marketing content using OpenAI's API."""
    try:
        system_message = """You are an expert marketing content generator. 
        Generate content that matches the provided type, tone, and platform. 
        Format your response with the following clear sections:

        Title: [Create an engaging title]
        Content: [Provide detailed main content]
        Keywords: [List relevant keywords separated by commas]
        Target Audience: [Describe the target audience]

        Make sure each section is clearly separated by newlines and properly labeled."""

        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        generated_text = response.choices[0].message.content

        content_dict = {
            "title": "",
            "content": "",
            "keywords": [],
            "target_audience": "",
            "tone": content_type
        }

        current_section = None
        current_content = []
        for line in generated_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.lower().startswith('title:'):
                current_section = 'title'
                content_dict['title'] = line.replace('Title:', '').strip()
            elif line.lower().startswith('content:'):
                if current_section == 'content':
                    content_dict['content'] = '\n'.join(current_content)
                current_section = 'content'
                current_content = []
            elif line.lower().startswith('keywords:'):
                if current_section == 'content':
                    content_dict['content'] = '\n'.join(current_content)
                current_section = 'keywords'
                keywords = line.replace('Keywords:', '').strip()
                content_dict['keywords'] = [k.strip() for k in keywords.split(',')]
            elif line.lower().startswith('target audience:'):
                if current_section == 'content':
                    content_dict['content'] = '\n'.join(current_content)
                current_section = 'target_audience'
                content_dict['target_audience'] = line.replace('Target Audience:', '').strip()
            else:
                if current_section == 'content':
                    current_content.append(line)
                elif current_section == 'target_audience':
                    content_dict['target_audience'] += ' ' + line

        if current_section == 'content':
            content_dict['content'] = '\n'.join(current_content)

        return content_dict

    except Exception as e:
        return {
            "title": "Error generating content",
            "content": f"An error occurred: {str(e)}",
            "keywords": [],
            "target_audience": "",
            "tone": content_type
        }

def analyze_audience(data: dict) -> dict:
    """Analyze audience data and provide insights."""
    prompt = f'''
    Analyze audience data and provide insights:
    {json.dumps(data)}
    Provide analysis in JSON format:
    {{
        "demographics": {{
            "age_groups": [],
            "locations": [],
            "interests": []
        }},
        "behavior": {{
            "purchasing_patterns": [],
            "platform_preferences": [],
            "content_engagement": []
        }},
        "recommendations": []
    }}
    '''

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)

def calculate_archetype_probabilities(brand_values: dict, icp_data: dict, seo_analysis: dict) -> dict:
    """
    Calculate the probabilities of each archetype based on user input data.
    Combines Brand Values, ICP data, and SEO analysis.
    """
    try:
        archetypes = ['Autonomous', 'Impulsive', 'Avoidant', 'Isolated']
        scores = {archetype: 0 for archetype in archetypes}

        # Factor in brand values
        for keyword in brand_values.get('keywords', []):
            if keyword in ['efficiency', 'growth']:
                scores['Autonomous'] += 10
            elif keyword in ['creativity', 'comfort']:
                scores['Impulsive'] += 10
            elif keyword in ['security', 'authenticity']:
                scores['Avoidant'] += 10
            elif keyword in ['mastery', 'balance']:
                scores['Isolated'] += 10

        # Factor in ICP answers
        for question, answer in icp_data.get('answers', {}).items():
            if isinstance(answer, list):
                for value in answer:
                    if value in ['Technology', 'Healthcare']:
                        scores['Autonomous'] += 5
                    elif value in ['Retail', 'Social Media']:
                        scores['Impulsive'] += 5
            elif isinstance(answer, str) and "growth" in answer:
                scores['Autonomous'] += 10

        # Factor in SEO analysis
        for keyword in seo_analysis.get('keyword_suggestions', []):
            if keyword.lower() in ['efficiency', 'trust']:
                scores['Autonomous'] += 5
            elif keyword.lower() in ['creativity', 'relaxation']:
                scores['Impulsive'] += 5

        total = sum(scores.values())
        probabilities = {k: round(v / total * 100, 2) if total > 0 else 0 for k, v in scores.items()}

        return probabilities

    except Exception as e:
        return {"error": f"Error calculating archetype probabilities: {str(e)}"}

def generate_archetype_recommendations(probabilities: dict) -> dict:
    """
    Generate recommendations for keywords and marketing campaigns based on archetype probabilities.
    """
    recommendations = {}
    for archetype, prob in probabilities.items():
        if prob > 25:  # High alignment threshold
            if archetype == 'Autonomous':
                recommendations[archetype] = {
                    "keywords": ["Efficiency", "Innovation", "Trust"],
                    "campaign_ideas": [
                        "Promote ROI-driven campaigns.",
                        "Highlight advanced features and productivity gains."
                    ]
                }
            elif archetype == 'Impulsive':
                recommendations[archetype] = {
                    "keywords": ["Creativity", "Excitement", "Relaxation"],
                    "campaign_ideas": [
                        "Use vibrant visuals and limited-time offers.",
                        "Focus on emotional storytelling."
                    ]
                }
            elif archetype == 'Avoidant':
                recommendations[archetype] = {
                    "keywords": ["Security", "Privacy", "Comfort"],
                    "campaign_ideas": [
                        "Emphasize secure and trustworthy solutions.",
                        "Highlight stress-free experiences."
                    ]
                }
            elif archetype == 'Isolated':
                recommendations[archetype] = {
                    "keywords": ["Balance", "Mastery", "Calm"],
                    "campaign_ideas": [
                        "Promote wellness-focused products.",
                        "Highlight benefits of self-improvement."
                    ]
                }
    return recommendations

def analyze_webpage(url: str) -> dict:
    """Analyze webpage content and extract relevant information."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else ""
        meta_description = ""
        meta_keywords = ""
        for meta in soup.find_all('meta'):
            if meta.get('name', '').lower() == 'description':
                meta_description = meta.get('content', '')
            elif meta.get('name', '').lower() == 'keywords':
                meta_keywords = meta.get('content', '')

        content = ' '.join(soup.stripped_strings)

        return {
            "url": url,
            "domain": urlparse(url).netloc,
            "title": title,
            "meta_description": meta_description,
            "meta_keywords": meta_keywords,
            "content": content[:1000]
        }

    except Exception as e:
        return {"error": f"Error analyzing webpage: {str(e)}"}

def match_archetypes_and_subscales(brand_values: Dict, icp_data: Dict, seo_data: Dict) -> Tuple[Dict[str, int], List[Dict]]:
    """Match user data to archetypes and subscales."""
    archetype_scores = {
        "Autonomous": 0,
        "Impulsive": 0,
        "Avoidant": 0,
        "Isolated": 0
    }
    subscale_matches = []

    # Match keywords to archetypes and subscales
    for archetype, subscales in archetype_data.items():
        for subscale, data in subscales.items():
            matched_keywords = [
                kw for kw in brand_values.get('keywords', []) if kw in data['keywords']
            ]
            if matched_keywords:
                archetype_scores[archetype] += len(matched_keywords)
                subscale_matches.append({
                    'archetype': archetype,
                    'subscale': subscale,
                    'interpretation': data['interpretation'],
                    'neuromarketing_objective': data['neuromarketing_objective'],
                    'consumer_type': data['consumer_type'],
                    'matched_keywords': matched_keywords,
                    'missing_keywords': list(set(data['keywords']) - set(matched_keywords))
                })

    return archetype_scores, subscale_matches
