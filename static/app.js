// State
let selectedCompany = null;
let allFilings = [];
let selectedFilings = new Set();
let scannedTables = [];
let selectedTableIds = new Set();
let currentScanId = null;

// Brand color database — keywords map to colors
const BRAND_COLORS = {
    "apple":       { primary: "#333333", accent: "#E0E0E0" },
    "aapl":        { primary: "#333333", accent: "#E0E0E0" },
    "microsoft":   { primary: "#0078D4", accent: "#DEECF9" },
    "msft":        { primary: "#0078D4", accent: "#DEECF9" },
    "google":      { primary: "#4285F4", accent: "#D2E3FC" },
    "alphabet":    { primary: "#4285F4", accent: "#D2E3FC" },
    "googl":       { primary: "#4285F4", accent: "#D2E3FC" },
    "amazon":      { primary: "#FF9900", accent: "#FFF2CC" },
    "amzn":        { primary: "#FF9900", accent: "#FFF2CC" },
    "meta":        { primary: "#0668E1", accent: "#D6E8FF" },
    "facebook":    { primary: "#0668E1", accent: "#D6E8FF" },
    "netflix":     { primary: "#E50914", accent: "#FDDEDE" },
    "nflx":        { primary: "#E50914", accent: "#FDDEDE" },
    "tesla":       { primary: "#CC0000", accent: "#F5D5D5" },
    "tsla":        { primary: "#CC0000", accent: "#F5D5D5" },
    "nvidia":      { primary: "#76B900", accent: "#E8F5CC" },
    "nvda":        { primary: "#76B900", accent: "#E8F5CC" },
    "jpmorgan":    { primary: "#004B87", accent: "#D0E2F0" },
    "jpm":         { primary: "#004B87", accent: "#D0E2F0" },
    "chase":       { primary: "#004B87", accent: "#D0E2F0" },
    "goldman":     { primary: "#6B9AC4", accent: "#E1ECF5" },
    "gs":          { primary: "#6B9AC4", accent: "#E1ECF5" },
    "morgan stanley": { primary: "#002F5F", accent: "#D0DFEE" },
    "ms":          { primary: "#002F5F", accent: "#D0DFEE" },
    "bank of america": { primary: "#012169", accent: "#CDD6E8" },
    "bac":         { primary: "#012169", accent: "#CDD6E8" },
    "wells fargo": { primary: "#D71E28", accent: "#F9D5D7" },
    "wfc":         { primary: "#D71E28", accent: "#F9D5D7" },
    "citigroup":   { primary: "#003B70", accent: "#CDDCED" },
    "citi":        { primary: "#003B70", accent: "#CDDCED" },
    "walmart":     { primary: "#0071CE", accent: "#D6ECFF" },
    "wmt":         { primary: "#0071CE", accent: "#D6ECFF" },
    "costco":      { primary: "#E31837", accent: "#F9D3D9" },
    "cost":        { primary: "#E31837", accent: "#F9D3D9" },
    "target":      { primary: "#CC0000", accent: "#F5D5D5" },
    "tgt":         { primary: "#CC0000", accent: "#F5D5D5" },
    "disney":      { primary: "#113CCF", accent: "#D4DDFA" },
    "dis":         { primary: "#113CCF", accent: "#D4DDFA" },
    "nike":        { primary: "#111111", accent: "#E0E0E0" },
    "nke":         { primary: "#111111", accent: "#E0E0E0" },
    "coca-cola":   { primary: "#F40000", accent: "#FDE0E0" },
    "coca cola":   { primary: "#F40000", accent: "#FDE0E0" },
    "coke":        { primary: "#F40000", accent: "#FDE0E0" },
    "ko":          { primary: "#F40000", accent: "#FDE0E0" },
    "pepsi":       { primary: "#004B93", accent: "#D0DFF0" },
    "pepsico":     { primary: "#004B93", accent: "#D0DFF0" },
    "pep":         { primary: "#004B93", accent: "#D0DFF0" },
    "berkshire":   { primary: "#2D2D6E", accent: "#D8D8EA" },
    "brk":         { primary: "#2D2D6E", accent: "#D8D8EA" },
    "johnson":     { primary: "#D51900", accent: "#F6D3CE" },
    "jnj":         { primary: "#D51900", accent: "#F6D3CE" },
    "procter":     { primary: "#003DA5", accent: "#CCDDF2" },
    "p&g":         { primary: "#003DA5", accent: "#CCDDF2" },
    "pg":          { primary: "#003DA5", accent: "#CCDDF2" },
    "visa":        { primary: "#1A1F71", accent: "#D2D4E9" },
    "v":           { primary: "#1A1F71", accent: "#D2D4E9" },
    "mastercard":  { primary: "#EB001B", accent: "#FBCCCE" },
    "ma":          { primary: "#EB001B", accent: "#FBCCCE" },
    "unitedhealth": { primary: "#002677", accent: "#CCD5EC" },
    "unh":         { primary: "#002677", accent: "#CCD5EC" },
    "exxon":       { primary: "#ED1C24", accent: "#FBD1D3" },
    "xom":         { primary: "#ED1C24", accent: "#FBD1D3" },
    "chevron":     { primary: "#0054A6", accent: "#CDE0F3" },
    "cvx":         { primary: "#0054A6", accent: "#CDE0F3" },
    "pfizer":      { primary: "#0093D0", accent: "#CCE9F6" },
    "pfe":         { primary: "#0093D0", accent: "#CCE9F6" },
    "intel":       { primary: "#0071C5", accent: "#D6ECFF" },
    "intc":        { primary: "#0071C5", accent: "#D6ECFF" },
    "amd":         { primary: "#ED1C24", accent: "#FBD1D3" },
    "salesforce":  { primary: "#00A1E0", accent: "#CCEDFA" },
    "crm":         { primary: "#00A1E0", accent: "#CCEDFA" },
    "adobe":       { primary: "#FF0000", accent: "#FFCCCC" },
    "adbe":        { primary: "#FF0000", accent: "#FFCCCC" },
    "oracle":      { primary: "#F80000", accent: "#FECCCC" },
    "orcl":        { primary: "#F80000", accent: "#FECCCC" },
    "ibm":         { primary: "#0530AD", accent: "#D0D8F2" },
    "cisco":       { primary: "#049FD9", accent: "#CDECF8" },
    "csco":        { primary: "#049FD9", accent: "#CDECF8" },
    "uber":        { primary: "#000000", accent: "#E0E0E0" },
    "airbnb":      { primary: "#FF5A5F", accent: "#FFD9DA" },
    "abnb":        { primary: "#FF5A5F", accent: "#FFD9DA" },
    "spotify":     { primary: "#1DB954", accent: "#D2F5DF" },
    "spot":        { primary: "#1DB954", accent: "#D2F5DF" },
    "snap":        { primary: "#FFFC00", accent: "#FFFEE6" },
    "snapchat":    { primary: "#FFFC00", accent: "#FFFEE6" },
    "paypal":      { primary: "#003087", accent: "#CCD8EE" },
    "pypl":        { primary: "#003087", accent: "#CCD8EE" },
    "starbucks":   { primary: "#006241", accent: "#CCDFDA" },
    "sbux":        { primary: "#006241", accent: "#CCDFDA" },
    "mcdonalds":   { primary: "#FFC72C", accent: "#FFF4D4" },
    "mcd":         { primary: "#FFC72C", accent: "#FFF4D4" },
    "boeing":      { primary: "#0033A0", accent: "#CCD6F0" },
    "ba":          { primary: "#0033A0", accent: "#CCD6F0" },
    "lockheed":    { primary: "#003366", accent: "#CCD6E0" },
    "lmt":         { primary: "#003366", accent: "#CCD6E0" },
    "caterpillar": { primary: "#FFCD11", accent: "#FFF5D0" },
    "cat":         { primary: "#FFCD11", accent: "#FFF5D0" },
    "3m":          { primary: "#FF0000", accent: "#FFCCCC" },
    "mmm":         { primary: "#FF0000", accent: "#FFCCCC" },
    "home depot":  { primary: "#F96302", accent: "#FEE0CC" },
    "hd":          { primary: "#F96302", accent: "#FEE0CC" },
    "lowes":       { primary: "#004990", accent: "#CCD8EE" },
    "low":         { primary: "#004990", accent: "#CCD8EE" },
};

