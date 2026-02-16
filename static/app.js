// State
let selectedCompany = null;
let allFilings = [];
let selectedFilings = new Set();
let scannedTables = [];
let selectedTableIds = new Set();
let currentScanId = null;

// Company brand color presets
const COLOR_PRESETS = {
    "Default":   { primary: "#4472C4", accent: "#D9E1F2" },
    "Apple":     { primary: "#333333", accent: "#E0E0E0" },
    "Microsoft": { primary: "#0078D4", accent: "#DEECF9" },
    "Google":    { primary: "#4285F4", accent: "#D2E3FC" },
    "Amazon":    { primary: "#FF9900", accent: "#FFF2CC" },
    "Meta":      { primary: "#0668E1", accent: "#D6E8FF" },
    "Netflix":   { primary: "#E50914", accent: "#FDDEDE" },
    "Tesla":     { primary: "#CC0000", accent: "#F5D5D5" },
    "JPMorgan":  { primary: "#004B87", accent: "#D0E2F0" },
    "Goldman":   { primary: "#6B9AC4", accent: "#E1ECF5" },
    "Walmart":   { primary: "#0071CE", accent: "#D6ECFF" },
    "Disney":    { primary: "#113CCF", accent: "#D4DDFA" },
    "Nike":      { primary: "#111111", accent: "#E0E0E0" },
    "Coca-Cola": { primary: "#F40000", accent: "#FDE0E0" },
    "Nvidia":    { primary: "#76B900", accent: "#E8F5CC" },
    "Berkshire": { primary: "#2D2D6E", accent: "#D8D8EA" },
};

let selectedPreset = "Default";

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
const previewPrimary = document.getElementById("preview-primary");
const previewAccent = document.getElementById("preview-accent");

// Debounce helper
function debounce(fn, ms) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), ms);
    };
}

// --- Color Theme ---
function renderColorPresets() {
    const container = document.getElementById("color-presets");
    let html = "";
    for (const [name, colors] of Object.entries(COLOR_PRESETS)) {
        const active = name === selectedPreset ? "active" : "";
        html += `
            <button class="color-preset ${active}" data-preset="${name}">
                <div class="color-swatch" style="background:${colors.primary}"></div>
                ${name}
            </button>
        `;
    }
    container.innerHTML = html;

    container.querySelectorAll(".color-preset").forEach((btn) => {
        btn.addEventListener("click", () => {
            selectedPreset = btn.dataset.preset;
            const colors = COLOR_PRESETS[selectedPreset];
            colorPrimary.value = colors.primary;
            colorAccent.value = colors.accent;
            updateColorPreview();
            renderColorPresets();
        });
    });
}

function updateColorPreview() {
    previewPrimary.style.background = colorPrimary.value;
    previewAccent.style.background = colorAccent.value;
}

colorPrimary.addEventListener("input", () => {
    selectedPreset = null;
    renderColorPresets();
    updateColorPreview();
});

colorAccent.addEventListener("input", () => {
    selectedPreset = null;
    renderColorPresets();
    updateColorPreview();
});

// Initialize
renderColorPresets();
updateColorPreview();

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
                searchResults.innerHTML = `<div class="dropdown-item"><span class="company-name" style="color:#f85149">${data.error}</span></div>`;
                searchResults.classList.remove("hidden");
                return;
            }

            if (data.length === 0) {
                searchResults.innerHTML = `<div class="dropdown-item"><span class="company-name" style="color:#8b949e">No results found</span></div>`;
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

    // Auto-select matching color preset if one exists
    const matchKey = Object.keys(COLOR_PRESETS).find(
        (k) => k.toLowerCase() === name.split(" ")[0].toLowerCase() ||
               k.toLowerCase() === ticker.toLowerCase()
    );
    if (matchKey) {
        selectedPreset = matchKey;
        colorPrimary.value = COLOR_PRESETS[matchKey].primary;
        colorAccent.value = COLOR_PRESETS[matchKey].accent;
        updateColorPreview();
        renderColorPresets();
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
    // Hide later steps when filing selection changes
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

    // Group tables by filing
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
    selectedPreset = "Default";
    searchInput.value = "";
    colorPrimary.value = "#4472C4";
    colorAccent.value = "#D9E1F2";
    updateColorPreview();
    renderColorPresets();
    stepFilings.classList.add("hidden");
    stepTables.classList.add("hidden");
    stepGenerate.classList.add("hidden");
    resetSection.classList.add("hidden");
    generateError.classList.add("hidden");
    scanError.classList.add("hidden");
    searchInput.focus();
});
