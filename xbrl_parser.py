"""Extract structured financial statements from SEC XBRL company facts JSON."""

from datetime import datetime

# Mapping of XBRL concept names to readable labels, grouped by statement.
# Each entry: (xbrl_concept, display_label)
# We try multiple concept names since companies may use different ones.

INCOME_STATEMENT_CONCEPTS = [
    ("Revenues", "Revenue"),
    ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenue"),
    ("SalesRevenueNet", "Revenue"),
    ("RevenueFromContractWithCustomerIncludingAssessedTax", "Revenue"),
    ("CostOfRevenue", "Cost of Revenue"),
    ("CostOfGoodsAndServicesSold", "Cost of Revenue"),
    ("CostOfGoodsSold", "Cost of Goods Sold"),
    ("GrossProfit", "Gross Profit"),
    ("ResearchAndDevelopmentExpense", "Research & Development"),
    ("SellingGeneralAndAdministrativeExpense", "Selling, General & Administrative"),
    ("SellingAndMarketingExpense", "Selling & Marketing"),
    ("GeneralAndAdministrativeExpense", "General & Administrative"),
    ("OperatingExpenses", "Total Operating Expenses"),
    ("OperatingIncomeLoss", "Operating Income (Loss)"),
    ("InterestExpense", "Interest Expense"),
    ("InterestIncome", "Interest Income"),
    ("InterestIncomeExpenseNet", "Net Interest Income (Expense)"),
    ("OtherNonoperatingIncomeExpense", "Other Non-Operating Income (Expense)"),
    ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "Income Before Tax"),
    ("IncomeTaxExpenseBenefit", "Income Tax Expense (Benefit)"),
    ("NetIncomeLoss", "Net Income (Loss)"),
    ("EarningsPerShareBasic", "EPS (Basic)"),
    ("EarningsPerShareDiluted", "EPS (Diluted)"),
    ("WeightedAverageNumberOfShareOutstandingBasicAndDiluted", "Weighted Avg Shares (Basic & Diluted)"),
    ("WeightedAverageNumberOfSharesOutstandingBasic", "Weighted Avg Shares (Basic)"),
    ("WeightedAverageNumberOfDilutedSharesOutstanding", "Weighted Avg Shares (Diluted)"),
]

BALANCE_SHEET_CONCEPTS = [
    ("CashAndCashEquivalentsAtCarryingValue", "Cash & Cash Equivalents"),
    ("ShortTermInvestments", "Short-Term Investments"),
    ("CashCashEquivalentsAndShortTermInvestments", "Cash, Equivalents & Short-Term Investments"),
    ("AccountsReceivableNetCurrent", "Accounts Receivable"),
    ("InventoryNet", "Inventory"),
    ("PrepaidExpenseAndOtherAssetsCurrent", "Prepaid Expenses & Other Current Assets"),
    ("AssetsCurrent", "Total Current Assets"),
    ("PropertyPlantAndEquipmentNet", "Property, Plant & Equipment (Net)"),
    ("Goodwill", "Goodwill"),
    ("IntangibleAssetsNetExcludingGoodwill", "Intangible Assets (Net)"),
    ("OtherAssetsNoncurrent", "Other Non-Current Assets"),
    ("Assets", "Total Assets"),
    ("AccountsPayableCurrent", "Accounts Payable"),
    ("AccruedLiabilitiesCurrent", "Accrued Liabilities"),
    ("LongTermDebtCurrent", "Current Portion of Long-Term Debt"),
    ("ShortTermBorrowings", "Short-Term Borrowings"),
    ("LiabilitiesCurrent", "Total Current Liabilities"),
    ("LongTermDebtNoncurrent", "Long-Term Debt"),
    ("LongTermDebt", "Long-Term Debt"),
    ("OperatingLeaseLiabilityNoncurrent", "Operating Lease Liabilities (Non-Current)"),
    ("OtherLiabilitiesNoncurrent", "Other Non-Current Liabilities"),
    ("Liabilities", "Total Liabilities"),
    ("CommonStockValue", "Common Stock"),
    ("AdditionalPaidInCapital", "Additional Paid-In Capital"),
    ("AdditionalPaidInCapitalCommonStock", "Additional Paid-In Capital"),
    ("RetainedEarningsAccumulatedDeficit", "Retained Earnings (Accumulated Deficit)"),
    ("AccumulatedOtherComprehensiveIncomeLossNetOfTax", "Accumulated Other Comprehensive Income (Loss)"),
    ("TreasuryStockValue", "Treasury Stock"),
    ("StockholdersEquity", "Total Stockholders' Equity"),
    ("LiabilitiesAndStockholdersEquity", "Total Liabilities & Stockholders' Equity"),
]