// DOM elements
const searchInput = document.getElementById("search-input");
const searchResults = document.getElementById("search-results");
const stepFilings = document.getElementById("step-filings");
const stepTables = document.getElementById("step-tables");
const stepGenerate = document.getElementById("step-generate");
const selectedCompanyEl = document.getElementById("selected-company");
const filingsList = document.getElementById("filings-list");
const filingsLoading = document.getElementById("filings-loading");
const btnScan = document.getElementById("btn-scan");
const scanLoading = document.getElementById("scan-loading");
const scanError = document.getElementById("scan-error");
const tablesList = document.getElementById("tables-list");
const tablesEmpty = document.getElementById("tables-empty");
const generateSummary = document.getElementById("generate-summary");
const btnGenerate = document.getElementById("btn-generate");
const generateLoading = document.getElementById("generate-loading");
const generateError = document.getElementById("generate-error");
const resetSection = document.getElementById("reset-section");
const colorPrimary = document.getElementById("color-primary");
const colorAccent = document.getElementById("color-accent");
const colorCompanyInput = document.getElementById("color-company-input");
const colorMatchResult = document.getElementById("color-match-result");
const matchSwatchPrimary = document.getElementById("match-swatch-primary");
const matchSwatchAccent = document.getElementById("match-swatch-accent");
const matchLabel = document.getElementById("match-label");

