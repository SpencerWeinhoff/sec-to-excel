import requests
import time
from datetime import datetime, timedelta

HEADERS = {
    "User-Agent": "SECToExcel/1.0 (sec-to-excel@example.com)",
    "Accept-Encoding": "gzip, deflate",
}

# Cache the company tickers list in memory
_company_tickers_cache = None
_cache_time = None
CACHE_TTL = 3600  # 1 hour


def _rate_limit():
    """Sleep briefly to respect SEC's 10 req/s limit."""
    time.sleep(0.12)


def _get_company_tickers():
    """Fetch and cache the SEC company tickers JSON."""
    global _company_tickers_cache, _cache_time
    if _company_tickers_cache and _cache_time and (time.time() - _cache_time < CACHE_TTL):
        return _company_tickers_cache

    _rate_limit()
    resp = requests.get(
        "https://www.sec.gov/files/company_tickers.json",
        headers=HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    # Convert from {0: {cik_str, ticker, title}, 1: ...} to list
    tickers = []
    for entry in data.values():
        tickers.append({
            "cik": str(entry["cik_str"]),
            "ticker": entry["ticker"],
            "name": entry["title"],
        })

    _company_tickers_cache = tickers
    _cache_time = time.time()
    return tickers


def search_company(query):
    """Search for companies by name or ticker. Returns top 15 matches."""
    tickers = _get_company_tickers()
    query_lower = query.lower().strip()
    if not query_lower:
        return []

    exact_ticker = []
    starts_with = []
    contains = []

    for co in tickers:
        ticker_lower = co["ticker"].lower()
        name_lower = co["name"].lower()

        if ticker_lower == query_lower:
            exact_ticker.append(co)
        elif ticker_lower.startswith(query_lower) or name_lower.startswith(query_lower):
            starts_with.append(co)
        elif query_lower in ticker_lower or query_lower in name_lower:
            contains.append(co)

    results = exact_ticker + starts_with + contains
    return results[:15]


def get_filings(cik, filing_types=None, years=5):
    """Get filings for a company from SEC EDGAR submissions endpoint.

    Returns list of {type, date, accession, primary_doc, description}.
    """
    if filing_types is None:
        filing_types = ["10-K", "10-Q", "8-K"]

    cik_padded = cik.zfill(10)
    _rate_limit()
    resp = requests.get(
        f"https://data.sec.gov/submissions/CIK{cik_padded}.json",
        headers=HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    cutoff = datetime.now() - timedelta(days=years * 365)
    filings = []

    def process_filing_batch(recent):
        forms = recent.get("form", [])
        dates = recent.get("filingDate", [])
        accessions = recent.get("accessionNumber", [])
        primary_docs = recent.get("primaryDocument", [])
        descriptions = recent.get("primaryDocDescription", [])

        for i in range(len(forms)):
            form_type = forms[i]
            # Match exact types and amendments (e.g., 10-K/A)
            if form_type not in filing_types and form_type.rstrip("/A") not in filing_types:
                continue

            filing_date = dates[i]
            try:
                dt = datetime.strptime(filing_date, "%Y-%m-%d")
            except ValueError:
                continue

            if dt < cutoff:
                continue

            accession = accessions[i]
            accession_no_dash = accession.replace("-", "")
            primary_doc = primary_docs[i] if i < len(primary_docs) else ""
            description = descriptions[i] if i < len(descriptions) else ""

            doc_url = ""
            if primary_doc:
                doc_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_no_dash}/{primary_doc}"

            filings.append({
                "type": form_type,
                "date": filing_date,
                "accession": accession,
                "primary_doc": primary_doc,
                "doc_url": doc_url,
                "description": description,
            })

    # Process recent filings
    if "recent" in data.get("filings", data):
        recent = data.get("filings", data).get("recent", data.get("recent", {}))
        process_filing_batch(recent)

    # Process older filing files if they exist
    for file_entry in data.get("filings", {}).get("files", []):
        _rate_limit()
        file_resp = requests.get(
            f"https://data.sec.gov/submissions/{file_entry['name']}",
            headers=HEADERS,
            timeout=30,
        )
        if file_resp.ok:
            process_filing_batch(file_resp.json())

    # Sort by date descending
    filings.sort(key=lambda f: f["date"], reverse=True)
    return filings


def get_xbrl_facts(cik):
    """Fetch all XBRL company facts for a CIK."""
    cik_padded = cik.zfill(10)
    _rate_limit()
    resp = requests.get(
        f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json",
        headers=HEADERS,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def get_filing_html(url):
    """Download the HTML content of a specific filing document."""
    _rate_limit()
    resp = requests.get(url, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    return resp.text


def get_filing_index(cik, accession):
    """Get the filing index page to find all documents in a filing."""
    cik_num = str(int(cik))
    accession_no_dash = accession.replace("-", "")
    _rate_limit()
    resp = requests.get(
        f"https://www.sec.gov/Archives/edgar/data/{cik_num}/{accession_no_dash}/index.json",
        headers=HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()
