# Power BI Export Feature Guide

## Overview

The RMEF Analytics Dashboard now includes a comprehensive Power BI export feature that allows users to compile and export dashboard data in formats compatible with Power BI Desktop and Power BI Service.

## Features

### Supported Export Formats

1. **Excel (.xlsx)** - Recommended for multi-dataset exports
   - Multiple datasets exported as separate sheets
   - Preserves data types and formatting
   - Easy to import into Power BI

2. **CSV (.csv)** - Universal compatibility
   - Single dataset per file
   - Compatible with all data tools
   - Lightweight file size

3. **JSON (.json)** - Structured data format
   - Hierarchical data structure
   - Preserves complex data types
   - Ideal for API integrations

### Available Datasets

Users can select from the following datasets:

1. **Summary Metrics** - Key performance indicators
   - Total Donations
   - Total Members
   - Total Elk Population
   - Total Acres Protected

2. **Donations** - Detailed transaction data
   - Donation amounts and dates
   - Donor information
   - Campaign details
   - Payment methods

3. **Membership** - Member directory
   - Contact information
   - Membership levels
   - Join dates
   - Geographic distribution

4. **Conservation Projects** - Project tracking
   - Budget and spending
   - Acres protected
   - Project status
   - Geographic location

5. **Habitat Areas** - Habitat information
   - Quality scores
   - Conservation status
   - Regional data

6. **Elk Population** - Population trends
   - Historical data by year
   - Habitat-specific counts
   - Population changes

## How to Use

### Step 1: Access the Export Feature

1. Open the RMEF Analytics Dashboard
2. Scroll to the bottom of the page
3. Expand the "Power BI Export" section

### Step 2: Select Datasets

1. Check the boxes for datasets you want to export
2. Review the record counts for each dataset
3. Read the descriptions to understand what each dataset contains

### Step 3: Choose Export Format

1. Select your preferred format from the dropdown:
   - **Excel** for multiple datasets
   - **CSV** for single dataset
   - **JSON** for structured data

2. Review the format information displayed

### Step 4: Generate and Download

1. Click the "Generate Export" button
2. Wait for the export to be prepared
3. Click the "Download File" button
4. Save the file to your desired location

## Importing into Power BI

### Excel Import (Recommended)

1. Open **Power BI Desktop**
2. Click **Home** → **Get Data** → **Excel Workbook**
3. Navigate to your downloaded file
4. Select the sheets (datasets) you want to import
5. Click **Load** or **Transform Data** for customization

### CSV Import

1. Open **Power BI Desktop**
2. Click **Home** → **Get Data** → **Text/CSV**
3. Select your downloaded CSV file
4. Review the data preview
5. Click **Load**

### JSON Import

1. Open **Power BI Desktop**
2. Click **Home** → **Get Data** → **JSON**
3. Select your downloaded JSON file
4. Expand the records in the Power Query Editor
5. Select columns to import
6. Click **Close & Apply**

## Creating Relationships in Power BI

After importing multiple datasets, create relationships for better analysis:

### Recommended Relationships

1. **Donations ↔ Membership**
   - Link: `donor_id` (both tables)
   - Cardinality: Many-to-One

2. **Elk Population ↔ Habitat Areas**
   - Link: `habitat_id` (both tables)
   - Cardinality: Many-to-One

3. **Conservation Projects ↔ Habitat Areas**
   - Link: `state` (both tables)
   - Cardinality: Many-to-Many

### Creating Relationships

1. Go to **Model** view in Power BI
2. Drag a field from one table to the matching field in another
3. Configure the relationship settings
4. Set the cross-filter direction as needed

## Power BI Dashboard Tips

### Key Measures to Create

```dax
Total Donations = SUM(Donations[amount])

Total Members = COUNTROWS(Membership)

Average Donation = AVERAGE(Donations[amount])

Member Growth Rate = 
DIVIDE(
    COUNTROWS(FILTER(Membership, Membership[join_date] >= TODAY() - 90)),
    COUNTROWS(Membership)
)

Conservation ROI = 
DIVIDE(
    SUM(Conservation_Projects[acres_protected]),
    SUM(Conservation_Projects[spent_to_date])
)
```

