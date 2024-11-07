import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import re
from typing import Dict, List, Optional
from urllib.parse import urljoin
import json
import io
from dataclasses import dataclass
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

@dataclass
class CompanyInfo:
    """Data structure for company information"""
    name: str
    description: str
    social_links: Dict[str, str]
    locations: List[Dict[str, str]]
    products: List[Dict]
    images: List[str]

def initialize_session_state():
    """Initialize session state variables"""
    if 'analyzed_data' not in st.session_state:
        st.session_state.analyzed_data = None
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'analyzer'
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None

def create_retry_session():
    """Create a requests session with retry logic"""
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[502, 503, 504]
    )
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

class UniversalWebScraper:
    """Universal web scraper with comprehensive data extraction capabilities"""
    
    def __init__(self):
        """Initialize the scraper"""
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def analyze_website(self, url: str) -> CompanyInfo:
        """Main function to analyze company website"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise exception for bad status codes
            soup = BeautifulSoup(response.text, 'html.parser')
            
            company_info = CompanyInfo(
                name=self.extract_company_name(soup, url),
                description=self.extract_company_description(soup),
                social_links=self.extract_social_links(soup),
                locations=self.extract_locations(soup, url),
                products=self.extract_products(soup, url),
                images=self.extract_images(soup, url)
            )
            return company_info
        except Exception as e:
            st.error(f"Error analyzing website: {str(e)}")
            raise

    def extract_company_name(self, soup: BeautifulSoup, url: str) -> str:
        """Extract company name using multiple methods"""
        # Try meta tags first
        meta_tags = {
            'meta[property="og:site_name"]': 'content',
            'meta[property="og:title"]': 'content',
            'meta[name="application-name"]': 'content'
        }
        
        for selector, attr in meta_tags.items():
            element = soup.select_one(selector)
            if element and element.get(attr):
                return element[attr].strip()

        # Try common header elements
        header_selectors = [
            '.logo', '.brand', '.company-name', '.site-title',
            'header h1', '#logo', '.header-logo'
        ]
        
        for selector in header_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()

        # Try title tag
        title = soup.title
        if title:
            title_text = title.string
            # Remove common suffixes
            for suffix in [' - Home', ' | Home', ' • Home', ' | Official Site']:
                title_text = title_text.replace(suffix, '')
            return title_text.strip()

        # Fallback to domain name
        domain = url.split('/')[2].replace('www.', '')
        return domain.split('.')[0].capitalize()

    def extract_company_description(self, soup: BeautifulSoup) -> str:
        """Extract company description from meta tags and content"""
        # Try meta description first
        meta_desc = soup.find('meta', {'name': 'description'}) or \
                   soup.find('meta', {'property': 'og:description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()

        # Try common about/description sections
        description_selectors = [
            '.about-us', '.company-description', '.description',
            '#about', '.mission-statement', '.overview'
        ]
        
        for selector in description_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()

        # Try to find first substantial paragraph
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if len(text) > 50 and not any(x in text.lower() for x in ['cookie', 'privacy', 'terms']):
                return text

        return "No description available"

    def extract_social_links(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract social media profile links"""
        social_platforms = {
            'facebook': r'facebook\.com',
            'twitter': r'twitter\.com|x\.com',
            'linkedin': r'linkedin\.com',
            'instagram': r'instagram\.com',
            'youtube': r'youtube\.com',
            'pinterest': r'pinterest\.com',
            'tiktok': r'tiktok\.com'
        }
        
        social_links = {}
        
        # Check both href attributes and text content
        for platform, pattern in social_platforms.items():
            links = soup.find_all('a', href=re.compile(pattern, re.I))
            if not links:
                # Try finding by icon classes
                links = soup.find_all('a', class_=re.compile(f'{platform}|{platform}-icon', re.I))
            
            if links:
                href = links[0].get('href', '')
                if href:
                    if not href.startswith(('http://', 'https://')):
                        href = f'https://{href.lstrip("/")}' if 'www.' in href else f'https://www.{href.lstrip("/")}'
                    social_links[platform] = href
        
        return social_links

    def extract_locations(self, soup: BeautifulSoup, url: str) -> List[Dict[str, str]]:
        """Extract company locations and contact information"""
        locations = []
        
        # Try to find dedicated contact/location page
        contact_page = None
        contact_links = soup.find_all('a', href=re.compile(r'contact|location|find-us', re.I))
        
        for link in contact_links:
            href = link.get('href')
            if href:
                contact_url = urljoin(url, href)
                try:
                    response = requests.get(contact_url, headers=self.headers)
                    contact_page = BeautifulSoup(response.text, 'html.parser')
                    break
                except:
                    continue

        # Use contact page if found, otherwise use main page
        target_soup = contact_page or soup

        # Look for structured address data
        address_elements = target_soup.find_all(['address', 'div', 'p'], 
            class_=re.compile(r'address|location|contact', re.I))
        
        for element in address_elements:
            text = element.get_text().strip()
            
            # Skip if text is too short or contains common false positives
            if len(text) < 10 or any(x in text.lower() for x in ['cookie', 'privacy', 'email us']):
                continue
            
            # Extract phone number
            phone_match = re.search(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
            phone = phone_match.group() if phone_match else None
            
            locations.append({
                "name": "Office",
                "address": text,
                "phone": phone
            })

        return locations

    def extract_products(self, soup: BeautifulSoup, url: str) -> List[Dict]:
        """Extract products/services information with enhanced detection"""
        products = []
        
        # Try to find products/services section first
        product_sections = soup.find_all(['div', 'section'], 
            class_=re.compile(r'products?|services?|solutions?|offerings?', re.I))
        
        if not product_sections:
            # Fallback to finding individual product cards
            product_sections = [soup]
        
        for section in product_sections:
            # Look for product cards/items
            product_elements = section.find_all(['div', 'article'], 
                class_=re.compile(r'product|service|item|card|solution', re.I))
            
            for element in product_elements:
                try:
                    # Extract product name
                    name_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5'], 
                        class_=re.compile(r'title|name|heading', re.I))
                    if not name_elem:
                        continue
                    name = name_elem.get_text().strip()
                    
                    # Extract description
                    desc_elem = element.find(['p', 'div'], 
                        class_=re.compile(r'description|content|text', re.I))
                    description = desc_elem.get_text().strip() if desc_elem else ""
                    
                    # Extract price
                    price_elem = element.find(text=re.compile(r'(\$|USD|EUR|£)\s*\d+', re.I))
                    price = None
                    if price_elem:
                        price_match = re.search(r'(\$|USD|EUR|£)\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', 
                            price_elem.string)
                        if price_match:
                            price = price_match.group(2)
                    
                    # Extract image
                    img = element.find('img')
                    image_url = None
                    if img:
                        src = img.get('src', img.get('data-src', ''))
                        if src:
                            image_url = urljoin(url, src)
                    
                    products.append({
                        "name": name,
                        "description": description,
                        "price": price,
                        "image_url": image_url
                    })
                    
                except Exception as e:
                    continue
        
        return products[:10]  # Limit to 10 products

    def extract_images(self, soup: BeautifulSoup, url: str) -> List[str]:
        """Extract relevant images from the website"""
        images = []
        img_tags = soup.find_all('img')
        
        for img in img_tags:
            try:
                # Get image source
                src = img.get('src') or img.get('data-src')
                if not src:
                    continue
                    
                # Make URL absolute
                img_url = urljoin(url, src)
                
                # Skip small images, icons, and logos
                if any(x in img_url.lower() for x in ['icon', 'logo', 'thumb', 'small']):
                    continue
                    
                # Skip common file formats for icons
                if not re.search(r'\.(jpg|jpeg|png|webp)$', img_url.lower()):
                    continue
                    
                images.append(img_url)
                
            except Exception as e:
                continue
        
        return list(set(images))[:10]  # Remove duplicates and limit to 10 images

