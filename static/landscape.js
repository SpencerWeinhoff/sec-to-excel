/* Industry Landscape Tool — Frontend JS */

let industries = [];
let selectedIndustry = null;
let selectedSubIds = new Set();

// DOM elements
const industryGrid = document.getElementById("industry-grid");
const stepIndustry = document.getElementById("step-industry");
const stepSubs = document.getElementById("step-subs");
const stepGenerate = document.getElementById("step-generate");
const selectedIndustryEl = document.getElementById("selected-industry");
const subsList = document.getElementById("subs-list");
const btnSelectAllSubs = document.getElementById("btn-select-all-subs");
const btnSelectNoSubs = document.getElementById("btn-select-no-subs");
const btnGenerate = document.getElementById("btn-generate");
const generateLoading = document.getElementById("generate-loading");
const generateError = document.getElementById("generate-error");
const generateSummary = document.getElementById("generate-summary");
const resetSection = document.getElementById("reset-section");
const btnReset = document.getElementById("btn-reset");

// Load industries on page load
async function loadIndustries() {
    try {
        const resp = await fetch("/api/industries");
        const data = await resp.json();
        if (data.error) throw new Error(data.error);
        industries = data.industries || [];
        renderIndustryGrid();
    } catch (err) {
        industryGrid.innerHTML = `<p class="error">Failed to load industries: ${err.message}</p>`;
    }
}

function renderIndustryGrid() {
    industryGrid.innerHTML = "";
    industries.forEach((ind) => {
        const card = document.createElement("button");
        card.className = "industry-card";
        card.innerHTML = `
            <span class="industry-card-name">${ind.name}</span>
            <span class="industry-card-count">${ind.sub_industries.length} verticals · ${ind.company_count} companies</span>
        `;
        card.addEventListener("click", () => selectIndustry(ind));
        industryGrid.appendChild(card);
    });
}

function selectIndustry(ind) {
    selectedIndustry = ind;

    // Show selected industry
    selectedIndustryEl.innerHTML = `<strong>${ind.name}</strong> — ${ind.sub_industries.length} sub-industries`;

    // Select all sub-industries by default
    selectedSubIds.clear();
    ind.sub_industries.forEach((s) => selectedSubIds.add(s.id));

    renderSubIndustries();
    updateGenerateStep();

    stepSubs.classList.remove("hidden");
    stepGenerate.classList.remove("hidden");
    resetSection.classList.remove("hidden");

    stepSubs.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderSubIndustries() {
    subsList.innerHTML = "";
    if (!selectedIndustry) return;

    selectedIndustry.sub_industries.forEach((sub) => {
        const item = document.createElement("label");
        item.className = "filing-item";

        const cb = document.createElement("input");
        cb.type = "checkbox";
        cb.checked = selectedSubIds.has(sub.id);
        cb.dataset.subId = sub.id;
        cb.addEventListener("change", () => {
            if (cb.checked) {
                selectedSubIds.add(sub.id);
            } else {
                selectedSubIds.delete(sub.id);
            }
            updateGenerateStep();
        });

        const text = document.createElement("span");
        text.innerHTML = `${sub.name} <span style="color:#9ca3af;font-size:12px;">(${sub.companies.length} companies)</span>`;

        item.appendChild(cb);
        item.appendChild(text);
        subsList.appendChild(item);
    });
}

function updateGenerateStep() {
    const totalCompanies = selectedIndustry.sub_industries
        .filter((s) => selectedSubIds.has(s.id))
        .reduce((sum, s) => sum + s.companies.length, 0);

    generateSummary.textContent = `${selectedSubIds.size} sub-industries selected · ${totalCompanies} companies will be included`;
    btnGenerate.disabled = selectedSubIds.size === 0;
}

// Select all / clear all
btnSelectAllSubs.addEventListener("click", () => {
    if (!selectedIndustry) return;
    selectedIndustry.sub_industries.forEach((s) => selectedSubIds.add(s.id));
    renderSubIndustries();
    updateGenerateStep();
});

btnSelectNoSubs.addEventListener("click", () => {
    selectedSubIds.clear();
    renderSubIndustries();
    updateGenerateStep();
});

// Generate PPT
btnGenerate.addEventListener("click", async () => {
    if (!selectedIndustry || selectedSubIds.size === 0) return;

    generateLoading.classList.remove("hidden");
    generateError.classList.add("hidden");
    btnGenerate.disabled = true;

    try {
        const resp = await fetch("/api/landscape/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                industry_id: selectedIndustry.id,
                sub_industry_ids: Array.from(selectedSubIds),
            }),
        });

        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(err.error || "Generation failed");
        }

        // Download the file
        const blob = await resp.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = resp.headers.get("content-disposition")
            ? resp.headers.get("content-disposition").split("filename=")[1].replace(/"/g, "")
            : `${selectedIndustry.name.replace(/[^a-zA-Z0-9]/g, "_")}_Landscape.pptx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (err) {
        generateError.textContent = err.message;
        generateError.classList.remove("hidden");
    } finally {
        generateLoading.classList.add("hidden");
        btnGenerate.disabled = false;
    }
});

// Reset
btnReset.addEventListener("click", () => {
    selectedIndustry = null;
    selectedSubIds.clear();
    stepSubs.classList.add("hidden");
    stepGenerate.classList.add("hidden");
    resetSection.classList.add("hidden");
    generateError.classList.add("hidden");
    stepIndustry.scrollIntoView({ behavior: "smooth" });
});

// Init
loadIndustries();
