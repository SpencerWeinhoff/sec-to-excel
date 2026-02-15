"""Parse SEC filing HTML documents to extract all numerical tables."""

import re
from bs4 import BeautifulSoup, NavigableString


def _clean_text(text):
    """Clean cell text: normalize whitespace, strip special chars."""
    if not text:
        return ""
    text = re.sub(r"[\xa0\u200b\t\n\r]+", " ", text)
    text = text.strip()
    return text


def _is_numeric(text):
    """Check if text represents a number (including currency, percentages, negatives)."""
    cleaned = re.sub(r"[$,%\s\(\)]", "", text).replace(",", "").replace("—", "").replace("–", "")
    if not cleaned or cleaned == "-":
        return True
    try:
        float(cleaned)
        return True
    except ValueError:
        return False


def _has_enough_numbers(rows, threshold=0.25):
    """Check if a table has enough numeric content to be a financial table."""
    if not rows:
        return False

    total_cells = 0
    numeric_cells = 0

    for row in rows:
        for cell in row:
            text = _clean_text(cell)
            if text:
                total_cells += 1
                if _is_numeric(text):
                    numeric_cells += 1

    if total_cells == 0:
        return False

    return (numeric_cells / total_cells) >= threshold and numeric_cells >= 3


# Keywords used to infer table subject from content
_CONTENT_PATTERNS = [
    # (keywords to look for in row labels/headers, resulting title)
    (["revenue", "sales", "net sales", "total revenue"], "Revenue Breakdown"),
    (["cost of revenue", "cost of goods", "cost of sales", "cogs"], "Cost of Revenue Detail"),
    (["operating lease", "right-of-use", "rou asset"], "Lease Obligations"),
    (["finance lease"], "Finance Lease Schedule"),
    (["long-term debt", "senior note", "credit facility", "term loan", "revolving", "maturity", "interest rate"], "Debt Schedule"),
    (["short-term borrowing", "commercial paper"], "Short-Term Borrowings"),
    (["stock option", "option activity", "options outstanding", "exercise price", "weighted average exercise"], "Stock Option Activity"),
    (["restricted stock", "rsu", "psu", "performance share", "unvested"], "Restricted Stock / RSU Activity"),
    (["warrant"], "Warrant Activity"),
    (["share repurchase", "buyback", "treasury stock"], "Share Repurchase Program"),
    (["goodwill"], "Goodwill"),
    (["intangible asset", "amortization of intangible", "finite-lived"], "Intangible Assets"),
    (["property, plant", "property and equipment", "pp&e", "useful life"], "Property, Plant & Equipment"),
    (["depreciation", "amortization schedule"], "Depreciation & Amortization"),
    (["income tax", "tax provision", "deferred tax", "effective tax rate", "tax rate reconciliation"], "Income Tax Detail"),
    (["segment", "reportable segment", "operating segment"], "Segment Data"),
    (["geographic", "by country", "by region", "united states", "international"], "Geographic Breakdown"),
    (["store", "supercenter", "location", "club", "unit count", "number of"], "Operating Metrics"),
    (["accounts receivable", "receivable aging", "allowance for doubtful"], "Accounts Receivable Detail"),
    (["inventory", "raw material", "finished goods", "work in process"], "Inventory Detail"),
    (["accrued", "accrued liabilities", "accrued expenses"], "Accrued Liabilities Detail"),
    (["pension", "retirement", "benefit obligation", "postretirement"], "Pension & Benefits"),
    (["fair value", "level 1", "level 2", "level 3", "hierarchy"], "Fair Value Measurements"),
    (["acquisition", "business combination", "purchase price"], "Acquisition Detail"),
    (["commitment", "contractual obligation", "future minimum"], "Commitments & Obligations"),
    (["dividend", "per share", "dividends declared"], "Dividend Information"),
    (["earnings per share", "basic and diluted", "eps"], "Earnings Per Share Detail"),
    (["comprehensive income", "other comprehensive", "oci"], "Other Comprehensive Income"),
    (["selling, general", "sg&a", "operating expense"], "Operating Expense Detail"),
    (["research and development", "r&d"], "Research & Development"),
    (["equity compensation", "stock-based compensation", "share-based"], "Stock-Based Compensation"),
    (["capital expenditure", "capex"], "Capital Expenditures"),
    (["investment", "marketable securities", "available-for-sale", "held-to-maturity"], "Investment Securities"),
]


