"""
CSS styling for RMEF Analytics Dashboard
Analytics.usa.gov inspired theme
"""

import streamlit as st


def apply_custom_css():
    """Apply custom CSS styling to the dashboard"""
    st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main app background */
    .stApp {
        background-color: #f9f9f9;
    }
    
    /* Header banner styling */
    .header-banner {
        background-color: #112e51;
        color: white;
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 1.5rem -1rem;
        text-align: left;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .header-banner img {
        height: 80px;
        width: auto;
    }
    
    .header-banner .header-text h1 {
        color: white !important;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        font-family: 'Source Sans Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    .header-banner .header-text p {
        color: #aeb0b5;
        margin: 0.25rem 0 0 0;
        font-size: 1rem;
    }
    
    /* Big number KPI styling - analytics.usa.gov style */
    .big-number {
        background-color: #112e51;
        color: white;
        padding: 1.5rem;
        border-radius: 0;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .big-number .value {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        line-height: 1;
    }
    
    .big-number .label {
        font-size: 0.9rem;
        color: #aeb0b5;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }
    
    .big-number .delta {
        font-size: 0.85rem;
        color: #2e8540;
        margin-top: 0.25rem;
    }
    
    /* Streamlit metric override */
    [data-testid="stMetric"] {
        background-color: #112e51 !important;
        padding: 1.5rem !important;
        border-radius: 0 !important;
        border: none !important;
    }
    
    [data-testid="stMetric"] label {
        color: #aeb0b5 !important;
        font-weight: 400 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #2e8540 !important;
    }
    
    /* Section headers */
    .section-header {
        color: #112e51;
        font-size: 1.25rem;
        font-weight: 600;
        border-bottom: 2px solid #112e51;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Popover button - force white background always */
    button[data-testid="baseButton-secondary"] {
        background-color: white !important;
        background: white !important;
        color: #212121 !important;
        border: 1px solid #d6d7d9 !important;
        padding: 0.35rem 0.75rem !important;
        border-radius: 4px !important;
        font-weight: 400 !important;
        font-size: 0.875rem !important;
        box-shadow: none !important;
        transition: none !important;
    }
    
    button[data-testid="baseButton-secondary"]:hover,
    button[data-testid="baseButton-secondary"]:focus,
    button[data-testid="baseButton-secondary"]:active,
    button[data-testid="baseButton-secondary"]:visited,
    button[data-testid="baseButton-secondary"][aria-expanded="true"] {
        background-color: white !important;
        background: white !important;
        color: #212121 !important;
        border: 1px solid #d6d7d9 !important;
        box-shadow: none !important;
    }
    
    /* Popover dropdown - target all nested containers */
    [data-testid="stPopover"],
    [data-testid="stPopover"] > div,
    [data-testid="stPopover"] > div > div,
    [data-testid="stPopover"] > div > div > div,
    [data-testid="stPopover"] [data-testid="stVerticalBlock"],
    [data-testid="stPopover"] [data-testid="stVerticalBlock"] > div,
    [data-testid="stPopover"] [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stPopover"] [data-testid="element-container"],
    [data-testid="stPopover"] [data-testid="column"],
    [data-testid="stPopover"] [class*="st"],
    [data-testid="stPopover"] * {
        background-color: white !important;
        background-image: none !important;
        background: white !important;
    }
    
    [data-testid="stPopover"] > div {
        border: 1px solid #d6d7d9 !important;
        border-radius: 4px !important;
        padding: 0.75rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        min-width: 200px !important;
    }
    
    /* Force all text elements to dark color */
    [data-testid="stPopover"] *,
    [data-testid="stPopover"] p,
    [data-testid="stPopover"] span,
    [data-testid="stPopover"] div,
    [data-testid="stPopover"] label,
    [data-testid="stPopover"] input {
        color: #212121 !important;
    }
    
    [data-testid="stPopover"] [data-testid="stMarkdownContainer"] p {
        margin: 0 0 0.5rem 0 !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    /* Checkbox styling */
    [data-testid="stPopover"] .stCheckbox,
    [data-testid="stPopover"] .stCheckbox > div,
    [data-testid="stPopover"] .stCheckbox > label {
        padding: 0.25rem 0 !important;
        margin: 0 !important;
    }
    
    [data-testid="stPopover"] .stCheckbox label {
        color: #212121 !important;
        font-size: 0.875rem !important;
    }
    
    /* Sidebar - match dashboard theme */
    section[data-testid="stSidebar"] {
        background-color: #112e51 !important;
    }
    
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] > div > div,
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"],
    section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"],
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stSelectbox > div,
    section[data-testid="stSidebar"] .block-container {
        background-color: #112e51 !important;
        cursor: default !important;
    }
    
    /* All sidebar text white */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] div {
        color: white !important;
        cursor: default !important;
    }
    
    /* Prevent text cursor on all sidebar elements */
    section[data-testid="stSidebar"] * {
        cursor: default !important;
    }
    
    /* Only allow pointer cursor on interactive elements */
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] [role="button"],
    section[data-testid="stSidebar"] [data-baseweb="select"],
    section[data-testid="stSidebar"] a {
        cursor: pointer !important;
    }
    
    /* Sidebar header */
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
        color: white !important;
        border-bottom: 1px solid #aeb0b5;
        padding-bottom: 0.5rem;
    }
    
    /* Sidebar selectbox - white background with dark text */
    section[data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: white !important;
        border-radius: 4px;
    }
    
    section[data-testid="stSidebar"] [data-baseweb="select"] div,
    section[data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #212121 !important;
        background-color: white !important;
    }
    
    section[data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: #212121 !important;
    }
    
    /* Dropdown popover menu */
    [data-baseweb="popover"],
    [data-baseweb="popover"] ul,
    [data-baseweb="popover"] li {
        background-color: white !important;
        color: #212121 !important;
    }
    
    [data-baseweb="popover"] li:hover {
        background-color: #e0e0e0 !important;
    }
    
    /* Sidebar divider */
    section[data-testid="stSidebar"] hr {
        border-color: #aeb0b5 !important;
    }
    
    /* Expander styling */
    [data-testid="stExpander"] {
        border: 1px solid #d6d7d9 !important;
    }
    
    [data-testid="stExpander"] summary {
        background-color: #112e51 !important;
    }
    
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span {
        color: white !important;
    }
    
    /* Chart containers */
    .chart-container {
        background-color: white;
        padding: 1rem;
        border: 1px solid #d6d7d9;
        margin-bottom: 1rem;
    }
    
    /* Subheader styling */
    .stSubheader {
        color: #112e51 !important;
        font-weight: 600 !important;
    }
    
    h3 {
        color: #112e51 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f1f1;
        border: 1px solid #d6d7d9;
        color: #112e51;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #112e51 !important;
        color: white !important;
    }
    
    /* Footer */
    .footer {
        background-color: #112e51;
        color: #aeb0b5;
        padding: 1rem;
        text-align: center;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)
