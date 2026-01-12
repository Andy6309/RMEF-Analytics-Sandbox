"""
Form 990 Analytics Dashboard Component
Displays multi-year financial data with YoY comparisons and trend lines
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Color scheme matching RMEF dashboard theme
COLORS = {
    'primary': '#112e51',      # Dark blue
    'secondary': '#0071bc',    # Medium blue
    'accent': '#2e8540',       # Green (positive)
    'warning': '#e31c3d',      # Red (negative)
    'light_gray': '#aeb0b5',
    'border': '#d6d7d9',
    'background': '#f9f9f9',
    'white': '#ffffff'
}

# Chart color sequences
REVENUE_COLORS = ['#112e51', '#205493', '#0071bc', '#4aa3df']
EXPENSE_COLORS = ['#112e51', '#205493', '#0071bc']
PROGRAM_COLORS = ['#112e51', '#0071bc', '#4aa3df']


def load_990_financial_data() -> pd.DataFrame:
    """Load Form 990 financial data from database"""
    from sqlalchemy import create_engine, text
    from pathlib import Path
    
    db_path = Path(__file__).parent.parent.parent / "data" / "rmef_analytics.db"
    engine = create_engine(f"sqlite:///{db_path}")
    
    # Check if table exists, if not run the ETL pipeline
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='fact_990_financial'"
        ))
        if not result.fetchone():
            # Table doesn't exist - run the Form 990 ETL pipeline
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            from pipelines.etl_990_pipeline import Form990Pipeline
            pipeline = Form990Pipeline(db_path=f"sqlite:///{db_path}")
            pipeline.run(extract_fresh=True)
    
    query = """
        SELECT * FROM fact_990_financial
        ORDER BY fiscal_year
    """
    return pd.read_sql(query, engine)


def load_990_program_data() -> pd.DataFrame:
    """Load Form 990 program service data from database"""
    from sqlalchemy import create_engine
    from pathlib import Path
    
    db_path = Path(__file__).parent.parent.parent / "data" / "rmef_analytics.db"
    engine = create_engine(f"sqlite:///{db_path}")
    query = """
        SELECT * FROM fact_990_program_service
        ORDER BY fiscal_year, program_name
    """
    return pd.read_sql(query, engine)


def calculate_yoy_changes(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Calculate year-over-year changes and percent changes"""
    df = df.sort_values('fiscal_year').copy()
    
    for col in columns:
        df[f'{col}_yoy_change'] = df[col].diff()
        df[f'{col}_yoy_pct'] = df[col].pct_change() * 100
    
    return df


def format_currency(value: float) -> str:
    """Format value as currency"""
    if pd.isna(value):
        return "N/A"
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:.0f}K"
    return f"${value:,.0f}"


def format_percent(value: float) -> str:
    """Format value as percentage"""
    if pd.isna(value):
        return "N/A"
    return f"{value:+.1f}%"


def render_form_990_analytics():
    """Main render function for Form 990 analytics section"""
    st.subheader("Form 990 Financial Analysis")
    st.markdown("*IRS Form 990 data across fiscal years - Revenue, Expenses, and Program Services*")
    
    # Load data
    try:
        financial_df = load_990_financial_data()
        program_df = load_990_program_data()
    except Exception as e:
        st.error(f"Error loading Form 990 data: {e}")
        st.info("Run the Form 990 ETL pipeline first: `python pipelines/etl_990_pipeline.py`")
        return
    
    if financial_df.empty:
        st.warning("No Form 990 data available. Please run the ETL pipeline.")
        return
    
    # Calculate YoY changes
    financial_cols = ['total_revenue', 'total_expenses', 'contributions_and_grants', 
                      'program_service_revenue', 'salaries_and_wages', 'grants_and_similar_paid']
    financial_df = calculate_yoy_changes(financial_df, financial_cols)
    
    # KPI Cards - Latest Year Summary
    render_kpi_cards(financial_df)
    
    # Revenue & Expenses Trend
    render_revenue_expense_trend(financial_df)
    
    # YoY Comparison Table
    render_yoy_comparison_table(financial_df)
    
    # Revenue Breakdown
    render_revenue_breakdown(financial_df)
    
    # Program Services Analysis
    render_program_services(program_df)


