"""
RMEF Analytics Dashboard
Interactive Streamlit dashboard for conservation and fundraising metrics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text

# Page configuration
st.set_page_config(
    page_title="RMEF Analytics Dashboard",
    page_icon="elk",
    layout="wide",
    initial_sidebar_state="expanded"
)

# analytics.usa.gov inspired CSS styling
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


@st.cache_resource
def get_db_connection():
    """Create database connection and ensure database exists"""
    db_path = Path(__file__).parent.parent / "data" / "rmef_analytics.db"
    
    # Run ETL pipeline if database doesn't exist (silently)
    if not db_path.exists():
        import logging
        logging.getLogger().setLevel(logging.ERROR)  # Suppress info logs
        try:
            from pipelines.etl_pipeline import RMEFPipeline
            pipeline = RMEFPipeline()
            pipeline.run()
        except Exception as e:
            st.error(f"Error initializing database: {e}")
            raise
        finally:
            logging.getLogger().setLevel(logging.INFO)
    
    return create_engine(f"sqlite:///{db_path}")


@st.cache_data(ttl=300)
def load_donations_data():
    """Load donation data with dimensions"""
    engine = get_db_connection()
    query = """
    SELECT 
        fd.donation_id,
        fd.amount,
        fd.payment_method,
        fd.is_recurring,
        dd.full_date as donation_date,
        dd.year,
        dd.quarter,
        dd.month,
        dd.month_name,
        dn.donor_id,
        dn.first_name,
        dn.last_name,
        dn.donor_type,
        dn.membership_level,
        dn.state as donor_state,
        dc.campaign_id,
        dc.campaign_name,
        dc.campaign_type,
        dc.target_region
    FROM fact_donation fd
    JOIN dim_date dd ON fd.date_key = dd.date_key
    JOIN dim_donor dn ON fd.donor_key = dn.donor_key
    JOIN dim_campaign dc ON fd.campaign_key = dc.campaign_key
    """
    return pd.read_sql(query, engine)


@st.cache_data(ttl=300)
def load_elk_population_data():
    """Load elk population data"""
    engine = get_db_connection()
    query = """
    SELECT 
        fep.year,
        fep.elk_count,
        fep.population_change,
        fep.population_change_pct,
        dh.habitat_id,
        dh.habitat_name,
        dh.state,
        dh.region,
        dh.total_acres,
        dh.habitat_quality_score,
        dh.conservation_status
    FROM fact_elk_population fep
    JOIN dim_habitat dh ON fep.habitat_key = dh.habitat_key
    """
    return pd.read_sql(query, engine)


@st.cache_data(ttl=300)
def load_conservation_data():
    """Load conservation project data"""
    engine = get_db_connection()
    query = """
    SELECT 
        fc.budget,
        fc.spent_to_date,
        fc.acres_protected,
        fc.elk_population_impacted,
        dp.project_id,
        dp.project_name,
        dp.project_type,
        dp.state,
        dp.county,
        dp.status
    FROM fact_conservation fc
    JOIN dim_project dp ON fc.project_key = dp.project_key
    """
    return pd.read_sql(query, engine)


@st.cache_data(ttl=300)
def load_habitat_data():
    """Load habitat dimension data"""
    engine = get_db_connection()
    query = "SELECT * FROM dim_habitat"
    return pd.read_sql(query, engine)


@st.cache_data(ttl=300)
def load_membership_data():
    """Load membership growth data"""
    engine = get_db_connection()
    query = """
    SELECT 
        donor_id,
        first_name,
        last_name,
        email,
        donor_type,
        membership_level,
        join_date,
        state
    FROM dim_donor
    """
    return pd.read_sql(query, engine)


def main():
    # Header banner - analytics.usa.gov style with logo
    logo_path = Path(__file__).parent.parent / "assets" / "rmef-logo.jpg"
    
    # Encode logo as base64 for HTML embedding
    import base64
    logo_html = ""
    if logo_path.exists():
        try:
            with open(logo_path, "rb") as f:
                logo_data = base64.b64encode(f.read()).decode()
                logo_html = f'<img src="data:image/jpeg;base64,{logo_data}" alt="RMEF Logo">'
        except Exception:
            pass
    
    st.markdown(f"""
        <div class="header-banner">
            {logo_html}
            <div class="header-text">
                <h1>RMEF Analytics Dashboard</h1>
                <p>Rocky Mountain Elk Foundation - Conservation & Fundraising Metrics</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data
    try:
        donations_df = load_donations_data()
        elk_df = load_elk_population_data()
        conservation_df = load_conservation_data()
        habitat_df = load_habitat_data()
        membership_df = load_membership_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Please run the ETL pipeline first: `python pipelines/etl_pipeline.py`")
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Time period filter (dropdown)
    time_periods = {
        'All Time': None,
        'Last 7 Days': 7,
        'Last 30 Days': 30,
        'Last 90 Days': 90,
        'Last 6 Months': 180,
        'Last Year': 365,
        'Current Fiscal Year': 'fiscal'
    }
    selected_period = st.sidebar.selectbox("Time Period", list(time_periods.keys()))
    
    # Apply time period filter
    if len(donations_df) > 0:
        donations_df['donation_date'] = pd.to_datetime(donations_df['donation_date'])
        max_date = donations_df['donation_date'].max().date()
        
        period_value = time_periods[selected_period]
        if period_value == 'fiscal':
            # Fiscal year starts October 1
            today = datetime.now().date()
            if today.month >= 10:
                fiscal_start = datetime(today.year, 10, 1).date()
            else:
                fiscal_start = datetime(today.year - 1, 10, 1).date()
            donations_df = donations_df[donations_df['donation_date'].dt.date >= fiscal_start]
        elif period_value is not None:
            cutoff_date = max_date - timedelta(days=period_value)
            donations_df = donations_df[donations_df['donation_date'].dt.date >= cutoff_date]
    
    st.sidebar.markdown("---")
    
    # Campaign type filter
    campaign_types = ['All'] + sorted(donations_df['campaign_type'].unique().tolist())
    selected_campaign_type = st.sidebar.selectbox("Campaign Type", campaign_types)
    if selected_campaign_type != 'All':
        donations_df = donations_df[donations_df['campaign_type'] == selected_campaign_type]
    
    # Donor type filter
    donor_types = ['All'] + sorted(donations_df['donor_type'].unique().tolist())
    selected_donor_type = st.sidebar.selectbox("Donor Type", donor_types)
    if selected_donor_type != 'All':
        donations_df = donations_df[donations_df['donor_type'] == selected_donor_type]
    
    # Region filter
    regions = ['All'] + sorted(elk_df['region'].unique().tolist())
    selected_region = st.sidebar.selectbox("Habitat Region", regions)
    if selected_region != 'All':
        elk_df = elk_df[elk_df['region'] == selected_region]
        habitat_df = habitat_df[habitat_df['region'] == selected_region]
    
    # Key Metrics Row
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_donations = donations_df['amount'].sum()
        st.metric(
            label="Total Donations",
            value=f"${total_donations:,.0f}",
            delta=f"{len(donations_df)} transactions"
        )
    
    with col2:
        total_acres = conservation_df['acres_protected'].sum()
        st.metric(
            label="Acres Protected",
            value=f"{total_acres:,}",
            delta="via conservation projects"
        )
    
    with col3:
        latest_elk = elk_df[elk_df['year'] == elk_df['year'].max()]['elk_count'].sum()
        prev_elk = elk_df[elk_df['year'] == elk_df['year'].max() - 1]['elk_count'].sum()
        elk_change = latest_elk - prev_elk
        st.metric(
            label="Elk Population (2024)",
            value=f"{latest_elk:,}",
            delta=f"{elk_change:+,} from 2023"
        )
    
    with col4:
        total_members = len(membership_df)
        st.metric(
            label="Total Members",
            value=f"{total_members:,}",
            delta="active donors"
        )
    
    # Donation Analytics - Collapsible
    with st.expander("Donation Analytics", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Donations by Campaign Type")
            campaign_donations = donations_df.groupby('campaign_type')['amount'].sum().reset_index()
            campaign_donations = campaign_donations.sort_values('amount', ascending=True)
            
            fig = px.bar(
                campaign_donations,
                x='amount',
                y='campaign_type',
                orientation='h',
                color='amount',
                color_continuous_scale='Blues',
                labels={'amount': 'Total Amount ($)', 'campaign_type': 'Campaign Type'}
            )
            fig.update_layout(
                showlegend=False,
                height=350,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Donations by Donor Type")
            donor_donations = donations_df.groupby('donor_type')['amount'].sum().reset_index()
            
            fig = px.pie(
                donor_donations,
                values='amount',
                names='donor_type',
                color_discrete_sequence=['#112e51', '#205493', '#0071bc', '#4aa3df'],
                hole=0.4
            )
            fig.update_layout(height=350)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    # Membership & Population - Collapsible
    with st.expander("Membership & Population Trends", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Membership Growth Over Time")
            membership_df['join_date'] = pd.to_datetime(membership_df['join_date'])
            membership_df['join_month'] = membership_df['join_date'].dt.to_period('M').astype(str)
            
            monthly_joins = membership_df.groupby('join_month').size().reset_index(name='new_members')
            monthly_joins['cumulative'] = monthly_joins['new_members'].cumsum()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=monthly_joins['join_month'],
                y=monthly_joins['new_members'],
                name='New Members',
                marker_color='#0071bc'
            ))
            fig.add_trace(go.Scatter(
                x=monthly_joins['join_month'],
                y=monthly_joins['cumulative'],
                name='Cumulative',
                mode='lines+markers',
                marker_color='#112e51',
                yaxis='y2'
            ))
            fig.update_layout(
                height=350,
                yaxis=dict(title='New Members'),
                yaxis2=dict(title='Cumulative Members', overlaying='y', side='right'),
                legend=dict(orientation='h', yanchor='bottom', y=1.02),
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Elk Population Trends by Habitat")
            fig = px.line(
                elk_df,
                x='year',
                y='elk_count',
                color='habitat_name',
                markers=True,
                labels={'elk_count': 'Elk Count', 'year': 'Year', 'habitat_name': 'Habitat'}
            )
            fig.update_layout(
                height=350,
                legend=dict(orientation='h', yanchor='bottom', y=-0.5)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Conservation & Habitat - Collapsible
    with st.expander("Conservation & Habitat Analysis", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Conservation Projects by Type")
            project_summary = conservation_df.groupby('project_type').agg({
                'budget': 'sum',
                'spent_to_date': 'sum',
                'acres_protected': 'sum'
            }).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Budget',
                x=project_summary['project_type'],
                y=project_summary['budget'],
                marker_color='#112e51'
            ))
            fig.add_trace(go.Bar(
                name='Spent to Date',
                x=project_summary['project_type'],
                y=project_summary['spent_to_date'],
                marker_color='#0071bc'
            ))
            fig.update_layout(
                barmode='group',
                height=350,
                legend=dict(orientation='h', yanchor='bottom', y=1.02),
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Habitat Quality by Region")
            habitat_quality = habitat_df.groupby('region').agg({
                'habitat_quality_score': 'mean',
                'total_acres': 'sum'
            }).reset_index()
            
            fig = px.scatter(
                habitat_quality,
                x='total_acres',
                y='habitat_quality_score',
                size='total_acres',
                color='region',
                labels={
                    'total_acres': 'Total Acres',
                    'habitat_quality_score': 'Avg Quality Score',
                    'region': 'Region'
                },
                color_discrete_sequence=['#112e51', '#205493', '#0071bc']
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Tables Section - Collapsible
    with st.expander("Detailed Data Views", expanded=False):
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Recent Donations", "Donors", "Conservation Projects", "Habitat Status", "Anomalies"])
        
        with tab1:
            st.subheader("Recent Donations")
            
            # Column selector
            all_donation_cols = {
                'Donation Date': 'donation_date',
                'Donor Type': 'donor_type',
                'Donor Name': 'donor_name',
                'Campaign Name': 'campaign_name',
                'Amount': 'amount',
                'Payment Method': 'payment_method',
                'Recurring': 'is_recurring',
                'State': 'donor_state'
            }
            
            # Add donor name column
            donations_display = donations_df.copy()
            donations_display['donor_name'] = donations_display['first_name'] + ' ' + donations_display['last_name']
            
            # Column selector
            selected_cols = st.multiselect(
                "Columns:",
                options=list(all_donation_cols.keys()),
                default=['Donation Date', 'Donor Type', 'Campaign Name', 'Amount', 'Payment Method'],
                key='don_cols'
            )
            
            if selected_cols:
                display_cols = [all_donation_cols[col] for col in selected_cols]
                recent_donations = donations_display.nlargest(20, 'donation_date')[display_cols].copy()
                
                # Format columns
                if 'donation_date' in display_cols:
                    recent_donations['donation_date'] = recent_donations['donation_date'].dt.strftime('%Y-%m-%d')
                if 'amount' in display_cols:
                    recent_donations['amount'] = recent_donations['amount'].apply(lambda x: f"${x:,.2f}")
                
                # Clean column names (remove underscores, title case)
                recent_donations.columns = [col.replace('_', ' ').title() for col in recent_donations.columns]
                
                st.dataframe(recent_donations, use_container_width=True, hide_index=True, height=400, column_config=None)
            else:
                st.info("Please select at least one column to display.")
        
        with tab2:
            st.subheader("Donor Directory")
            
            # Column selector for donors
            all_donor_cols = {
                'Donor ID': 'donor_id',
                'First Name': 'first_name',
                'Last Name': 'last_name',
                'Email': 'email',
                'Donor Type': 'donor_type',
                'Membership Level': 'membership_level',
                'State': 'state',
                'Join Date': 'join_date'
            }
            
            # Column selector
            selected_donor_cols = st.multiselect(
                "Columns:",
                options=list(all_donor_cols.keys()),
                default=['First Name', 'Last Name', 'Donor Type', 'Membership Level', 'State'],
                key='donor_cols'
            )
            
            if selected_donor_cols:
                display_cols = [all_donor_cols[col] for col in selected_donor_cols]
                donors_display = membership_df[display_cols].copy()
                
                # Format join date if selected
                if 'join_date' in display_cols:
                    donors_display['join_date'] = pd.to_datetime(donors_display['join_date']).dt.strftime('%Y-%m-%d')
                
                # Clean column names
                donors_display.columns = [col.replace('_', ' ').title() for col in donors_display.columns]
                
                st.dataframe(donors_display, use_container_width=True, hide_index=True, height=400, column_config=None)
            else:
                st.info("Please select at least one column to display.")
    
        with tab3:
            st.subheader("Conservation Projects")
            
            # Column selector for projects
            all_project_cols = {
                'Project Name': 'project_name',
                'Project Type': 'project_type',
                'State': 'state',
                'Status': 'status',
                'Budget': 'budget',
                'Spent To Date': 'spent_to_date',
                'Acres Protected': 'acres_protected',
                'Elk Population Impacted': 'elk_population_impacted'
            }
            
            # Column selector
            selected_project_cols = st.multiselect(
                "Columns:",
                options=list(all_project_cols.keys()),
                default=['Project Name', 'Project Type', 'State', 'Status', 'Budget', 'Acres Protected'],
                key='project_cols'
            )
            
            if selected_project_cols:
                display_cols = [all_project_cols[col] for col in selected_project_cols]
                projects_display = conservation_df[display_cols].copy()
                
                # Format currency columns
                if 'budget' in display_cols:
                    projects_display['budget'] = projects_display['budget'].apply(lambda x: f"${x:,.0f}")
                if 'spent_to_date' in display_cols:
                    projects_display['spent_to_date'] = projects_display['spent_to_date'].apply(lambda x: f"${x:,.0f}")
                
                # Clean column names
                projects_display.columns = [col.replace('_', ' ').title() for col in projects_display.columns]
                
                st.dataframe(projects_display, use_container_width=True, hide_index=True, height=400, column_config=None)
            else:
                st.info("Please select at least one column to display.")
        
        with tab4:
            st.subheader("Habitat Status")
            
            # Column selector for habitat
            all_habitat_cols = {
                'Habitat Name': 'habitat_name',
                'State': 'state',
                'Region': 'region',
                'Total Acres': 'total_acres',
                'Quality Score': 'habitat_quality_score',
                'Conservation Status': 'conservation_status'
            }
            
            # Column selector
            selected_habitat_cols = st.multiselect(
                "Columns:",
                options=list(all_habitat_cols.keys()),
                default=['Habitat Name', 'State', 'Region', 'Quality Score', 'Conservation Status'],
                key='habitat_cols'
            )
            
            if selected_habitat_cols:
                display_cols = [all_habitat_cols[col] for col in selected_habitat_cols]
                habitat_display = habitat_df[display_cols].copy()
                
                # Format acres
                if 'total_acres' in display_cols:
                    habitat_display['total_acres'] = habitat_display['total_acres'].apply(lambda x: f"{x:,}")
                
                # Clean column names
                habitat_display.columns = [col.replace('_', ' ').title() for col in habitat_display.columns]
                
                st.dataframe(habitat_display, use_container_width=True, hide_index=True, height=400, column_config=None)
            else:
                st.info("Please select at least one column to display.")
        
        with tab5:
            st.subheader("Anomaly Detection")
            
            # Large donations
            large_donations = donations_df[donations_df['amount'] > 10000][
                ['donation_date', 'donor_type', 'campaign_name', 'amount']
            ].copy()
            large_donations['donation_date'] = large_donations['donation_date'].dt.strftime('%Y-%m-%d')
            large_donations['amount'] = large_donations['amount'].apply(lambda x: f"${x:,.2f}")
            
            # Clean column names
            large_donations.columns = [col.replace('_', ' ').title() for col in large_donations.columns]
            
            if len(large_donations) > 0:
                st.markdown("**Large Donations (>$10,000)**")
                st.dataframe(large_donations, use_container_width=True, hide_index=True)
            
            # At-risk habitats
            at_risk = habitat_df[habitat_df['conservation_status'] == 'At Risk'][
                ['habitat_name', 'state', 'habitat_quality_score', 'conservation_status']
            ].copy()
            
            # Clean column names
            at_risk.columns = [col.replace('_', ' ').title() for col in at_risk.columns]
            
            if len(at_risk) > 0:
                st.markdown("**At-Risk Habitats**")
                st.dataframe(at_risk, use_container_width=True, hide_index=True)
            
            # Population declines
            declining = elk_df[elk_df['population_change'] < 0][
                ['habitat_name', 'year', 'elk_count', 'population_change', 'population_change_pct']
            ].copy()
            
            # Clean column names
            declining.columns = [col.replace('_', ' ').title() for col in declining.columns]
            
            if len(declining) > 0:
                st.markdown("**Habitats with Population Decline**")
                st.dataframe(declining, use_container_width=True, hide_index=True)
    
    # Footer - analytics.usa.gov style
    st.markdown(
        """
        <div class="footer">
            <p style="margin: 0;">RMEF Analytics Sandbox | Data refreshed: """ + datetime.now().strftime('%Y-%m-%d %H:%M') + """</p>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem;">Supporting elk conservation and habitat protection across the Rocky Mountain West</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
