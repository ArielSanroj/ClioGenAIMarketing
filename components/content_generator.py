import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import json
from ai_utils import generate_marketing_content
from database import db
from marketing_campaign_system import (
    ContentMarketingCampaign,
    BuyerPersona,
    ContentPiece,
    MarketingGoal
)

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'content_form_state' not in st.session_state:
        st.session_state.content_form_state = {
            'business_name': '',
            'business_description': '',
            'content_type': 'Blog Post',
            'format': '',
            'length': '',
            'tone': 'Professional',
            'generated_content': None,
            'analysis': None
        }
    
    # Add missing state variables
    if 'brand_values' not in st.session_state:
        st.session_state.brand_values = {}
    if 'icp_data' not in st.session_state:
        st.session_state.icp_data = {}

def update_form_state(key: str, value: Optional[str]):
    """Update session state with form data"""
    if value is not None:  # Only update if value is not None
        st.session_state.content_form_state[key] = value

def render_content_generator():
    initialize_session_state()
    
    st.markdown("## Content Marketing Generator")
    
    with st.form(key='content_generator_form', clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Business Information")
            business_name = st.text_input(
                "Business Name",
                value=st.session_state.content_form_state['business_name'],
                key='business_name_input',
                help="Enter your business name"
            )
            
            business_description = st.text_area(
                "Business Description",
                value=st.session_state.content_form_state['business_description'],
                key='business_description_input',
                help="Describe your business and its unique value proposition",
                height=150
            )
        
        with col2:
            st.subheader("Content Configuration")
            
            content_types = {
                "Blog Post": ["How-to Guide", "Industry Analysis", "Case Study", "List Article"],
                "Social Media Post": ["Text Post", "Image Caption", "Poll", "Story"],
                "Email Newsletter": ["Welcome Series", "Product Update", "Industry News", "Educational"],
                "Landing Page Copy": ["Product Launch", "Service Offering", "Lead Magnet", "Event Registration"]
            }
            
            content_type = st.selectbox(
                "Content Type",
                options=list(content_types.keys()),
                index=list(content_types.keys()).index(st.session_state.content_form_state['content_type']),
                key='content_type_input'
            )
            
            format_options = content_types[content_type]
            selected_format = st.selectbox(
                "Format",
                options=format_options,
                key='format_input'
            )
            
            content_lengths = ["Short (500 words)", "Medium (1000 words)", "Long (2000+ words)"]
            selected_length = st.selectbox(
                "Content Length",
                options=content_lengths,
                key='length_input'
            )
            
            content_tones = ["Professional", "Casual", "Enthusiastic", "Educational", "Persuasive"]
            selected_tone = st.selectbox(
                "Content Tone",
                options=content_tones,
                index=content_tones.index(st.session_state.content_form_state['tone']),
                key='tone_input'
            )
        
        # Submit buttons
        col1, col2 = st.columns(2)
        with col1:
            analyze_button = st.form_submit_button(
                "Analyze Content Strategy",
                type="secondary",
                help="Analyze your content strategy before generation"
            )
        
        with col2:
            generate_button = st.form_submit_button(
                "Generate Content",
                type="primary",
                help="Generate optimized content based on your inputs"
            )
        
        # Update session state when form is submitted
        if analyze_button or generate_button:
            # Update form state with safe handling of None values
            update_form_state('business_name', business_name)
            update_form_state('business_description', business_description)
            update_form_state('content_type', content_type)
            update_form_state('format', selected_format)
            update_form_state('length', selected_length)
            update_form_state('tone', selected_tone)
    
    # Handle form submissions
    if analyze_button and business_name and business_description:
        with st.spinner("Analyzing content strategy..."):
            try:
                # Create context for analysis
                prompt = f"""
                Business Name: {business_name}
                Business Description: {business_description}
                Brand Values: {json.dumps(st.session_state.brand_values)}
                ICP Data: {json.dumps(st.session_state.icp_data)}
                
                Analyze this business context and provide:
                1. Key industry keywords and topics
                2. Suggested content tone
                3. Target audience insights
                4. Content strategy recommendations
                """
                
                analysis = generate_marketing_content(prompt, "content_analysis")
                st.session_state.content_form_state['analysis'] = analysis
                
                st.success("Analysis completed!")
                st.subheader("Content Strategy Analysis")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Key Topics**")
                    for topic in analysis.get('keywords', []):
                        st.markdown(f"- {topic}")
                
                with col2:
                    st.markdown("**Target Audience**")
                    if 'target_audience' in analysis:
                        st.markdown(analysis['target_audience'])
                
                st.markdown("**Content Strategy**")
                if 'recommendations' in analysis:
                    for rec in analysis['recommendations']:
                        st.markdown(f"- {rec}")
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
    
    elif generate_button and business_name and business_description:
        with st.spinner("Generating content..."):
            try:
                # Create context for content generation
                prompt = f"""
                Business Name: {business_name}
                Business Description: {business_description}
                Content Type: {content_type}
                Format: {selected_format}
                Length: {selected_length}
                Tone: {selected_tone}
                Analysis: {json.dumps(st.session_state.content_form_state.get('analysis', {}))}
                Brand Values: {json.dumps(st.session_state.brand_values)}
                ICP Data: {json.dumps(st.session_state.icp_data)}
                """
                
                content = generate_marketing_content(prompt, content_type)
                
                # Save to session state and database
                st.session_state.content_form_state['generated_content'] = content
                db.save_campaign(
                    business_name=business_name,
                    campaign_type=content_type,
                    content=content['content']
                )
                
                # Display generated content
                st.success("Content generated successfully!")
                
                tabs = st.tabs(["Content", "SEO Analysis", "Distribution"])
                
                with tabs[0]:
                    st.markdown(f"**Title:** {content['title']}")
                    st.markdown("**Content:**")
                    st.markdown(content['content'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "Export Content",
                            content['content'],
                            file_name=f"{business_name}_{content_type}.txt",
                            mime="text/plain"
                        )
                
                with tabs[1]:
                    st.markdown("**Target Keywords:**")
                    for keyword in content.get('keywords', []):
                        st.markdown(f"- {keyword}")
                
                with tabs[2]:
                    st.markdown("**Distribution Strategy:**")
                    channels = content.get('distribution_channels', 
                        ['Website Blog', 'Email Newsletter', 'LinkedIn', 'Industry Forums'])
                    for channel in channels:
                        st.markdown(f"- {channel}")
                
            except Exception as e:
                st.error(f"Error generating content: {str(e)}")
    
    elif generate_button or analyze_button:
        st.warning("Please fill in all required fields before proceeding.")
