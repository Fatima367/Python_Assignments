import streamlit as st
import time
from prompt_builder import PromptBuilder
from gemini_integration import enhance_prompt_with_gemini
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="AI Prompt Builder",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: normal;
        color: #888;
        margin-bottom: 2rem;
    }
    .prompt-box {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
        border: 1px solid #dee2e6;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
for key, default in {
    'answers': {},
    'current_step': 0,
    'generated_prompt': "",
    'selected_use_case': "",
    'use_gemini': False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


builder = PromptBuilder()
use_cases = builder.get_use_cases()

# Header
st.markdown('<div class="main-header">AI Prompt Builder</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Create effective prompts for AI tools based on your needs</div>', unsafe_allow_html=True)

import os
if st.session_state.use_gemini:
    if not os.getenv("GOOGLE_API_KEY"):
        st.warning("⚠️ GOOGLE_API_KEY not found. Please add it to your .env.local file.")
    else:
        st.info("🔐 Using Gemini API via GOOGLE_API_KEY from .env.local.")

# Main Logic
if not st.session_state.generated_prompt:
    use_case_options = {uc.name: uc_id for uc_id, uc in use_cases.items()}
    selected_use_case_name = st.selectbox(
        "Select what you want to create",
        options=[""] + list(use_case_options.keys()),
        index=0
    )

    if selected_use_case_name:
        selected_use_case_id = use_case_options[selected_use_case_name]

        if st.session_state.selected_use_case != selected_use_case_id:
            st.session_state.selected_use_case = selected_use_case_id
            st.session_state.current_step = 0
            st.session_state.answers = {}
            st.session_state.generated_prompt = ""
            st.rerun()

        use_case = use_cases[selected_use_case_id]
        questions = use_case.questions

        if questions and 0 <= st.session_state.current_step < len(questions):
            question = questions[st.session_state.current_step]
            st.subheader(f"Step {st.session_state.current_step + 1} of {len(questions)}")

            if question['type'] == 'text':
                user_input = st.text_input(
                    question['label'],
                    value=st.session_state.answers.get(question['id'], ""),
                    key=f"input_{question['id']}"
                )
            elif question['type'] == 'text_area':
                user_input = st.text_area(
                    question['label'],
                    value=st.session_state.answers.get(question['id'], ""),
                    height=150,
                    key=f"textarea_{question['id']}"
                )
            elif question['type'] == 'select':
                user_input = st.selectbox(
                    question['label'],
                    options=question['options'],
                    index=0 if question['id'] not in st.session_state.answers
                    else question['options'].index(st.session_state.answers[question['id']]),
                    key=f"select_{question['id']}"
                )

            st.session_state.answers[question['id']] = user_input

            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.current_step > 0 and st.button("← Previous"):
                    st.session_state.current_step -= 1
                    st.rerun()

            with col2:
                next_disabled = not st.session_state.answers.get(question['id'])
                if st.session_state.current_step < len(questions) - 1:
                    if st.button("Next →", disabled=next_disabled):
                        st.session_state.current_step += 1
                        st.rerun()
                else:
                    # Final step: show Gemini option and generate button
                    st.session_state.use_gemini = st.checkbox("Enhance with Google Gemini AI", value=st.session_state.use_gemini)
                    # st.info("Note: Requires GOOGLE_API_KEY set in .env.local") if st.session_state.use_gemini else None
                    if st.button("Generate Prompt", disabled=not next_disabled == False):
                        with st.spinner("Generating your prompt..."):
                            base_prompt = builder.build_prompt(
                                st.session_state.selected_use_case,
                                st.session_state.answers
                            )
                            if st.session_state.use_gemini:
                                enhanced = enhance_prompt_with_gemini(
                                    st.session_state.selected_use_case,
                                    st.session_state.answers,
                                    base_prompt
                                )
                                if enhanced:
                                    st.session_state.generated_prompt = enhanced
                                else:
                                    st.warning("Gemini enhancement failed. Showing base prompt.")
                                    st.session_state.generated_prompt = base_prompt
                            else:
                                st.session_state.generated_prompt = base_prompt
                            st.rerun()
else:
    # Display final result
    st.subheader("Your Generated Prompt")
    st.markdown(f'<div class="prompt-box">{st.session_state.generated_prompt}</div>', unsafe_allow_html=True)

    st.download_button("📄 Download Prompt", st.session_state.generated_prompt, "prompt.txt")

    if st.button("🔁 Create New Prompt"):
        for key in ['generated_prompt', 'answers', 'selected_use_case']:
            st.session_state[key] = ""
        st.session_state.current_step = 0
        st.rerun()

st.markdown("---")
st.markdown("Built with ❤️ using Python and Streamlit")