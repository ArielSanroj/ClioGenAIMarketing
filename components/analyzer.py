import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import re
from typing import Dict, List
import io

def extract_company_info(url: str) -> Dict:
    """Extract detailed company information from website"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract About Us information
        about_info = extract_about_info(soup, url)
        
        # Extract Locations
        locations = extract_locations(soup, url)
        
        # Extract Social Media
        social_media = extract_social_media(soup)
        
        # Extract Products/Services
        products = extract_products(soup, url)
        
        return {
            "background": about_info.get("background", "Not found"),
            "mission": about_info.get("mission", "Not found"),
            "values": about_info.get("values", []),
            "locations": locations,
            "socialMedia": social_media,
            "products": products
        }
    except Exception as e:
        raise Exception(f"Error analyzing website: {str(e)}")

def extract_about_info(soup: BeautifulSoup, base_url: str) -> Dict:
    """Extract About Us information"""
    about_link = soup.find('a', text=re.compile(r'about', re.I))
    
    if about_link:
        about_url = about_link.get('href')
        if not about_url.startswith('http'):
            about_url = base_url.rstrip('/') + '/' + about_url.lstrip('/')
        
        try:
            about_response = requests.get(about_url)
            about_soup = BeautifulSoup(about_response.text, 'html.parser')
        except:
            about_soup = soup
    else:
        about_soup = soup

    background = ""
    mission = ""
    values = []

    # Look for relevant sections
    for tag in about_soup.find_all(['h1', 'h2', 'h3', 'h4', 'p']):
        text = tag.get_text().strip().lower()
        if any(keyword in text for keyword in ['about us', 'our story', 'who we are']):
            background = tag.find_next('p').get_text().strip()
        elif any(keyword in text for keyword in ['mission', 'our purpose']):
            mission = tag.find_next('p').get_text().strip()
        elif any(keyword in text for keyword in ['values', 'principles']):
            values_list = tag.find_next('ul')
            if values_list:
                values = [li.get_text().strip() for li in values_list.find_all('li')]

    return {
        "background": background,
        "mission": mission,
        "values": values
    }

def extract_locations(soup: BeautifulSoup, base_url: str) -> List[Dict]:
    """Extract company locations"""
    locations = []
    contact_link = soup.find('a', text=re.compile(r'contact|location', re.I))
    
    if contact_link:
        contact_url = contact_link.get('href')
        if not contact_url.startswith('http'):
            contact_url = base_url.rstrip('/') + '/' + contact_url.lstrip('/')
        
        try:
            contact_response = requests.get(contact_url)
            contact_soup = BeautifulSoup(contact_response.text, 'html.parser')
        except:
            contact_soup = soup
    else:
        contact_soup = soup

    # Look for address patterns
    address_pattern = re.compile(r'\d+\s+[A-Za-z]+\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Suite|Ste).*')
    for tag in contact_soup.find_all(['p', 'div', 'address']):
        text = tag.get_text().strip()
        if address_pattern.search(text):
            # Look for phone number
            phone_pattern = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
            phone = phone_pattern.search(text)
            
            locations.append({
                "name": "Office",
                "address": text,
                "phone": phone.group() if phone else None
            })
    
    return locations

def extract_social_media(soup: BeautifulSoup) -> List[Dict]:
    """Extract social media profiles"""
    social_platforms = {
        'facebook': r'facebook\.com',
        'twitter': r'twitter\.com|x\.com',
        'linkedin': r'linkedin\.com',
        'instagram': r'instagram\.com',
        'youtube': r'youtube\.com'
    }
    
    social_media = []
    for platform, pattern in social_platforms.items():
        links = soup.find_all('a', href=re.compile(pattern))
        for link in links:
            social_media.append({
                "platform": platform.capitalize(),
                "url": link['href']
            })
    
    return social_media

def extract_products(soup: BeautifulSoup, base_url: str) -> List[Dict]:
    """Extract products/services information"""
    products = []
    products_link = soup.find('a', text=re.compile(r'products?|services?', re.I))
    
    if products_link:
        products_url = products_link.get('href')
        if not products_url.startswith('http'):
            products_url = base_url.rstrip('/') + '/' + products_url.lstrip('/')
        
        try:
            products_response = requests.get(products_url)
            products_soup = BeautifulSoup(products_response.text, 'html.parser')
        except:
            products_soup = soup
    else:
        products_soup = soup

    # Look for product elements
    product_elements = products_soup.find_all(class_=re.compile(r'product|service|item'))
    
    for element in product_elements[:5]:  # Limit to 5 products
        name = element.find(['h2', 'h3', 'h4'])
        name = name.get_text().strip() if name else "Unknown Product"
        
        description = element.find(['p', 'div'], class_=re.compile(r'description|details'))
        description = description.get_text().strip() if description else ""
        
        price_element = element.find(text=re.compile(r'\$\d+\.?\d*'))
        price = float(re.search(r'\$(\d+\.?\d*)', price_element).group(1)) if price_element else None
        
        image = element.find('img')
        image_url = image['src'] if image else None
        if image_url and not image_url.startswith('http'):
            image_url = base_url.rstrip('/') + '/' + image_url.lstrip('/')

        products.append({
            "name": name,
            "description": description,
            "price": price,
            "image": image_url
        })
    
    return products

def render_analyzer():
    st.markdown("## Company Analyzer")
    
    # URL Analysis Section
    st.markdown("### Analyze Website Content")
    url_input = st.text_input("Enter company website URL", placeholder="https://example.com")
    
    if st.button("Analyze Website", key="analyze_website"):
        if url_input:
            with st.spinner("Analyzing website content..."):
                try:
                    result = extract_company_info(url_input)
                    
                    # Display results in organized sections with icons
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🌐 Company Background")
                        st.markdown(f"**Background:**\n{result['background']}")
                        st.markdown(f"**Mission:**\n{result['mission']}")
                        if result['values']:
                            st.markdown("**Values:**")
                            for value in result['values']:
                                st.markdown(f"- {value}")
                    
                    with col2:
                        st.markdown("#### 📍 Locations")
                        for location in result['locations']:
                            st.markdown(f"**{location['name']}**")
                            st.markdown(f"Address: {location['address']}")
                            if location['phone']:
                                st.markdown(f"Phone: {location['phone']}")
                            st.markdown("---")
                    
                    st.markdown("#### 🔗 Social Media Profiles")
                    social_cols = st.columns(len(result['socialMedia']) if result['socialMedia'] else 1)
                    for idx, social in enumerate(result['socialMedia']):
                        with social_cols[idx]:
                            st.markdown(f"[{social['platform']}]({social['url']})")
                    
                    st.markdown("#### 📦 Products/Services")
                    for product in result['products']:
                        with st.expander(product['name']):
                            if product['image']:
                                st.image(product['image'], width=200)
                            st.markdown(product['description'])
                            if product['price']:
                                st.markdown(f"**Price:** ${product['price']}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
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
                # Add image analysis logic here
            elif uploaded_file.type == 'text/plain':
                content = uploaded_file.getvalue().decode('utf-8')
                st.text_area("File Content", content, height=200)
            elif uploaded_file.type == 'application/pdf':
                st.markdown(f"PDF file uploaded: {uploaded_file.name}")
                # Add PDF analysis logic here
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    render_analyzer()
