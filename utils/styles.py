import streamlit as st


def apply_styles():
    st.markdown("""
    <style>

        /* Main application background */
        .stApp {
            background: #eef3f8;
        }

        .main {
            background: #eef3f8;
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2.5rem;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #172033 0%,
                #10213d 100%
            );
        }

        [data-testid="stSidebar"] * {
            color: white;
        }

        /* Headings */
        h1 {
            color: #172033;
            font-weight: 700;
        }

        h2, h3 {
            color: #263449;
            font-weight: 650;
        }

        /* KPI cards */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid #e2e8f0;
            padding: 18px;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(23, 32, 51, 0.06);
        }

        [data-testid="stMetricLabel"] {
            color: #64748b;
        }

        [data-testid="stMetricValue"] {
            color: #172033;
            font-weight: 700;
        }

        /* Data tables */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }

        /* Alerts / info boxes */
        .stAlert {
            border-radius: 12px;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
        }

        /* Select boxes */
        div[data-baseweb="select"] > div {
            border-radius: 8px;
        }

        /* Dividers */
        hr {
            border-color: #dbe3ec;
        }

    </style>
    """, unsafe_allow_html=True)