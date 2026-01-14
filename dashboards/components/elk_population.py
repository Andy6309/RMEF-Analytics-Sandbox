"""
Elk Population Component
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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
            st.subheader("Elk Population by Habitat - US Map")
            
            # Prepare data for map visualization
            latest_elk_data = elk_df[elk_df['year'] == latest_year].copy()
            
            # Aggregate by state for the map
            state_data = latest_elk_data.groupby('state').agg({
                'elk_count': 'sum',
                'habitat_name': lambda x: '<br>'.join(x.unique()),
                'region': 'first'
            }).reset_index()
            
            # Create hover text with habitat details
            hover_text = []
            for idx, row in state_data.iterrows():
                # Get all habitats in this state
                state_habitats = latest_elk_data[latest_elk_data['state'] == row['state']]
                habitat_details = []
                for _, habitat in state_habitats.iterrows():
                    habitat_details.append(
                        f"  • {habitat['habitat_name']}: {habitat['elk_count']:,} elk"
                    )
                
                hover_info = (
                    f"<b>{row['state']}</b><br>"
                    f"<b>Total Population: {row['elk_count']:,}</b><br>"
                    f"Region: {row['region']}<br>"
                    f"<br><b>Habitats:</b><br>" +
                    '<br>'.join(habitat_details)
                )
                hover_text.append(hover_info)
            
            state_data['hover_text'] = hover_text
            
            # Create choropleth map
            fig = go.Figure(data=go.Choropleth(
                locations=state_data['state'],
                z=state_data['elk_count'],
                locationmode='USA-states',
                colorscale=[
                    [0, '#fee5d9'],
                    [0.2, '#fcbba1'],
                    [0.4, '#fc9272'],
                    [0.6, '#fb6a4a'],
                    [0.8, '#de2d26'],
                    [1, '#a50f15']
                ],
                text=state_data['hover_text'],
                hovertemplate='%{text}<extra></extra>',
                colorbar=dict(
                    title="Elk Count",
                    thickness=15,
                    len=0.7
                ),
                marker_line_color='white',
                marker_line_width=1.5
            ))
            
            fig.update_layout(
                geo=dict(
                    scope='usa',
                    projection=go.layout.geo.Projection(type='albers usa'),
                    showlakes=True,
                    lakecolor='#1a1a1a',
                    bgcolor='#112e51',
                    landcolor='#2a2a2a',
                    coastlinecolor='#aeb0b5',
                    showland=True
                ),
                height=450,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='#112e51',
                plot_bgcolor='#112e51',
                font=dict(color='white')
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
