"""
Data formatting utilities for RMEF Analytics Dashboard
"""

import pandas as pd


def format_currency(value):
    """Format value as currency"""
    return f"${value:,.2f}"


def format_number(value):
    """Format value as number with commas"""
    return f"{value:,}"


def clean_column_names(df):
    """Clean column names by removing underscores and title casing"""
    df_copy = df.copy()
    df_copy.columns = [col.replace('_', ' ').title() for col in df_copy.columns]
    return df_copy


def format_dataframe_for_display(df, currency_cols=None, number_cols=None, date_cols=None):
    """
    Format a dataframe for display with proper formatting
    
    Args:
        df: DataFrame to format
        currency_cols: List of columns to format as currency
        number_cols: List of columns to format as numbers
        date_cols: List of columns to format as dates
    
    Returns:
        Formatted DataFrame
    """
    df_display = df.copy()
    
    if currency_cols:
        for col in currency_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")
    
    if number_cols:
        for col in number_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "")
    
    if date_cols:
        for col in date_cols:
            if col in df_display.columns:
                df_display[col] = pd.to_datetime(df_display[col]).dt.strftime('%Y-%m-%d')
    
    return df_display
