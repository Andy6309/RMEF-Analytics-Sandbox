"""
RMEF Analytics Sandbox - Database Schema
Star schema design for conservation analytics
"""

from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Date, DateTime,
    Boolean, ForeignKey, Text, Enum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()


# Dimension Tables

class DimDonor(Base):
    """Dimension table for donors/members"""
    __tablename__ = 'dim_donor'
    
    donor_key = Column(Integer, primary_key=True, autoincrement=True)
    donor_id = Column(String(10), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(2))
    zip_code = Column(String(10))
    donor_type = Column(String(50))  # Individual, Corporate, Foundation
    join_date = Column(Date)
    membership_level = Column(String(50))  # Bronze, Silver, Gold, Platinum
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    donations = relationship("FactDonation", back_populates="donor")


class DimCampaign(Base):
    """Dimension table for fundraising campaigns"""
    __tablename__ = 'dim_campaign'
    
    campaign_key = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(String(10), unique=True, nullable=False)
    campaign_name = Column(String(255), nullable=False)
    campaign_type = Column(String(50))  # Habitat, Membership, Land, Education, etc.
    start_date = Column(Date)
    end_date = Column(Date)
    goal_amount = Column(Float)
    description = Column(Text)
    target_region = Column(String(100))
    status = Column(String(50))  # Active, Completed, Cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    donations = relationship("FactDonation", back_populates="campaign")


class DimDate(Base):
    """Date dimension for time-based analysis"""
    __tablename__ = 'dim_date'
    
    date_key = Column(Integer, primary_key=True)  # YYYYMMDD format
    full_date = Column(Date, unique=True, nullable=False)
    year = Column(Integer)
    quarter = Column(Integer)
    month = Column(Integer)
    month_name = Column(String(20))
    week = Column(Integer)
    day_of_month = Column(Integer)
    day_of_week = Column(Integer)
    day_name = Column(String(20))
    is_weekend = Column(Boolean)
    fiscal_year = Column(Integer)
    fiscal_quarter = Column(Integer)


class DimHabitat(Base):
    """Dimension table for habitat areas"""
    __tablename__ = 'dim_habitat'
    
    habitat_key = Column(Integer, primary_key=True, autoincrement=True)
    habitat_id = Column(String(10), unique=True, nullable=False)
    habitat_name = Column(String(255), nullable=False)
    state = Column(String(2))
    region = Column(String(100))
    total_acres = Column(Integer)
    habitat_quality_score = Column(Integer)
    conservation_status = Column(String(50))  # Protected, Partially Protected, At Risk
    primary_threats = Column(Text)  # JSON string of threats
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    population_facts = relationship("FactElkPopulation", back_populates="habitat")
    conservation_facts = relationship("FactConservation", back_populates="habitat")


class DimProject(Base):
    """Dimension table for conservation projects"""
    __tablename__ = 'dim_project'
    
    project_key = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(10), unique=True, nullable=False)
    project_name = Column(String(255), nullable=False)
    project_type = Column(String(100))  # Habitat Protection, Restoration, Land Acquisition, Research
    state = Column(String(2))
    county = Column(String(100))
    status = Column(String(50))  # In Progress, Completed, Planned
    partner_organizations = Column(Text)  # JSON string
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    conservation_facts = relationship("FactConservation", back_populates="project")


# Fact Tables

class FactDonation(Base):
    """Fact table for donation transactions"""
    __tablename__ = 'fact_donation'
    
    donation_key = Column(Integer, primary_key=True, autoincrement=True)
    donation_id = Column(String(10), unique=True, nullable=False)
    donor_key = Column(Integer, ForeignKey('dim_donor.donor_key'))
    campaign_key = Column(Integer, ForeignKey('dim_campaign.campaign_key'))
    date_key = Column(Integer, ForeignKey('dim_date.date_key'))
    
    # Measures
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50))
    is_recurring = Column(Boolean, default=False)
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    donor = relationship("DimDonor", back_populates="donations")
    campaign = relationship("DimCampaign", back_populates="donations")


class FactElkPopulation(Base):
    """Fact table for elk population metrics over time"""
    __tablename__ = 'fact_elk_population'
    
    population_key = Column(Integer, primary_key=True, autoincrement=True)
    habitat_key = Column(Integer, ForeignKey('dim_habitat.habitat_key'))
    year = Column(Integer, nullable=False)
    
    # Measures
    elk_count = Column(Integer)
    population_change = Column(Integer)  # Change from previous year
    population_change_pct = Column(Float)  # Percentage change
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    habitat = relationship("DimHabitat", back_populates="population_facts")


class FactConservation(Base):
    """Fact table for conservation project metrics"""
    __tablename__ = 'fact_conservation'
    
    conservation_key = Column(Integer, primary_key=True, autoincrement=True)
    project_key = Column(Integer, ForeignKey('dim_project.project_key'))
    habitat_key = Column(Integer, ForeignKey('dim_habitat.habitat_key'), nullable=True)
    date_key = Column(Integer, ForeignKey('dim_date.date_key'))
    
    # Measures
    budget = Column(Float)
    spent_to_date = Column(Float)
    acres_protected = Column(Integer)
    elk_population_impacted = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("DimProject", back_populates="conservation_facts")
    habitat = relationship("DimHabitat", back_populates="conservation_facts")


# Database initialization functions

def get_engine(db_path: str = "sqlite:///data/rmef_analytics.db"):
    """Create and return database engine"""
    return create_engine(db_path, echo=False)


def create_tables(engine):
    """Create all tables in the database"""
    Base.metadata.create_all(engine)


def get_session(engine):
    """Create and return a database session"""
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    # Create database and tables
    engine = get_engine()
    create_tables(engine)
    print("Database schema created successfully!")
