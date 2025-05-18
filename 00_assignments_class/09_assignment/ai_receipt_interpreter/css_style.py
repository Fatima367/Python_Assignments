import streamlit as st

def custom_css():
    st.markdown("""
        <style>
        /* Header styling */
        .receipt-header {
            font-size: 2.5rem !important;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 0.5rem;
            letter-spacing: 1px;
        }
        /* User info row */
        .user-info-row {
            display: flex;
            align-items: center;
            gap: 0.1rem;
            margin-top: 0.3rem;
        }
        .user-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: #cbd5e1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            color: #475569;
            margin-right: 0.5rem;
        }
        /* Receipt card styling */
        .receipt-card {
            background: #f8fafc;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(60,72,88,0.06);
            padding: 1.2rem 1rem 1rem 1rem;
            margin-bottom: 1.2rem;
            border: 1px solid #e2e8f0;
            transition: box-shadow 0.2s;
        }
        .receipt-card:hover {
            box-shadow: 0 4px 16px rgba(60,72,88,0.12);
            border-color: #cbd5e1;
        }
        /* Download button tweaks */
        .stDownloadButton>button {
            background: #4f8cff;
            color: white;
            border-radius: 6px;
            border: none;
            padding: 0.5rem 1.2rem;
            font-weight: 600;
            transition: background 0.2s;
        }
        .stDownloadButton>button:hover {
            background: #2563eb;
        }
        /* Sidebar tweaks */
        .css-1d391kg, .css-1lcbmhc {
            background: #f1f5fa !important;
        }
        .custom-div {
            background: #f8fafc;
            border-radius: 12px; 
            box-shadow: 0 2px 8px rgba(60,72,88,0.06);
            padding: 1.2rem 1rem 1rem 1rem;
            margin-bottom: 1.2rem;
            border: 1px solid #e2e8f0;
            transition: box-shadow 0.2s;
        }
        </style>
    """, unsafe_allow_html=True)
