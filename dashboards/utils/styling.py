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
    
    [data-testid="stMetric"] label,
    [data-testid="stMetric"] label *,
    [data-testid="stMetric"] [data-testid="stMetricLabel"],
    [data-testid="stMetric"] [data-testid="stMetricLabel"] * {
        color: #aeb0b5 !important;
        font-weight: 400 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"],
    [data-testid="stMetric"] [data-testid="stMetricValue"] *,
    [data-testid="stMetric"] [data-testid="stMetricValue"] div,
    [data-testid="stMetric"] [data-testid="stMetricValue"] span {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"],
    [data-testid="stMetric"] [data-testid="stMetricDelta"] * {
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
    
    /* All selectbox styling - both sidebar and main content */
    [data-baseweb="select"],
    [data-baseweb="select"] > div,
    [data-baseweb="select"] [role="button"] {
        background-color: white !important;
    }
    
    [data-baseweb="select"] div,
    [data-baseweb="select"] span,
    [data-baseweb="select"] input,
    [data-baseweb="select"] [role="button"] {
        color: #212121 !important;
        background-color: white !important;
    }
    
    [data-baseweb="select"] svg {
        fill: #212121 !important;
    }
    
    /* Dropdown menu items */
    [role="listbox"],
    [role="listbox"] ul,
    [role="listbox"] li,
    [role="option"] {
        background-color: white !important;
        color: #212121 !important;
    }
    
    [role="option"]:hover,
    [role="option"][aria-selected="true"] {
        background-color: #e0e0e0 !important;
        color: #212121 !important;
    }
    
    /* Force all text in dropdown to be visible */
    [role="listbox"] *,
    [role="option"] * {
        color: #212121 !important;
    }
    
    /* Info box styling */
    .stAlert {
        background-color: #e7f2f8 !important;
        border: 1px solid #0071bc !important;
        color: #212121 !important;
    }
    
    .stAlert p,
    .stAlert span,
    .stAlert div {
        color: #212121 !important;
    }
    
    /* Sidebar divider */
    section[data-testid="stSidebar"] hr {
        border-color: #aeb0b5 !important;
    }
    
    /* Expander styling */
    [data-testid="stExpander"] {
        border: 1px solid #d6d7d9 !important;
        background-color: white !important;
    }
    
    [data-testid="stExpander"] summary {
        background-color: #112e51 !important;
    }
    
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span {
        color: white !important;
    }
    
    /* Expander content area - force white background and dark text */
    [data-testid="stExpander"] > div:not(summary),
    [data-testid="stExpander"] [data-testid="stExpanderDetails"],
    [data-testid="stExpander"] [data-testid="stVerticalBlock"] {
        background-color: white !important;
    }
    
    /* All text inside expander CONTENT (not summary) should be dark - EXCEPT metric labels */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMarkdownContainer"] strong,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] .stCheckbox label {
        color: #212121 !important;
    }
    
    /* Labels inside expanders - but NOT metric labels */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] label:not([data-testid="stMetric"] label):not([data-testid="stMetric"] *) {
        color: #212121 !important;
    }
    
    /* Subheaders inside expander content - but NOT inside metrics */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] h1:not([data-testid="stMetric"] h1),
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] h2:not([data-testid="stMetric"] h2),
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] h3:not([data-testid="stMetric"] h3) {
        color: #112e51 !important;
    }
    
    /* Ensure ALL metric components inside expanders have proper colors - highest specificity */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMetric"],
    [data-testid="stExpander"] [data-testid="stMetric"] {
        background-color: #112e51 !important;
    }
    
    /* Metric labels - light gray on dark background */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMetric"] label,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMetric"] [data-testid="stMetricLabel"],
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMetric"] [data-testid="stMetricLabel"] *,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMetric"] [data-testid="stMetricLabel"] div,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMetric"] [data-testid="stMetricLabel"] span,
    [data-testid="stExpander"] [data-testid="stMetric"] label,
    [data-testid="stExpander"] [data-testid="stMetric"] [data-testid="stMetricLabel"],
    [data-testid="stExpander"] [data-testid="stMetric"] [data-testid="stMetricLabel"] *,
    [data-testid="stExpander"] [data-testid="stMetric"] [data-testid="stMetricLabel"] div,
    [data-testid="stExpander"] [data-testid="stMetric"] [data-testid="stMetricLabel"] span {
        color: #aeb0b5 !important;
        background-color: transparent !important;
    }
    
    /* Metric values - white on dark background */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMetric"] [data-testid="stMetricValue"],
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMetric"] [data-testid="stMetricValue"] *,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMetric"] [data-testid="stMetricValue"] div,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMetric"] [data-testid="stMetricValue"] span,
    [data-testid="stExpander"] [data-testid="stMetric"] [data-testid="stMetricValue"],
    [data-testid="stExpander"] [data-testid="stMetric"] [data-testid="stMetricValue"] *,
    [data-testid="stExpander"] [data-testid="stMetric"] [data-testid="stMetricValue"] div,
    [data-testid="stExpander"] [data-testid="stMetric"] [data-testid="stMetricValue"] span {
        color: white !important;
        background-color: transparent !important;
    }
    
    /* Metric deltas - green */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMetric"] [data-testid="stMetricDelta"],
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMetric"] [data-testid="stMetricDelta"] *,
    [data-testid="stExpander"] [data-testid="stMetric"] [data-testid="stMetricDelta"],
    [data-testid="stExpander"] [data-testid="stMetric"] [data-testid="stMetricDelta"] * {
        color: #2e8540 !important;
        background-color: transparent !important;
    }
    
    /* Caption text inside expander content */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stCaptionContainer"],
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] .stCaption {
        color: #5a5a5a !important;
    }
    
    /* Multiselect inside expander content */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMultiSelect"] label,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] .stMultiSelect label {
        color: #212121 !important;
    }
    
    /* Table headers and data inside expander content */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] table,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] table th,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] table td,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stDataFrame"],
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stDataFrame"] * {
        color: #212121 !important;
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
        color: #112e51 !important;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] * {
        color: #112e51 !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #112e51 !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"],
    .stTabs [data-baseweb="tab"][aria-selected="true"] *,
    .stTabs [data-baseweb="tab"][aria-selected="true"] button,
    .stTabs [data-baseweb="tab"][aria-selected="true"] p,
    .stTabs [data-baseweb="tab"][aria-selected="true"] span,
    .stTabs [data-baseweb="tab"][aria-selected="true"] div,
    .stTabs button[aria-selected="true"],
    .stTabs button[aria-selected="true"] *,
    .stTabs button[aria-selected="true"] p,
    .stTabs button[aria-selected="true"] span,
    .stTabs button[aria-selected="true"] div {
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