def display_analysis_results(result: Optional[CompanyInfo]):
    """Display the analysis results in an organized layout"""
    st.markdown("### Analysis Results")
    
    if result:  # For website analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏢 Company Information")
            st.markdown(f"**Name:** {result.name}")
            st.markdown("**Description:**")
            st.markdown(result.description)
        
        with col2:
            st.markdown("### 📍 Locations")
            for location in result.locations:
                with st.expander(f"Office - {location['address'][:30]}..."):
                    st.markdown(f"**Address:** {location['address']}")
                    if location['phone']:
                        st.markdown(f"**Phone:** {location['phone']}")
        
        # Social Media Section
        if result.social_links:
            st.markdown("### 🔗 Social Media Profiles")
            social_cols = st.columns(len(result.social_links))
            for idx, (platform, url) in enumerate(result.social_links.items()):
                with social_cols[idx]:
                    st.markdown(f"[{platform.capitalize()}]({url})")
        
        # Products Section
        if result.products:
            st.markdown("### 📦 Products/Services")
            for product in result.products:
                with st.expander(product['name']):
                    cols = st.columns(2)
                    with cols[0]:
                        st.markdown(f"**Description:**\n{product['description']}")
                        if product.get('price'):
                            st.markdown(f"**Price:** ${product['price']}")
                    
                    with cols[1]:
                        if product.get('image_url'):
                            try:
                                st.image(product['image_url'], use_container_width=True)
                            except:
                                st.warning("Unable to load product image")
    
    # Continue Button - Show for both file and website analysis
    if st.session_state.analysis_complete:
        st.markdown("---")
        # Use columns to center the button
        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue to Chat", type="primary", use_container_width=True):
                st.session_state.show_chat = True
                st.session_state.current_page = 'chat'
                st.switch_page("pages/main")  # Direct path to main.py in pages directory

def render_analyzer():
    """Render the analyzer component in Streamlit"""
    initialize_session_state()
    
    st.markdown("## Company Website Analyzer")
    
    # Clean URL input interface at the top
    col1, col2 = st.columns([3, 1])
    with col1:
        url_input = st.text_input(
            "Enter company website URL",
            placeholder="https://example.com",
            help="Enter the URL of the company website you want to analyze",
            key="url_input"
        )
    with col2:
        analyze_button = st.button("Analyze Website", use_container_width=True)

    # Handle URL analysis
    if analyze_button and url_input:
        with st.spinner("Analyzing website content..."):
            try:
                scraper = UniversalWebScraper()
                result = scraper.analyze_website(url_input)
                
                # Save to session state
                st.session_state.analyzed_data = {
                    'type': 'website',
                    'url': url_input,
                    'data': result.__dict__
                }
                st.session_state.analysis_complete = True
                
                # Show analysis results
                display_analysis_results(result)
                
            except Exception as e:
                st.error(f"Error analyzing website: {str(e)}")
                st.session_state.analysis_complete = False
    
if __name__ == "__main__":
    render_analyzer()