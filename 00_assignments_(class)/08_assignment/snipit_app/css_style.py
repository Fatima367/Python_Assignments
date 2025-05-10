import streamlit as st
# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .note-card {
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        position: relative;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .note-card:hover {
        transform: translateY(-5px);
    }
    .note-actions {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
    }
    .note-action-icon {
        cursor: pointer;
        font-size: 18px;
        color: #555;
    }
    .note-action-icon:hover {
        color: #000;
    }
    .hero-container {
        text-align: center;
        padding: 2rem 0;
    }
    .cards-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    .card:hover {
        transform: translateY(-10px);
    }
    .card-icon {
        font-size: 48px;
        color: #3498db;
        margin-bottom: 1rem;
    }
    footer {
        text-align: center;
        padding: 1rem 0;
        margin-top: 2rem;
        border-top: 1px solid #eee;
    }
    .home-button {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    .stButton button {
        width: 100%;
    }
    .category-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    .category-card:hover {
        transform: translateY(-5px);
    }
    .cheat-code-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        border: 1px solid #dee2e6;
    }
    .action-button {
        margin-top: 10px;
        margin-right: 10px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #e6f7ff;
        border-left: 5px solid #1890ff;
    }
    .chat-message.assistant {
        background-color: #f6ffed;
        border-left: 5px solid #52c41a;
    }
    .chat-message .content {
        margin-top: 0.5rem;
    }
    .chat-input {
        display: flex;
        padding: 1rem;
        background-color: white;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)