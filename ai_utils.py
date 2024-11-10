import os
from openai import OpenAI
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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
        messages=[{"role": "user", "content": prompt}]
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
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)

def analyze_webpage(url: str) -> dict:
    """Analyze webpage content and extract relevant information"""
    try:
        # Fetch webpage content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract metadata
        title = soup.title.string if soup.title else ""
        meta_description = ""
        meta_keywords = ""
        
        for meta in soup.find_all('meta'):
            if meta.get('name', '').lower() == 'description':
                meta_description = meta.get('content', '')
            elif meta.get('name', '').lower() == 'keywords':
                meta_keywords = meta.get('content', '')
        
        # Extract main content (remove scripts, styles, etc.)
        for script in soup(['script', 'style', 'iframe', 'nav', 'footer']):
            script.decompose()
        
        main_content = ' '.join(soup.stripped_strings)
        
        # Analyze content with AI
        analysis_prompt = f"""
        Analyze this webpage content and provide SEO recommendations in JSON format:
        
        URL: {url}
        Title: {title}
        Meta Description: {meta_description}
        Content: {main_content[:2000]}...
        
        Please structure your response as a JSON object with the following fields:
        - topics: list of main topics covered
        - keyword_suggestions: list of relevant keywords
        - content_gaps: list of missing topics or areas
        - meta_suggestions: object with title and description
        - content_recommendations: list of improvements
        - semantic_topics: list of related topics
        - estimated_word_count: number
        - readability_score: number (0-100)
        """
        
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": analysis_prompt}]
            )
            
            # Parse the response content
            content = response.choices[0].message.content
            try:
                analysis = json.loads(content)  # Try to parse as JSON first
            except json.JSONDecodeError:
                # If not valid JSON, create structured format from text
                analysis = {
                    "topics": [],
                    "keyword_suggestions": [],
                    "content_gaps": [],
                    "meta_suggestions": {
                        "title": "",
                        "description": ""
                    },
                    "content_recommendations": [],
                    "semantic_topics": [],
                    "estimated_word_count": 0,
                    "readability_score": 0
                }
            
            return {
                "url": url,
                "domain": urlparse(url).netloc,
                "title": title,
                "meta_description": meta_description,
                "meta_keywords": meta_keywords,
                "analysis": analysis
            }
            
        except Exception as e:
            return {
                "error": f"AI analysis error: {str(e)}",
                "url": url,
                "domain": urlparse(url).netloc,
            }
            
    except requests.RequestException as e:
        return {
            "error": f"Request error: {str(e)}",
            "url": url,
            "domain": urlparse(url).netloc if url else "",
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "url": url,
            "domain": urlparse(url).netloc if url else "",
        }

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
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)
