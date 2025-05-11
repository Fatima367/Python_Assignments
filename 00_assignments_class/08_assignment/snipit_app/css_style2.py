import streamlit as st

def load_css():
    st.markdown("""
    <style>
    /* Existing styles */
    .main {
        padding: 2rem;
    }
    /* ... (other styles) ... */
    
    /* New CSS to hide GitHub elements */
    .github-icon {
        display: none;
    }
    #fork-button {
        display: none;
    }
    /* Add more selectors as needed */
    </style>
    """, unsafe_allow_html=True)