// Debounce helper
function debounce(fn, ms) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), ms);
    };
}

// --- Color Theme ---
function lookupBrandColor(query) {
    if (!query) return null;
    const q = query.toLowerCase().trim();
    // Direct match
    if (BRAND_COLORS[q]) return { name: query, colors: BRAND_COLORS[q] };
    // Partial match — find first key that contains the query or vice versa
    for (const [key, colors] of Object.entries(BRAND_COLORS)) {
        if (key.includes(q) || q.includes(key)) {
            return { name: key.charAt(0).toUpperCase() + key.slice(1), colors };
        }
    }
    return null;
}

colorCompanyInput.addEventListener("input", debounce(function () {
    const match = lookupBrandColor(colorCompanyInput.value);
    if (match) {
        colorPrimary.value = match.colors.primary;
        colorAccent.value = match.colors.accent;
        matchSwatchPrimary.style.background = match.colors.primary;
        matchSwatchAccent.style.background = match.colors.accent;
        matchLabel.textContent = match.name;
        colorMatchResult.classList.add("visible");
    } else {
        colorMatchResult.classList.remove("visible");
    }
}, 200));

// --- Search ---
searchInput.addEventListener(
    "input",
    debounce(async function () {
        const query = searchInput.value.trim();
        if (query.length < 1) {
            searchResults.classList.add("hidden");
            return;
        }

        try {
            const resp = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const data = await resp.json();

            if (data.error) {
                searchResults.innerHTML = `<div class="dropdown-item"><span class="company-name" style="color:#dc2626">${data.error}</span></div>`;
                searchResults.classList.remove("hidden");
                return;
            }

            if (data.length === 0) {
                searchResults.innerHTML = `<div class="dropdown-item"><span class="company-name" style="color:#9ca3af">No results found</span></div>`;
                searchResults.classList.remove("hidden");
                return;
            }

            searchResults.innerHTML = data
                .map(
                    (co) => `
                <div class="dropdown-item" data-cik="${co.cik}" data-ticker="${co.ticker}" data-name="${co.name}">
                    <span class="company-name">${co.name}</span>
                    <span class="company-ticker">${co.ticker}</span>
                </div>
            `
                )
                .join("");

            searchResults.classList.remove("hidden");

            searchResults.querySelectorAll(".dropdown-item").forEach((item) => {
                item.addEventListener("click", () => selectCompany(item.dataset));
            });
        } catch (err) {
            console.error("Search error:", err);
        }
    }, 250)
);

document.addEventListener("click", (e) => {
    if (!e.target.closest(".search-box")) {
        searchResults.classList.add("hidden");
    }
});

// --- Select Company ---
async function selectCompany({ cik, ticker, name }) {
    selectedCompany = { cik, ticker, name };
    searchResults.classList.add("hidden");
    searchInput.value = `${name} (${ticker})`;

    // Auto-fill color company input
    const match = lookupBrandColor(name) || lookupBrandColor(ticker);
    if (match) {
        colorCompanyInput.value = match.name;
        colorPrimary.value = match.colors.primary;
        colorAccent.value = match.colors.accent;
        matchSwatchPrimary.style.background = match.colors.primary;
        matchSwatchAccent.style.background = match.colors.accent;
        matchLabel.textContent = match.name;
        colorMatchResult.classList.add("visible");
    } else {
        colorCompanyInput.value = "";
        colorMatchResult.classList.remove("visible");
    }

    // Show filings step, hide later steps
    stepFilings.classList.remove("hidden");
    stepTables.classList.add("hidden");
    stepGenerate.classList.add("hidden");
    selectedCompanyEl.innerHTML = `
        <span class="name">${name}</span>
        <span class="ticker">${ticker} &middot; CIK ${cik}</span>
    `;

    filingsList.innerHTML = "";
    filingsLoading.classList.remove("hidden");
    btnScan.classList.add("hidden");
    resetSection.classList.remove("hidden");

    try {
        const resp = await fetch(`/api/filings?cik=${encodeURIComponent(cik)}`);
        const data = await resp.json();

        if (data.error) {
            filingsList.innerHTML = `<div class="error">${data.error}</div>`;
            filingsLoading.classList.add("hidden");
            return;
        }

        allFilings = data;
        selectedFilings.clear();
        renderFilings();
    } catch (err) {
        filingsList.innerHTML = `<div class="error">Failed to load filings: ${err.message}</div>`;
    } finally {
        filingsLoading.classList.add("hidden");
    }
}

