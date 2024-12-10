import streamlit as st
from utils.session_manager import get_user_state, set_user_state, get_current_user_id
from emotion_engine import EmotionEngine

# Initialize EmotionEngine
emotion_engine = EmotionEngine()

def initialize_icp_state():
    """Initialize ICP session state."""
    user_id = get_current_user_id()
    if user_id and not get_user_state(user_id, "icp_data"):
        set_user_state(user_id, "icp_data", {
            'current_question': 1,
            'answers': {},
            'is_completed': False
        })

def get_question(question_number: int) -> dict:
    """Get questions based on the question number."""
    questions = {
        1: {
            "question": "What challenges do your customers typically face?",
            "type": "text_area",
            "help": "List the main problems your customers are trying to solve."
        },
        2: {
            "question": "Which industries do your customers come from?",
            "type": "multiselect",
            "options": ["Technology", "Healthcare", "Finance", "Education", "Retail", "Manufacturing", "Other"],
            "help": "Select all industries that apply."
        },
        3: {
            "question": "What is your target market's budget range?",
            "type": "select",
            "options": ["Under $1,000", "$1,000-$5,000", "$5,000-$10,000", "$10,000-$50,000", "$50,000+"],
            "help": "Select the typical budget range of your target customers."
        },
        4: {
            "question": "What are your customers' goals and growth objectives?",
            "type": "text_area",
            "help": "Describe your customers' business growth goals."
        },
        5: {
            "question": "How do your customers prefer to communicate?",
            "type": "multiselect",
            "options": ["Email", "Phone", "Video Calls", "In-Person Meetings", "Chat", "Social Media"],
            "help": "Select all preferred communication channels."
        }
    }
    return questions.get(question_number, None)

def calculate_archetype_probabilities(answers: dict) -> dict:
    """Calculate archetype probabilities based on user answers."""
    try:
        # Example of mapping answers to archetype scores
        archetype_scores = {key: 0 for key in emotion_engine.trigger_mappings.keys()}
        if "Technology" in answers.get("q2", []):
            archetype_scores['autonomous'] += 1
        if "$50,000+" in answers.get("q3", ""):
            archetype_scores['impulsive'] += 1

        return emotion_engine.calculate_archetype_alignment(archetype_scores)
    except Exception as e:
        st.error(f"Error calculating archetype probabilities: {e}")
        return {}

def generate_recommendations(archetype_probabilities: dict):
    """Generate keyword and marketing recommendations based on archetypes."""
    st.subheader("Archetype Insights and Recommendations")

    if not archetype_probabilities:
        st.warning("No archetype alignment detected. Consider revisiting the ICP questionnaire or refining your inputs.")
        return

    for archetype, probability in sorted(archetype_probabilities.items(), key=lambda x: x[1], reverse=True):
        st.markdown(f"### {archetype.capitalize()} Archetype")
        st.write(f"**Probability:** {probability:.2f}")

        # Display relevant keywords
        keywords = emotion_engine.trigger_mappings.get(archetype, [])
        if keywords:
            st.markdown(f"**Recommended Keywords:** {', '.join(keywords[:5])}")

        # Provide richer marketing strategies
        if archetype == "autonomous":
            st.write("**Marketing Strategy:** Focus on data-driven content, like case studies or white papers, "
                     "to appeal to logical and achievement-oriented thinkers.")
        elif archetype == "impulsive":
            st.write("**Marketing Strategy:** Leverage urgency-based CTAs like 'Limited Offer' or 'Act Now', "
                     "and emphasize exciting and visually engaging content.")
        elif archetype == "isolative":
            st.write("**Marketing Strategy:** Highlight privacy, comfort, and authenticity in your messaging. "
                     "Use reassuring tones to establish trust.")
        elif archetype == "avoidant":
            st.write("**Marketing Strategy:** Stress stability, reliability, and protection. Use a gentle tone "
                     "to build security and familiarity.")

        # Add visual appeal with separators
        st.markdown("---")

def render_icp_questionnaire():
    """Render the ICP questionnaire."""
    initialize_icp_state()
    user_id = get_current_user_id()

    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    st.image("assets/logoclio.png", width=100)

    icp_data = get_user_state(user_id, "icp_data") or {}
    current_q = icp_data.get('current_question', 1)

    # If the first question is unanswered, offer a fallback option
    if current_q == 1 and not icp_data.get('answers', {}).get("q1"):
        st.markdown("## Define Your ICP")
        st.markdown("If you're unsure about your ICP, click the button below.")

        if st.button("I don't know my ICP"):
            set_user_state(user_id, "icp_data", {
                'current_question': 1,
                'answers': {"q1": "I don't know my ICP"},
                'is_completed': True
            })
            st.success("You can revisit this section later!")
            st.rerun()

    # Show progress bar and question
    st.progress(current_q / 5)
    st.markdown(f"### Question {current_q} / 5")

    # Retrieve the current question data
    question_data = get_question(current_q)
    if question_data:
        st.markdown(f"## {question_data['question']}")
        answer_key = f"q{current_q}"
        current_answer = icp_data.get('answers', {}).get(answer_key, '')

        # Handle different question types
        if question_data['type'] == 'text_area':
            answer = st.text_area("Your answer", value=current_answer, help=question_data['help'])
        elif question_data['type'] == 'select':
            answer = st.selectbox("Select an option", options=question_data['options'],
                                  index=question_data['options'].index(current_answer) if current_answer in question_data['options'] else 0,
                                  help=question_data['help'])
        elif question_data['type'] == 'multiselect':
            answer = st.multiselect("Select all that apply", options=question_data['options'],
                                     default=current_answer if isinstance(current_answer, list) else [],
                                     help=question_data['help'])

        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous", disabled=current_q == 1):
                icp_data['current_question'] -= 1
                set_user_state(user_id, "icp_data", icp_data)
                st.rerun()

        with col2:
            if st.button("Next" if current_q < 5 else "Complete"):
                # Validate that the answer is not empty
                if not answer:
                    st.error("Please provide an answer before proceeding.")
                    return
                # Save the answer and navigate
                icp_data['answers'][answer_key] = answer
                icp_data['current_question'] += 1 if current_q < 5 else 0
                icp_data['is_completed'] = current_q == 5
                set_user_state(user_id, "icp_data", icp_data)
                if current_q == 5:
                    # Generate recommendations upon completion
                    archetype_probabilities = calculate_archetype_probabilities(icp_data['answers'])
                    generate_recommendations(archetype_probabilities)
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
