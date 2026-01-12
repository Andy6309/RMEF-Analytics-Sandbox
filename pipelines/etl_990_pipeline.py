"""
RMEF Analytics - Form 990 ETL Pipeline
Loads extracted Form 990 data into the analytics database
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.schema import (
    get_engine, create_tables, get_session,
    Fact990Financial, Fact990ProgramService
)
from pipelines.extract_990_data import extract_all_990s, save_extracted_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Form990_ETL')


class Form990Pipeline:
    """ETL Pipeline for Form 990 data"""
    
    def __init__(self, db_path: str = "sqlite:///data/rmef_analytics.db"):
        self.db_path = db_path
        self.engine = get_engine(db_path)
        self.session = None
        self.stats = {
            'financial_records_loaded': 0,
            'program_records_loaded': 0,
            'errors': []
        }
    
    def run(self, extract_fresh: bool = True) -> Dict[str, Any]:
        """Execute the full ETL pipeline"""
        logger.info("=" * 60)
        logger.info("Starting Form 990 ETL Pipeline")
        logger.info("=" * 60)
        
        try:
            # Initialize database
            self._init_database()
            
            # Extract data from PDFs (or load from JSON)
            if extract_fresh:
                logger.info("Extracting fresh data from PDFs...")
                data = extract_all_990s()
                save_extracted_data(data)
            else:
                logger.info("Loading existing extracted data...")
                data = self._load_extracted_data()
            
            # Transform and load
            self._load_financial_data(data)
            self._load_program_services(data)
            
            # Commit all changes
            self.session.commit()
            logger.info("=" * 60)
            logger.info("Form 990 ETL Pipeline completed successfully!")
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
    
    def _load_extracted_data(self) -> List[Dict]:
        """Load previously extracted data from JSON"""
        json_path = Path("data/raw/form_990_data.json")
        if not json_path.exists():
            raise FileNotFoundError(f"Extracted data not found: {json_path}")
        
        with open(json_path, 'r') as f:
            return json.load(f)
    
    def _load_financial_data(self, data: List[Dict]):
        """Load financial summary data"""
        logger.info("Loading Form 990 financial data...")
        
        for record in data:
            fiscal_year = record['fiscal_year']
            
            # Check if record already exists
            existing = self.session.query(Fact990Financial).filter_by(
                fiscal_year=fiscal_year
            ).first()
            
            if existing:
                # Update existing record
                existing.contributions_and_grants = record['contributions_and_grants']
                existing.program_service_revenue = record['program_service_revenue']
                existing.investment_income = record['investment_income']
                existing.other_revenue = record['other_revenue']
                existing.total_revenue = record['total_revenue']
                existing.grants_and_similar_paid = record['grants_and_similar_paid']
                existing.salaries_and_wages = record['salaries_and_wages']
                existing.total_expenses = record['total_expenses']
                existing.total_assets = record['total_assets']
                existing.total_liabilities = record['total_liabilities']
                existing.net_assets = record['net_assets']
                existing.program_services_expenses = record['program_services_expenses']
                existing.revenue_less_expenses = record['total_revenue'] - record['total_expenses']
                logger.info(f"Updated financial record for {fiscal_year}")
            else:
                # Create new record
                financial = Fact990Financial(
                    fiscal_year=fiscal_year,
                    tax_year=record['tax_year'],
                    contributions_and_grants=record['contributions_and_grants'],
                    program_service_revenue=record['program_service_revenue'],
                    investment_income=record['investment_income'],
                    other_revenue=record['other_revenue'],
                    total_revenue=record['total_revenue'],
                    grants_and_similar_paid=record['grants_and_similar_paid'],
                    salaries_and_wages=record['salaries_and_wages'],
                    total_expenses=record['total_expenses'],
                    total_assets=record['total_assets'],
                    total_liabilities=record['total_liabilities'],
                    net_assets=record['net_assets'],
                    program_services_expenses=record['program_services_expenses'],
                    management_and_general_expenses=record['management_and_general_expenses'],
                    fundraising_expenses=record['fundraising_expenses'],
                    revenue_less_expenses=record['total_revenue'] - record['total_expenses']
                )
                self.session.add(financial)
                self.stats['financial_records_loaded'] += 1
                logger.info(f"Loaded financial record for {fiscal_year}")
    
    def _load_program_services(self, data: List[Dict]):
        """Load program service details"""
        logger.info("Loading Form 990 program service data...")
        
        for record in data:
            fiscal_year = record['fiscal_year']
            programs = record.get('program_services', {})
            
            for program_name, program_data in programs.items():
                # Check if record already exists
                existing = self.session.query(Fact990ProgramService).filter_by(
                    fiscal_year=fiscal_year,
                    program_name=program_name
                ).first()
                
                if existing:
                    # Update existing record
                    existing.expenses = program_data['expenses']
                    existing.grants = program_data['grants']
                    existing.revenue = program_data['revenue']
                else:
                    # Create new record
                    program = Fact990ProgramService(
                        fiscal_year=fiscal_year,
                        program_name=program_name,
                        expenses=program_data['expenses'],
                        grants=program_data['grants'],
                        revenue=program_data['revenue']
                    )
                    self.session.add(program)
                    self.stats['program_records_loaded'] += 1
        
        logger.info(f"Loaded {self.stats['program_records_loaded']} program service records")


if __name__ == "__main__":
    pipeline = Form990Pipeline()
    stats = pipeline.run(extract_fresh=True)
    print(f"\nPipeline completed with stats: {stats}")
