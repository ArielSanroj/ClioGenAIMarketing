import streamlit as st
from utils.session_manager import get_user_state, set_user_state, get_current_user_id

def initialize_icp_state():
    """Initialize ICP session state"""
    user_id = get_current_user_id()
    if not get_user_state(user_id, "icp_data"):
        set_user_state(user_id, "icp_data", {
            'knowledge_level': '',
            'current_question': 1,
            'demographics': {},
            'psychographics': {},
            'archetype': '',
            'pain_points': [],
            'goals': [],
            'answers': {},
            'is_completed': False
        })

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
    user_id = get_current_user_id()
    
    # Add custom styles for back button
    st.markdown("""
        <style>
        .back-button {
            background-color: transparent;
            color: #1E1B4B;
            border: 1px solid #1E1B4B;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s;
            margin-bottom: 1rem;
        }
        .back-button:hover {
            background-color: #F3F4F6;
            transform: translateY(-1px);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Center align the content
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    
    # Show logo
    st.image("logoclio.png", width=100)
    
    if not get_user_state(user_id, "icp_data").get('knowledge_level'):
        st.markdown("## What is your current level of ICP knowledge?")
        
        knowledge_levels = [
            "I don't know my ICP yet",
            "I know my ICP",
            "I want to refine my existing ICP"
        ]
        
        for level in knowledge_levels:
            if st.button(level):
                set_user_state(user_id, "icp_data", {
                    **get_user_state(user_id, "icp_data"),
                    'knowledge_level': level,
                    'current_question': 1
                })
                st.rerun()
        
        if st.button("Skip", type="secondary"):
            # Update session state to skip ICP and navigate to market analysis
            set_user_state(user_id, "icp_data", {
                'knowledge_level': '',
                'current_question': 1,
                'answers': {},
                'is_completed': True
            })
            set_user_state(user_id, "selected_option", "market_analysis")
            st.rerun()
    
    else:
        # Show progress
        current_q = get_user_state(user_id, "icp_data").get('current_question', 1)
        st.progress(current_q / 5)
        st.markdown(f"{current_q} / 5 questions")
        
        # Show back button at the top
        st.markdown("""
            <button class="back-button" onclick="javascript:document.querySelector('[data-testid="stForm"] button.back-btn').click();">
                ← Go Back
            </button>
        """, unsafe_allow_html=True)
        
        # Get current question
        question_data = get_question_by_knowledge_level(
            get_user_state(user_id, "icp_data").get('knowledge_level'),
            current_q
        )
        
        if question_data:
            st.markdown(f"## {question_data['question']}")
            
            # Render appropriate input based on question type
            answer_key = f"q{current_q}"
            current_answer = get_user_state(user_id, "icp_data").get('answers', {}).get(answer_key, '')
            
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
                if st.button("Previous", disabled=current_q == 1, key="back-btn"):
                    icp_data = get_user_state(user_id, "icp_data")
                    icp_data['answers'][answer_key] = answer
                    if current_q > 1:
                        icp_data['current_question'] -= 1
                    else:
                        icp_data['knowledge_level'] = ''
                    set_user_state(user_id, "icp_data", icp_data)
                    st.rerun()
            
            with col2:
                if current_q < 5:
                    if st.button("Next", type="primary"):
                        icp_data = get_user_state(user_id, "icp_data")
                        icp_data['answers'][answer_key] = answer
                        icp_data['current_question'] += 1
                        set_user_state(user_id, "icp_data", icp_data)
                        st.rerun()
                else:
                    if st.button("Complete", type="primary"):
                        icp_data = get_user_state(user_id, "icp_data")
                        icp_data['answers'][answer_key] = answer
                        icp_data['is_completed'] = True
                        set_user_state(user_id, "icp_data", icp_data)
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
