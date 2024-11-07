import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io

def analyze_url(url):
    """Analyze website content"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content
        title = soup.title.string if soup.title else ""
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description['content'] if meta_description else ""
        
        # Extract keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        keywords = meta_keywords['content'].split(',') if meta_keywords else []
        
        return {
            'title': title,
            'description': description,
            'content': '\n'.join(paragraphs[:5]),  # First 5 paragraphs
            'keywords': keywords
        }
    except Exception as e:
        st.error(f"Error analyzing URL: {str(e)}")
        return None

def analyze_file(file):
    """Analyze uploaded file content"""
    try:
        if file.type.startswith('image'):
            # Handle image files
            image = Image.open(file)
            return {
                'type': 'image',
                'size': f"{image.size[0]}x{image.size[1]}",
                'format': image.format,
                'mode': image.mode
            }
        elif file.type == 'text/plain':
            # Handle text files
            content = file.getvalue().decode('utf-8')
            return {
                'type': 'text',
                'content': content[:1000],  # First 1000 characters
                'size': len(content)
            }
        else:
            return {
                'type': 'unsupported',
                'message': f"File type {file.type} is not supported"
            }
    except Exception as e:
        st.error(f"Error analyzing file: {str(e)}")
        return None

def render_analyzer():
    st.markdown("## Content Analyzer")
    
    # Create tabs for URL and File upload
    url_tab, file_tab = st.tabs(["URL Analysis", "File Analysis"])
    
    with url_tab:
        st.markdown("### Analyze Website Content")
        url_input = st.text_input("Enter website URL", placeholder="https://example.com")
        
        if st.button("Analyze URL", key="analyze_url"):
            if url_input:
                with st.spinner("Analyzing website content..."):
                    result = analyze_url(url_input)
                    if result:
                        st.markdown("#### Analysis Results")
                        st.markdown(f"**Title:** {result['title']}")
                        st.markdown(f"**Description:** {result['description']}")
                        st.markdown("**Content Preview:**")
                        st.text(result['content'])
                        if result['keywords']:
                            st.markdown("**Keywords:**")
                            st.write(', '.join(result['keywords']))
            else:
                st.warning("Please enter a URL to analyze")
    
    with file_tab:
        st.markdown("### Analyze Uploaded Content")
        uploaded_file = st.file_uploader(
            "Choose a file to analyze",
            type=['txt', 'png', 'jpg', 'jpeg'],
            help="Supported formats: Text files, Images"
        )
        
        if uploaded_file is not None:
            with st.spinner("Analyzing file content..."):
                result = analyze_file(uploaded_file)
                if result:
                    st.markdown("#### Analysis Results")
                    if result['type'] == 'image':
                        st.image(uploaded_file, caption="Uploaded Image")
                        st.json({
                            'Size': result['size'],
                            'Format': result['format'],
                            'Mode': result['mode']
                        })
                    elif result['type'] == 'text':
                        st.markdown("**Content Preview:**")
                        st.text(result['content'])
                        st.markdown(f"**Total Size:** {result['size']} characters")
                    else:
                        st.warning(result['message'])

if __name__ == "__main__":
    render_analyzer()
