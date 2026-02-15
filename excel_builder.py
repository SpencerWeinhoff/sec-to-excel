"""Build organized Excel workbooks from extracted SEC filing data."""

import os
import re
import tempfile
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter


# Styles
HEADER_FONT = Font(bold=True, size=11)
TITLE_FONT = Font(bold=True, size=13)
SUBTITLE_FONT = Font(bold=True, size=11, color="555555")
HEADER_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
TITLE_FILL = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
TITLE_FONT_WHITE = Font(bold=True, size=13, color="FFFFFF")
THIN_BORDER = Border(
    bottom=Side(style="thin", color="CCCCCC"),
)

# Accounting format: negative in parens, thousands separator, no decimals for whole numbers
ACCT_FMT = '#,##0_);(#,##0)'
ACCT_FMT_DEC = '#,##0.00_);(#,##0.00)'
PCT_FMT = '0.00%'


def _safe_sheet_name(name, max_len=31):
    """Make a string safe for use as an Excel sheet name."""
    name = re.sub(r'[\\/*?\[\]:]', '', name)
    if len(name) > max_len:
        name = name[:max_len]
    return name.strip()


def _unique_sheet_name(name, used_names):
    """Ensure a sheet name is unique by appending a counter if needed."""
    base = _safe_sheet_name(name)
    if not base:
        base = "Table"
    result = base
    counter = 2
    while result in used_names:
        suffix = f" ({counter})"
        result = _safe_sheet_name(base[:31 - len(suffix)] + suffix)
        counter += 1
    used_names.add(result)
    return result


def _is_year_like(val):
    """Check if a value looks like a year (1900-2099) and should NOT get comma formatting."""
    if isinstance(val, int) and 1900 <= val <= 2099:
        return True
    if isinstance(val, float) and val == int(val) and 1900 <= int(val) <= 2099:
        return True
    return False


def _try_parse_number(text):
    """Try to convert text to a number for Excel."""
    if not text or text in ("—", "–", "-", ""):
        return None, False

    cleaned = text.replace("$", "").replace(",", "").replace(" ", "").strip()

    # Handle parentheses as negatives: (123) -> -123
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = "-" + cleaned[1:-1]

    is_pct = cleaned.endswith("%")
    if is_pct:
        cleaned = cleaned[:-1]

    try:
        val = float(cleaned)
        if is_pct:
            val = val / 100.0
            return val, True  # True = percentage
        if val == int(val):
            return int(val), False
        return val, False
    except (ValueError, OverflowError):
        return None, False


def _format_number_cell(cell, val, is_pct=False):
    """Apply accounting formatting to a number cell."""
    cell.value = val
    cell.alignment = Alignment(horizontal="right")

    if is_pct:
        cell.number_format = PCT_FMT
    elif _is_year_like(val):
        cell.number_format = '0'  # Plain number, no commas
    elif isinstance(val, float):
        cell.number_format = ACCT_FMT_DEC
    elif isinstance(val, int):
        cell.number_format = ACCT_FMT


def _auto_width(ws, min_width=12, max_width=45):
    """Auto-fit column widths based on content."""
    for col_cells in ws.columns:
        max_length = min_width
        col_letter = get_column_letter(col_cells[0].column)
        for cell in col_cells:
            if cell.value:
                length = len(str(cell.value)) + 3
                max_length = max(max_length, min(length, max_width))
        ws.column_dimensions[col_letter].width = max_length


def _write_title_bar(ws, row, title, num_cols):
    """Write a blue title bar spanning multiple columns."""
    ws.cell(row=row, column=1, value=title).font = TITLE_FONT_WHITE
    ws.cell(row=row, column=1).fill = TITLE_FILL
    for col in range(2, num_cols + 1):
        ws.cell(row=row, column=col).fill = TITLE_FILL


