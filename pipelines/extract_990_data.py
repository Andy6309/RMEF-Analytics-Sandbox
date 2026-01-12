"""
RMEF Analytics - Form 990 PDF Data Extraction
Extracts financial data from IRS Form 990 PDFs for multi-year analysis
"""

import pdfplumber
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Form990Extractor')


@dataclass
class Form990Data:
    """Unified schema for Form 990 data across years"""
    # Identification
    fiscal_year: int
    tax_year: int
    organization_name: str
    ein: str
    
    # Revenue (Part I / Part VIII)
    contributions_and_grants: float
    program_service_revenue: float
    investment_income: float
    other_revenue: float
    total_revenue: float
    
    # Expenses (Part I / Part IX)
    grants_and_similar_paid: float
    salaries_and_wages: float
    other_employee_benefits: float
    payroll_taxes: float
    professional_fees: float
    occupancy: float
    travel: float
    conferences_and_meetings: float
    depreciation: float
    other_expenses: float
    total_expenses: float
    
    # Balance Sheet (Part X)
    total_assets: float
    total_liabilities: float
    net_assets: float
    
    # Functional Expenses Allocation
    program_services_expenses: float
    management_and_general_expenses: float
    fundraising_expenses: float
    
    # Key Metrics
    revenue_less_expenses: float
    employees_count: int
    volunteers_count: int
    
    # Program Service Details
    program_services: Dict[str, Dict[str, float]] = field(default_factory=dict)


