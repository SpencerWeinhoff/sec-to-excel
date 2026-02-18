"""Flask application for Spencer's Toolkit."""

import os
import time
import traceback
import uuid

from flask import Flask, render_template, request, jsonify, send_file

import json

import sec_client
import xbrl_parser
import html_parser
import excel_builder
import ppt_builder
import value_chain_builder

app = Flask(__name__)

# Load industry data at startup
_industry_data_path = os.path.join(os.path.dirname(__file__), "industry_data.json")
with open(_industry_data_path, "r") as _f:
    _industry_data = json.load(_f)

# Load value chain data at startup
_vc_data_path = os.path.join(os.path.dirname(__file__), "value_chain_data.json")
with open(_vc_data_path, "r") as _f:
    _vc_data = json.load(_f)

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
def home():
    return render_template("home.html")


@app.route("/sec-to-excel")
def sec_to_excel():
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
    brand_colors = data.get("brand_colors")

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
            brand_colors=brand_colors,
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


# ── Industry Landscape routes ──

@app.route("/landscape")
def landscape():
    return render_template("landscape.html")


@app.route("/api/industries")
def api_industries():
    """Return industry list with sub-industry summaries."""
    result = []
    for ind in _industry_data.get("industries", []):
        subs = []
        total_companies = 0
        for sub in ind.get("sub_industries", []):
            companies = sub.get("companies", [])
            total_companies += len(companies)
            subs.append({
                "id": sub["id"],
                "name": sub["name"],
                "companies": companies,
            })
        result.append({
            "id": ind["id"],
            "name": ind["name"],
            "sub_industries": subs,
            "company_count": total_companies,
        })
    return jsonify({"industries": result})


@app.route("/api/landscape/generate", methods=["POST"])
def api_landscape_generate():
    """Generate industry landscape PPT."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    industry_id = data.get("industry_id", "")
    sub_industry_ids = set(data.get("sub_industry_ids", []))

    if not industry_id:
        return jsonify({"error": "Industry ID is required"}), 400

    # Find the industry
    industry = None
    for ind in _industry_data.get("industries", []):
        if ind["id"] == industry_id:
            industry = ind
            break

    if not industry:
        return jsonify({"error": "Industry not found"}), 404

    try:
        filepath, filename = ppt_builder.build_landscape_ppt(
            industry=industry,
            selected_sub_ids=sub_industry_ids if sub_industry_ids else None,
        )

        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"PPT generation failed: {str(e)}"}), 500


# ── Value Chain routes ──

@app.route("/value-chain")
def value_chain():
    return render_template("value_chain.html")


@app.route("/api/value-chains")
def api_value_chains():
    """Return list of available value chains with summary info."""
    result = []
    for vc in _vc_data.get("value_chains", []):
        broad_stages = len(vc.get("broad", {}).get("stages", []))
        narrow = vc.get("narrow", {})
        narrow_stages = len(narrow.get("stages", []))
        result.append({
            "id": vc["id"],
            "name": vc["name"],
            "keywords": vc.get("keywords", []),
            "broad_stages": broad_stages,
            "narrow_stages": narrow_stages,
            "narrow_focus": narrow.get("focus", ""),
        })
    return jsonify({"value_chains": result})


@app.route("/api/value-chain/generate", methods=["POST"])
def api_value_chain_generate():
    """Generate value chain PPT."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    chain_id = data.get("chain_id", "")
    scope = data.get("scope", "broad")

    if not chain_id:
        return jsonify({"error": "Chain ID is required"}), 400

    if scope not in ("broad", "narrow", "both"):
        return jsonify({"error": "Invalid scope"}), 400

    # Find the value chain
    chain = None
    for vc in _vc_data.get("value_chains", []):
        if vc["id"] == chain_id:
            chain = vc
            break

    if not chain:
        return jsonify({"error": "Value chain not found"}), 404

    try:
        filepath, filename = value_chain_builder.build_value_chain_ppt(
            value_chain=chain,
            scope=scope,
        )

        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"PPT generation failed: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=True, port=port)
