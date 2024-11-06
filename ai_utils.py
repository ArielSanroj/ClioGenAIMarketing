import os
from openai import OpenAI
import json

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_marketing_content(business_info: str, content_type: str) -> dict:
    prompt = f"""
    Generate marketing content for the following business:
    {business_info}
    Content type: {content_type}
    
    Provide the response in JSON format with the following structure:
    {{
        "title": "Campaign title",
        "content": "Main content",
        "keywords": ["keyword1", "keyword2"],
        "target_audience": "Description of target audience"
    }}
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def analyze_audience(business_info: str) -> dict:
    prompt = f"""
    Analyze the target audience for the following business:
    {business_info}
    
    Provide detailed demographic information and insights in JSON format:
    {{
        "demographics": {{
            "age_groups": [],
            "interests": [],
            "locations": []
        }},
        "psychographics": [],
        "pain_points": [],
        "recommendations": []
    }}
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def generate_seo_recommendations(content: str) -> dict:
    prompt = f"""
    Analyze the following content and provide SEO recommendations:
    {content}
    
    Provide recommendations in JSON format:
    {{
        "keywords": [],
        "meta_description": "",
        "title_suggestions": [],
        "content_improvements": [],
        "technical_suggestions": []
    }}
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
