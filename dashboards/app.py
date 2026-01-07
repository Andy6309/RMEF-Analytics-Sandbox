"""
RMEF Analytics Dashboard
Interactive Streamlit dashboard for conservation and fundraising metrics
Refactored for better maintainability and modularity
"""

import streamlit as st
import sys
from pathlib import Path
import base64

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import utilities
from dashboards.utils.styling import apply_custom_css
from dashboards.utils.data_loaders import (
    load_donations_data,
    load_elk_population_data,
    load_conservation_data,
    load_habitat_data,
    load_membership_data
)

# Import components
from dashboards.components.sidebar import render_sidebar
from dashboards.components.membership_analytics import render_membership_analytics
from dashboards.components.donation_analytics import render_donation_analytics
from dashboards.components.elk_population import render_elk_population
from dashboards.components.conservation_habitat import render_conservation_habitat
from dashboards.components.data_tables import render_data_tables

# Page configuration
st.set_page_config(
    page_title="RMEF Analytics Dashboard",
    page_icon="elk",
    layout="wide",
    initial_sidebar_state="expanded"
)


def render_header():
    """Render dashboard header with logo"""
    logo_path = Path(__file__).parent.parent / "assets" / "rmef-logo.jpg"
    
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


def render_kpis(donations_df, membership_df, elk_df, conservation_df):
    """Render key performance indicators"""
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_donations = donations_df['amount'].sum()
        st.metric(
            label="Total Donations",
            value=f"${total_donations:,.0f}"
        )
    
    with col2:
        total_members = len(membership_df)
        st.metric(
            label="Total Members",
            value=f"{total_members:,}"
        )
    
    with col3:
        if len(elk_df) > 0:
            latest_year = elk_df['year'].max()
            total_elk = elk_df[elk_df['year'] == latest_year]['elk_count'].sum()
            st.metric(
                label=f"Elk Population ({latest_year})",
                value=f"{total_elk:,}"
            )
    
    with col4:
        total_acres = conservation_df['acres_protected'].sum()
        st.metric(
            label="Acres Protected",
            value=f"{total_acres:,.0f}"
        )
    
    st.markdown("---")


def main():
    """Main dashboard application"""
    
    # Apply custom styling
    apply_custom_css()
    
    # Render header
    render_header()
    
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
    
    # Render sidebar filters (returns filtered dataframes)
    donations_df, elk_df, habitat_df, membership_df, conservation_df = render_sidebar(
        donations_df, elk_df, habitat_df, membership_df, conservation_df
    )
    
    # Render KPIs (now using filtered data)
    render_kpis(donations_df, membership_df, elk_df, conservation_df)
    
    # Render main components
    render_membership_analytics(membership_df)
    render_donation_analytics(donations_df)
    render_elk_population(elk_df)
    render_conservation_habitat(conservation_df, habitat_df)
    render_data_tables(donations_df, membership_df, conservation_df, habitat_df)
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>RMEF Analytics Dashboard | Data updated in real-time from conservation database</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