// --- Render Filings ---
function renderFilings() {
    const groups = {};
    const typeOrder = ["10-K", "10-K/A", "10-Q", "10-Q/A", "8-K", "8-K/A"];

    for (const filing of allFilings) {
        const type = filing.type;
        if (!groups[type]) groups[type] = [];
        groups[type].push(filing);
    }

    const sortedTypes = Object.keys(groups).sort((a, b) => {
        const ai = typeOrder.indexOf(a);
        const bi = typeOrder.indexOf(b);
        return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
    });

    let html = "";
    for (const type of sortedTypes) {
        const filings = groups[type];
        html += `<div class="filing-group">`;
        html += `<div class="filing-group-header">${type} (${filings.length})</div>`;

        for (const f of filings) {
            const id = f.accession;
            const checked = selectedFilings.has(id) ? "checked" : "";
            html += `
                <div class="filing-item">
                    <input type="checkbox" id="f-${id}" data-accession="${id}" ${checked}>
                    <label for="f-${id}">
                        <span class="filing-type">${f.type}</span>
                        <span class="filing-date">${f.date}</span>
                    </label>
                </div>
            `;
        }
        html += `</div>`;
    }

    filingsList.innerHTML = html;

    filingsList.querySelectorAll('input[type="checkbox"]').forEach((cb) => {
        cb.addEventListener("change", () => {
            if (cb.checked) {
                selectedFilings.add(cb.dataset.accession);
            } else {
                selectedFilings.delete(cb.dataset.accession);
            }
            updateScanButton();
        });
    });

    updateScanButton();
}

function updateScanButton() {
    if (selectedFilings.size > 0) {
        btnScan.classList.remove("hidden");
        btnScan.textContent = `Scan ${selectedFilings.size} Filing(s)`;
    } else {
        btnScan.classList.add("hidden");
    }
    stepTables.classList.add("hidden");
    stepGenerate.classList.add("hidden");
}

// --- Bulk selection buttons ---
document.getElementById("btn-select-all-10k").addEventListener("click", () => selectByType("10-K"));
document.getElementById("btn-select-all-10q").addEventListener("click", () => selectByType("10-Q"));
document.getElementById("btn-select-all-8k").addEventListener("click", () => selectByType("8-K"));
document.getElementById("btn-select-none").addEventListener("click", () => {
    selectedFilings.clear();
    renderFilings();
});

function selectByType(type) {
    for (const f of allFilings) {
        if (f.type === type || f.type === type + "/A") {
            selectedFilings.add(f.accession);
        }
    }
    renderFilings();
}

// --- Scan filings ---
btnScan.addEventListener("click", async () => {
    if (!selectedCompany || selectedFilings.size === 0) return;

    btnScan.disabled = true;
    scanLoading.classList.remove("hidden");
    scanError.classList.add("hidden");
    stepTables.classList.add("hidden");
    stepGenerate.classList.add("hidden");

    const filingsToScan = allFilings
        .filter((f) => selectedFilings.has(f.accession))
        .map((f) => ({
            type: f.type,
            date: f.date,
            accession: f.accession,
            doc_url: f.doc_url,
        }));

    try {
        const resp = await fetch("/api/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                cik: selectedCompany.cik,
                filings: filingsToScan,
            }),
        });

        const data = await resp.json();

        if (!resp.ok || data.error) {
            throw new Error(data.error || `Server error ${resp.status}`);
        }

        currentScanId = data.scan_id;
        scannedTables = data.tables;
        selectedTableIds.clear();

        renderTables();
        stepTables.classList.remove("hidden");
        stepGenerate.classList.remove("hidden");
        updateGenerateSummary();
    } catch (err) {
        scanError.textContent = err.message;
        scanError.classList.remove("hidden");
    } finally {
        scanLoading.classList.add("hidden");
        btnScan.disabled = false;
    }
});