def render_kpi_cards(df: pd.DataFrame):
    """Render KPI cards for latest year with YoY comparison"""
    st.subheader("Latest Year Summary")
    
    latest = df.iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta = latest.get('total_revenue_yoy_pct', 0)
        st.metric(
            label=f"Total Revenue ({int(latest['fiscal_year'])})",
            value=format_currency(latest['total_revenue']),
            delta=f"{delta:+.1f}%" if not pd.isna(delta) else None
        )
    
    with col2:
        delta = latest.get('total_expenses_yoy_pct', 0)
        st.metric(
            label=f"Total Expenses ({int(latest['fiscal_year'])})",
            value=format_currency(latest['total_expenses']),
            delta=f"{delta:+.1f}%" if not pd.isna(delta) else None,
            delta_color="inverse"
        )
    
    with col3:
        surplus = latest['total_revenue'] - latest['total_expenses']
        prev_surplus = df.iloc[-2]['total_revenue'] - df.iloc[-2]['total_expenses'] if len(df) > 1 else 0
        delta_pct = ((surplus - prev_surplus) / abs(prev_surplus) * 100) if prev_surplus != 0 else 0
        st.metric(
            label="Net Surplus",
            value=format_currency(surplus),
            delta=f"{delta_pct:+.1f}%" if len(df) > 1 else None
        )
    
    with col4:
        delta = latest.get('contributions_and_grants_yoy_pct', 0)
        st.metric(
            label="Contributions & Grants",
            value=format_currency(latest['contributions_and_grants']),
            delta=f"{delta:+.1f}%" if not pd.isna(delta) else None
        )


def render_revenue_expense_trend(df: pd.DataFrame):
    """Render revenue vs expenses trend chart"""
    st.subheader("Revenue & Expenses Trend")
    
    fig = go.Figure()
    
    # Revenue line - using primary dark blue
    fig.add_trace(go.Scatter(
        x=df['fiscal_year'],
        y=df['total_revenue'],
        name='Total Revenue',
        mode='lines+markers',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=10),
        hovertemplate='%{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
    ))
    
    # Expenses line - using secondary blue
    fig.add_trace(go.Scatter(
        x=df['fiscal_year'],
        y=df['total_expenses'],
        name='Total Expenses',
        mode='lines+markers',
        line=dict(color=COLORS['secondary'], width=3),
        marker=dict(size=10),
        hovertemplate='%{x}<br>Expenses: $%{y:,.0f}<extra></extra>'
    ))
    
    # Net surplus - using green accent
    fig.add_trace(go.Scatter(
        x=df['fiscal_year'],
        y=df['total_revenue'] - df['total_expenses'],
        name='Net Surplus',
        mode='lines+markers',
        line=dict(color=COLORS['accent'], width=2, dash='dot'),
        marker=dict(size=8),
        hovertemplate='%{x}<br>Surplus: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        height=400,
        xaxis_title="Fiscal Year",
        yaxis_title="Amount ($)",
        yaxis_tickformat='$,.0f',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )
    
    fig.update_xaxes(dtick=1)
    
    st.plotly_chart(fig, use_container_width=True)


def render_yoy_comparison_table(df: pd.DataFrame):
    """Render year-over-year comparison table"""
    st.subheader("Year-over-Year Comparison")
    
    # Prepare comparison data
    comparison_data = []
    
    metrics = [
        ('Total Revenue', 'total_revenue'),
        ('Total Expenses', 'total_expenses'),
        ('Contributions & Grants', 'contributions_and_grants'),
        ('Program Service Revenue', 'program_service_revenue'),
        ('Investment Income', 'investment_income'),
        ('Salaries & Wages', 'salaries_and_wages'),
        ('Grants Paid', 'grants_and_similar_paid'),
    ]
    
    for label, col in metrics:
        row = {'Metric': label}
        for _, record in df.iterrows():
            year = int(record['fiscal_year'])
            row[str(year)] = format_currency(record[col])
        
        # Add YoY change columns
        if len(df) > 1:
            for i in range(1, len(df)):
                prev_year = int(df.iloc[i-1]['fiscal_year'])
                curr_year = int(df.iloc[i]['fiscal_year'])
                pct_col = f'{col}_yoy_pct'
                if pct_col in df.columns:
                    pct = df.iloc[i][pct_col]
                    row[f'{prev_year}→{curr_year}'] = format_percent(pct)
        
        comparison_data.append(row)
    
    comparison_df = pd.DataFrame(comparison_data)
    
    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )


