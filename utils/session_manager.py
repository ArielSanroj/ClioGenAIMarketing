import streamlit as st
from typing import Optional, Any, Dict, List

def initialize_user_session(user_id: str):
    """Initialize user-specific session state variables."""
    prefix = f"user_{user_id}_"

    # Brand values
    if f'{prefix}brand_values' not in st.session_state:
        st.session_state[f'{prefix}brand_values'] = {
            'mission': '',
            'values': [],
            'virtues': [],
            'is_completed': False
        }

    # ICP data
    if f'{prefix}icp_data' not in st.session_state:
        st.session_state[f'{prefix}icp_data'] = {
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

    # Webpage analysis
    if f'{prefix}webpage_analysis' not in st.session_state:
        st.session_state[f'{prefix}webpage_analysis'] = {
            'url': '',
            'analysis': {},
            'is_completed': False
        }

    # Archetype analysis
    if f'{prefix}archetype_analysis' not in st.session_state:
        st.session_state[f'{prefix}archetype_analysis'] = {
            'archetype_scores': {},
            'subscale_matches': [],
            'is_completed': False
        }

    # Navigation and UI state
    if f'{prefix}selected_option' not in st.session_state:
        st.session_state[f'{prefix}selected_option'] = 'content'
    if f'{prefix}show_icp_questionnaire' not in st.session_state:
        st.session_state[f'{prefix}show_icp_questionnaire'] = False
    if f'{prefix}archetype_view' not in st.session_state:
        st.session_state[f'{prefix}archetype_view'] = 'archetypes'

    # Chat state
    if f'{prefix}chat_history' not in st.session_state:
        st.session_state[f'{prefix}chat_history'] = []
    if f'{prefix}current_chat_id' not in st.session_state:
        st.session_state[f'{prefix}current_chat_id'] = None


def get_user_state(user_id: str, key: str, default: Any = None) -> Any:
    """Get user-specific session state value."""
    prefix = f"user_{user_id}_"
    return st.session_state.get(f'{prefix}{key}', default)


def set_user_state(user_id: str, key: str, value: Any):
    """Set user-specific session state value."""
    prefix = f"user_{user_id}_"
    st.session_state[f'{prefix}{key}'] = value


def clear_user_session(user_id: str):
    """Clear all session state variables for a specific user."""
    prefix = f"user_{user_id}_"
    keys_to_remove = [key for key in st.session_state.keys() if key.startswith(prefix)]
    for key in keys_to_remove:
        del st.session_state[key]


def get_current_user_id() -> Optional[str]:
    """Get the current user's ID from session state."""
    return st.session_state.get("user_id")


def save_brand_values(user_id: str, brand_values: Dict):
    """Save brand values to session state."""
    set_user_state(user_id, "brand_values", brand_values)


def save_icp_data(user_id: str, icp_data: Dict):
    """Save ICP data to session state."""
    set_user_state(user_id, "icp_data", icp_data)


def save_webpage_analysis(user_id: str, url: str, analysis: Dict):
    """Save webpage analysis results to session state."""
    set_user_state(user_id, "webpage_analysis", {
        "url": url,
        "analysis": analysis,
        "is_completed": True
    })


def save_archetype_analysis(user_id: str, archetype_scores: Dict, subscale_matches: List[Dict]):
    """Save archetype analysis results to session state."""
    set_user_state(user_id, "archetype_analysis", {
        "archetype_scores": archetype_scores,
        "subscale_matches": subscale_matches,
        "is_completed": True
    })
