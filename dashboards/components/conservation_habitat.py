"""
Conservation & Habitat Component
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def render_conservation_habitat(conservation_df, habitat_df):
    """Render conservation and habitat analysis section"""
    
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
                    'habitat_quality_score': 'Quality Score',
                    'region': 'Region'
                }
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
