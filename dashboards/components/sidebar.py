"""
Sidebar filters component for RMEF Analytics Dashboard
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def render_sidebar(donations_df, elk_df, habitat_df):
    """
    Render sidebar with filters
    
    Args:
        donations_df: Donations dataframe
        elk_df: Elk population dataframe
        habitat_df: Habitat dataframe
    
    Returns:
        Tuple of filtered dataframes (donations_df, elk_df, habitat_df)
    """
    st.sidebar.header("Filters")
    
    # Time period filter
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
    
    return donations_df, elk_df, habitat_df