class Form990Extractor:
    """Extract structured data from Form 990 PDFs"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.text_by_page: Dict[int, str] = {}
        self.tables_by_page: Dict[int, List] = {}
        self.summary_values: List[float] = []  # Ordered values from Part I Summary
        
    def extract_all_text(self) -> str:
        """Extract all text from PDF"""
        all_text = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                self.text_by_page[i] = text
                all_text.append(text)
                
                # Also extract tables
                tables = page.extract_tables()
                if tables:
                    self.tables_by_page[i] = tables
                    
        return "\n".join(all_text)
    
    def _clean_number(self, value: str) -> float:
        """Clean and convert string to float"""
        if not value:
            return 0.0
        cleaned = str(value).strip()
        # Handle trailing period (common in 990 forms like "52,185,551.")
        cleaned = re.sub(r'\.$', '', cleaned)
        cleaned = re.sub(r'[,$\s]', '', cleaned)
        # Handle parentheses as negative
        if '(' in cleaned and ')' in cleaned:
            cleaned = '-' + cleaned.replace('(', '').replace(')', '')
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    
    def _extract_summary_table_values(self) -> List[float]:
        """Extract ordered numeric values from Part I Summary table"""
        values = []
        
        # Try both page 0 and page 1 - different PDFs have different structures
        for page_idx in [0, 1]:
            if page_idx in self.tables_by_page:
                for table in self.tables_by_page[page_idx]:
                    for row in table:
                        if row:
                            for cell in row:
                                if cell:
                                    cell_str = str(cell).strip()
                                    # Match values like "52,185,551." or "0."
                                    if re.match(r'^[\d,]+\.$', cell_str):
                                        val = self._clean_number(cell_str)
                                        values.append(val)
        
        return values
    
    def extract_fiscal_year(self, text: str) -> tuple:
        """Extract fiscal year from Form 990"""
        tax_year_match = re.search(r'20(\d{2})', self.pdf_path.name)
        tax_year = int('20' + tax_year_match.group(1)) if tax_year_match else 0
        
        form_year_match = re.search(r'Form\s+990\s*\((\d{4})\)', text)
        if form_year_match:
            tax_year = int(form_year_match.group(1))
        
        return tax_year, tax_year
    
    def extract_organization_info(self, text: str) -> Dict[str, str]:
        """Extract organization name and EIN"""
        info = {
            'name': 'Rocky Mountain Elk Foundation, Inc.',
            'ein': '81-0421425'
        }
        
        ein_match = re.search(r'(\d{2}-\d{7})', text)
        if ein_match:
            info['ein'] = ein_match.group(1)
        
        return info
    
    def extract_financial_data_from_tables(self) -> Dict[str, float]:
        """Extract financial data from the Part I Summary table structure"""
        # Based on the table structure observed:
        # Table 2 on Page 2 contains the summary with values in order:
        # Row 6: 52,185,551. (Contributions - Prior Year)
        # Row 7: 7,406,675. (Program Service Revenue - Prior Year)
        # Row 8: 696,168. (Investment Income - Prior Year)
        # Row 9: 1,622,582. (Other Revenue - Prior Year)
        # Row 10: 61,910,976. (Total Revenue - Prior Year)
        # Row 11: 4,250,918. (Grants - Prior Year)
        # Row 12: 0. (Benefits to members)
        # Row 13: 12,708,353. (Salaries)
        # Row 14: 6,050. (?)
        # Row 16: 29,140,315. (Other expenses)
        # Row 17: 46,105,636. (Total expenses)
        # Row 18: 15,805,340. (Revenue less expenses)
        
        values = self._extract_summary_table_values()
        
        data = {
            'contributions_and_grants': 0.0,
            'program_service_revenue': 0.0,
            'investment_income': 0.0,
            'other_revenue': 0.0,
            'total_revenue': 0.0,
            'grants_and_similar_paid': 0.0,
            'salaries_and_wages': 0.0,
            'total_expenses': 0.0,
            'revenue_less_expenses': 0.0,
            'total_assets': 0.0,
            'total_liabilities': 0.0,
            'net_assets': 0.0,
        }
        
        # Map values by position (these are Prior Year values from the table)
        # The Current Year values follow in subsequent columns
        if len(values) >= 12:
            # Revenue section (lines 8-12)
            data['contributions_and_grants'] = values[0]  # 52,185,551
            data['program_service_revenue'] = values[1]   # 7,406,675
            data['investment_income'] = values[2]         # 696,168
            data['other_revenue'] = values[3]             # 1,622,582
            data['total_revenue'] = values[4]             # 61,910,976
            
            # Expense section (lines 13-18)
            data['grants_and_similar_paid'] = values[5]   # 4,250,918
            # values[6] is benefits to members (usually 0)
            data['salaries_and_wages'] = values[7] if len(values) > 7 else 0  # 12,708,353
            
            # Find total expenses and revenue less expenses
            # Look for values that make sense (total expenses > salaries)
            for i, val in enumerate(values[8:], start=8):
                if val > data['salaries_and_wages'] and val > 30000000:
                    if data['total_expenses'] == 0:
                        data['total_expenses'] = val
                    elif data['revenue_less_expenses'] == 0 and val < data['total_expenses']:
                        data['revenue_less_expenses'] = val
        
        return data
    
    def extract_employee_data(self, text: str) -> Dict[str, int]:
        """Extract employee and volunteer counts"""
        data = {
            'employees_count': 0,
            'volunteers_count': 0
        }
        
        emp_match = re.search(r'Total\s+number\s+of\s+individuals\s+employed.*?(\d+)', text, re.IGNORECASE | re.DOTALL)
        if emp_match:
            data['employees_count'] = int(emp_match.group(1))
        
        vol_match = re.search(r'Total\s+number\s+of\s+volunteers.*?(\d+)', text, re.IGNORECASE | re.DOTALL)
        if vol_match:
            data['volunteers_count'] = int(vol_match.group(1))
        
        return data
    
    def extract_program_services(self, text: str) -> Dict[str, Dict[str, float]]:
        """Extract program service accomplishments from Part III"""
        programs = {}
        
        # Pattern: 4a (Code: ) (Expenses $ XX,XXX,XXX. including grants of $ XX,XXX. ) (Revenue $ XX,XXX. )
        program_patterns = [
            (r'4a.*?Expens\s*es\s*\$\s*([\d,]+).*?grants\s+of\s*\$\s*([\d,]+).*?Revenue\s*\$\s*([\d,]+)', 'Land Protection & Access'),
            (r'4b.*?Expens\s*es\s*\$\s*([\d,]+).*?grants\s+of\s*\$\s*([\d,]+).*?Revenue\s*\$\s*([\d,]+)', 'Hunting Heritage'),
            (r'4c.*?Expens\s*es\s*\$\s*([\d,]+).*?grants\s+of\s*\$\s*([\d,]+).*?Revenue\s*\$\s*([\d,]+)', 'Habitat Stewardship'),
        ]
        
        for pattern, name in program_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                programs[name] = {
                    'expenses': self._clean_number(match.group(1)),
                    'grants': self._clean_number(match.group(2)),
                    'revenue': self._clean_number(match.group(3))
                }
        
        return programs
    
    def extract(self) -> Form990Data:
        """Main extraction method"""
        logger.info(f"Extracting data from {self.pdf_path.name}")
        
        text = self.extract_all_text()
        
        # Extract all components
        tax_year, fiscal_year = self.extract_fiscal_year(text)
        org_info = self.extract_organization_info(text)
        
        # Use table-based extraction for financial data
        financial = self.extract_financial_data_from_tables()
        employees = self.extract_employee_data(text)
        programs = self.extract_program_services(text)
        
        # Calculate program expenses total
        program_services_expenses = sum(p.get('expenses', 0) for p in programs.values())
        
        return Form990Data(
            fiscal_year=fiscal_year,
            tax_year=tax_year,
            organization_name=org_info['name'],
            ein=org_info['ein'],
            contributions_and_grants=financial['contributions_and_grants'],
            program_service_revenue=financial['program_service_revenue'],
            investment_income=financial['investment_income'],
            other_revenue=financial['other_revenue'],
            total_revenue=financial['total_revenue'],
            grants_and_similar_paid=financial['grants_and_similar_paid'],
            salaries_and_wages=financial['salaries_and_wages'],
            other_employee_benefits=0.0,
            payroll_taxes=0.0,
            professional_fees=0.0,
            occupancy=0.0,
            travel=0.0,
            conferences_and_meetings=0.0,
            depreciation=0.0,
            other_expenses=0.0,
            total_expenses=financial['total_expenses'],
            total_assets=financial['total_assets'],
            total_liabilities=financial['total_liabilities'],
            net_assets=financial['net_assets'],
            program_services_expenses=program_services_expenses,
            management_and_general_expenses=0.0,
            fundraising_expenses=0.0,
            revenue_less_expenses=financial['revenue_less_expenses'],
            employees_count=employees['employees_count'],
            volunteers_count=employees['volunteers_count'],
            program_services=programs
        )


def extract_all_990s(assets_dir: str = "assets") -> List[Dict[str, Any]]:
    """Extract data from all Form 990 PDFs in the assets directory"""
    assets_path = Path(assets_dir)
    pdf_files = list(assets_path.glob("*990*.pdf"))
    
    results = []
    for pdf_file in sorted(pdf_files):
        try:
            extractor = Form990Extractor(pdf_file)
            data = extractor.extract()
            results.append(asdict(data))
            logger.info(f"Successfully extracted: {pdf_file.name} (Tax Year: {data.tax_year})")
        except Exception as e:
            logger.error(f"Failed to extract {pdf_file.name}: {e}")
    
    return results


def save_extracted_data(data: List[Dict], output_path: str = "data/raw/form_990_data.json"):
    """Save extracted data to JSON file"""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output, 'w') as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"Saved extracted data to {output_path}")


if __name__ == "__main__":
    # Extract all 990 data
    data = extract_all_990s()
    
    # Save to JSON
    save_extracted_data(data)
    
    # Print summary
    print("\n" + "="*60)
    print("Form 990 Extraction Summary")
    print("="*60)
    for record in data:
        print(f"\nTax Year: {record['tax_year']}")
        print(f"  Total Revenue: ${record['total_revenue']:,.0f}")
        print(f"  Total Expenses: ${record['total_expenses']:,.0f}")
        print(f"  Net Assets: ${record['net_assets']:,.0f}")
