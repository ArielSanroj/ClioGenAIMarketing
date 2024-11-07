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

@dataclass
class CompanyInfo:
    """Data structure for company information"""
    name: str
    description: str
    social_links: Dict[str, str]
    locations: List[Dict[str, str]]
    products: List[Dict]
    images: List[str]

class UniversalWebScraper:
    """Universal web scraper with comprehensive data extraction capabilities"""
    
    def analyze_website(self, url: str) -> CompanyInfo:
        """Main function to analyze company website"""
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return CompanyInfo(
                name=self.extract_company_name(soup, url),
                description=self.extract_company_description(soup),
                social_links=self.extract_social_links(soup),
                locations=self.extract_locations(soup, url),
                products=self.extract_products(soup, url),
                images=self.extract_images(soup, url)
            )
        except Exception as e:
            st.error(f"Error analyzing website: {str(e)}")
            raise

    def extract_company_name(self, soup: BeautifulSoup, url: str) -> str:
        """Extract company name using multiple fallback methods"""
        possible_elements = [
            soup.find('meta', property='og:site_name'),
            soup.find('meta', property='og:title'),
            soup.find(['h1', 'h2'], class_=re.compile(r'logo|brand|company|header', re.I)),
            soup.find('title')
        ]
        
        for element in possible_elements:
            if element:
                name = element.get('content', element.text)
                if name and len(name) > 1:
                    return name.strip()
        
        return url.split('/')[2].replace('www.', '').split('.')[0].capitalize()

    def extract_company_description(self, soup: BeautifulSoup) -> str:
        """Extract company description from various locations"""
        possible_elements = [
            soup.find('meta', {'name': 'description'}),
            soup.find('meta', property='og:description'),
            soup.find(class_=re.compile(r'about|description|company-info', re.I)),
            soup.find(['p', 'div'], class_=re.compile(r'intro|summary|mission', re.I))
        ]
        
        for element in possible_elements:
            if element:
                desc = element.get('content', element.text)
                if desc and len(desc) > 10:
                    return desc.strip()
        
        return "Description not found"

    def extract_social_links(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract social media links"""
        social_platforms = {
            'facebook': r'facebook\.com',
            'twitter': r'twitter\.com|x\.com',
            'linkedin': r'linkedin\.com',
            'instagram': r'instagram\.com',
            'youtube': r'youtube\.com'
        }
        
        social_links = {}
        for platform, pattern in social_platforms.items():
            links = soup.find_all('a', href=re.compile(pattern))
            if links:
                social_links[platform] = links[0]['href']
        
        return social_links

    def extract_locations(self, soup: BeautifulSoup, url: str) -> List[Dict[str, str]]:
        """Extract company locations and contact information"""
        locations = []
        
        # Try to find contact/location page
        contact_link = soup.find('a', text=re.compile(r'contact|location', re.I))
        if contact_link:
            contact_url = contact_link.get('href')
            if not contact_url.startswith('http'):
                contact_url = urljoin(url, contact_url)
            try:
                response = requests.get(contact_url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.text, 'html.parser')
            except:
                pass

        # Look for address patterns
        address_pattern = re.compile(r'\d+\s+[A-Za-z]+\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Suite|Ste).*')
        phone_pattern = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
        
        for tag in soup.find_all(['p', 'div', 'address']):
            text = tag.get_text().strip()
            if address_pattern.search(text):
                phone = phone_pattern.search(text)
                locations.append({
                    "name": "Office",
                    "address": text,
                    "phone": phone.group() if phone else None
                })
        
        return locations

    def extract_products(self, soup: BeautifulSoup, url: str) -> List[Dict]:
        """Extract products/services information"""
        products = []
        
        # Try to find products page
        products_link = soup.find('a', text=re.compile(r'products?|services?', re.I))
        if products_link:
            products_url = products_link.get('href')
            if not products_url.startswith('http'):
                products_url = urljoin(url, products_url)
            try:
                response = requests.get(products_url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.text, 'html.parser')
            except:
                pass

        # Look for product elements
        product_elements = soup.find_all(class_=re.compile(r'product|service|item', re.I))
        
        for element in product_elements[:5]:  # Limit to 5 products
            try:
                name = element.find(['h2', 'h3', 'h4'])
                name = name.get_text().strip() if name else "Unknown Product"
                
                description = element.find(['p', 'div'], class_=re.compile(r'description|details', re.I))
                description = description.get_text().strip() if description else ""
                
                price_element = element.find(text=re.compile(r'\$\d+\.?\d*'))
                price = re.search(r'\$(\d+\.?\d*)', price_element).group(1) if price_element else None
                
                image = element.find('img')
                image_url = image['src'] if image else None
                if image_url and not image_url.startswith('http'):
                    image_url = urljoin(url, image_url)

                products.append({
                    "name": name,
                    "description": description,
                    "price": price,
                    "image_url": image_url
                })
            except Exception as e:
                continue
        
        return products

    def extract_images(self, soup: BeautifulSoup, url: str) -> List[str]:
        """Extract relevant images"""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src:
                if not re.search(r'icon|logo|small', src, re.I):
                    full_url = urljoin(url, src)
                    images.append(full_url)
        return images[:10]  # Limit to 10 images

def render_analyzer():
    """Render the analyzer component in Streamlit"""
    st.markdown("## Company Website Analyzer")
    
    # URL Analysis Section
    url_input = st.text_input(
        "Enter company website URL",
        placeholder="https://example.com",
        help="Enter the URL of the company website you want to analyze"
    )
    
    if st.button("Analyze Website", key="analyze_website"):
        if url_input:
            with st.spinner("Analyzing website content..."):
                try:
                    scraper = UniversalWebScraper()
                    result = scraper.analyze_website(url_input)
                    
                    # Display results in organized sections
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
                    st.markdown("### 🔗 Social Media Profiles")
                    social_cols = st.columns(len(result.social_links) if result.social_links else 1)
                    for idx, (platform, url) in enumerate(result.social_links.items()):
                        with social_cols[idx]:
                            st.markdown(f"[{platform.capitalize()}]({url})")
                    
                    # Products Section
                    if result.products:
                        st.markdown("### 📦 Products/Services")
                        for product in result.products:
                            with st.expander(product['name']):
                                if product['image_url']:
                                    st.image(product['image_url'], width=200)
                                st.markdown(product['description'])
                                if product['price']:
                                    st.markdown(f"**Price:** ${product['price']}")
                    
                    # Images Section
                    if result.images:
                        st.markdown("### 📸 Company Images")
                        image_cols = st.columns(3)
                        for idx, image_url in enumerate(result.images):
                            with image_cols[idx % 3]:
                                try:
                                    st.image(image_url, use_column_width=True)
                                except:
                                    continue
                    
                except Exception as e:
                    st.error(f"Error analyzing website: {str(e)}")
        else:
            st.warning("Please enter a URL to analyze")
    
    # File Upload Section
    st.markdown("### 📤 Upload Company Documents")
    uploaded_file = st.file_uploader(
        "Upload documents for analysis",
        type=['pdf', 'txt', 'png', 'jpg', 'jpeg'],
        help="Supported formats: PDF, Text files, Images"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, caption="Uploaded Image")
            elif uploaded_file.type == 'text/plain':
                content = uploaded_file.getvalue().decode('utf-8')
                st.text_area("File Content", content, height=200)
            else:
                st.markdown(f"File uploaded: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    render_analyzer()
