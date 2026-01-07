"""
RMEF Analytics Sandbox - Pipeline Tests
Tests for ETL pipeline functionality
"""

import pytest
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
import tempfile
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.schema import (
    get_engine, create_tables, get_session,
    DimDonor, DimCampaign, DimDate, DimHabitat, DimProject,
    FactDonation, FactElkPopulation, FactConservation, Base
)
from pipelines.etl_pipeline import RMEFPipeline


class TestDatabaseSchema:
    """Test database schema creation"""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing"""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        engine = create_engine(f"sqlite:///{path}")
        yield engine, path
        os.unlink(path)
    
    def test_create_tables(self, temp_db):
        """Test that all tables are created successfully"""
        engine, path = temp_db
        create_tables(engine)
        
        # Check tables exist
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ))
            tables = [row[0] for row in result]
        
        expected_tables = [
            'dim_donor', 'dim_campaign', 'dim_date', 
            'dim_habitat', 'dim_project',
            'fact_donation', 'fact_elk_population', 'fact_conservation'
        ]
        
        for table in expected_tables:
            assert table in tables, f"Table {table} not created"
    
    def test_dimension_table_columns(self, temp_db):
        """Test that dimension tables have expected columns"""
        engine, path = temp_db
        create_tables(engine)
        
        with engine.connect() as conn:
            # Check dim_donor columns
            result = conn.execute(text("PRAGMA table_info(dim_donor)"))
            columns = [row[1] for row in result]
            
            expected_columns = ['donor_key', 'donor_id', 'first_name', 'last_name', 
                              'email', 'donor_type', 'membership_level']
            for col in expected_columns:
                assert col in columns, f"Column {col} not in dim_donor"


class TestPipelineExecution:
    """Test ETL pipeline execution"""
    
    @pytest.fixture
    def pipeline_with_temp_db(self):
        """Create pipeline with temporary database"""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        pipeline = RMEFPipeline(db_path=f"sqlite:///{path}")
        yield pipeline, path
        os.unlink(path)
    
    def test_pipeline_runs_without_error(self, pipeline_with_temp_db):
        """Test that pipeline completes without errors"""
        pipeline, path = pipeline_with_temp_db
        
        # Change to project root for file paths
        original_cwd = os.getcwd()
        os.chdir(Path(__file__).parent.parent)
        
        try:
            stats = pipeline.run()
            assert 'errors' in stats
            assert len(stats['errors']) == 0, f"Pipeline had errors: {stats['errors']}"
        finally:
            os.chdir(original_cwd)
    
    def test_pipeline_loads_data(self, pipeline_with_temp_db):
        """Test that pipeline loads data into tables"""
        pipeline, path = pipeline_with_temp_db
        
        original_cwd = os.getcwd()
        os.chdir(Path(__file__).parent.parent)
        
        try:
            stats = pipeline.run()
            
            # Check that data was loaded
            assert stats['donors_loaded'] > 0, "No donors loaded"
            assert stats['campaigns_loaded'] > 0, "No campaigns loaded"
            assert stats['donations_loaded'] > 0, "No donations loaded"
            assert stats['habitats_loaded'] > 0, "No habitats loaded"
            assert stats['projects_loaded'] > 0, "No projects loaded"
        finally:
            os.chdir(original_cwd)
    
    def test_pipeline_idempotent(self, pipeline_with_temp_db):
        """Test that running pipeline twice doesn't duplicate data"""
        pipeline, path = pipeline_with_temp_db
        
        original_cwd = os.getcwd()
        os.chdir(Path(__file__).parent.parent)
        
        try:
            # Run pipeline twice
            stats1 = pipeline.run()
            
            # Create new pipeline instance for second run
            pipeline2 = RMEFPipeline(db_path=f"sqlite:///{path}")
            stats2 = pipeline2.run()
            
            # Second run should load 0 new records (already exist)
            assert stats2['donors_loaded'] == 0, "Duplicate donors loaded on second run"
            assert stats2['campaigns_loaded'] == 0, "Duplicate campaigns loaded on second run"
        finally:
            os.chdir(original_cwd)


class TestDataIntegrity:
    """Test data integrity after pipeline execution"""
    
    @pytest.fixture
    def loaded_db(self):
        """Create and load a temporary database"""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        
        original_cwd = os.getcwd()
        os.chdir(Path(__file__).parent.parent)
        
        pipeline = RMEFPipeline(db_path=f"sqlite:///{path}")
        pipeline.run()
        
        engine = create_engine(f"sqlite:///{path}")
        
        os.chdir(original_cwd)
        
        yield engine, path
        os.unlink(path)
    
    def test_foreign_key_integrity(self, loaded_db):
        """Test that all foreign keys reference valid records"""
        engine, path = loaded_db
        
        with engine.connect() as conn:
            # Check donation foreign keys
            result = conn.execute(text("""
                SELECT COUNT(*) FROM fact_donation fd
                LEFT JOIN dim_donor dd ON fd.donor_key = dd.donor_key
                WHERE dd.donor_key IS NULL
            """))
            orphan_donations = result.scalar()
            assert orphan_donations == 0, f"Found {orphan_donations} donations with invalid donor references"
    
    def test_date_dimension_coverage(self, loaded_db):
        """Test that date dimension covers all transaction dates"""
        engine, path = loaded_db
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT COUNT(*) FROM fact_donation fd
                LEFT JOIN dim_date dd ON fd.date_key = dd.date_key
                WHERE dd.date_key IS NULL
            """))
            missing_dates = result.scalar()
            assert missing_dates == 0, f"Found {missing_dates} donations with missing date references"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
