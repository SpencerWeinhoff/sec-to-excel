/* Value Chain Generator — Frontend JS */

let valueChains = [];
let selectedChain = null;

// DOM elements
const searchInput = document.getElementById("vc-search-input");
const dropdown = document.getElementById("vc-dropdown");
const vcGrid = document.getElementById("vc-grid");
const stepSearch = document.getElementById("step-search");
const stepScope = document.getElementById("step-scope");
const stepGenerate = document.getElementById("step-generate");
const selectedChainEl = document.getElementById("selected-chain");
const narrowDesc = document.getElementById("narrow-desc");
const generateSummary = document.getElementById("vc-generate-summary");
const btnGenerate = document.getElementById("btn-vc-generate");
const generateLoading = document.getElementById("vc-generate-loading");
const generateError = document.getElementById("vc-generate-error");
const resetSection = document.getElementById("vc-reset-section");
const btnReset = document.getElementById("btn-vc-reset");

// Load value chains on page load
async function loadValueChains() {
    try {
        const resp = await fetch("/api/value-chains");
        const data = await resp.json();
        if (data.error) throw new Error(data.error);
        valueChains = data.value_chains || [];
        renderGrid(valueChains);
    } catch (err) {
        vcGrid.innerHTML = `<p class="error">Failed to load value chains: ${err.message}</p>`;
    }
}

function renderGrid(chains) {
    vcGrid.innerHTML = "";
    chains.forEach((vc) => {
        const card = document.createElement("button");
        card.className = "industry-card";
        const broadCount = vc.broad_stages || 0;
        const narrowCount = vc.narrow_stages || 0;
        card.innerHTML = `
            <span class="industry-card-name">${vc.name}</span>
            <span class="industry-card-count">${broadCount} broad stages · ${narrowCount} narrow stages</span>
        `;
        card.addEventListener("click", () => selectChain(vc));
        vcGrid.appendChild(card);
    });
}

// Search / filter
searchInput.addEventListener("input", () => {
    const q = searchInput.value.trim().toLowerCase();
    if (q.length === 0) {
        dropdown.classList.add("hidden");
        renderGrid(valueChains);
        return;
    }

    const matches = valueChains.filter((vc) => {
        const keywords = (vc.keywords || []).join(" ").toLowerCase();
        const name = vc.name.toLowerCase();
        return name.includes(q) || keywords.includes(q);
    });

    if (matches.length === 0) {
        dropdown.innerHTML = `<div class="dropdown-item"><span class="company-name" style="color:#9ca3af">No matching industries</span></div>`;
        dropdown.classList.remove("hidden");
        renderGrid([]);
    } else {
        dropdown.classList.add("hidden");
        renderGrid(matches);
    }
});

function selectChain(vc) {
    selectedChain = vc;

    // Show selected chain info
    const narrowFocus = vc.narrow_focus || "Specific niche";
    selectedChainEl.innerHTML = `<span class="name">${vc.name}</span>`;
    narrowDesc.textContent = `Granular, ${vc.narrow_stages || "7–10"} stages — ${narrowFocus}`;

    // Reset scope to broad
    document.querySelector('input[name="scope"][value="broad"]').checked = true;

    updateGenerateSummary();

    stepScope.classList.remove("hidden");
    stepGenerate.classList.remove("hidden");
    resetSection.classList.remove("hidden");

    stepScope.scrollIntoView({ behavior: "smooth", block: "start" });
}

function getSelectedScope() {
    return document.querySelector('input[name="scope"]:checked').value;
}

function updateGenerateSummary() {
    if (!selectedChain) return;
    const scope = getSelectedScope();
    let desc = "";
    if (scope === "broad") {
        desc = `Broad value chain for ${selectedChain.name} — ${selectedChain.broad_stages || "?"} stages`;
    } else if (scope === "narrow") {
        desc = `Narrow value chain: ${selectedChain.narrow_focus || selectedChain.name} — ${selectedChain.narrow_stages || "?"} stages`;
    } else {
        desc = `Both broad (${selectedChain.broad_stages || "?"} stages) and narrow (${selectedChain.narrow_stages || "?"} stages) value chains`;
    }
    generateSummary.textContent = desc;
}

// Update summary when scope changes
document.querySelectorAll('input[name="scope"]').forEach((radio) => {
    radio.addEventListener("change", updateGenerateSummary);
});

// Generate PPT
btnGenerate.addEventListener("click", async () => {
    if (!selectedChain) return;

    generateLoading.classList.remove("hidden");
    generateError.classList.add("hidden");
    btnGenerate.disabled = true;

    try {
        const scope = getSelectedScope();
        const resp = await fetch("/api/value-chain/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                chain_id: selectedChain.id,
                scope: scope,
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
            : `${selectedChain.name.replace(/[^a-zA-Z0-9]/g, "_")}_Value_Chain.pptx`;
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
    selectedChain = null;
    searchInput.value = "";
    dropdown.classList.add("hidden");
    stepScope.classList.add("hidden");
    stepGenerate.classList.add("hidden");
    resetSection.classList.add("hidden");
    generateError.classList.add("hidden");
    renderGrid(valueChains);
    stepSearch.scrollIntoView({ behavior: "smooth" });
});

// Init
loadValueChains();