def _write_xbrl_statement(ws, statement_name, statement_data, periods, start_row):
    """Write a single XBRL financial statement. Returns next available row."""
    if not statement_data:
        return start_row

    row = start_row
    num_cols = len(periods) + 1

    # Title bar
    _write_title_bar(ws, row, statement_name, num_cols)
    row += 1

    # Period headers
    ws.cell(row=row, column=1, value="Line Item").font = HEADER_FONT
    ws.cell(row=row, column=1).fill = HEADER_FILL
    for i, period in enumerate(periods):
        cell = ws.cell(row=row, column=i + 2, value=period)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center")
    row += 1

    # Data rows
    for label, period_values in statement_data.items():
        ws.cell(row=row, column=1, value=label)
        ws.cell(row=row, column=1).border = THIN_BORDER
        for i, period in enumerate(periods):
            if period in period_values:
                val = period_values[period]
                if isinstance(val, (int, float)):
                    _format_number_cell(ws.cell(row=row, column=i + 2), val)
                else:
                    ws.cell(row=row, column=i + 2, value=val)
        row += 1

    row += 1
    return row


def _write_html_table(ws, table_dict, start_row, title_override=None, filing_source=None):
    """Write one HTML-extracted table with matching formatting. Returns next available row."""
    row = start_row
    title = title_override or table_dict.get("title") or "Table"
    headers = table_dict.get("headers", [])
    data_rows = table_dict.get("rows", [])

    # Determine column count
    max_cols = 1
    for hr in headers:
        max_cols = max(max_cols, len(hr))
    for dr in data_rows:
        max_cols = max(max_cols, len(dr))

    # Title bar (same blue bar as XBRL sheets)
    _write_title_bar(ws, row, title, max_cols)
    row += 1

    # Source subtitle if provided
    if filing_source:
        ws.cell(row=row, column=1, value=f"Source: {filing_source}").font = SUBTITLE_FONT
        row += 1

    # Headers
    for header_row in headers:
        for col_idx, val in enumerate(header_row):
            cell = ws.cell(row=row, column=col_idx + 1, value=val)
            cell.font = HEADER_FONT
            cell.fill = HEADER_FILL
            cell.alignment = Alignment(horizontal="center")
        row += 1

    # Data rows
    for data_row in data_rows:
        for col_idx, val in enumerate(data_row):
            num, is_pct = _try_parse_number(val)
            if num is not None:
                _format_number_cell(ws.cell(row=row, column=col_idx + 1), num, is_pct)
            else:
                ws.cell(row=row, column=col_idx + 1, value=val)
                if col_idx == 0:
                    ws.cell(row=row, column=col_idx + 1).border = THIN_BORDER
        row += 1

    row += 1
    return row


def build_workbook(company_name, ticker, xbrl_data, selected_tables, selected_filings, single_sheet=False):
    """Build and save an Excel workbook.

    Args:
        company_name: Company display name.
        ticker: Company ticker symbol.
        xbrl_data: Output from xbrl_parser.extract_financials().
        selected_tables: List of {table, filing_type, filing_date} dicts.
        selected_filings: List of filing dicts {type, date, accession, ...}.
        single_sheet: If True, put everything on one sheet instead of separate tabs.

    Returns:
        (filepath, filename) tuple.
    """
    wb = Workbook()
    used_sheet_names = set()
    periods = xbrl_data.get("periods", [])

    if single_sheet:
        _build_single_sheet(wb, company_name, ticker, xbrl_data, selected_tables, selected_filings, periods)
    else:
        _build_multi_sheet(wb, company_name, ticker, xbrl_data, selected_tables, selected_filings, periods, used_sheet_names)

    # Save
    safe_ticker = re.sub(r'[^A-Za-z0-9]', '', ticker or company_name[:10])
    filename = f"{safe_ticker}_SEC_Filings.xlsx"
    output_dir = tempfile.mkdtemp()
    filepath = os.path.join(output_dir, filename)
    wb.save(filepath)

    return filepath, filename


