# RMEF Analytics Sandbox

![CI Pipeline](https://github.com/Andy6309/RMEF-Analytics-Sandbox/workflows/CI%20Pipeline/badge.svg)
![Deploy Dashboard](https://github.com/Andy6309/RMEF-Analytics-Sandbox/workflows/Deploy%20Dashboard/badge.svg)
![Data Quality](https://github.com/Andy6309/RMEF-Analytics-Sandbox/workflows/Data%20Quality%20Checks/badge.svg)

A full-stack analytics project demonstrating end-to-end data engineering and dashboard capabilities, themed around the Rocky Mountain Elk Foundation (RMEF). This project simulates integrating multiple conservation-related data sources, modeling data, building ETL/ELT pipelines, and creating interactive dashboards.

## Live Dashboard

**[View Live Dashboard](https://rmef-analytics.streamlit.app/)**

![RMEF Analytics Dashboard](assets/RMEF-Analytics.png)

## Project Overview

This analytics sandbox provides:
- **Data Integration**: Ingests data from CSV, JSON, and PDF sources (donors, donations, campaigns, conservation projects, habitat areas, IRS Form 990 filings)
- **Star Schema Data Model**: Dimensional modeling with fact and dimension tables optimized for analytics
- **ETL Pipeline**: Automated data extraction, transformation, and loading with error handling and logging, including PDF parsing for Form 990 data
- **Interactive Dashboard**: Streamlit-based visualization of key conservation and fundraising metrics
- **Financial Analysis**: Multi-year Form 990 financial reporting with revenue, expense, and program service analytics

## Project Structure

```
RMEF Analytics Sandbox/
├── data/
│   ├── raw/                    # Source data files
│   │   ├── donors.csv          # Donor/member information
│   │   ├── donations.csv       # Donation transactions
│   │   ├── campaigns.csv       # Fundraising campaigns
│   │   ├── conservation_projects.json  # Conservation projects
│   │   └── habitat_areas.json  # Elk habitat data
│   └── processed/              # Transformed data (if needed)
├── pipelines/
│   ├── __init__.py
│   └── etl_pipeline.py         # Main ETL pipeline
├── models/
│   ├── __init__.py
│   └── schema.py               # SQLAlchemy ORM models (star schema)
├── dashboards/
│   └── app.py                  # Streamlit dashboard application
├── notebooks/                  # Jupyter notebooks for exploration
├── tests/
│   ├── __init__.py
│   ├── test_data_quality.py    # Data quality validation tests
│   └── test_pipeline.py        # Pipeline functionality tests
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Tech Stack

- **Backend**: Python 3.9+, Pandas, SQLAlchemy
- **Database**: SQLite (easily portable to PostgreSQL)
- **Dashboard**: Streamlit with Plotly visualizations
- **PDF Processing**: pdfplumber for Form 990 data extraction
- **Testing**: pytest

## Data Model

### Star Schema Design

**Dimension Tables:**
- `dim_donor` - Donor/member information (type, membership level, location)
- `dim_campaign` - Fundraising campaign details (type, goals, status)
- `dim_date` - Date dimension for time-based analysis
- `dim_habitat` - Elk habitat areas (region, quality score, conservation status)
- `dim_project` - Conservation project details (type, status, partners)

**Fact Tables:**
- `fact_donation` - Donation transactions with amounts and payment details
- `fact_elk_population` - Elk population counts by habitat and year
- `fact_conservation` - Conservation project metrics (budget, acres, impact)
- `fact_990_financial` - IRS Form 990 financial data (revenue, expenses, assets, liabilities)
- `fact_990_program_service` - Form 990 program service details (expenses, grants, revenue by program)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the ETL Pipeline

```bash
python pipelines/etl_pipeline.py
```

This will:
- Create the SQLite database (`data/rmef_analytics.db`)
- Load all dimension and fact tables
- Validate data quality
- Log progress to `pipelines/etl.log`

### 3. Launch the Dashboard

```bash
streamlit run dashboards/app.py
```

The dashboard will open at `http://localhost:8501`

### 4. Run Tests

```bash
pytest tests/ -v
```

## Dashboard Features

The dashboard includes **two main tabs**: Operations Dashboard and Form 990 Financial Analysis.

### Operations Dashboard

#### Key Metrics (KPIs)
1. **Total Donations** - Sum of all donation amounts
2. **Acres Protected** - Total conservation land protected
3. **Elk Population** - Current elk count with year-over-year change
4. **Total Members** - Active donor/member count

#### Interactive Visualizations
- Donations by Campaign Type (bar chart)
- Donations by Donor Type (pie chart)
- Membership Growth Over Time (combo chart)
- **Elk Population by Habitat** - Interactive US map heatmap with state-level population density and hover cards showing individual habitat breakdowns
- Conservation Projects by Type (grouped bar)
- Habitat Quality by Region (scatter plot)

### Form 990 Financial Analysis

Comprehensive financial reporting dashboard analyzing IRS Form 990 data across multiple fiscal years.

#### Features:
- **Multi-Year Financial Overview** - Revenue, expenses, and net assets trends (2020-2023)
- **Year-over-Year Comparisons** - Percentage changes and growth metrics
- **Revenue Breakdown** - Contributions, program service revenue, investment income, and other revenue
- **Expense Analysis** - Program services, management & general, and fundraising expenses
- **Functional Allocation** - Pie chart showing expense distribution across functions
- **Program Service Details** - Individual program expenses, grants, and revenue
- **Balance Sheet Metrics** - Total assets, liabilities, and net assets over time
- **Financial Health Indicators** - Program efficiency ratios and sustainability metrics

#### Data Source:
- Automated PDF extraction from actual RMEF Form 990 filings (2020-2023)
- ETL pipeline processes PDF data into structured database tables
- Real financial data providing authentic nonprofit analytics experience

#### Key Metrics Tracked:
- Total Revenue & Expenses by year
- Net Assets (End of Year)
- Program Services Expenses vs. Total Expenses
- Revenue Less Expenses (surplus/deficit)
- Grants and Similar Amounts Paid
- Investment Income trends

### Filters
- **Date Range** - Filter donations by date
- **Campaign Type** - Filter by campaign category
- **Donor Type** - Individual, Corporate, or Foundation
- **Habitat Region** - Northern Rockies, Pacific Northwest, Southern Rockies

### Anomaly Detection
- Large donations (>$10,000) flagged
- At-risk habitats highlighted
- Population decline alerts

### Power BI Export
Export dashboard data for advanced analysis in Power BI:

**Available Datasets:**
- Summary Metrics - Key performance indicators
- Donations - Transaction details with donor and campaign info
- Membership - Member directory and contact information
- Conservation Projects - Budget, spending, and impact metrics
- Habitat Areas - Quality scores and conservation status
- Elk Population - Historical population data by habitat

**Export Formats:**
- **Excel (.xlsx)** - Recommended for multi-dataset exports with separate sheets
- **CSV (.csv)** - Single dataset, universal compatibility
- **JSON (.json)** - Structured data for API integrations

**How to Use:**
1. Open the "Power BI Export" section at the bottom of the dashboard
2. Select the datasets you want to export
3. Choose your preferred format (Excel recommended)
4. Click "Generate Export" then "Download File"
5. Import into Power BI Desktop: Get Data → Excel/CSV/JSON

**Power BI Integration:**
- Create relationships between tables (e.g., Donations ↔ Membership via `donor_id`)
- Enable Auto Date/Time for time-based analysis
- Use Summary Metrics sheet for quick KPI dashboards
- See `docs/POWERBI_EXPORT_GUIDE.md` for detailed instructions

## Data Sources

### Donors (`donors.csv`)
30 mock donors including individuals, corporations, and foundations across MT, WY, ID, and CO.

### Campaigns (`campaigns.csv`)
15 fundraising campaigns covering:
- Habitat protection and restoration
- Membership drives
- Land acquisition
- Research and education
- Corporate partnerships

### Donations (`donations.csv`)
50 donation transactions with amounts ranging from $25 to $100,000.

### Conservation Projects (`conservation_projects.json`)
10 active and completed projects including:
- Migration corridor protection
- Habitat restoration
- Land acquisition
- Research stations
- Public access improvements

### Habitat Areas (`habitat_areas.json`)
10 elk habitat regions with:
- Population data (2020-2024)
- Quality scores
- Conservation status
- Threat assessments

### Form 990 Financial Data (PDF)
IRS Form 990 filings for fiscal years 2020-2023 including:
- Total revenue and expenses
- Revenue breakdown (contributions, program service, investment, other)
- Expense allocation (program services, management, fundraising)
- Balance sheet data (assets, liabilities, net assets)
- Program service details with individual program metrics
- Automated PDF extraction and parsing into structured database

## Data Quality Checks

The pipeline includes automated validation:
- Missing value detection
- Duplicate ID checks
- Referential integrity validation
- Business rule validation (e.g., end_date > start_date)
- Anomaly flagging (large donations, budget overruns)

## Conservation Metrics

Key metrics tracked for RMEF decision-making:

| Metric | Description |
|--------|-------------|
| Donation Revenue | Total and by campaign/donor type |
| Membership Growth | New members and retention |
| Acres Protected | Land acquired or under easement |
| Elk Population | Counts and trends by habitat |
| Habitat Quality | Scores and conservation status |
| Project Progress | Budget utilization and completion |

## Configuration

### Database Connection
Default: `sqlite:///data/rmef_analytics.db`

To use PostgreSQL, update the connection string in `models/schema.py`:
```python
engine = get_engine("postgresql://user:pass@localhost/rmef_analytics")
```

### Logging
ETL logs are written to `pipelines/etl.log` with timestamps and severity levels.

## CI/CD & Deployment

### GitHub Actions Pipelines
Three automated workflows run on every push:

- **CI Pipeline** - Runs tests, linting, and code coverage
- **Deploy Pipeline** - Creates deployment artifacts
- **Data Quality** - Daily automated data quality checks

### Deployment
Live dashboard: Deploy to Streamlit Cloud by connecting your GitHub repository at https://share.streamlit.io

## License

This is a demonstration/portfolio project using mock data. Not affiliated with the actual Rocky Mountain Elk Foundation.

---

*Built for elk conservation and data analytics*
