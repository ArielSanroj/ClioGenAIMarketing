import streamlit as st
import pandas as pd

def initialize_icp_state():
    """Initialize ICP session state"""
    if 'icp_data' not in st.session_state:
        st.session_state.icp_data = {
            'knowledge_level': '',
            'current_question': 1,
            'demographics': {},
            'psychographics': {},
            'archetype': '',
            'pain_points': [],
            'goals': [],
            'answers': {},
            'is_completed': False
        }

def get_question_by_knowledge_level(knowledge_level: str, question_number: int) -> dict:
    """Get questions based on knowledge level and question number"""
    beginner_questions = {
        1: {
            "question": "How do you identify and reach key decision-makers?",
            "type": "text_area",
            "help": "Describe your current process for finding and connecting with decision-makers"
        },
        2: {
            "question": "What challenges do your customers typically face?",
            "type": "text_area",
            "help": "List the main problems your customers are trying to solve"
        },
        3: {
            "question": "What is your target market's budget range?",
            "type": "select",
            "options": ["Under $1,000", "$1,000-$5,000", "$5,000-$10,000", "$10,000-$50,000", "$50,000+"],
            "help": "Select the typical budget range of your target customers"
        },
        4: {
            "question": "Which industries do your customers come from?",
            "type": "multiselect",
            "options": ["Technology", "Healthcare", "Finance", "Education", "Retail", "Manufacturing", "Other"],
            "help": "Select all industries that apply"
        },
        5: {
            "question": "What is the typical company size of your customers?",
            "type": "select",
            "options": ["1-10 employees", "11-50 employees", "51-200 employees", "201-1000 employees", "1000+ employees"],
            "help": "Select the most common company size"
        }
    }
    
    intermediate_questions = {
        1: {
            "question": "What are your customer's key performance indicators (KPIs)?",
            "type": "text_area",
            "help": "List the metrics your customers use to measure success"
        },
        2: {
            "question": "Describe your customer's buying process and decision timeline",
            "type": "text_area",
            "help": "Detail the steps and timeline of your customer's purchasing journey"
        },
        3: {
            "question": "What objections do you commonly encounter during sales?",
            "type": "text_area",
            "help": "List common concerns or hesitations from potential customers"
        },
        4: {
            "question": "What are your customer's growth objectives?",
            "type": "text_area",
            "help": "Describe your customer's business growth goals"
        },
        5: {
            "question": "How do your customers prefer to communicate?",
            "type": "multiselect",
            "options": ["Email", "Phone", "Video Calls", "In-Person Meetings", "Chat", "Social Media"],
            "help": "Select all preferred communication channels"
        }
    }
    
    advanced_questions = {
        1: {
            "question": "What is your customer's technology stack and integration requirements?",
            "type": "text_area",
            "help": "Detail the technical requirements and integrations needed"
        },
        2: {
            "question": "How do your customers measure ROI on your solution?",
            "type": "text_area",
            "help": "Explain how customers calculate return on investment"
        },
        3: {
            "question": "What regulatory or compliance requirements affect your customers?",
            "type": "text_area",
            "help": "Detail any industry-specific regulations or compliance needs"
        },
        4: {
            "question": "What are your customer's vendor evaluation criteria?",
            "type": "text_area",
            "help": "List the key factors in their vendor selection process"
        },
        5: {
            "question": "What strategic initiatives are driving your customer's decisions?",
            "type": "text_area",
            "help": "Describe the strategic goals influencing purchase decisions"
        }
    }
    
    question_sets = {
        "I don't know my ICP yet": beginner_questions,
        "I know my ICP": intermediate_questions,
        "I want to refine my existing ICP": advanced_questions
    }
    
    return question_sets.get(knowledge_level, {}).get(question_number, None)

def render_icp_definition():
    """Render the ICP definition form"""
    initialize_icp_state()
    
    # Center align the content
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    
    # Show logo
    st.image("logoclio.png", width=100)
    
    if not st.session_state.icp_data.get('knowledge_level'):
        st.markdown("## What is your current level of ICP knowledge?")
        
        knowledge_levels = [
            "I don't know my ICP yet",
            "I know my ICP",
            "I want to refine my existing ICP"
        ]
        
        for level in knowledge_levels:
            if st.button(level):
                st.session_state.icp_data['knowledge_level'] = level
                st.session_state.icp_data['current_question'] = 1
                st.rerun()
        
        if st.button("Skip", type="secondary"):
            st.session_state.icp_data['is_completed'] = True
            st.rerun()
    
    else:
        # Show progress
        current_q = st.session_state.icp_data['current_question']
        st.progress(current_q / 5)
        st.markdown(f"{current_q} / 5 questions")
        
        # Show back button
        col1, col2 = st.columns([1, 11])
        with col1:
            if st.button("Go back"):
                if current_q > 1:
                    st.session_state.icp_data['current_question'] -= 1
                else:
                    st.session_state.icp_data['knowledge_level'] = ''
                st.rerun()
        
        # Get current question
        question_data = get_question_by_knowledge_level(
            st.session_state.icp_data['knowledge_level'],
            current_q
        )
        
        if question_data:
            st.markdown(f"## {question_data['question']}")
            
            # Render appropriate input based on question type
            answer_key = f"q{current_q}"
            current_answer = st.session_state.icp_data['answers'].get(answer_key, '')
            
            if question_data['type'] == 'text_area':
                answer = st.text_area(
                    "Your answer",
                    value=current_answer,
                    help=question_data['help'],
                    key=f"answer_{current_q}"
                )
            elif question_data['type'] == 'select':
                answer = st.selectbox(
                    "Select an option",
                    options=question_data['options'],
                    index=question_data['options'].index(current_answer) if current_answer in question_data['options'] else 0,
                    help=question_data['help'],
                    key=f"answer_{current_q}"
                )
            elif question_data['type'] == 'multiselect':
                answer = st.multiselect(
                    "Select all that apply",
                    options=question_data['options'],
                    default=current_answer if isinstance(current_answer, list) else [],
                    help=question_data['help'],
                    key=f"answer_{current_q}"
                )
            
            # Navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Previous", disabled=current_q == 1):
                    st.session_state.icp_data['answers'][answer_key] = answer
                    st.session_state.icp_data['current_question'] -= 1
                    st.rerun()
            
            with col2:
                if current_q < 5:
                    if st.button("Next", type="primary"):
                        st.session_state.icp_data['answers'][answer_key] = answer
                        st.session_state.icp_data['current_question'] += 1
                        st.rerun()
                else:
                    if st.button("Complete", type="primary"):
                        st.session_state.icp_data['answers'][answer_key] = answer
                        st.session_state.icp_data['is_completed'] = True
                        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

    # Display summary if completed
    if st.session_state.icp_data.get('is_completed') and st.session_state.icp_data.get('answers'):
        st.markdown("### Your ICP Profile")
        st.markdown(f"**Knowledge Level:** {st.session_state.icp_data['knowledge_level']}")
        
        st.markdown("**Your Answers:**")
        for q_num in range(1, 6):
            question = get_question_by_knowledge_level(
                st.session_state.icp_data['knowledge_level'],
                q_num
            )
            if question:
                answer = st.session_state.icp_data['answers'].get(f"q{q_num}", "Not answered")
                st.markdown(f"**{question['question']}**")
                if isinstance(answer, list):
                    for item in answer:
                        st.markdown(f"- {item}")
                else:
                    st.markdown(f"{answer}")
