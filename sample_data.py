"""Dummy sample datasets for quick testing of the CA Copilot application."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# ═══════════════════════════════════════════════════════════════
# CLIENT DATABASE
# ═══════════════════════════════════════════════════════════════

CLIENTS = [
    {
        "client_id": "CL001",
        "name": "Rajesh Kumar & Associates",
        "type": "Partnership Firm",
        "pan": "AABPR1234C",
        "industry": "IT Services",
        "annual_turnover": 8500000,
        "tax_regime": "Regular",
        "gst_registered": True,
        "compliance_status": "Up to Date",
    },
    {
        "client_id": "CL002",
        "name": "Shree Electronics Pvt Ltd",
        "type": "Private Limited",
        "pan": "AABCS5678D",
        "industry": "Electronics Manufacturing",
        "annual_turnover": 42000000,
        "tax_regime": "Regular",
        "gst_registered": True,
        "compliance_status": "Up to Date",
    },
    {
        "client_id": "CL003",
        "name": "Priya Sharma",
        "type": "Individual",
        "pan": "BGRPS9012E",
        "industry": "Consulting",
        "annual_turnover": 2200000,
        "tax_regime": "New Regime",
        "gst_registered": False,
        "compliance_status": "Pending Review",
    },
    {
        "client_id": "CL004",
        "name": "Green Valley Foods",
        "type": "LLP",
        "pan": "AABFG3456F",
        "industry": "Food & Beverage",
        "annual_turnover": 15000000,
        "tax_regime": "Regular",
        "gst_registered": True,
        "compliance_status": "Up to Date",
    },
    {
        "client_id": "CL005",
        "name": "Vikram Real Estate Corp",
        "type": "Private Limited",
        "pan": "AABCV7890G",
        "industry": "Real Estate",
        "annual_turnover": 68000000,
        "tax_regime": "Regular",
        "gst_registered": True,
        "compliance_status": "Defaulter Notice",
    },
]


# ═══════════════════════════════════════════════════════════════
# FINANCIAL DATA (Monthly for FY 2025-26)
# ═══════════════════════════════════════════════════════════════

MONTHS = [
    "Apr 2025", "May 2025", "Jun 2025", "Jul 2025", "Aug 2025", "Sep 2025",
    "Oct 2025", "Nov 2025", "Dec 2025", "Jan 2026", "Feb 2026", "Mar 2026",
]

EXPENSE_CATEGORIES = [
    "Salaries & Wages", "Rent & Utilities", "Raw Materials", "Marketing",
    "Professional Fees", "Travel & Conveyance", "Depreciation", "Insurance",
    "Miscellaneous",
]

TAX_TYPES = ["Income Tax", "GST", "TDS", "Professional Tax", "Stamp Duty"]


def get_financial_summary(client_id: str = "CL001") -> dict:
    """Generate monthly financial data for a given client."""
    seed = hash(client_id) % 10000
    rng = np.random.default_rng(seed)

    base_revenue = {
        "CL001": 708333, "CL002": 3500000, "CL003": 183333,
        "CL004": 1250000, "CL005": 5666667,
    }.get(client_id, 500000)

    revenue = [int(base_revenue * rng.uniform(0.8, 1.3)) for _ in range(12)]
    expenses = {}
    for cat in EXPENSE_CATEGORIES:
        cat_base = base_revenue * rng.uniform(0.03, 0.18)
        expenses[cat] = [int(cat_base * rng.uniform(0.7, 1.4)) for _ in range(12)]

    total_expenses = [sum(expenses[cat][i] for cat in expenses) for i in range(12)]
    profit_before_tax = [revenue[i] - total_expenses[i] for i in range(12)]

    tax_rates = {"Income Tax": 0.25, "GST": 0.18, "TDS": 0.10, "Professional Tax": 0.01, "Stamp Duty": 0.005}
    taxes = {}
    for tax in TAX_TYPES:
        taxes[tax] = [int(profit_before_tax[i] * tax_rates[tax] * rng.uniform(0.8, 1.2)) for i in range(12)]

    return {
        "months": MONTHS,
        "revenue": revenue,
        "expenses": expenses,
        "total_expenses": total_expenses,
        "profit_before_tax": profit_before_tax,
        "taxes": taxes,
        "net_profit": [profit_before_tax[i] - sum(taxes[t][i] for t in taxes) for i in range(12)],
    }


# ═══════════════════════════════════════════════════════════════
# SAMPLE INVOICES
# ═══════════════════════════════════════════════════════════════

SAMPLE_INVOICES = [
    {"invoice_no": "INV-2025-001", "date": "2025-04-15", "vendor": "Tata Consultancy Services", "amount": 250000.00, "tax": 45000.00, "category": "IT Services", "status": "Paid"},
    {"invoice_no": "INV-2025-002", "date": "2025-04-22", "vendor": "Wipro Limited", "amount": 180000.00, "tax": 32400.00, "category": "Software Licenses", "status": "Paid"},
    {"invoice_no": "INV-2025-003", "date": "2025-05-01", "vendor": "Infosys BPM", "amount": 320000.00, "tax": 57600.00, "category": "BPO Services", "status": "Pending"},
    {"invoice_no": "INV-2025-004", "date": "2025-05-10", "vendor": "HDFC Bank", "amount": 45000.00, "tax": 8100.00, "category": "Bank Charges", "status": "Paid"},
    {"invoice_no": "INV-2025-005", "date": "2025-05-18", "vendor": "Reliance Jio", "amount": 12500.00, "tax": 2250.00, "category": "Telecom", "status": "Paid"},
    {"invoice_no": "INV-2025-006", "date": "2025-06-02", "vendor": "Godrej Properties", "amount": 480000.00, "tax": 86400.00, "category": "Office Rent", "status": "Paid"},
    {"invoice_no": "INV-2025-007", "date": "2025-06-15", "vendor": "Bajaj Allianz", "amount": 78000.00, "tax": 14040.00, "category": "Insurance", "status": "Pending"},
    {"invoice_no": "INV-2025-008", "date": "2025-07-01", "vendor": "TCS", "amount": 295000.00, "tax": 53100.00, "category": "IT Services", "status": "Paid"},
    {"invoice_no": "INV-2025-009", "date": "2025-07-20", "vendor": "Amazon Web Services", "amount": 67500.00, "tax": 12150.00, "category": "Cloud Services", "status": "Paid"},
    {"invoice_no": "INV-2025-010", "date": "2025-08-05", "vendor": "Mphasis Ltd", "amount": 210000.00, "tax": 37800.00, "category": "IT Services", "status": "Overdue"},
]


# ═══════════════════════════════════════════════════════════════
# TAX RULES KNOWLEDGE BASE (for RAG)
# ═══════════════════════════════════════════════════════════════

TAX_RULES_KB = [
    {
        "doc_id": "TR001",
        "title": "Income Tax Act - Section 80C Deductions",
        "source": "Income Tax Act, 1961",
        "content": (
            "Section 80C of the Income Tax Act allows deductions up to ₹1,50,000 per annum "
            "from gross total income. Eligible investments include: (a) Life Insurance Premium, "
            "(b) Public Provident Fund (PPF), (c) Employee Provident Fund (EPF), "
            "(d) National Savings Certificate (NSC), (e) Equity Linked Savings Scheme (ELSS), "
            "(f) Home Loan Principal Repayment, (g) Tuition Fees for up to 2 children. "
            "The deduction is available to individuals and Hindu Undivided Families (HUF). "
            "For senior citizens under Section 80C, an additional ₹50,000 deduction is available "
            "under Section 80TTB for interest income."
        ),
        "tags": ["deductions", "80C", "investments", "savings"],
    },
    {
        "doc_id": "TR002",
        "title": "GST Rate Structure - HSN Codes",
        "source": "GST Council Notification 2024",
        "content": (
            "GST rates in India are classified into slabs: 0%, 5%, 12%, 18%, and 28%. "
            "Essential items like food grains, fresh vegetables, and milk are exempt (0%). "
            "Packaged food items, footwear below ₹1000, and transport services fall under 5%. "
            "Business services, IT services, and most manufactured goods attract 18% GST. "
            "Luxury items like cars, tobacco, and aerated drinks attract 28% GST plus Cess. "
            "HSN codes must be mandatorily declared on invoices for goods with turnover > ₹5 crore. "
            "Reverse charge mechanism applies for specified categories under Section 9(3) of CGST Act."
        ),
        "tags": ["GST", "rates", "HSN", "tax slabs"],
    },
    {
        "doc_id": "TR003",
        "title": "TDS Rates for FY 2025-26",
        "source": "CBDT Circular No. 12/2025",
        "content": (
            "TDS (Tax Deducted at Source) rates for FY 2025-26: "
            "Section 194A - Interest other than interest on securities: 10% (individuals), "
            "for senior citizens no TDS if form 15H/15G is submitted. "
            "Section 194C - Payment to contractors: 1% (individuals/HUF), 2% (others). "
            "Section 194H - Commission or brokerage: 5%. "
            "Section 194I(a) - Rent on plant and machinery: 2%. "
            "Section 194I(b) - Rent on land/building: 10%. "
            "Section 194J - Technical services/royalty: 2% (technical), 10% (others). "
            "Section 194Q - Purchase of goods > ₹50 lakh: 0.1%. "
            "Non-deduction attracts disallowance of 30% of expenditure under Section 40(a)(ia)."
        ),
        "tags": ["TDS", "deduction rates", "194A", "194C", "194J"],
    },
    {
        "doc_id": "TR004",
        "title": "New Tax Regime vs Old Tax Regime FY 2025-26",
        "source": "Finance Act 2025",
        "content": (
            "From FY 2025-26, the New Tax Regime is the default regime. Taxpayers can opt out "
            "and choose the Old Regime if beneficial. New Regime slabs (up to ₹12L income = NIL): "
            "0-3L: Nil, 3-7L: 5%, 7-10L: 10%, 10-12L: 15%, 12-15L: 20%, above 15L: 30%. "
            "Standard deduction of ₹75,000 available in New Regime (revised from ₹50,000). "
            "Old Regime slabs: 0-2.5L: Nil, 2.5-5L: 5%, 5-10L: 20%, above 10L: 30%. "
            "Rebate under Section 87A: New Regime ₹60,000 (income up to ₹12L), Old Regime ₹12,500. "
            "Surcharge: 10% (50L-1Cr), 15% (1Cr-2Cr), 25% (2Cr-5Cr, New Regime), 37% (>5Cr, Old). "
            "Health & Education Cess: 4% on income tax + surcharge."
        ),
        "tags": ["new regime", "old regime", "slabs", "rebate", "surcharge"],
    },
    {
        "doc_id": "TR005",
        "title": "GST Filing Deadlines & Penalties",
        "source": "CGST Act Section 47",
        "content": (
            "GST return filing deadlines: GSTR-1 (outward supplies) - 11th of following month. "
            "GSTR-3B (summary return) - 20th of following month. "
            "GSTR-9 (Annual return) - 31st December of following FY. "
            "GSTR-9C (Reconciliation statement) - if turnover > ₹5 crore. "
            "Late filing fee: ₹50/day under GST (₹25 CGST + ₹25 SGST), "
            "maximum 10% of tax liability or ₹10,000 whichever is higher. "
            "ITR filing deadline: 31st July (non-audit), 30th September (audit cases). "
            "Late filing fee under Section 234F: ₹5,000 (income > ₹5L), ₹1,000 (income ≤ ₹5L). "
            "Interest on delayed payment: 18% per annum under GST, 1% per month under IT Act."
        ),
        "tags": ["filing", "deadlines", "penalties", "GSTR", "ITR"],
    },
    {
        "doc_id": "TR006",
        "title": "Transfer Pricing Provisions - Section 92",
        "source": "Income Tax Act, 1961 - Chapter X",
        "content": (
            "Transfer pricing provisions apply to international transactions and specified domestic "
            "transactions exceeding ₹1 crore. Arm's length price (ALP) must be determined using "
            "four methods: (1) Comparable Uncontrolled Price (CUP), (2) Resale Price Method (RPM), "
            "(3) Cost Plus Method (CPM), (4) Transactional Net Margin Method (TNMM). "
            "BEPS Action 13 requires Country-by-Country Reporting (CbCR) for MNEs with consolidated "
            "revenue > €750 million. Transfer pricing documentation must be maintained under "
            "Section 92D and filed in Form 3CEB. Penalties for non-compliance: 2% of value of "
            "transaction under Section 271BA. Safe harbor rules apply for specified categories."
        ),
        "tags": ["transfer pricing", "section 92", "ALP", "BEPS", "documentation"],
    },
    {
        "doc_id": "TR007",
        "title": "GST Input Tax Credit (ITC) Rules",
        "source": "CGST Act Section 16 & Rule 36",
        "content": (
            "Input Tax Credit (ITC) can be claimed only if: (a) Possession of tax invoice or "
            "debit note, (b) Goods or services received, (c) Tax has been actually paid to the "
            "government, (d) Return filed under Section 39. ITC time limit: Within 30th November "
            "of the year following the financial year. Rule 36(4): ITC restricted to 105% of "
            "eligible credit appearing in GSTR-2B (5% provisional over ITC in auto-populated returns). "
            "Blocked credits (Section 17(5)): Food/beverages, outdoor catering, beauty treatment, "
            "health services, cosmetic/plastic surgery, membership of club/health/fitness centre, "
            "travel benefits to employees on vacation, works contract for immovable property "
            "(except for further supply), motor vehicles for personal use. "
            "ITC reversal required for exempt supplies under Rule 42/43."
        ),
        "tags": ["ITC", "input tax credit", "blocked credits", "rules"],
    },
    {
        "doc_id": "TR008",
        "title": "Capital Gains Taxation - Sections 111A, 112A",
        "source": "Income Tax Act, 1961",
        "content": (
            "Short-term capital gains (STCG) on equity/equity-oriented mutual funds listed on recognized "
            "stock exchange (holding ≤ 12 months) taxable under Section 111A at 20% + 4% cess = 20.8%. "
            "Long-term capital gains (LTCG) exceeding ₹1.25 lakh on equity/equity-oriented mutual funds "
            "(holding > 12 months) taxable under Section 112A at 12.5% + 4% cess. "
            "For unlisted securities and immovable property: STCG (holding ≤ 24/36 months) at slab rates. "
            "LTCG (holding > 24/36 months) at 20% with indexation benefit. "
            "Exemption under Section 54: Invest in one residential house in India within 1 year before "
            "or 2 years after transfer, or construct within 3 years. Maximum ₹10 crore exemption. "
            "Section 54EC: Invest in specified bonds (NHAI/REC/IRFC) within 6 months, max ₹50 lakh."
        ),
        "tags": ["capital gains", "STCG", "LTCG", "section 112A", "exemptions"],
    },
]


# ═══════════════════════════════════════════════════════════════
# GST RETURN DATA
# ═══════════════════════════════════════════════════════════════

def get_gst_returns(client_id: str = "CL001") -> list:
    """Generate monthly GST return filing data."""
    seed = hash(client_id) % 10000
    rng = np.random.default_rng(seed)
    
    returns = []
    for i, month in enumerate(MONTHS):
        year = 2025 + (4 + i - 1) // 12
        mon = ((4 + i - 1) % 12) + 1
        month_date = datetime(year, mon, 1)
        turnover = int(rng.uniform(500000, 3000000))
        output_gst = int(turnover * 0.18)
        input_gst = int(output_gst * rng.uniform(0.4, 0.8))
        net_gst = output_gst - input_gst
        
        filed = rng.random() > 0.1
        filing_date = month_date + timedelta(days=int(rng.uniform(5, 25))) if filed else None
        
        returns.append({
            "month": month,
            "taxable_turnover": turnover,
            "output_gst": output_gst,
            "input_gst": input_gst,
            "net_gst_payable": max(net_gst, 0),
            "itc_claimed": input_gst,
            "filing_status": "Filed" if filed else "Pending",
            "filing_date": filing_date.strftime("%Y-%m-%d") if filing_date else None,
        })
    
    return returns


# ═══════════════════════════════════════════════════════════════
# DOCUMENT TEMPLATES (for OCR simulation)
# ═══════════════════════════════════════════════════════════════

EXTRACTED_DOCUMENTS = [
    {
        "filename": "invoice_tcs_apr2025.pdf",
        "doc_type": "Invoice",
        "extracted_data": {
            "invoice_number": "TCS/2025-26/0412",
            "date": "2025-04-15",
            "vendor_name": "Tata Consultancy Services Limited",
            "vendor_gstin": "27AABCT1234F1Z5",
            "client_name": "Rajesh Kumar & Associates",
            "client_gstin": "27AABPR1234C1Z8",
            "line_items": [
                {"description": "IT Consulting Services - April 2025", "hsn": "998314", "quantity": 1, "rate": 200000, "amount": 200000, "gst_rate": 18, "gst_amount": 36000},
                {"description": "Software Development Support", "hsn": "998316", "quantity": 1, "rate": 50000, "amount": 50000, "gst_rate": 18, "gst_amount": 9000},
            ],
            "subtotal": 250000,
            "total_gst": 45000,
            "total_amount": 295000,
            "payment_terms": "Net 30 days",
            "bank_details": "HDFC Bank, A/C: 50100012345678, IFSC: HDFC0001234",
        },
        "confidence": 0.96,
    },
    {
        "filename": "salary_register_may2025.xlsx",
        "doc_type": "Payroll Register",
        "extracted_data": {
            "period": "May 2025",
            "total_employees": 45,
            "gross_salary": 1800000,
            "epf_contribution": 216000,
            "esi_contribution": 9000,
            "tds_deducted": 180000,
            "net_salary_paid": 1395000,
            "professional_tax": 4500,
        },
        "confidence": 0.92,
    },
    {
        "filename": "bank_statement_q1_2025.pdf",
        "doc_type": "Bank Statement",
        "extracted_data": {
            "bank": "HDFC Bank Limited",
            "account_number": "50100012345678",
            "statement_period": "April 2025 - June 2025",
            "opening_balance": 2450000,
            "closing_balance": 3120000,
            "total_credits": 8500000,
            "total_debits": 7830000,
            "key_transactions": [
                {"date": "2025-04-05", "description": "TCS Payment - Consulting", "amount": 295000, "type": "Credit"},
                {"date": "2025-04-10", "description": "Salary Transfer", "amount": 1395000, "type": "Debit"},
                {"date": "2025-04-15", "description": "GST Payment", "amount": 185000, "type": "Debit"},
                {"date": "2025-05-01", "description": "Client Payment - Wipro", "amount": 212400, "type": "Credit"},
                {"date": "2025-05-18", "description": "Office Rent", "amount": 480000, "type": "Debit"},
            ],
        },
        "confidence": 0.89,
    },
    {
        "filename": "gst_return_jun2025.pdf",
        "doc_type": "GST Return (GSTR-3B)",
        "extracted_data": {
            "return_period": "June 2025",
            "gstin": "27AABPR1234C1Z8",
            "total_outward_supply": 2800000,
            "inter_state_supply": 1200000,
            "intra_state_supply": 1600000,
            "output_cgst": 144000,
            "output_sgst": 144000,
            "output_igst": 216000,
            "input_cgst": 85000,
            "input_sgst": 85000,
            "input_igst": 130000,
            "net_cgst_payable": 59000,
            "net_sgst_payable": 59000,
            "net_igst_payable": 86000,
            "total_tax_payable": 204000,
            "filing_date": "2025-07-18",
        },
        "confidence": 0.94,
    },
]