def _infer_title_from_content(headers, rows):
    """Analyze header and row label text to infer what a table is about."""
    # Gather all text from headers and first column of rows
    text_pool = []
    for header_row in headers:
        for cell in header_row:
            text_pool.append(_clean_text(cell).lower())
    for row in rows:
        if row:
            text_pool.append(_clean_text(row[0]).lower())

    combined = " ".join(text_pool)

    # Try each pattern
    best_match = None
    best_count = 0
    for keywords, title in _CONTENT_PATTERNS:
        count = sum(1 for kw in keywords if kw in combined)
        if count > best_count:
            best_count = count
            best_match = title

    if best_match and best_count >= 1:
        return best_match

    # Fallback: use the most common non-numeric text from the first column
    first_col_labels = []
    for row in rows[:10]:
        if row:
            label = _clean_text(row[0])
            if label and not _is_numeric(label) and len(label) > 2:
                first_col_labels.append(label)

    if first_col_labels:
        # Use the shortest meaningful label as a hint
        shortest = min(first_col_labels, key=len)
        if len(shortest) <= 60:
            return f"Data: {shortest}..."

    return None


def _detect_table_title(table_element, headers, rows):
    """Try to detect a title for the table from surrounding HTML, then from content."""
    # 1. Look at preceding siblings in HTML
    for sibling in _prev_siblings(table_element, limit=5):
        if isinstance(sibling, NavigableString):
            text = _clean_text(str(sibling))
            if text and len(text) > 3 and len(text) < 200:
                return text
            continue

        tag_name = sibling.name if sibling.name else ""
        if tag_name in ("table", "hr"):
            break

        text = _clean_text(sibling.get_text())
        if text and len(text) > 3 and len(text) < 200:
            if tag_name in ("b", "strong", "h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "span"):
                lower = text.lower()
                title_keywords = [
                    "statement", "balance", "income", "cash flow", "operations",
                    "financial", "schedule", "table", "equity", "debt",
                    "assets", "liabilities", "revenue", "expenses", "shares",
                    "stock", "compensation", "lease", "segment", "quarter",
                    "annual", "fiscal", "consolidated", "unaudited",
                    "warrant", "option", "restricted", "goodwill", "intangible",
                    "depreciation", "amortization", "tax", "provision",
                    "comprehensive", "accumulated", "capital", "investment",
                ]
                if any(kw in lower for kw in title_keywords) or tag_name in ("b", "strong", "h1", "h2", "h3", "h4"):
                    return text

    # 2. Check the first row for a spanning title cell
    first_row = table_element.find("tr")
    if first_row:
        cells = first_row.find_all(["td", "th"])
        if len(cells) == 1:
            text = _clean_text(cells[0].get_text())
            if text and len(text) > 3 and not _is_numeric(text):
                return text

    # 3. Infer from table content
    return _infer_title_from_content(headers, rows)


def _prev_siblings(element, limit=5):
    """Get previous siblings of an element, up to a limit."""
    count = 0
    sibling = element.previous_sibling
    while sibling and count < limit:
        yield sibling
        sibling = sibling.previous_sibling
        count += 1


def _parse_table(table_element):
    """Parse an HTML table element into headers and rows."""
    rows = []
    header_rows = []

    for tr in table_element.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        row_data = []
        is_header = all(cell.name == "th" for cell in cells) if cells else False

        for cell in cells:
            colspan = int(cell.get("colspan", 1))
            text = _clean_text(cell.get_text())
            row_data.append(text)
            for _ in range(colspan - 1):
                row_data.append("")

        if not any(row_data):
            continue

        if is_header:
            header_rows.append(row_data)
        else:
            rows.append(row_data)

    headers = []
    if header_rows:
        headers = header_rows
    elif rows:
        first_row = rows[0]
        non_numeric_count = sum(1 for c in first_row if c and not _is_numeric(c))
        if non_numeric_count > len(first_row) * 0.5:
            headers = [rows.pop(0)]

    return headers, rows


def _tables_are_similar(t1, t2):
    """Check if two table dicts are likely duplicates."""
    if t1.get("title") and t2.get("title") and t1["title"] == t2["title"]:
        if len(t1["rows"]) == len(t2["rows"]):
            return True

    rows1 = t1["rows"][:3]
    rows2 = t2["rows"][:3]
    if rows1 and rows2 and rows1 == rows2:
        return True

    return False


def extract_tables(html_content):
    """Extract all numerical tables from SEC filing HTML.

    Returns list of dicts: [{title, headers, rows}, ...]
    """
    soup = BeautifulSoup(html_content, "lxml")

    for element in soup.find_all(["script", "style"]):
        element.decompose()

    tables = []

    for table_el in soup.find_all("table"):
        headers, rows = _parse_table(table_el)

        if len(rows) < 2:
            continue

        if not _has_enough_numbers(rows):
            continue

        title = _detect_table_title(table_el, headers, rows)

        table_dict = {
            "title": title,
            "headers": headers,
            "rows": rows,
        }

        is_dup = False
        for existing in tables:
            if _tables_are_similar(existing, table_dict):
                is_dup = True
                break

        if not is_dup:
            tables.append(table_dict)

    return tables
