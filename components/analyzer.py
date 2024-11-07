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
        self.session = create_retry_session()
    
    def analyze_website(self, url: str) -> CompanyInfo:
        """Main function to analyze company website"""
        try:
            response = self.session.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return CompanyInfo(
                name=self.extract_company_name(soup, url),
                description=self.extract_company_description(soup),
                social_links=self.extract_social_links(soup),
                locations=self.extract_locations(soup, url),
                products=self.extract_products(soup, url),
                images=self.extract_images(soup, url)
            )
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}. Please try again.")
            raise
        except Exception as e:
            st.error(f"Error analyzing website: {str(e)}")
            raise

    # ... [Previous extract methods remain unchanged] ...

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

    # File upload section below
    st.markdown("### 📤 Upload Company Documents")
    uploaded_file = st.file_uploader(
        "Upload documents for analysis",
        type=['pdf', 'txt', 'png', 'jpg', 'jpeg'],
        help="Supported formats: PDF, Text files, Images"
    )
    
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
                
                # Show continue button
                if st.button("Continue to Chat", type="primary"):
                    st.session_state.show_chat = True
                    st.rerun()
                
            except Exception as e:
                st.error(f"Error analyzing website: {str(e)}")
                st.session_state.analysis_complete = False
    
    # Handle file upload analysis
    if uploaded_file is not None:
        try:
            file_content = None
            if uploaded_file.type.startswith('image'):
                file_content = {
                    'type': 'image',
                    'content': uploaded_file
                }
                st.image(uploaded_file, caption="Uploaded Image")
            elif uploaded_file.type == 'text/plain':
                content = uploaded_file.getvalue().decode('utf-8')
                file_content = {
                    'type': 'text',
                    'content': content
                }
                st.text_area("File Content", content, height=200)
            else:
                file_content = {
                    'type': uploaded_file.type,
                    'name': uploaded_file.name
                }
                st.markdown(f"File uploaded: {uploaded_file.name}")
            
            # Save to session state
            if file_content:
                st.session_state.analyzed_data = {
                    'type': 'file',
                    'file_info': file_content
                }
                st.session_state.analysis_complete = True
                
                # Show continue button
                if st.button("Continue to Chat", type="primary", key="file_continue"):
                    st.session_state.show_chat = True
                    st.rerun()
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.session_state.analysis_complete = False

def display_analysis_results(result: CompanyInfo):
    """Display the analysis results in an organized layout"""
    st.markdown("### Analysis Results")
    
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
                cols = st.columns([2, 1])
                with cols[0]:
                    st.markdown(f"**Description:**\n{product['description']}")
                    if product.get('features'):
                        st.markdown("**Features:**")
                        for feature in product['features']:
                            st.markdown(f"- {feature}")
                    if product.get('price'):
                        st.markdown(f"**Price:** ${product['price']}")
                    if product.get('cta'):
                        st.markdown(f"[{product['cta']['text']}]({product['cta']['url']})")
                
                with cols[1]:
                    if product.get('image_url'):
                        try:
                            st.image(product['image_url'], use_container_width=True)
                        except Exception:
                            st.warning("Unable to load product image")

if __name__ == "__main__":
    render_analyzer()