// --- Render scanned tables ---
function renderTables() {
    if (scannedTables.length === 0) {
        tablesList.innerHTML = "";
        tablesEmpty.classList.remove("hidden");
        return;
    }
    tablesEmpty.classList.add("hidden");

    const groups = {};
    for (const t of scannedTables) {
        const key = `${t.filing_type} (${t.filing_date})`;
        if (!groups[key]) groups[key] = [];
        groups[key].push(t);
    }

    let html = "";
    for (const [filingLabel, tables] of Object.entries(groups)) {
        html += `<div class="filing-group">`;
        html += `<div class="filing-group-header">${filingLabel} &mdash; ${tables.length} table(s)</div>`;

        for (const t of tables) {
            const checked = selectedTableIds.has(t.id) ? "checked" : "";
            const dims = `${t.rows} rows`;
            html += `
                <div class="filing-item">
                    <input type="checkbox" id="t-${t.id}" data-table-id="${t.id}" ${checked}>
                    <label for="t-${t.id}">
                        <span class="table-title">${t.title}</span>
                        <span class="filing-date">${dims}</span>
                    </label>
                </div>
            `;
        }
        html += `</div>`;
    }

    tablesList.innerHTML = html;

    tablesList.querySelectorAll('input[type="checkbox"]').forEach((cb) => {
        cb.addEventListener("change", () => {
            if (cb.checked) {
                selectedTableIds.add(cb.dataset.tableId);
            } else {
                selectedTableIds.delete(cb.dataset.tableId);
            }
            updateGenerateSummary();
        });
    });
}

// Table bulk selection
document.getElementById("btn-select-all-tables").addEventListener("click", () => {
    for (const t of scannedTables) {
        selectedTableIds.add(t.id);
    }
    renderTables();
    updateGenerateSummary();
});

document.getElementById("btn-select-no-tables").addEventListener("click", () => {
    selectedTableIds.clear();
    renderTables();
    updateGenerateSummary();
});

// --- Generate summary ---
function updateGenerateSummary() {
    const tableCount = selectedTableIds.size;
    let text = `Core financials (Income Statement, Balance Sheet, Cash Flow) will always be included.`;
    if (tableCount > 0) {
        text += ` Plus ${tableCount} additional table(s) you selected.`;
    }
    generateSummary.textContent = text;
}

// --- Generate ---
btnGenerate.addEventListener("click", async () => {
    if (!selectedCompany || selectedFilings.size === 0) return;

    btnGenerate.disabled = true;
    generateLoading.classList.remove("hidden");
    generateError.classList.add("hidden");

    const filingsToSend = allFilings
        .filter((f) => selectedFilings.has(f.accession))
        .map((f) => ({
            type: f.type,
            date: f.date,
            accession: f.accession,
            doc_url: f.doc_url,
        }));

    const singleSheet = document.querySelector('input[name="output-mode"]:checked')?.value === "single";

    try {
        const resp = await fetch("/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                cik: selectedCompany.cik,
                company_name: selectedCompany.name,
                ticker: selectedCompany.ticker,
                filings: filingsToSend,
                scan_id: currentScanId,
                selected_tables: Array.from(selectedTableIds),
                single_sheet: singleSheet,
                brand_colors: {
                    primary: colorPrimary.value,
                    accent: colorAccent.value,
                },
            }),
        });

        if (!resp.ok) {
            const errData = await resp.json().catch(() => ({}));
            throw new Error(errData.error || `Server error ${resp.status}`);
        }

        const blob = await resp.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${selectedCompany.ticker}_SEC_Filings.xlsx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (err) {
        generateError.textContent = err.message;
        generateError.classList.remove("hidden");
    } finally {
        generateLoading.classList.add("hidden");
        btnGenerate.disabled = false;
    }
});

// --- Reset ---
document.getElementById("btn-reset").addEventListener("click", () => {
    selectedCompany = null;
    allFilings = [];
    selectedFilings.clear();
    scannedTables = [];
    selectedTableIds.clear();
    currentScanId = null;
    searchInput.value = "";
    colorCompanyInput.value = "";
    colorPrimary.value = "#4472C4";
    colorAccent.value = "#D9E1F2";
    colorMatchResult.classList.remove("visible");
    stepFilings.classList.add("hidden");
    stepTables.classList.add("hidden");
    stepGenerate.classList.add("hidden");
    resetSection.classList.add("hidden");
    generateError.classList.add("hidden");
    scanError.classList.add("hidden");
    searchInput.focus();
});
