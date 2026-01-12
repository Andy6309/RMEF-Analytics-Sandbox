"""
Membership Analytics Component
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def render_membership_analytics(membership_df):
    """Render membership analytics section"""
    
    with st.expander("Membership Analytics & Business Targets", expanded=True):
        tier_pricing = {
            'Supporting': 35,
            'Team Elk': 50,
            'Sportsman': 100,
            'Heritage': 250,
            'Life': 1500
        }
        
        tier_breakdown = membership_df['membership_level'].value_counts()
        total_members = len(membership_df)
        
        arr_by_tier = {}
        for tier, count in tier_breakdown.items():
            if tier in tier_pricing:
                if tier == 'Life':
                    arr_by_tier[tier] = (count * tier_pricing[tier]) / 10
                else:
                    arr_by_tier[tier] = count * tier_pricing[tier]
        
        total_arr = sum(arr_by_tier.values())
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="Total Members", value=f"{total_members:,}")
        
        with col2:
            avg_tier_value = total_arr / total_members if total_members > 0 else 0
            st.metric(label="Avg Member Value/Year", value=f"${avg_tier_value:,.0f}")
        
        with col3:
            st.metric(label="Annual Recurring Revenue", value=f"${total_arr:,.0f}")
        
        with col4:
            premium_members = tier_breakdown.get('Heritage', 0) + tier_breakdown.get('Life', 0)
            premium_pct = (premium_members / total_members * 100) if total_members > 0 else 0
            st.metric(label="Premium Members %", value=f"{premium_pct:.1f}%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Membership Distribution by Tier")
            
            tier_data = []
            for tier in ['Supporting', 'Team Elk', 'Sportsman', 'Heritage', 'Life']:
                count = tier_breakdown.get(tier, 0)
                revenue = arr_by_tier.get(tier, 0)
                tier_data.append({
                    'Tier': tier,
                    'Members': count,
                    'ARR': revenue,
                    'Price': tier_pricing.get(tier, 0)
                })
            
            tier_df = pd.DataFrame(tier_data)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Members',
                x=tier_df['Tier'],
                y=tier_df['Members'],
                marker_color='#0071bc',
                text=tier_df['Members'],
                textposition='outside'
            ))
            fig.update_layout(height=350, yaxis_title='Number of Members', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("**Tier Performance Summary**")
            summary_df = tier_df[['Tier', 'Members', 'Price', 'ARR']].copy()
            summary_df['Price'] = summary_df['Price'].apply(lambda x: f'${x:,.0f}')
            summary_df['ARR'] = summary_df['ARR'].apply(lambda x: f'${x:,.0f}')
            summary_df.columns = ['Membership Tier', 'Members', 'Annual Price', 'Total ARR']
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("Membership Growth Trends")
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
            
            st.markdown("**Growth Metrics**")

            # Date range picker for growth metrics
            max_date = membership_df['join_date'].max().date()
            min_date = membership_df['join_date'].min().date()
            default_start = (max_date - pd.DateOffset(months=3))
            if hasattr(default_start, 'date'):
                default_start = default_start.date()

            # Initialize session state for dates
            if 'growth_start_date' not in st.session_state:
                st.session_state.growth_start_date = default_start
            if 'growth_end_date' not in st.session_state:
                st.session_state.growth_end_date = max_date

            date_col1, date_col2, date_col3 = st.columns([2, 2, 1])
            with date_col1:
                start_date = st.date_input(
                    "Start Date",
                    value=st.session_state.growth_start_date,
                    min_value=min_date,
                    max_value=max_date,
                    key="growth_start_input"
                )
            with date_col2:
                end_date = st.date_input(
                    "End Date",
                    value=st.session_state.growth_end_date,
                    min_value=min_date,
                    max_value=max_date,
                    key="growth_end_input"
                )
            with date_col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Clear", key="clear_growth_dates"):
                    st.session_state.growth_start_date = default_start
                    st.session_state.growth_end_date = max_date
                    st.rerun()

            # Update session state
            st.session_state.growth_start_date = start_date
            st.session_state.growth_end_date = end_date

            recent_members = membership_df[
                (membership_df['join_date'].dt.date >= start_date) & 
                (membership_df['join_date'].dt.date <= end_date)
            ]
            growth_rate = (len(recent_members) / total_members * 100) if total_members > 0 else 0

            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.metric("New Members", len(recent_members))
            with metrics_col2:
                st.metric("Growth Rate", f"{growth_rate:.1f}%")
        
            st.markdown("---")
        
            st.subheader("Membership by State (Top 10)")
            state_breakdown = membership_df['state'].value_counts().head(10).reset_index()
            state_breakdown.columns = ['State', 'Members']
        
    fig = px.bar(
            state_breakdown,
            x='State',
            y='Members',
            color='Members',
            color_continuous_scale='Blues',
            labels={'Members': 'Member Count'}
        )
    fig.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
