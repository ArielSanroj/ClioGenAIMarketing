import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, List
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
    if 'content_form' not in st.session_state:
        st.session_state.content_form = {
            'business_name': '',
            'business_description': '',
            'selected_type': 'Blog Post',
            'content_options': {},
            'selected_tone': 'Professional',
            'analysis': None,
            'generated_content': None
        }

def update_session_state(key, value):
    """Update session state with form data"""
    st.session_state.content_form[key] = value

class EnhancedContentGenerator:
    def __init__(self):
        self.campaign = ContentMarketingCampaign("Dynamic Campaign")
        
    def analyze_business_context(self, business_name: str, description: str) -> Dict:
        """Analyze business context to inform content generation"""
        prompt = f"""
        Analyze the following business context and provide insights:
        Business: {business_name}
        Description: {description}
        
        Format the response as JSON with:
        - industry_keywords: list of relevant keywords
        - tone: suggested content tone
        - target_segments: identified target audience segments
        - unique_selling_points: key differentiators
        """
        
        analysis = generate_marketing_content(prompt, "business_analysis")
        return analysis

def render_content_generator():
    initialize_session_state()
    
    st.markdown("## AI-Powered Content Marketing Generator")
    
    # Initialize generator
    generator = EnhancedContentGenerator()
    
    with st.form(key='content_generator_form'):
        # Business Information
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Business Information")
            business_name = st.text_input(
                "Business Name",
                value=st.session_state.content_form['business_name'],
                key='business_name',
                help="Enter your business name"
            )
            
            business_description = st.text_area(
                "Business Description",
                value=st.session_state.content_form['business_description'],
                key='business_description',
                height=150,
                help="Describe your business, products/services, and target market"
            )
            
            analyze_button = st.form_submit_button(
                "Analyze Business Context",
                type="primary",
                disabled=not (business_name and business_description)
            )
            
        with col2:
            st.subheader("Content Configuration")
            
            content_types = {
                "Blog Post": {
                    "formats": ["How-to Guide", "Industry Analysis", "Case Study", "List Article"],
                    "lengths": ["Short (500 words)", "Medium (1000 words)", "Long (2000+ words)"]
                },
                "Social Media Post": {
                    "platforms": ["LinkedIn", "Twitter", "Instagram", "Facebook"],
                    "formats": ["Text", "Image Caption", "Poll", "Story"]
                },
                "Email Newsletter": {
                    "types": ["Welcome Series", "Product Update", "Industry News", "Educational"],
                    "lengths": ["Brief", "Standard", "Detailed"]
                },
                "Landing Page Copy": {
                    "purposes": ["Product Launch", "Service Offering", "Lead Magnet", "Event Registration"],
                    "styles": ["Minimal", "Detailed", "Storytelling"]
                }
            }
            
            selected_type = st.selectbox(
                "Content Type",
                list(content_types.keys()),
                index=list(content_types.keys()).index(st.session_state.content_form['selected_type'])
            )
            
            # Dynamic options based on content type
            content_options = {}
            if selected_type == "Blog Post":
                content_options['format_type'] = st.selectbox("Format", content_types[selected_type]["formats"])
                content_options['length'] = st.selectbox("Length", content_types[selected_type]["lengths"])
            elif selected_type == "Social Media Post":
                content_options['platform'] = st.selectbox("Platform", content_types[selected_type]["platforms"])
                content_options['format_type'] = st.selectbox("Format", content_types[selected_type]["formats"])
            elif selected_type == "Email Newsletter":
                content_options['email_type'] = st.selectbox("Newsletter Type", content_types[selected_type]["types"])
                content_options['length'] = st.selectbox("Length", content_types[selected_type]["lengths"])
            else:
                content_options['purpose'] = st.selectbox("Purpose", content_types[selected_type]["purposes"])
                content_options['style'] = st.selectbox("Style", content_types[selected_type]["styles"])
            
            # Tone selection
            tone_options = ["Professional", "Casual", "Enthusiastic", "Educational", "Persuasive"]
            selected_tone = st.selectbox(
                "Content Tone",
                tone_options,
                index=tone_options.index(st.session_state.content_form['selected_tone'])
            )
            
            generate_button = st.form_submit_button(
                "Generate Content",
                type="primary"
            )

    # Update session state after form submission
    if analyze_button:
        try:
            analysis = generator.analyze_business_context(business_name, business_description)
            st.session_state.content_form.update({
                'business_name': business_name,
                'business_description': business_description,
                'analysis': analysis
            })
            
            st.success("Analysis completed successfully!")
            st.subheader("Business Analysis")
            
            col1a, col1b = st.columns(2)
            with col1a:
                st.markdown("**Industry Keywords**")
                for keyword in analysis['industry_keywords']:
                    st.markdown(f"- {keyword}")
            
            with col1b:
                st.markdown("**Target Segments**")
                for segment in analysis['target_segments']:
                    st.markdown(f"- {segment}")
            
            st.markdown("**Suggested Tone**")
            st.info(analysis['tone'])
            
            st.markdown("**Unique Selling Points**")
            for usp in analysis['unique_selling_points']:
                st.markdown(f"- {usp}")
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")

    # Handle content generation
    if generate_button and st.session_state.content_form.get('analysis'):
        try:
            with st.spinner("Generating optimized content..."):
                # Update session state
                st.session_state.content_form.update({
                    'selected_type': selected_type,
                    'content_options': content_options,
                    'selected_tone': selected_tone
                })
                
                prompt = f"""
                Business Name: {st.session_state.content_form['business_name']}
                Business Description: {st.session_state.content_form['business_description']}
                Content Type: {selected_type}
                Tone: {selected_tone}
                
                Additional Context:
                {json.dumps(content_options, indent=2)}
                Analysis: {json.dumps(st.session_state.content_form['analysis'], indent=2)}
                
                Generate marketing content that is engaging, SEO-optimized, and aligned with the business goals.
                """
                
                content_data = generate_marketing_content(prompt, selected_type)
                st.session_state.content_form['generated_content'] = content_data
                
                # Create content piece
                content = ContentPiece(
                    title=content_data['title'],
                    content_type=selected_type,
                    target_persona="General Audience",
                    emotional_tone=selected_tone,
                    keywords=content_data['keywords'],
                    content_body=content_data['content'],
                    created_at=datetime.now()
                )
                
                # Display Results
                st.subheader("Generated Content")
                tabs = st.tabs(["Content", "SEO Analysis", "Performance Prediction", "Distribution Strategy"])
                
                with tabs[0]:
                    st.markdown(f"**Title:** {content.title}")
                    st.markdown("**Content:**")
                    st.text_area("", content.content_body, height=300, disabled=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "Export Content",
                            content.content_body,
                            file_name=f"{st.session_state.content_form['business_name']}_{selected_type}.txt",
                            mime="text/plain"
                        )
                    with col2:
                        if st.button("Save to Campaign"):
                            generator.campaign.content_pieces.append(content)
                            # Save to database
                            db.save_campaign(
                                business_name=st.session_state.content_form['business_name'],
                                campaign_type=selected_type,
                                content=content.content_body
                            )
                            st.success("Content saved to campaign!")
                
                with tabs[1]:
                    st.markdown("### SEO Analysis")
                    st.markdown("**Target Keywords:**")
                    for keyword in content_data['keywords']:
                        st.markdown(f"- {keyword}")
                
                with tabs[2]:
                    st.markdown("### Performance Prediction")
                    metrics = {
                        'Engagement Rate': '75%',
                        'Click-through Rate': '12%',
                        'Conversion Potential': 'High'
                    }
                    st.json(metrics)
                
                with tabs[3]:
                    st.markdown("### Recommended Distribution Channels")
                    channels = ['Website Blog', 'Email Newsletter', 'LinkedIn', 'Industry Forums']
                    for channel in channels:
                        st.markdown(f"- {channel}")
                    
                    st.markdown("### Posting Schedule")
                    schedule_df = pd.DataFrame({
                        'Channel': channels,
                        'Best Time': ['9:00 AM', '12:00 PM', '3:00 PM', '5:00 PM'],
                        'Expected Engagement': ['High', 'Medium', 'High', 'Medium']
                    })
                    st.dataframe(schedule_df)
        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
    elif generate_button and not st.session_state.content_form.get('analysis'):
        st.info("Please complete the business analysis before generating content.")
