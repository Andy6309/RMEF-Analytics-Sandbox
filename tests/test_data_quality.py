"""
RMEF Analytics Sandbox - Data Quality Tests
Validates data integrity and quality across all datasets
"""

import pytest
import pandas as pd
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestDonorsDataQuality:
    """Test data quality for donors dataset"""
    
    @pytest.fixture
    def donors_df(self):
        return pd.read_csv('data/raw/donors.csv')
    
    def test_no_missing_donor_ids(self, donors_df):
        """Ensure all donors have an ID"""
        assert donors_df['donor_id'].notna().all(), "Found missing donor_id values"
    
    def test_unique_donor_ids(self, donors_df):
        """Ensure donor IDs are unique"""
        assert donors_df['donor_id'].is_unique, "Found duplicate donor_id values"
    
    def test_valid_email_format(self, donors_df):
        """Ensure emails contain @ symbol"""
        valid_emails = donors_df['email'].str.contains('@', na=False)
        assert valid_emails.all(), f"Found {(~valid_emails).sum()} invalid emails"
    
    def test_valid_states(self, donors_df):
        """Ensure state codes are valid 2-letter codes"""
        valid_states = ['MT', 'WY', 'ID', 'CO', 'OR', 'WA', 'UT', 'NV', 'AZ', 'NM']
        assert donors_df['state'].isin(valid_states).all(), "Found invalid state codes"
    
    def test_valid_membership_levels(self, donors_df):
        """Ensure membership levels are valid"""
        valid_levels = ['Bronze', 'Silver', 'Gold', 'Platinum']
        assert donors_df['membership_level'].isin(valid_levels).all(), "Found invalid membership levels"
    
    def test_valid_donor_types(self, donors_df):
        """Ensure donor types are valid"""
        valid_types = ['Individual', 'Corporate', 'Foundation']
        assert donors_df['donor_type'].isin(valid_types).all(), "Found invalid donor types"


class TestCampaignsDataQuality:
    """Test data quality for campaigns dataset"""
    
    @pytest.fixture
    def campaigns_df(self):
        return pd.read_csv('data/raw/campaigns.csv')
    
    def test_no_missing_campaign_ids(self, campaigns_df):
        """Ensure all campaigns have an ID"""
        assert campaigns_df['campaign_id'].notna().all(), "Found missing campaign_id values"
    
    def test_unique_campaign_ids(self, campaigns_df):
        """Ensure campaign IDs are unique"""
        assert campaigns_df['campaign_id'].is_unique, "Found duplicate campaign_id values"
    
    def test_valid_date_range(self, campaigns_df):
        """Ensure end_date is after start_date"""
        campaigns_df['start'] = pd.to_datetime(campaigns_df['start_date'])
        campaigns_df['end'] = pd.to_datetime(campaigns_df['end_date'])
        assert (campaigns_df['end'] >= campaigns_df['start']).all(), "Found campaigns with end_date before start_date"
    
    def test_positive_goal_amounts(self, campaigns_df):
        """Ensure goal amounts are positive"""
        assert (campaigns_df['goal_amount'] > 0).all(), "Found campaigns with non-positive goal amounts"
    
    def test_valid_status(self, campaigns_df):
        """Ensure campaign status is valid"""
        valid_statuses = ['Active', 'Completed', 'Cancelled', 'Planned']
        assert campaigns_df['status'].isin(valid_statuses).all(), "Found invalid campaign statuses"


class TestDonationsDataQuality:
    """Test data quality for donations dataset"""
    
    @pytest.fixture
    def donations_df(self):
        return pd.read_csv('data/raw/donations.csv')
    
    @pytest.fixture
    def donors_df(self):
        return pd.read_csv('data/raw/donors.csv')
    
    @pytest.fixture
    def campaigns_df(self):
        return pd.read_csv('data/raw/campaigns.csv')
    
    def test_no_missing_donation_ids(self, donations_df):
        """Ensure all donations have an ID"""
        assert donations_df['donation_id'].notna().all(), "Found missing donation_id values"
    
    def test_unique_donation_ids(self, donations_df):
        """Ensure donation IDs are unique"""
        assert donations_df['donation_id'].is_unique, "Found duplicate donation_id values"
    
    def test_positive_amounts(self, donations_df):
        """Ensure donation amounts are positive"""
        assert (donations_df['amount'] > 0).all(), "Found donations with non-positive amounts"
    
    def test_valid_donor_references(self, donations_df, donors_df):
        """Ensure all donor_ids exist in donors table"""
        valid_donors = donors_df['donor_id'].tolist()
        assert donations_df['donor_id'].isin(valid_donors).all(), "Found donations with invalid donor references"
    
    def test_valid_campaign_references(self, donations_df, campaigns_df):
        """Ensure all campaign_ids exist in campaigns table"""
        valid_campaigns = campaigns_df['campaign_id'].tolist()
        assert donations_df['campaign_id'].isin(valid_campaigns).all(), "Found donations with invalid campaign references"
    
    def test_valid_payment_methods(self, donations_df):
        """Ensure payment methods are valid"""
        valid_methods = ['Credit Card', 'Check', 'Wire Transfer', 'Cash', 'ACH']
        assert donations_df['payment_method'].isin(valid_methods).all(), "Found invalid payment methods"


