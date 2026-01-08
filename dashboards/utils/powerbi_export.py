"""
Power BI Export Utilities
Provides functionality to export dashboard data in Power BI-compatible formats
"""

import pandas as pd
import streamlit as st
from io import BytesIO
import json
from datetime import datetime


class PowerBIExporter:
    """Handle data exports for Power BI integration"""
    
    def __init__(self):
        self.export_formats = {
            'Excel (.xlsx)': 'xlsx',
            'CSV (.csv)': 'csv',
            'JSON (.json)': 'json'
        }
    
    def prepare_donations_export(self, donations_df):
        """Prepare donations data for export"""
        export_df = donations_df.copy()
        
        if len(export_df) > 0:
            export_df['donation_date'] = pd.to_datetime(export_df['donation_date'])
            export_df['donor_full_name'] = export_df['first_name'] + ' ' + export_df['last_name']
            
            columns_order = [
                'donation_id', 'donation_date', 'donor_id', 'donor_full_name',
                'donor_type', 'membership_level', 'donor_state', 'amount',
                'payment_method', 'is_recurring', 'campaign_id', 'campaign_name',
                'campaign_type', 'target_region', 'year', 'quarter', 'month', 'month_name'
            ]
            
            available_columns = [col for col in columns_order if col in export_df.columns]
            export_df = export_df[available_columns]
        
        return export_df
    
    def prepare_membership_export(self, membership_df):
        """Prepare membership data for export"""
        export_df = membership_df.copy()
        
        if len(export_df) > 0:
            export_df['join_date'] = pd.to_datetime(export_df['join_date'])
            
            columns_order = [
                'donor_id', 'first_name', 'last_name', 'email',
                'donor_type', 'membership_level', 'state', 'join_date'
            ]
            
            available_columns = [col for col in columns_order if col in export_df.columns]
            export_df = export_df[available_columns]
        
        return export_df
    
    def prepare_conservation_export(self, conservation_df):
        """Prepare conservation projects data for export"""
        export_df = conservation_df.copy()
        
        if len(export_df) > 0:
            export_df['budget_utilization_pct'] = (
                export_df['spent_to_date'] / export_df['budget'] * 100
            ).round(2)
            
            columns_order = [
                'project_id', 'project_name', 'project_type', 'state', 'county',
                'status', 'budget', 'spent_to_date', 'budget_utilization_pct',
                'acres_protected', 'elk_population_impacted'
            ]
            
            available_columns = [col for col in columns_order if col in export_df.columns]
            export_df = export_df[available_columns]
        
        return export_df
    
    def prepare_habitat_export(self, habitat_df):
        """Prepare habitat data for export"""
        export_df = habitat_df.copy()
        
        if len(export_df) > 0:
            columns_order = [
                'habitat_id', 'habitat_name', 'state', 'region',
                'total_acres', 'habitat_quality_score', 'conservation_status'
            ]
            
            available_columns = [col for col in columns_order if col in export_df.columns]
            export_df = export_df[available_columns]
        
        return export_df
    
    def prepare_elk_population_export(self, elk_df):
        """Prepare elk population data for export"""
        export_df = elk_df.copy()
        
        if len(export_df) > 0:
            columns_order = [
                'year', 'habitat_id', 'habitat_name', 'state', 'region',
                'elk_count', 'population_change', 'population_change_pct',
                'total_acres', 'habitat_quality_score', 'conservation_status'
            ]
            
            available_columns = [col for col in columns_order if col in export_df.columns]
            export_df = export_df[available_columns]
        
        return export_df
    
    def prepare_summary_metrics_export(self, donations_df, membership_df, 
                                       elk_df, conservation_df):
        """Prepare summary metrics for export"""
        metrics_data = []
        
        total_donations = donations_df['amount'].sum() if len(donations_df) > 0 else 0
        total_members = len(membership_df)
        total_acres = conservation_df['acres_protected'].sum() if len(conservation_df) > 0 else 0
        
        if len(elk_df) > 0:
            latest_year = elk_df['year'].max()
            total_elk = elk_df[elk_df['year'] == latest_year]['elk_count'].sum()
        else:
            latest_year = datetime.now().year
            total_elk = 0
        
        metrics_data.append({
            'metric_name': 'Total Donations',
            'metric_value': total_donations,
            'metric_category': 'Financial',
            'as_of_date': datetime.now().strftime('%Y-%m-%d')
        })
        
        metrics_data.append({
            'metric_name': 'Total Members',
            'metric_value': total_members,
            'metric_category': 'Membership',
            'as_of_date': datetime.now().strftime('%Y-%m-%d')
        })
        
        metrics_data.append({
            'metric_name': 'Total Elk Population',
            'metric_value': total_elk,
            'metric_category': 'Conservation',
            'as_of_date': f'{latest_year}-12-31'
        })
        
        metrics_data.append({
            'metric_name': 'Total Acres Protected',
            'metric_value': total_acres,
            'metric_category': 'Conservation',
            'as_of_date': datetime.now().strftime('%Y-%m-%d')
        })
        
        return pd.DataFrame(metrics_data)
    
    def export_to_excel(self, datasets_dict):
        """Export multiple datasets to Excel with separate sheets"""
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for sheet_name, df in datasets_dict.items():
                if len(df) > 0:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        output.seek(0)
        return output
    
    def export_to_csv(self, df):
        """Export single dataset to CSV"""
        return df.to_csv(index=False).encode('utf-8')
    
    def export_to_json(self, datasets_dict):
        """Export datasets to JSON format"""
        json_data = {}
        
        for name, df in datasets_dict.items():
            if len(df) > 0:
                df_copy = df.copy()
                for col in df_copy.select_dtypes(include=['datetime64']).columns:
                    df_copy[col] = df_copy[col].astype(str)
                json_data[name] = df_copy.to_dict(orient='records')
        
        return json.dumps(json_data, indent=2, default=str).encode('utf-8')
    
    def get_export_filename(self, dataset_names, file_format):
        """
        Generate filename for export including selected dataset names
        
        Args:
            dataset_names: List of dataset names selected for export
            file_format: File extension (xlsx, csv, json)
        
        Returns:
            Formatted filename with dataset names and timestamp
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if len(dataset_names) == 1:
            dataset_part = dataset_names[0].replace(' ', '_')
        elif len(dataset_names) <= 3:
            dataset_part = '_'.join([name.replace(' ', '_') for name in dataset_names])
        else:
            dataset_part = f"{len(dataset_names)}_Datasets"
        
        return f"RMEF_{dataset_part}_{timestamp}.{file_format}"