CASH_FLOW_CONCEPTS = [
    ("NetIncomeLoss", "Net Income"),
    ("DepreciationDepletionAndAmortization", "Depreciation & Amortization"),
    ("ShareBasedCompensation", "Stock-Based Compensation"),
    ("DeferredIncomeTaxExpenseBenefit", "Deferred Income Taxes"),
    ("IncreaseDecreaseInAccountsReceivable", "Change in Accounts Receivable"),
    ("IncreaseDecreaseInInventories", "Change in Inventories"),
    ("IncreaseDecreaseInAccountsPayable", "Change in Accounts Payable"),
    ("IncreaseDecreaseInAccruedLiabilities", "Change in Accrued Liabilities"),
    ("NetCashProvidedByUsedInOperatingActivities", "Net Cash from Operating Activities"),
    ("PaymentsToAcquirePropertyPlantAndEquipment", "Capital Expenditures"),
    ("PaymentsToAcquireBusinessesNetOfCashAcquired", "Acquisitions (Net of Cash)"),
    ("PaymentsToAcquireInvestments", "Purchases of Investments"),
    ("ProceedsFromSaleAndMaturityOfMarketableSecurities", "Proceeds from Sale of Investments"),
    ("ProceedsFromMaturitiesPrepaymentsAndCallsOfAvailableForSaleSecurities", "Proceeds from Maturities of Investments"),
    ("NetCashProvidedByUsedInInvestingActivities", "Net Cash from Investing Activities"),
    ("ProceedsFromIssuanceOfLongTermDebt", "Proceeds from Long-Term Debt"),
    ("RepaymentsOfLongTermDebt", "Repayments of Long-Term Debt"),
    ("PaymentsOfDividends", "Dividends Paid"),
    ("PaymentsOfDividendsCommonStock", "Dividends Paid (Common Stock)"),
    ("PaymentsForRepurchaseOfCommonStock", "Share Repurchases"),
    ("ProceedsFromIssuanceOfCommonStock", "Proceeds from Stock Issuance"),
    ("NetCashProvidedByUsedInFinancingActivities", "Net Cash from Financing Activities"),
    ("CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect", "Net Change in Cash"),
    ("CashAndCashEquivalentsPeriodIncreaseDecrease", "Net Change in Cash"),
]

STATEMENTS = {
    "Income Statement": INCOME_STATEMENT_CONCEPTS,
    "Balance Sheet": BALANCE_SHEET_CONCEPTS,
    "Cash Flow": CASH_FLOW_CONCEPTS,
}


def _parse_xbrl_date(date_str):
    """Parse a date string from XBRL data."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def _get_fact_values(facts_data, concept, taxonomy="us-gaap"):
    """Get all reported values for a given XBRL concept.

    Returns list of {value, end_date, start_date, form, filed, fy, fp, unit}.
    """
    tax_data = facts_data.get("facts", {}).get(taxonomy, {})
    concept_data = tax_data.get(concept, {})

    results = []
    for unit_key, unit_data in concept_data.get("units", {}).items():
        for entry in unit_data:
            results.append({
                "value": entry.get("val"),
                "end": entry.get("end", ""),
                "start": entry.get("start", ""),
                "form": entry.get("form", ""),
                "filed": entry.get("filed", ""),
                "fy": entry.get("fy"),
                "fp": entry.get("fp", ""),
                "unit": unit_key,
            })
    return results


def _match_filing_period(fact, filing_date, filing_type):
    """Check if a fact matches a specific filing period."""
    fact_form = fact.get("form", "")
    fact_end = fact.get("end", "")

    # Match by form type and approximate date
    if filing_type.startswith("10-K") and fact_form in ("10-K", "10-K/A"):
        # For 10-K, end date should be close to filing period end
        if fact_end:
            end_dt = _parse_xbrl_date(fact_end)
            filing_dt = _parse_xbrl_date(filing_date)
            if end_dt and filing_dt:
                # Filing end date should be within ~120 days before filing date
                diff = (filing_dt - end_dt).days
                if 0 <= diff <= 120:
                    return True
    elif filing_type.startswith("10-Q") and fact_form in ("10-Q", "10-Q/A"):
        if fact_end:
            end_dt = _parse_xbrl_date(fact_end)
            filing_dt = _parse_xbrl_date(filing_date)
            if end_dt and filing_dt:
                diff = (filing_dt - end_dt).days
                if 0 <= diff <= 90:
                    return True

    return False


def extract_financials(xbrl_facts, selected_filings):
    """Extract structured financial data from XBRL facts for selected filings.

    Args:
        xbrl_facts: Raw XBRL company facts JSON from SEC API.
        selected_filings: List of {type, date, accession, ...} dicts.

    Returns:
        Dict of:
        {
            "Income Statement": {
                "Revenue": {"2024-01-28": 123456, "2023-01-29": 111222},
                "Net Income": {...},
                ...
            },
            "Balance Sheet": {...},
            "Cash Flow": {...},
            "periods": ["2024-01-28", "2023-01-29", ...]
        }
    """
    result = {}
    all_periods = set()

    for statement_name, concepts in STATEMENTS.items():
        statement_data = {}
        seen_labels = set()

        for concept_name, label in concepts:
            # Skip duplicate labels (we try multiple concept names for the same item)
            if label in seen_labels:
                continue

            facts = _get_fact_values(xbrl_facts, concept_name)
            if not facts:
                continue

            period_values = {}
            for filing in selected_filings:
                for fact in facts:
                    if _match_filing_period(fact, filing["date"], filing["type"]):
                        period_key = fact.get("end", filing["date"])
                        if fact["value"] is not None:
                            period_values[period_key] = fact["value"]
                            all_periods.add(period_key)
                            break

            if period_values:
                statement_data[label] = period_values
                seen_labels.add(label)

        result[statement_name] = statement_data

    # Sort periods chronologically
    sorted_periods = sorted(all_periods)
    result["periods"] = sorted_periods

    return result
