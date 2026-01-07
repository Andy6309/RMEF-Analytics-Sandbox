"""
RMEF Analytics Sandbox - ETL Pipeline
Extracts, transforms, and loads conservation data into the analytics database
"""

import pandas as pd
import json
import logging
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.schema import (
    get_engine, create_tables, get_session,
    DimDonor, DimCampaign, DimDate, DimHabitat, DimProject,
    FactDonation, FactElkPopulation, FactConservation
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipelines/etl.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('RMEF_ETL')


class DataQualityError(Exception):
    """Custom exception for data quality issues"""
    pass


class RMEFPipeline:
    """ETL Pipeline for RMEF Analytics data"""
    
    def __init__(self, db_path: str = "sqlite:///data/rmef_analytics.db"):
        self.db_path = db_path
        self.engine = get_engine(db_path)
        self.session = None
        self.stats = {
            'donors_loaded': 0,
            'campaigns_loaded': 0,
            'donations_loaded': 0,
            'projects_loaded': 0,
            'habitats_loaded': 0,
            'dates_loaded': 0,
            'errors': []
        }
    
    def run(self) -> Dict[str, Any]:
        """Execute the full ETL pipeline"""
        logger.info("=" * 60)
        logger.info("Starting RMEF Analytics ETL Pipeline")
        logger.info("=" * 60)
        
        try:
            # Initialize database
            self._init_database()
            
            # Extract and load dimension tables
            self._load_date_dimension()
            self._load_donors()
            self._load_campaigns()
            self._load_habitats()
            self._load_projects()
            
            # Extract and load fact tables
            self._load_donations()
            self._load_elk_populations()
            self._load_conservation_facts()
            
            # Commit all changes
            self.session.commit()
            logger.info("=" * 60)
            logger.info("ETL Pipeline completed successfully!")
            logger.info(f"Stats: {self.stats}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            self.stats['errors'].append(str(e))
            if self.session:
                self.session.rollback()
            raise
        finally:
            if self.session:
                self.session.close()
        
        return self.stats
    
    def _init_database(self):
        """Initialize database and create tables"""
        logger.info("Initializing database...")
        create_tables(self.engine)
        self.session = get_session(self.engine)
        logger.info("Database initialized successfully")
    
    def _load_date_dimension(self):
        """Generate and load date dimension"""
        logger.info("Loading date dimension...")
        
        # Check if dates already exist
        existing = self.session.query(DimDate).count()
        if existing > 0:
            logger.info(f"Date dimension already populated with {existing} records")
            return
        
        # Generate dates from 2015 to 2026
        start_date = datetime(2015, 1, 1)
        end_date = datetime(2026, 12, 31)
        
        current = start_date
        dates_added = 0
        
        while current <= end_date:
            date_key = int(current.strftime('%Y%m%d'))
            
            # Calculate fiscal year (assuming Oct 1 fiscal year start)
            fiscal_year = current.year if current.month >= 10 else current.year
            fiscal_quarter = ((current.month - 10) % 12) // 3 + 1
            
            dim_date = DimDate(
                date_key=date_key,
                full_date=current.date(),
                year=current.year,
                quarter=(current.month - 1) // 3 + 1,
                month=current.month,
                month_name=current.strftime('%B'),
                week=current.isocalendar()[1],
                day_of_month=current.day,
                day_of_week=current.weekday(),
                day_name=current.strftime('%A'),
                is_weekend=current.weekday() >= 5,
                fiscal_year=fiscal_year,
                fiscal_quarter=fiscal_quarter
            )
            self.session.add(dim_date)
            dates_added += 1
            current += timedelta(days=1)
        
        self.stats['dates_loaded'] = dates_added
        logger.info(f"Loaded {dates_added} dates into dimension")
    
    def _load_donors(self):
        """Extract, transform, and load donor data"""
        logger.info("Loading donors...")
        
        try:
            df = pd.read_csv('data/raw/donors.csv')
            
            # Data quality checks
            self._validate_donors(df)
            
            # Transform and load
            for _, row in df.iterrows():
                # Check if donor already exists
                existing = self.session.query(DimDonor).filter_by(
                    donor_id=row['donor_id']
                ).first()
                
                if existing:
                    continue
                
                donor = DimDonor(
                    donor_id=row['donor_id'],
                    first_name=row['first_name'] if pd.notna(row['first_name']) else None,
                    last_name=row['last_name'] if pd.notna(row['last_name']) else None,
                    email=row['email'],
                    phone=row['phone'],
                    address=row['address'],
                    city=row['city'],
                    state=row['state'],
                    zip_code=row['zip_code'],
                    donor_type=row['donor_type'],
                    join_date=pd.to_datetime(row['join_date']).date(),
                    membership_level=row['membership_level']
                )
                self.session.add(donor)
                self.stats['donors_loaded'] += 1
            
            logger.info(f"Loaded {self.stats['donors_loaded']} donors")
            
        except FileNotFoundError:
            logger.error("Donors file not found: data/raw/donors.csv")
            raise
    
    def _validate_donors(self, df: pd.DataFrame):
        """Validate donor data quality"""
        errors = []
        
        # Check for required fields
        if df['donor_id'].isna().any():
            errors.append("Missing donor_id values found")
        
        # Check for duplicates
        duplicates = df['donor_id'].duplicated().sum()
        if duplicates > 0:
            errors.append(f"Found {duplicates} duplicate donor_id values")
        
        # Check email format (basic)
        invalid_emails = df[~df['email'].str.contains('@', na=False)]
        if len(invalid_emails) > 0:
            logger.warning(f"Found {len(invalid_emails)} records with invalid email format")
        
        if errors:
            raise DataQualityError(f"Donor data quality issues: {errors}")
        
        logger.info("Donor data quality validation passed")
    
    def _load_campaigns(self):
        """Extract, transform, and load campaign data"""
        logger.info("Loading campaigns...")
        
        try:
            df = pd.read_csv('data/raw/campaigns.csv')
            
            # Data quality checks
            self._validate_campaigns(df)
            
            for _, row in df.iterrows():
                existing = self.session.query(DimCampaign).filter_by(
                    campaign_id=row['campaign_id']
                ).first()
                
                if existing:
                    continue
                
                campaign = DimCampaign(
                    campaign_id=row['campaign_id'],
                    campaign_name=row['campaign_name'],
                    campaign_type=row['campaign_type'],
                    start_date=pd.to_datetime(row['start_date']).date(),
                    end_date=pd.to_datetime(row['end_date']).date(),
                    goal_amount=float(row['goal_amount']),
                    description=row['description'],
                    target_region=row['target_region'],
                    status=row['status']
                )
                self.session.add(campaign)
                self.stats['campaigns_loaded'] += 1
            
            logger.info(f"Loaded {self.stats['campaigns_loaded']} campaigns")
            
        except FileNotFoundError:
            logger.error("Campaigns file not found: data/raw/campaigns.csv")
            raise
    
    def _validate_campaigns(self, df: pd.DataFrame):
        """Validate campaign data quality"""
        errors = []
        
        if df['campaign_id'].isna().any():
            errors.append("Missing campaign_id values found")
        
        if df['campaign_name'].isna().any():
            errors.append("Missing campaign_name values found")
        
        # Check date logic
        df['start'] = pd.to_datetime(df['start_date'])
        df['end'] = pd.to_datetime(df['end_date'])
        invalid_dates = df[df['start'] > df['end']]
        if len(invalid_dates) > 0:
            errors.append(f"Found {len(invalid_dates)} campaigns with end_date before start_date")
        
        if errors:
            raise DataQualityError(f"Campaign data quality issues: {errors}")
        
        logger.info("Campaign data quality validation passed")
    
    def _load_habitats(self):
        """Extract, transform, and load habitat data"""
        logger.info("Loading habitats...")
        
        try:
            with open('data/raw/habitat_areas.json', 'r') as f:
                habitats = json.load(f)
            
            for habitat_data in habitats:
                existing = self.session.query(DimHabitat).filter_by(
                    habitat_id=habitat_data['habitat_id']
                ).first()
                
                if existing:
                    continue
                
                habitat = DimHabitat(
                    habitat_id=habitat_data['habitat_id'],
                    habitat_name=habitat_data['habitat_name'],
                    state=habitat_data['state'],
                    region=habitat_data['region'],
                    total_acres=habitat_data['total_acres'],
                    habitat_quality_score=habitat_data['habitat_quality_score'],
                    conservation_status=habitat_data['conservation_status'],
                    primary_threats=json.dumps(habitat_data['primary_threats'])
                )
                self.session.add(habitat)
                self.stats['habitats_loaded'] += 1
            
            logger.info(f"Loaded {self.stats['habitats_loaded']} habitats")
            
        except FileNotFoundError:
            logger.error("Habitats file not found: data/raw/habitat_areas.json")
            raise
    
    def _load_projects(self):
        """Extract, transform, and load conservation project data"""
        logger.info("Loading conservation projects...")
        
        try:
            with open('data/raw/conservation_projects.json', 'r') as f:
                projects = json.load(f)
            
            for project_data in projects:
                existing = self.session.query(DimProject).filter_by(
                    project_id=project_data['project_id']
                ).first()
                
                if existing:
                    continue
                
                project = DimProject(
                    project_id=project_data['project_id'],
                    project_name=project_data['project_name'],
                    project_type=project_data['project_type'],
                    state=project_data['state'],
                    county=project_data['county'],
                    status=project_data['status'],
                    partner_organizations=json.dumps(project_data['partner_organizations']),
                    description=project_data['description']
                )
                self.session.add(project)
                self.stats['projects_loaded'] += 1
            
            logger.info(f"Loaded {self.stats['projects_loaded']} projects")
            
        except FileNotFoundError:
            logger.error("Projects file not found: data/raw/conservation_projects.json")
            raise
    
    def _load_donations(self):
        """Extract, transform, and load donation fact data"""
        logger.info("Loading donations...")
        
        try:
            df = pd.read_csv('data/raw/donations.csv')
            
            # Data quality checks
            self._validate_donations(df)
            
            for _, row in df.iterrows():
                existing = self.session.query(FactDonation).filter_by(
                    donation_id=row['donation_id']
                ).first()
                
                if existing:
                    continue
                
                # Get foreign keys
                donor = self.session.query(DimDonor).filter_by(
                    donor_id=row['donor_id']
                ).first()
                
                campaign = self.session.query(DimCampaign).filter_by(
                    campaign_id=row['campaign_id']
                ).first()
                
                donation_date = pd.to_datetime(row['donation_date'])
                date_key = int(donation_date.strftime('%Y%m%d'))
                
                if not donor or not campaign:
                    logger.warning(f"Skipping donation {row['donation_id']}: missing donor or campaign reference")
                    continue
                
                donation = FactDonation(
                    donation_id=row['donation_id'],
                    donor_key=donor.donor_key,
                    campaign_key=campaign.campaign_key,
                    date_key=date_key,
                    amount=float(row['amount']),
                    payment_method=row['payment_method'],
                    is_recurring=row['is_recurring'] == True or row['is_recurring'] == 'True',
                    notes=row['notes'] if pd.notna(row['notes']) else None
                )
                self.session.add(donation)
                self.stats['donations_loaded'] += 1
            
            logger.info(f"Loaded {self.stats['donations_loaded']} donations")
            
        except FileNotFoundError:
            logger.error("Donations file not found: data/raw/donations.csv")
            raise
    
    def _validate_donations(self, df: pd.DataFrame):
        """Validate donation data quality"""
        errors = []
        
        if df['donation_id'].isna().any():
            errors.append("Missing donation_id values found")
        
        if df['amount'].isna().any():
            errors.append("Missing amount values found")
        
        # Check for negative amounts
        negative = df[df['amount'] < 0]
        if len(negative) > 0:
            errors.append(f"Found {len(negative)} donations with negative amounts")
        
        # Flag unusually large donations (potential anomalies)
        large_donations = df[df['amount'] > 50000]
        if len(large_donations) > 0:
            logger.info(f"ANOMALY ALERT: Found {len(large_donations)} donations over $50,000")
        
        if errors:
            raise DataQualityError(f"Donation data quality issues: {errors}")
        
        logger.info("Donation data quality validation passed")
    
    def _load_elk_populations(self):
        """Load elk population fact data from habitat areas"""
        logger.info("Loading elk population facts...")
        
        try:
            with open('data/raw/habitat_areas.json', 'r') as f:
                habitats = json.load(f)
            
            populations_loaded = 0
            
            for habitat_data in habitats:
                habitat = self.session.query(DimHabitat).filter_by(
                    habitat_id=habitat_data['habitat_id']
                ).first()
                
                if not habitat:
                    continue
                
                # Load population data for each year
                years = [2020, 2021, 2022, 2023, 2024]
                prev_count = None
                
                for year in years:
                    pop_key = f'elk_population_{year}'
                    if pop_key not in habitat_data:
                        continue
                    
                    elk_count = habitat_data[pop_key]
                    
                    # Check if already exists
                    existing = self.session.query(FactElkPopulation).filter_by(
                        habitat_key=habitat.habitat_key,
                        year=year
                    ).first()
                    
                    if existing:
                        prev_count = elk_count
                        continue
                    
                    # Calculate change from previous year
                    change = elk_count - prev_count if prev_count else 0
                    change_pct = (change / prev_count * 100) if prev_count else 0
                    
                    pop_fact = FactElkPopulation(
                        habitat_key=habitat.habitat_key,
                        year=year,
                        elk_count=elk_count,
                        population_change=change,
                        population_change_pct=round(change_pct, 2)
                    )
                    self.session.add(pop_fact)
                    populations_loaded += 1
                    prev_count = elk_count
            
            logger.info(f"Loaded {populations_loaded} elk population records")
            
        except FileNotFoundError:
            logger.error("Habitat file not found for population data")
            raise
    
    def _load_conservation_facts(self):
        """Load conservation project fact data"""
        logger.info("Loading conservation facts...")
        
        try:
            with open('data/raw/conservation_projects.json', 'r') as f:
                projects = json.load(f)
            
            facts_loaded = 0
            
            for project_data in projects:
                project = self.session.query(DimProject).filter_by(
                    project_id=project_data['project_id']
                ).first()
                
                if not project:
                    continue
                
                # Use start date for date key
                start_date = pd.to_datetime(project_data['start_date'])
                date_key = int(start_date.strftime('%Y%m%d'))
                
                # Check if already exists
                existing = self.session.query(FactConservation).filter_by(
                    project_key=project.project_key
                ).first()
                
                if existing:
                    continue
                
                conservation_fact = FactConservation(
                    project_key=project.project_key,
                    habitat_key=None,  # Could be linked if we had mapping
                    date_key=date_key,
                    budget=project_data['budget'],
                    spent_to_date=project_data['spent_to_date'],
                    acres_protected=project_data['acres_protected'],
                    elk_population_impacted=project_data['elk_population_impacted']
                )
                self.session.add(conservation_fact)
                facts_loaded += 1
            
            logger.info(f"Loaded {facts_loaded} conservation fact records")
            
        except FileNotFoundError:
            logger.error("Projects file not found for conservation facts")
            raise


if __name__ == "__main__":
    pipeline = RMEFPipeline()
    stats = pipeline.run()
    print(f"\nPipeline completed with stats: {stats}")
