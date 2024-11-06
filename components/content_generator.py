import streamlit as st
from ai_utils import generate_marketing_content
from database import db

def render_content_generator():
    st.markdown("## Content Marketing Generator")
    
    business_name = st.text_input("Business Name")
    business_description = st.text_area("Business Description")
    
    content_types = [
        "Blog Post",
        "Social Media Post",
        "Email Newsletter",
        "Landing Page Copy"
    ]
    
    selected_type = st.selectbox("Content Type", content_types)
    
    if st.button("Generate Content"):
        if business_name and business_description:
            with st.spinner("Generating content..."):
                content = generate_marketing_content(
                    f"{business_name}: {business_description}",
                    selected_type
                )
                
                st.markdown("### Generated Content")
                st.markdown(f"**Title:** {content['title']}")
                st.markdown(f"**Content:**\n{content['content']}")
                st.markdown("**Keywords:**")
                for keyword in content['keywords']:
                    st.markdown(f"- {keyword}")
                
                if st.button("Save Content"):
                    db.save_campaign(
                        business_name,
                        selected_type,
                        content['content']
                    )
                    st.success("Content saved successfully!")
                
                # Export option
                st.download_button(
                    "Export Content",
                    content['content'],
                    file_name=f"{business_name}_content.txt",
                    mime="text/plain"
                )
        else:
            st.error("Please fill in all required fields.")