class TestConservationProjectsDataQuality:
    """Test data quality for conservation projects dataset"""
    
    @pytest.fixture
    def projects_data(self):
        with open('data/raw/conservation_projects.json', 'r') as f:
            return json.load(f)
    
    def test_no_missing_project_ids(self, projects_data):
        """Ensure all projects have an ID"""
        for project in projects_data:
            assert 'project_id' in project and project['project_id'], f"Missing project_id in {project}"
    
    def test_unique_project_ids(self, projects_data):
        """Ensure project IDs are unique"""
        ids = [p['project_id'] for p in projects_data]
        assert len(ids) == len(set(ids)), "Found duplicate project_id values"
    
    def test_budget_greater_than_spent(self, projects_data):
        """Ensure spent_to_date does not exceed budget"""
        for project in projects_data:
            assert project['spent_to_date'] <= project['budget'], \
                f"Project {project['project_id']} has spent more than budget"
    
    def test_valid_status(self, projects_data):
        """Ensure project status is valid"""
        valid_statuses = ['In Progress', 'Completed', 'Planned', 'On Hold']
        for project in projects_data:
            assert project['status'] in valid_statuses, \
                f"Project {project['project_id']} has invalid status: {project['status']}"
    
    def test_non_negative_acres(self, projects_data):
        """Ensure acres_protected is non-negative"""
        for project in projects_data:
            assert project['acres_protected'] >= 0, \
                f"Project {project['project_id']} has negative acres_protected"


class TestHabitatAreasDataQuality:
    """Test data quality for habitat areas dataset"""
    
    @pytest.fixture
    def habitats_data(self):
        with open('data/raw/habitat_areas.json', 'r') as f:
            return json.load(f)
    
    def test_no_missing_habitat_ids(self, habitats_data):
        """Ensure all habitats have an ID"""
        for habitat in habitats_data:
            assert 'habitat_id' in habitat and habitat['habitat_id'], f"Missing habitat_id"
    
    def test_unique_habitat_ids(self, habitats_data):
        """Ensure habitat IDs are unique"""
        ids = [h['habitat_id'] for h in habitats_data]
        assert len(ids) == len(set(ids)), "Found duplicate habitat_id values"
    
    def test_valid_quality_scores(self, habitats_data):
        """Ensure quality scores are between 0 and 100"""
        for habitat in habitats_data:
            score = habitat['habitat_quality_score']
            assert 0 <= score <= 100, \
                f"Habitat {habitat['habitat_id']} has invalid quality score: {score}"
    
    def test_protected_acres_not_exceed_total(self, habitats_data):
        """Ensure protected acres don't exceed total acres"""
        for habitat in habitats_data:
            assert habitat['protected_acres'] <= habitat['total_acres'], \
                f"Habitat {habitat['habitat_id']} has protected_acres > total_acres"
    
    def test_elk_population_positive(self, habitats_data):
        """Ensure elk populations are positive"""
        years = [2020, 2021, 2022, 2023, 2024]
        for habitat in habitats_data:
            for year in years:
                key = f'elk_population_{year}'
                if key in habitat:
                    assert habitat[key] > 0, \
                        f"Habitat {habitat['habitat_id']} has non-positive elk population for {year}"


class TestDataConsistency:
    """Test cross-dataset consistency"""
    
    def test_donation_amounts_reasonable(self):
        """Check for reasonable donation amounts"""
        donations_df = pd.read_csv('data/raw/donations.csv')
        
        # Flag very large donations (over $100k) as potential anomalies
        large_donations = donations_df[donations_df['amount'] > 100000]
        
        # This is informational, not a failure
        if len(large_donations) > 0:
            print(f"INFO: Found {len(large_donations)} donations over $100,000")
    
    def test_campaign_goal_progress(self):
        """Check campaign goal achievement"""
        campaigns_df = pd.read_csv('data/raw/campaigns.csv')
        donations_df = pd.read_csv('data/raw/donations.csv')
        
        campaign_totals = donations_df.groupby('campaign_id')['amount'].sum()
        
        for _, campaign in campaigns_df.iterrows():
            campaign_id = campaign['campaign_id']
            goal = campaign['goal_amount']
            raised = campaign_totals.get(campaign_id, 0)
            
            # Informational check
            pct = (raised / goal * 100) if goal > 0 else 0
            if pct > 100 and campaign['status'] == 'Active':
                print(f"INFO: Campaign {campaign_id} has exceeded goal ({pct:.1f}%)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
