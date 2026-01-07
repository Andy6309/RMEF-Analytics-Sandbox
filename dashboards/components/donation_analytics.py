"""
Donation Analytics Component
"""

import streamlit as st
import plotly.express as px


def render_donation_analytics(donations_df):
    """Render donation analytics section"""
    
    with st.expander("Donation Analytics", expanded=False):
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
            fig.update_layout(showlegend=False, height=350, coloraxis_showscale=False)
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