def _build_single_sheet(wb, company_name, ticker, xbrl_data, selected_tables, selected_filings, periods):
    """Put all data on a single sheet, one section after another."""
    ws = wb.active
    ws.title = "All Data"

    row = 1
    ws.cell(row=row, column=1, value=f"{company_name} ({ticker})").font = TITLE_FONT
    row += 1
    ws.cell(row=row, column=1, value=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}").font = SUBTITLE_FONT
    row += 2

    # XBRL statements
    for statement_name in ("Income Statement", "Balance Sheet", "Cash Flow"):
        statement_data = xbrl_data.get(statement_name, {})
        if statement_data:
            row = _write_xbrl_statement(ws, statement_name, statement_data, periods, start_row=row)
            row += 1

    # Selected HTML tables
    for entry in selected_tables:
        table = entry["table"]
        filing_type = entry.get("filing_type", "")
        filing_date = entry.get("filing_date", "")
        source = f"{filing_type} ({filing_date})"
        row = _write_html_table(ws, table, start_row=row, filing_source=source)
        row += 1

    ws.freeze_panes = "B1"
    _auto_width(ws)


def _build_multi_sheet(wb, company_name, ticker, xbrl_data, selected_tables, selected_filings, periods, used_sheet_names):
    """Separate tabs: Index + core financials + one sheet per selected table."""

    # --- Index Sheet ---
    ws_index = wb.active
    ws_index.title = "Index"
    used_sheet_names.add("Index")

    ws_index.cell(row=1, column=1, value=f"{company_name} ({ticker})").font = TITLE_FONT
    ws_index.cell(row=2, column=1, value=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}").font = SUBTITLE_FONT

    ws_index.cell(row=4, column=1, value="Filings Included:").font = HEADER_FONT
    row = 5
    ws_index.cell(row=row, column=1, value="Type").font = HEADER_FONT
    ws_index.cell(row=row, column=1).fill = HEADER_FILL
    ws_index.cell(row=row, column=2, value="Date").font = HEADER_FONT
    ws_index.cell(row=row, column=2).fill = HEADER_FILL
    row += 1
    for filing in selected_filings:
        ws_index.cell(row=row, column=1, value=filing.get("type", ""))
        ws_index.cell(row=row, column=2, value=filing.get("date", ""))
        row += 1

    if selected_tables:
        row += 1
        ws_index.cell(row=row, column=1, value="Additional Tables Included:").font = HEADER_FONT
        row += 1
        ws_index.cell(row=row, column=1, value="Sheet Name").font = HEADER_FONT
        ws_index.cell(row=row, column=1).fill = HEADER_FILL
        ws_index.cell(row=row, column=2, value="Source").font = HEADER_FONT
        ws_index.cell(row=row, column=2).fill = HEADER_FILL
        row += 1

    _auto_width(ws_index)

    # --- Core Financial Statement Sheets ---
    for statement_name in ("Income Statement", "Balance Sheet", "Cash Flow"):
        statement_data = xbrl_data.get(statement_name, {})
        if not statement_data:
            continue

        sheet_name = _unique_sheet_name(statement_name, used_sheet_names)
        ws = wb.create_sheet(title=sheet_name)
        ws.freeze_panes = "B3"
        _write_xbrl_statement(ws, statement_name, statement_data, periods, start_row=1)
        _auto_width(ws)

    # --- Individual Table Sheets ---
    index_table_row = row
    for entry in selected_tables:
        table = entry["table"]
        filing_type = entry.get("filing_type", "")
        filing_date = entry.get("filing_date", "")
        title = table.get("title") or "Table"
        source = f"{filing_type} ({filing_date})"

        sheet_name = _unique_sheet_name(title, used_sheet_names)
        ws = wb.create_sheet(title=sheet_name)
        ws.freeze_panes = "A3"

        _write_html_table(ws, table, start_row=1, filing_source=source)
        _auto_width(ws)

        # Add to index
        ws_index.cell(row=index_table_row, column=1, value=sheet_name)
        ws_index.cell(row=index_table_row, column=2, value=source)
        index_table_row += 1

    _auto_width(ws_index)