### Recommended Visualizations

1. **KPI Cards** - Use Summary Metrics for quick insights
2. **Time Series Charts** - Track donations and membership over time
3. **Geographic Maps** - Show distribution by state
4. **Funnel Charts** - Display membership tier progression
5. **Scatter Plots** - Analyze habitat quality vs. elk population

### Date Intelligence

Enable Auto Date/Time in Power BI:
1. Go to **File** → **Options and Settings** → **Options**
2. Select **Data Load** → **Time Intelligence**
3. Check **Auto Date/Time**

This enables time-based analysis without creating date tables.

## Filtering and Slicing

The exported data respects all filters applied in the dashboard:

- **Time Period** - Filters donations and membership by date
- **Campaign Type** - Filters donation data
- **Donor Type** - Filters donation data
- **Region** - Filters elk population and habitat data

Export data with different filter combinations to create multiple views.

## Best Practices

### Data Refresh Strategy

1. **Manual Refresh**: Export new data periodically
2. **Scheduled Updates**: Set a regular export schedule (weekly/monthly)
3. **Version Control**: Include timestamps in filenames

### Performance Optimization

1. **Selective Exports**: Only export datasets you need
2. **Date Filtering**: Use dashboard filters to limit data range
3. **Excel Format**: Use for best performance with multiple datasets

### Data Quality

1. **Verify Record Counts**: Check total records before export
2. **Review Data Types**: Ensure dates and numbers are formatted correctly
3. **Test Imports**: Import a small sample first to verify structure

## Troubleshooting

### Common Issues

**Issue**: CSV export only includes one dataset
- **Solution**: Use Excel format for multiple datasets

**Issue**: Dates not recognized in Power BI
- **Solution**: In Power Query, change column type to Date/DateTime

**Issue**: Large file size
- **Solution**: Apply filters in dashboard before exporting

**Issue**: Missing relationships in Power BI
- **Solution**: Manually create relationships in Model view

### Getting Help

If you encounter issues:
1. Check the in-dashboard instructions (expand "Power BI Import Instructions")
2. Verify your Power BI Desktop version is up to date
3. Review the export format compatibility

## Advanced Usage

### Combining with Other Data Sources

Power BI can combine RMEF data with:
- External databases (SQL Server, PostgreSQL)
- Web APIs
- Other Excel/CSV files
- SharePoint lists

### Creating Custom Calculations

Use DAX (Data Analysis Expressions) to create:
- Custom KPIs
- Year-over-year comparisons
- Running totals
- Percentage calculations

### Publishing to Power BI Service

1. Create your report in Power BI Desktop
2. Click **File** → **Publish** → **Publish to Power BI**
3. Select your workspace
4. Share with stakeholders

## File Naming Convention

Exported files follow this pattern:
```
RMEF_[DatasetType]_[YYYYMMDD]_[HHMMSS].[extension]
```

Example: `RMEF_Dashboard_Data_20260108_143022.xlsx`

## Data Dictionary

### Donations Dataset
- `donation_id`: Unique donation identifier
- `donation_date`: Date of donation
- `amount`: Donation amount in USD
- `donor_type`: Individual, Corporate, Foundation, etc.
- `campaign_type`: Type of fundraising campaign
- `is_recurring`: Boolean for recurring donations

### Membership Dataset
- `donor_id`: Unique member identifier
- `membership_level`: Supporting, Team Elk, Sportsman, Heritage, Life
- `join_date`: Date member joined
- `state`: Member's state of residence

### Conservation Projects Dataset
- `project_id`: Unique project identifier
- `budget`: Total project budget
- `spent_to_date`: Amount spent so far
- `acres_protected`: Total acres protected by project
- `status`: Active, Completed, Planned

### Habitat Areas Dataset
- `habitat_id`: Unique habitat identifier
- `habitat_quality_score`: Quality rating (0-100)
- `conservation_status`: Protected, At Risk, etc.
- `total_acres`: Size of habitat area

### Elk Population Dataset
- `year`: Year of population count
- `elk_count`: Number of elk counted
- `population_change`: Change from previous year
- `population_change_pct`: Percentage change

## Support

For technical support or feature requests, contact the RMEF Analytics team.
