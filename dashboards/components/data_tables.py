"""
Data Tables Component
"""

import streamlit as st
import pandas as pd


def render_data_tables(donations_df, membership_df, conservation_df, habitat_df):
    """Render detailed data tables section"""
    
    with st.expander("Detailed Data Views", expanded=False):
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Recent Donations",
            "Donor Directory",
            "Conservation Projects",
            "Habitat Areas",
            "Anomaly Detection"
        ])
        
        with tab1:
            st.subheader("Recent Donations")
            
            all_donation_cols = {
                'Donation Date': 'donation_date',
                'Donor Name': 'donor_name',
                'Donor Type': 'donor_type',
                'Campaign Name': 'campaign_name',
                'Campaign Type': 'campaign_type',
                'Amount': 'amount',
                'Payment Method': 'payment_method',
                'Recurring': 'is_recurring',
                'State': 'donor_state'
            }
            
            donations_display = donations_df.copy()
            donations_display['donor_name'] = donations_display['first_name'] + ' ' + donations_display['last_name']
            
            if len(donations_display) > 0:
                donations_display['donation_date'] = pd.to_datetime(donations_display['donation_date'])
            
            selected_cols = st.multiselect(
                "Columns:",
                options=list(all_donation_cols.keys()),
                default=['Donation Date', 'Donor Type', 'Campaign Name', 'Amount', 'Payment Method'],
                key='don_cols'
            )
            
            if selected_cols:
                if len(donations_display) > 0:
                    display_cols = [all_donation_cols[col] for col in selected_cols]
                    recent_donations = donations_display.nlargest(20, 'donation_date')[display_cols].copy()
                    
                    if 'donation_date' in display_cols:
                        recent_donations['donation_date'] = recent_donations['donation_date'].dt.strftime('%Y-%m-%d')
                    if 'amount' in display_cols:
                        recent_donations['amount'] = recent_donations['amount'].apply(lambda x: f"${x:,.2f}")
                    
                    recent_donations.columns = [col.replace('_', ' ').title() for col in recent_donations.columns]
                    st.dataframe(recent_donations, use_container_width=True, hide_index=True, height=400)
                else:
                    st.warning("No donation data available. Please ensure donations.csv and campaigns.csv are loaded.")
            else:
                st.info("Please select at least one column to display.")
        
        with tab2:
            st.subheader("Donor Directory")
            
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
            
            selected_donor_cols = st.multiselect(
                "Columns:",
                options=list(all_donor_cols.keys()),
                default=['First Name', 'Last Name', 'Email', 'Membership Level', 'State'],
                key='donor_cols'
            )
            
            if selected_donor_cols:
                display_cols = [all_donor_cols[col] for col in selected_donor_cols]
                donors_display = membership_df[display_cols].copy()
                donors_display.columns = [col.replace('_', ' ').title() for col in donors_display.columns]
                st.dataframe(donors_display, use_container_width=True, hide_index=True, height=400)
            else:
                st.info("Please select at least one column to display.")
        
        with tab3:
            st.subheader("Conservation Projects")
            
            all_project_cols = {
                'Project Name': 'project_name',
                'Project Type': 'project_type',
                'State': 'state',
                'Status': 'status',
                'Budget': 'budget',
                'Spent to Date': 'spent_to_date',
                'Acres Protected': 'acres_protected'
            }
            
            selected_project_cols = st.multiselect(
                "Columns:",
                options=list(all_project_cols.keys()),
                default=['Project Name', 'Project Type', 'State', 'Status', 'Budget'],
                key='proj_cols'
            )
            
            if selected_project_cols:
                display_cols = [all_project_cols[col] for col in selected_project_cols]
                projects_display = conservation_df[display_cols].copy()
                
                if 'budget' in display_cols:
                    projects_display['budget'] = projects_display['budget'].apply(lambda x: f"${x:,.2f}")
                if 'spent_to_date' in display_cols:
                    projects_display['spent_to_date'] = projects_display['spent_to_date'].apply(lambda x: f"${x:,.2f}")
                
                projects_display.columns = [col.replace('_', ' ').title() for col in projects_display.columns]
                st.dataframe(projects_display, use_container_width=True, hide_index=True, height=400)
            else:
                st.info("Please select at least one column to display.")
        
        with tab4:
            st.subheader("Habitat Areas")
            
            all_habitat_cols = {
                'Habitat Name': 'habitat_name',
                'State': 'state',
                'Region': 'region',
                'Total Acres': 'total_acres',
                'Quality Score': 'habitat_quality_score',
                'Conservation Status': 'conservation_status'
            }
            
            selected_habitat_cols = st.multiselect(
                "Columns:",
                options=list(all_habitat_cols.keys()),
                default=['Habitat Name', 'State', 'Region', 'Total Acres', 'Quality Score'],
                key='hab_cols'
            )
            
            if selected_habitat_cols:
                display_cols = [all_habitat_cols[col] for col in selected_habitat_cols]
                habitat_display = habitat_df[display_cols].copy()
                
                if 'total_acres' in display_cols:
                    habitat_display['total_acres'] = habitat_display['total_acres'].apply(lambda x: f"{x:,.0f}")
                
                habitat_display.columns = [col.replace('_', ' ').title() for col in habitat_display.columns]
                st.dataframe(habitat_display, use_container_width=True, hide_index=True, height=400)
            else:
                st.info("Please select at least one column to display.")
        
        with tab5:
            st.subheader("Anomaly Detection")
            
            large_donations = donations_df[donations_df['amount'] > 10000][
                ['donation_date', 'donor_type', 'campaign_name', 'amount']
            ].copy()
            
            if len(large_donations) > 0:
                large_donations['donation_date'] = pd.to_datetime(large_donations['donation_date']).dt.strftime('%Y-%m-%d')
                large_donations['amount'] = large_donations['amount'].apply(lambda x: f"${x:,.2f}")
            
            large_donations.columns = [col.replace('_', ' ').title() for col in large_donations.columns]
            
            if len(large_donations) > 0:
                st.markdown("**Large Donations (>$10,000)**")
                st.dataframe(large_donations, use_container_width=True, hide_index=True)
            
            at_risk = habitat_df[habitat_df['conservation_status'] == 'At Risk'][
                ['habitat_name', 'state', 'habitat_quality_score', 'conservation_status']
            ].copy()
            
            at_risk.columns = [col.replace('_', ' ').title() for col in at_risk.columns]
            
            if len(at_risk) > 0:
                st.markdown("**At-Risk Habitats**")
                st.dataframe(at_risk, use_container_width=True, hide_index=True)
