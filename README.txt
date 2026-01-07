# Project Name: RMEF Analytics Sandbox

## Objective:
Generate a full-stack analytics project that demonstrates end-to-end data engineering and dashboard capabilities, themed around the Rocky Mountain Elk Foundation (RMEF). The project should simulate integrating multiple conservation-related data sources, modeling data, building ETL/ELT pipelines, and creating interactive dashboards for leadership, operational teams, and public stakeholders.

## Requirements:

### 1. Data Integration:
- Ingest data from multiple sources (CSV, JSON, or mock ERP/CRM API).  
- Include datasets such as:  
  - Donor/member contributions  
  - Fundraising campaigns  
  - Public land acreage and habitat areas  
  - Elk population or habitat conservation metrics  
- Clean and transform data to create a **single source of truth**.  
- Implement ETL/ELT pipelines with error handling and logging.

### 2. Data Modeling:
- Create relational and/or dimensional models suitable for analytics (star schema or simplified schema).  
- Include tables for donors/members, donations/transactions, campaigns, conservation projects, and habitat areas.  
- Ensure data is queryable for dashboards and metrics.

### 3. Dashboard / Analytics Interface:
- Build a user-facing dashboard displaying key conservation and fundraising metrics:  
  - Total donations by campaign and donor type  
  - Membership growth over time  
  - Public land acquired or conserved  
  - Elk habitat coverage and population trends  
- Dashboard should include interactive filters (campaign, donor type, habitat region, date range).  
- Optional: highlight anomalies or outliers (e.g., unusually large donations or habitat changes).

### 4. Tech Stack:
- Backend: Python (Pandas, SQLAlchemy)  
- Database: SQL (SQLite or PostgreSQL)  
- Dashboard: Streamlit, Flask, or React  
- Optional: BI integration (Power BI or similar)  

### 5. Code Structure:
- `data/` – raw and processed datasets  
- `pipelines/` – ETL/ELT scripts  
- `models/` – SQL or ORM models  
- `dashboards/` – front-end dashboard code  
- `notebooks/` – optional for exploration and testing  
- `tests/` – scripts to validate pipeline/data quality  

### 6. Features & Extras:
- Include data quality checks (missing values, duplicates)  
- Dashboard should be intuitive for non-technical users  
- Document pipeline steps, schema, and conservation-focused metrics in markdown  
- Optional: simulate alerts for pipeline errors or habitat/metric anomalies  

### 7. Deliverables:
- Fully working ETL/ELT pipeline scripts  
- SQL data models ready for analytics  
- Interactive dashboard with at least 4 key metrics (fundraising + conservation)  
- README with project overview, usage instructions, and structure  

## Notes:
- Focus on **RMEF-relevant metrics**: conservation, elk habitat, public land, donor/member contributions.  
- Build a realistic, portfolio-ready analytics project that could **support a conservation organization’s decision-making**.  
- Generate mock datasets as needed; assume no access to real ERP/CRM systems.
