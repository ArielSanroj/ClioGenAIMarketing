import os
from openai import OpenAI
import json
from typing import Dict

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def validate_inputs(story: str, content_type: str) -> bool:
    """Validate input parameters before generating content"""
    if not story or not story.strip():
        return False
    if not content_type or not content_type.strip():
        return False
    return True

def generate_marketing_content(prompt: str, content_type: str) -> Dict:
    """Generate marketing content using OpenAI's API with improved parsing and error handling"""
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
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        generated_text = response.choices[0].message.content
        
        # Initialize content dictionary
        content_dict = {
            "title": "",
            "content": "",
            "keywords": [],
            "target_audience": "",
            "tone": content_type
        }
        
        # Split the text into sections and parse
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
        
        # Handle any remaining content
        if current_section == 'content':
            content_dict['content'] = '\n'.join(current_content)
        
        return content_dict
        
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return {
            "title": "Error generating content",
            "content": f"An error occurred: {str(e)}",
            "keywords": [],
            "target_audience": "",
            "tone": content_type
        }

def analyze_audience(data: dict) -> dict:
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

def analyze_market_trends(keywords, region=None) -> dict:
    """Analyze market trends for given keywords"""
    trend_prompt = f"""
    Analyze market trends for these keywords: {keywords}
    Region: {region if region else 'Global'}
    
    Provide the analysis in JSON format with the following structure:
    {{
        "search_volume": {{
            "trend": "Monthly search volume trend description",
            "data": [monthly_volumes_list]
        }},
        "competition": {{
            "level": "high/medium/low",
            "analysis": "Detailed competition analysis"
        }},
        "regional_popularity": {{
            "top_regions": ["region1", "region2"],
            "scores": [score1, score2]
        }},
        "rising_topics": ["topic1", "topic2"],
        "seasonal_patterns": {{
            "peak_months": ["month1", "month2"],
            "low_months": ["month3", "month4"],
            "pattern_description": "Description of seasonality"
        }}
    }}
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": trend_prompt}]
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
        Analyze this webpage content and provide SEO recommendations:
        
        URL: {url}
        Title: {title}
        Meta Description: {meta_description}
        Content: {main_content[:2000]}...
        
        Provide recommendations in JSON format with:
        - topics: list of main topics covered
        - keyword_suggestions: list of relevant keywords with search volumes
        - content_gaps: list of missing topics or areas
        - meta_suggestions: object with title and description
        - content_recommendations: list of improvements
        - semantic_topics: list of related topics
        - estimated_word_count: number
        - readability_score: number (0-100)
        - traffic_potential: {{
            "estimated_monthly_visits": number,
            "conversion_potential": "high/medium/low",
            "engagement_metrics": {{
                "avg_time_on_page": string,
                "bounce_rate": string
            }}
        }}
        """
        
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": analysis_prompt}]
            )
            
            # Parse the response content
            content = response.choices[0].message.content
            try:
                analysis = json.loads(content)
                
                # Get market trends for suggested keywords
                market_trends = analyze_market_trends(analysis['keyword_suggestions'])
                analysis['market_trends'] = market_trends
                
            except json.JSONDecodeError:
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
                    "readability_score": 0,
                    "traffic_potential": {
                        "estimated_monthly_visits": 0,
                        "conversion_potential": "low",
                        "engagement_metrics": {
                            "avg_time_on_page": "0:00",
                            "bounce_rate": "0%"
                        }
                    }
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