"""
Sidebar filters component for RMEF Analytics Dashboard
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def render_sidebar(donations_df, elk_df, habitat_df, membership_df, conservation_df):
    """
    Render sidebar with filters
    
    Args:
        donations_df: Donations dataframe
        elk_df: Elk population dataframe
        habitat_df: Habitat dataframe
        membership_df: Membership dataframe
        conservation_df: Conservation dataframe
    
    Returns:
        Tuple of filtered dataframes (donations_df, elk_df, habitat_df, membership_df, conservation_df)
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
    
    # Apply time period filter to ALL data
    period_value = time_periods[selected_period]
    
    if period_value is not None:
        # Determine cutoff date
        if period_value == 'fiscal':
            today = datetime.now().date()
            if today.month >= 10:
                cutoff_date = datetime(today.year, 10, 1).date()
            else:
                cutoff_date = datetime(today.year - 1, 10, 1).date()
        else:
            # Use max date from donations as reference
            if len(donations_df) > 0:
                donations_df['donation_date'] = pd.to_datetime(donations_df['donation_date'])
                max_date = donations_df['donation_date'].max().date()
                cutoff_date = max_date - timedelta(days=period_value)
            else:
                cutoff_date = datetime.now().date() - timedelta(days=period_value)
        
        # Filter donations by donation_date
        if len(donations_df) > 0:
            donations_df['donation_date'] = pd.to_datetime(donations_df['donation_date'])
            donations_df = donations_df[donations_df['donation_date'].dt.date >= cutoff_date]
        
        # Filter membership by join_date
        if len(membership_df) > 0:
            membership_df['join_date'] = pd.to_datetime(membership_df['join_date'])
            membership_df = membership_df[membership_df['join_date'].dt.date >= cutoff_date]
        
        # Filter elk population by year (convert cutoff_date to year)
        if len(elk_df) > 0:
            cutoff_year = cutoff_date.year
            elk_df = elk_df[elk_df['year'] >= cutoff_year]
        
        # Note: Conservation projects and habitat data don't have time dimensions,
        # so they remain unfiltered by time period
    
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
        conservation_df = conservation_df[conservation_df['state'].isin(habitat_df['state'].unique())]
    
    return donations_df, elk_df, habitat_df, membership_df, conservation_df
