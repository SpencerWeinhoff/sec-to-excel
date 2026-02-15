"""Flask application for SEC Filing to Excel converter."""

import os
import time
import traceback
import uuid

from flask import Flask, render_template, request, jsonify, send_file

import sec_client
import xbrl_parser
import html_parser
import excel_builder

app = Flask(__name__)

# In-memory cache for scanned tables (scan_id -> data)
# So we don't have to re-fetch filings on generate
_scan_cache = {}
_CACHE_TTL = 600  # 10 minutes


def _clean_cache():
    """Remove expired cache entries."""
    now = time.time()
    expired = [k for k, v in _scan_cache.items() if now - v["time"] > _CACHE_TTL]
    for k in expired:
        del _scan_cache[k]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").strip()
    if not query or len(query) < 1:
        return jsonify([])

    try:
        results = sec_client.search_company(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/filings")
def api_filings():
    cik = request.args.get("cik", "").strip()
    if not cik:
        return jsonify({"error": "CIK is required"}), 400

    try:
        filings = sec_client.get_filings(cik)
        return jsonify(filings)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/scan", methods=["POST"])
def api_scan():
    """Fetch selected filings, extract all tables, return table list for user to pick from."""
    _clean_cache()

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    cik = data.get("cik", "")
    selected_filings = data.get("filings", [])

    if not cik or not selected_filings:
        return jsonify({"error": "CIK and at least one filing are required"}), 400

    try:
        # Fetch and parse HTML for each filing
        all_tables = []  # flat list with filing metadata attached
        tables_by_filing = {}

        for filing in selected_filings:
            doc_url = filing.get("doc_url", "")
            accession = filing.get("accession", "")
            if doc_url:
                try:
                    html_content = sec_client.get_filing_html(doc_url)
                    tables = html_parser.extract_tables(html_content)
                    tables_by_filing[accession] = tables

                    for i, table in enumerate(tables):
                        all_tables.append({
                            "id": f"{accession}:{i}",
                            "title": table.get("title") or f"Table {i + 1}",
                            "filing_type": filing.get("type", ""),
                            "filing_date": filing.get("date", ""),
                            "accession": accession,
                            "table_index": i,
                            "rows": len(table.get("rows", [])),
                            "cols": len(table.get("rows", [[]])[0]) if table.get("rows") else 0,
                        })
                except Exception:
                    tables_by_filing[accession] = []

        # Cache the full parsed data for generate step
        scan_id = str(uuid.uuid4())
        _scan_cache[scan_id] = {
            "time": time.time(),
            "tables_by_filing": tables_by_filing,
            "filings": selected_filings,
            "cik": cik,
        }

        return jsonify({
            "scan_id": scan_id,
            "tables": all_tables,
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Scan failed: {str(e)}"}), 500


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    cik = data.get("cik", "")
    company_name = data.get("company_name", "Unknown")
    ticker = data.get("ticker", "")
    selected_filings = data.get("filings", [])
    scan_id = data.get("scan_id", "")
    selected_table_ids = set(data.get("selected_tables", []))
    single_sheet = data.get("single_sheet", False)

    if not cik or not selected_filings:
        return jsonify({"error": "CIK and at least one filing are required"}), 400

    try:
        # 1. Fetch XBRL data for core financials
        xbrl_facts = sec_client.get_xbrl_facts(cik)
        xbrl_data = xbrl_parser.extract_financials(xbrl_facts, selected_filings)

        # 2. Get HTML tables — from cache if available, otherwise re-fetch
        selected_tables = []
        cached = _scan_cache.get(scan_id)

        if cached:
            # Pull only the user-selected tables from cache
            for filing in selected_filings:
                accession = filing.get("accession", "")
                tables = cached["tables_by_filing"].get(accession, [])
                for i, table in enumerate(tables):
                    table_id = f"{accession}:{i}"
                    if table_id in selected_table_ids:
                        selected_tables.append({
                            "table": table,
                            "filing_type": filing.get("type", ""),
                            "filing_date": filing.get("date", ""),
                        })
        else:
            # No cache — re-fetch (fallback)
            for filing in selected_filings:
                doc_url = filing.get("doc_url", "")
                accession = filing.get("accession", "")
                if doc_url:
                    try:
                        html_content = sec_client.get_filing_html(doc_url)
                        tables = html_parser.extract_tables(html_content)
                        for i, table in enumerate(tables):
                            table_id = f"{accession}:{i}"
                            if table_id in selected_table_ids:
                                selected_tables.append({
                                    "table": table,
                                    "filing_type": filing.get("type", ""),
                                    "filing_date": filing.get("date", ""),
                                })
                    except Exception:
                        pass

        # 3. Build Excel workbook
        filepath, filename = excel_builder.build_workbook(
            company_name=company_name,
            ticker=ticker,
            xbrl_data=xbrl_data,
            selected_tables=selected_tables,
            selected_filings=selected_filings,
            single_sheet=single_sheet,
        )

        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Generation failed: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=True, port=port)
