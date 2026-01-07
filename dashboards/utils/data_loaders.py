"""
Data loading functions for RMEF Analytics Dashboard
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine


@st.cache_resource
def get_db_connection():
    """Create database connection and ensure database exists"""
    db_path = Path(__file__).parent.parent.parent / "data" / "rmef_analytics.db"
    
    # Run ETL pipeline if database doesn't exist (silently)
    if not db_path.exists():
        import logging
        logging.getLogger().setLevel(logging.ERROR)
        try:
            from pipelines.etl_pipeline import RMEFPipeline
            pipeline = RMEFPipeline()
            pipeline.run()
        except Exception as e:
            st.error(f"Error initializing database: {e}")
            raise
        finally:
            logging.getLogger().setLevel(logging.INFO)
    
    return create_engine(f"sqlite:///{db_path}")


@st.cache_data(ttl=300)
def load_donations_data():
    """Load donation data with dimensions"""
    engine = get_db_connection()
    query = """
    SELECT 
        fd.donation_id,
        fd.amount,
        fd.payment_method,
        fd.is_recurring,
        dd.full_date as donation_date,
        dd.year,
        dd.quarter,
        dd.month,
        dd.month_name,
        dn.donor_id,
        dn.first_name,
        dn.last_name,
        dn.donor_type,
        dn.membership_level,
        dn.state as donor_state,
        dc.campaign_id,
        dc.campaign_name,
        dc.campaign_type,
        dc.target_region
    FROM fact_donation fd
    JOIN dim_date dd ON fd.date_key = dd.date_key
    JOIN dim_donor dn ON fd.donor_key = dn.donor_key
    JOIN dim_campaign dc ON fd.campaign_key = dc.campaign_key
    """
    return pd.read_sql(query, engine)


@st.cache_data(ttl=300)
def load_elk_population_data():
    """Load elk population data"""
    engine = get_db_connection()
    query = """
    SELECT 
        fep.year,
        fep.elk_count,
        fep.population_change,
        fep.population_change_pct,
        dh.habitat_id,
        dh.habitat_name,
        dh.state,
        dh.region,
        dh.total_acres,
        dh.habitat_quality_score,
        dh.conservation_status
    FROM fact_elk_population fep
    JOIN dim_habitat dh ON fep.habitat_key = dh.habitat_key
    """
    return pd.read_sql(query, engine)


@st.cache_data(ttl=300)
def load_conservation_data():
    """Load conservation project data"""
    engine = get_db_connection()
    query = """
    SELECT 
        fc.budget,
        fc.spent_to_date,
        fc.acres_protected,
        fc.elk_population_impacted,
        dp.project_id,
        dp.project_name,
        dp.project_type,
        dp.state,
        dp.county,
        dp.status
    FROM fact_conservation fc
    JOIN dim_project dp ON fc.project_key = dp.project_key
    """
    return pd.read_sql(query, engine)


@st.cache_data(ttl=300)
def load_habitat_data():
    """Load habitat dimension data"""
    engine = get_db_connection()
    query = "SELECT * FROM dim_habitat"
    return pd.read_sql(query, engine)


@st.cache_data(ttl=300)
def load_membership_data():
    """Load membership growth data"""
    engine = get_db_connection()
    query = """
    SELECT 
        donor_id,
        first_name,
        last_name,
        email,
        donor_type,
        membership_level,
        join_date,
        state
    FROM dim_donor
    """
    return pd.read_sql(query, engine)
