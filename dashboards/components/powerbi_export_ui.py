"""
Power BI Export UI Component
Interactive component for selecting and exporting data to Power BI-compatible formats
"""

import streamlit as st
from dashboards.utils.powerbi_export import PowerBIExporter


def render_powerbi_export(donations_df, membership_df, elk_df, conservation_df, habitat_df):
    """
    Render Power BI export interface
    
    Args:
        donations_df: Donations dataframe
        membership_df: Membership dataframe
        elk_df: Elk population dataframe
        conservation_df: Conservation projects dataframe
        habitat_df: Habitat dataframe
    """
    
    with st.expander("Power BI Export", expanded=False):
        exporter = PowerBIExporter()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Select Datasets to Export")
            
            export_options = {
                'Summary Metrics': {
                    'description': 'Key performance indicators and summary statistics',
                    'records': 4,
                    'selected': st.checkbox('Summary Metrics', value=True, key='export_summary')
                },
                'Donations': {
                    'description': 'Detailed donation transactions with donor and campaign info',
                    'records': len(donations_df),
                    'selected': st.checkbox('Donations', value=True, key='export_donations')
                },
                'Membership': {
                    'description': 'Member directory with contact and membership details',
                    'records': len(membership_df),
                    'selected': st.checkbox('Membership', value=True, key='export_membership')
                },
                'Conservation Projects': {
                    'description': 'Conservation project details with budget and impact metrics',
                    'records': len(conservation_df),
                    'selected': st.checkbox('Conservation Projects', value=True, key='export_conservation')
                },
                'Habitat Areas': {
                    'description': 'Habitat area information with quality scores',
                    'records': len(habitat_df),
                    'selected': st.checkbox('Habitat Areas', value=True, key='export_habitat')
                },
                'Elk Population': {
                    'description': 'Historical elk population data by habitat and year',
                    'records': len(elk_df),
                    'selected': st.checkbox('Elk Population', value=True, key='export_elk')
                }
            }
            
            for dataset_name, info in export_options.items():
                if info['selected']:
                    st.caption(f"  ↳ {info['description']} ({info['records']:,} records)")
        
        with col2:
            st.subheader("Export Settings")
            
            export_format = st.selectbox(
                "File Format",
                options=list(exporter.export_formats.keys()),
                help="Excel is recommended for multi-dataset exports"
            )
            
            file_extension = exporter.export_formats[export_format]
            
            format_info = "Multiple sheets supported" if file_extension == 'xlsx' else "Single dataset per file"
            type_info = "Preserves data types" if file_extension in ['xlsx', 'json'] else "Universal compatibility"
            
            st.markdown(f"""
            <div style="background-color: #e7f2f8; border: 1px solid #0071bc; border-radius: 4px; padding: 1rem; margin-top: 0.5rem;">
                <p style="color: #212121; margin: 0; font-weight: 600;">Format: {export_format}</p>
                <ul style="color: #212121; margin: 0.5rem 0 0 0; padding-left: 1.5rem;">
                    <li style="color: #212121;">{format_info}</li>
                    <li style="color: #212121;">{type_info}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        selected_datasets = {name: info for name, info in export_options.items() if info['selected']}
        
        if not selected_datasets:
            st.warning("Please select at least one dataset to export.")
            return
        
        total_records = sum(info['records'] for info in selected_datasets.values())
        st.markdown(f"**Total records to export:** {total_records:,}")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("Generate Export", type="primary", use_container_width=True):
                with st.spinner("Preparing export..."):
                    try:
                        datasets_to_export = {}
                        
                        if export_options['Summary Metrics']['selected']:
                            datasets_to_export['Summary_Metrics'] = exporter.prepare_summary_metrics_export(
                                donations_df, membership_df, elk_df, conservation_df
                            )
                        
                        if export_options['Donations']['selected']:
                            datasets_to_export['Donations'] = exporter.prepare_donations_export(donations_df)
                        
                        if export_options['Membership']['selected']:
                            datasets_to_export['Membership'] = exporter.prepare_membership_export(membership_df)
                        
                        if export_options['Conservation Projects']['selected']:
                            datasets_to_export['Conservation_Projects'] = exporter.prepare_conservation_export(conservation_df)
                        
                        if export_options['Habitat Areas']['selected']:
                            datasets_to_export['Habitat_Areas'] = exporter.prepare_habitat_export(habitat_df)
                        
                        if export_options['Elk Population']['selected']:
                            datasets_to_export['Elk_Population'] = exporter.prepare_elk_population_export(elk_df)
                        
                        selected_dataset_names = [name for name, info in export_options.items() if info['selected']]
                        
                        if file_extension == 'xlsx':
                            export_data = exporter.export_to_excel(datasets_to_export)
                            mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                            filename = exporter.get_export_filename(selected_dataset_names, 'xlsx')
                        
                        elif file_extension == 'json':
                            export_data = exporter.export_to_json(datasets_to_export)
                            mime_type = 'application/json'
                            filename = exporter.get_export_filename(selected_dataset_names, 'json')
                        
                        else:
                            if len(datasets_to_export) > 1:
                                st.warning("CSV format selected with multiple datasets. Only the first dataset will be exported. Use Excel for multi-dataset exports.")
                            
                            first_dataset = list(datasets_to_export.values())[0]
                            export_data = exporter.export_to_csv(first_dataset)
                            mime_type = 'text/csv'
                            filename = exporter.get_export_filename([selected_dataset_names[0]], 'csv')
                        
                        st.session_state['export_data'] = export_data
                        st.session_state['export_filename'] = filename
                        st.session_state['export_mime'] = mime_type
                        st.session_state['export_ready'] = True
                        
                        st.success("Export generated successfully!")
                        
                    except Exception as e:
                        st.error(f"Error generating export: {str(e)}")
                        st.session_state['export_ready'] = False
        
        with col2:
            if st.session_state.get('export_ready', False):
                st.download_button(
                    label="Download File",
                    data=st.session_state['export_data'],
                    file_name=st.session_state['export_filename'],
                    mime=st.session_state['export_mime'],
                    use_container_width=True,
                    key='download_export_file'
                )
        
        with col3:
            if st.session_state.get('export_ready', False):
                if st.button("Clear Export", use_container_width=True, key='clear_export'):
                    st.session_state['export_ready'] = False
                    st.session_state.pop('export_data', None)
                    st.session_state.pop('export_filename', None)
                    st.session_state.pop('export_mime', None)
                    st.rerun()
                else:
                    st.success(f"Ready: `{st.session_state['export_filename']}`")