def render_revenue_breakdown(df: pd.DataFrame):
    """Render revenue breakdown by category"""
    st.subheader("Revenue Composition")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Stacked bar chart for revenue composition
        revenue_data = []
        for _, row in df.iterrows():
            year = int(row['fiscal_year'])
            revenue_data.extend([
                {'Year': year, 'Category': 'Contributions & Grants', 'Amount': row['contributions_and_grants']},
                {'Year': year, 'Category': 'Program Service Revenue', 'Amount': row['program_service_revenue']},
                {'Year': year, 'Category': 'Investment Income', 'Amount': row['investment_income']},
                {'Year': year, 'Category': 'Other Revenue', 'Amount': row['other_revenue']},
            ])
        
        revenue_df = pd.DataFrame(revenue_data)
        
        fig = px.bar(
            revenue_df,
            x='Year',
            y='Amount',
            color='Category',
            title='Revenue by Source',
            color_discrete_sequence=REVENUE_COLORS
        )
        
        fig.update_layout(
            height=450,
            yaxis_tickformat='$,.0f',
            legend=dict(orientation="h", yanchor="top", y=-0.15, font=dict(size=9)),
            margin=dict(b=120, t=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pie chart for latest year
        latest = df.iloc[-1]
        year = int(latest['fiscal_year'])
        
        pie_data = pd.DataFrame({
            'Category': ['Contributions', 'Program Revenue', 'Investment', 'Other'],
            'Amount': [
                latest['contributions_and_grants'],
                latest['program_service_revenue'],
                latest['investment_income'],
                latest['other_revenue']
            ]
        })
        
        fig = px.pie(
            pie_data,
            values='Amount',
            names='Category',
            title=f'Revenue Mix ({year})',
            color_discrete_sequence=REVENUE_COLORS
        )
        
        fig.update_traces(textposition='inside', textinfo='percent')
        fig.update_layout(
            height=450,
            showlegend=True,
            legend=dict(orientation="h", yanchor="top", y=-0.05, font=dict(size=10)),
            margin=dict(b=80, t=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)


def render_program_services(df: pd.DataFrame):
    """Render program services analysis"""
    st.subheader("Program Services")
    
    if df.empty:
        st.info("No program service data available.")
        return
    
    # Clean up program names for display
    df = df.copy()
    df['program_name'] = df['program_name'].str.replace('_', ' ').str.title()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Program expenses by year
        fig = px.bar(
            df,
            x='fiscal_year',
            y='expenses',
            color='program_name',
            title='Program Expenses by Year',
            barmode='group',
            color_discrete_sequence=PROGRAM_COLORS
        )
        
        fig.update_layout(
            height=450,
            xaxis_title="Fiscal Year",
            yaxis_title="Expenses ($)",
            yaxis_tickformat='$,.0f',
            legend=dict(orientation="h", yanchor="top", y=-0.15, font=dict(size=9)),
            margin=dict(b=120, t=50)
        )
        
        fig.update_xaxes(dtick=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Program grants by year
        fig = px.bar(
            df,
            x='fiscal_year',
            y='grants',
            color='program_name',
            title='Grants Distributed by Program',
            barmode='group',
            color_discrete_sequence=PROGRAM_COLORS
        )
        
        fig.update_layout(
            height=450,
            xaxis_title="Fiscal Year",
            yaxis_title="Grants ($)",
            yaxis_tickformat='$,.0f',
            legend=dict(orientation="h", yanchor="top", y=-0.15, font=dict(size=9)),
            margin=dict(b=120, t=50)
        )
        
        fig.update_xaxes(dtick=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Program services trend table
    st.markdown("**Program Services Summary**")
    
    # Pivot the data for display
    pivot_df = df.pivot_table(
        index='program_name',
        columns='fiscal_year',
        values=['expenses', 'grants'],
        aggfunc='sum'
    ).round(0)
    
    # Flatten column names - clean format
    pivot_df.columns = [f'{col[0].title()} ({int(col[1])})' for col in pivot_df.columns]
    pivot_df = pivot_df.reset_index()
    
    # Clean up program names (remove underscores, title case)
    pivot_df['program_name'] = pivot_df['program_name'].str.replace('_', ' ').str.title()
    pivot_df.columns = ['Program'] + list(pivot_df.columns[1:])
    
    # Format currency
    for col in pivot_df.columns[1:]:
        pivot_df[col] = pivot_df[col].apply(lambda x: format_currency(x) if pd.notna(x) else 'N/A')
    
    st.dataframe(pivot_df, use_container_width=True, hide_index=True)
