"""
Elk Population Component
"""

import streamlit as st
import pandas as pd
import plotly.express as px


def render_elk_population(elk_df):
    """Render elk population trends section"""
    
    with st.expander("Elk Population Trends", expanded=False):
        if len(elk_df) > 0:
            latest_year = elk_df['year'].max()
            latest_pop = elk_df[elk_df['year'] == latest_year]['elk_count'].sum()
            prev_year_pop = elk_df[elk_df['year'] == latest_year - 1]['elk_count'].sum()
            pop_change = latest_pop - prev_year_pop
            pop_change_pct = (pop_change / prev_year_pop * 100) if prev_year_pop > 0 else 0
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label=f"Total Elk Population ({latest_year})",
                    value=f"{latest_pop:,}",
                    delta=f"{pop_change:+,} from {latest_year-1}"
                )
            
            with col2:
                num_habitats = elk_df[elk_df['year'] == latest_year]['habitat_name'].nunique()
                st.metric(label="Monitored Habitats", value=f"{num_habitats}")
            
            with col3:
                avg_habitat_pop = latest_pop / num_habitats if num_habitats > 0 else 0
                st.metric(label="Avg Elk per Habitat", value=f"{avg_habitat_pop:,.0f}")
            
            with col4:
                st.metric(label="Population Change %", value=f"{pop_change_pct:+.1f}%")
            
            st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Elk Population by Habitat")
            fig = px.line(
                elk_df,
                x='year',
                y='elk_count',
                color='habitat_name',
                markers=True,
                labels={'elk_count': 'Elk Count', 'year': 'Year', 'habitat_name': 'Habitat'}
            )
            fig.update_layout(
                height=400,
                legend=dict(
                    orientation='h',
                    yanchor='top',
                    y=-0.15,
                    xanchor='center',
                    x=0.5
                ),
                margin=dict(b=100)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Population Change by Habitat")
            if len(elk_df) > 0:
                habitat_change = elk_df[elk_df['year'].isin([latest_year, latest_year-1])].copy()
                habitat_change = habitat_change.pivot_table(
                    index='habitat_name',
                    columns='year',
                    values='elk_count',
                    aggfunc='sum'
                ).reset_index()
                
                if latest_year in habitat_change.columns and (latest_year-1) in habitat_change.columns:
                    habitat_change['change'] = habitat_change[latest_year] - habitat_change[latest_year-1]
                    habitat_change['change_pct'] = (habitat_change['change'] / habitat_change[latest_year-1] * 100)
                    habitat_change = habitat_change.sort_values('change', ascending=True)
                    
                    fig = px.bar(
                        habitat_change,
                        y='habitat_name',
                        x='change',
                        orientation='h',
                        color='change',
                        color_continuous_scale=['#d62728', '#ffffff', '#2ca02c'],
                        color_continuous_midpoint=0,
                        labels={'change': 'Population Change', 'habitat_name': 'Habitat'}
                    )
                    fig.update_layout(height=350, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
