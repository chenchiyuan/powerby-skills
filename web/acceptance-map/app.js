const ERROR_MESSAGES = {
  RESULT_SCHEMA_INVALID: "分析结果结构非法，无法渲染",
  HEATMAP_DATA_MISSING: "缺少热力图数据，已降级为仅展示区域列表",
  REGION_NOT_FOUND: "选择的区域不存在",
};

const appState = {
  result: null,
  selectedRegionId: null,
};

const elements = {
  fileInput: document.getElementById("result-file-input"),
  jsonInput: document.getElementById("result-json-input"),
  renderButton: document.getElementById("render-result-button"),
  status: document.getElementById("status-message"),
  summary: document.getElementById("input-summary"),
  heatmap: document.getElementById("heatmap-section"),
  regions: document.getElementById("regions-section"),
};

function setStatus(code, detail = "") {
  if (!code) {
    elements.status.textContent = detail;
    return;
  }
  const prefix = ERROR_MESSAGES[code] || code;
  elements.status.textContent = detail ? `${prefix}: ${detail}` : prefix;
}

function assertResultShape(result) {
  const supportedViewMode = "heatmap+regions";
  const isFiniteNumber = (value) => Number.isFinite(Number(value));
  const hasIncreasingBounds = (entry) =>
    Number(entry.lower_bound) < Number(entry.upper_bound);
  const isProbability = (value) => {
    const parsed = Number(value);
    return Number.isFinite(parsed) && parsed >= 0 && parsed <= 1;
  };
  const hasDiagnostics = (entry) =>
    entry.coverage_count != null || entry.weighted_volume_contribution != null;
  const hasCompleteDiagnostics = (entry) =>
    entry.coverage_count != null && entry.weighted_volume_contribution != null;
  const hasValidDiagnostics = (entry) =>
    hasCompleteDiagnostics(entry) &&
    Number.isInteger(entry.coverage_count) &&
    entry.coverage_count >= 0 &&
    isFiniteNumber(entry.weighted_volume_contribution);

  if (!result || typeof result !== "object") {
    throw new Error("RESULT_SCHEMA_INVALID");
  }
  if (!Array.isArray(result.regions)) {
    throw new Error("RESULT_SCHEMA_INVALID");
  }
  if (
    result.selected_region_id != null &&
    typeof result.selected_region_id !== "string"
  ) {
    throw new Error("RESULT_SCHEMA_INVALID");
  }
  if (
    result.view_mode != null &&
    result.view_mode !== supportedViewMode
  ) {
    throw new Error("RESULT_SCHEMA_INVALID");
  }
  if (result.regions.length === 0) {
    throw new Error("RESULT_SCHEMA_INVALID");
  }
  const regionsAreValid = result.regions.every((region) => {
    if (!region || typeof region !== "object") {
      return false;
    }
    return (
      typeof region.region_id === "string" &&
      isFiniteNumber(region.lower_bound) &&
      isFiniteNumber(region.upper_bound) &&
      hasIncreasingBounds(region) &&
      isProbability(region.price_acceptance_probability) &&
      (!hasDiagnostics(region) || hasValidDiagnostics(region))
    );
  });
  if (!regionsAreValid) {
    throw new Error("RESULT_SCHEMA_INVALID");
  }
  if (result.heatmap != null && !Array.isArray(result.heatmap)) {
    throw new Error("RESULT_SCHEMA_INVALID");
  }
  if (Array.isArray(result.heatmap)) {
    const heatmapIsValid = result.heatmap.every((entry) => {
      if (!entry || typeof entry !== "object") {
        return false;
      }
      return (
        isFiniteNumber(entry.lower_bound) &&
        isFiniteNumber(entry.upper_bound) &&
        hasIncreasingBounds(entry) &&
        isProbability(entry.price_acceptance_probability) &&
        (!hasDiagnostics(entry) || hasValidDiagnostics(entry))
      );
    });
    if (!heatmapIsValid) {
      throw new Error("RESULT_SCHEMA_INVALID");
    }
  }
}

function escapeText(value) {
  return String(value ?? "");
}

function renderSummary(result) {
  elements.summary.innerHTML = "";
  const summary = result.input_summary || {};
  const params = result.params || {};
  const chips = [
    `交易对: ${escapeText(summary.symbol || "-")}`,
    `周期: ${escapeText(summary.timeframe || "-")}`,
    `样本: ${escapeText(summary.sample_size || "-")}`,
    `区域模式: ${escapeText(params.partition_mode || "-")}`,
  ];

  chips.forEach((text) => {
    const node = document.createElement("div");
    node.className = "chip";
    node.textContent = text;
    elements.summary.appendChild(node);
  });
}

export function renderHeatmap(result) {
  elements.heatmap.innerHTML = "";
  const heatmapEnabled = result.params?.include_heatmap !== false;
  if (!Array.isArray(result.heatmap)) {
    if (heatmapEnabled) {
      setStatus("HEATMAP_DATA_MISSING");
    } else {
      setStatus(null, "结果已渲染");
    }
    const node = document.createElement("div");
    node.className = "chip";
    node.textContent = heatmapEnabled
      ? "当前结果未提供 heatmap，页面已降级为仅展示区域列表。"
      : "当前结果已关闭 heatmap，仅展示区域列表。";
    elements.heatmap.appendChild(node);
    return;
  }

  setStatus(null, "结果已渲染");
  result.heatmap.forEach((entry) => {
    const row = document.createElement("div");
    row.className = "heatmap-row";

    const range = document.createElement("div");
    range.textContent = `${Number(entry.lower_bound).toFixed(2)} - ${Number(entry.upper_bound).toFixed(2)}`;

    const bar = document.createElement("div");
    bar.className = "heatmap-bar";
    const fill = document.createElement("div");
    fill.className = "heatmap-fill";
    fill.style.width = `${Math.max(0, Number(entry.price_acceptance_probability) * 100)}%`;
    bar.appendChild(fill);

    const probability = document.createElement("div");
    probability.textContent = `${(Number(entry.price_acceptance_probability) * 100).toFixed(2)}%`;

    row.append(range, bar, probability);
    elements.heatmap.appendChild(row);
  });
}

function renderSelectedRegion(result) {
  if (!appState.selectedRegionId) {
    return;
  }

  const exists = result.regions.some((region) => region.region_id === appState.selectedRegionId);
  if (!exists) {
    setStatus("REGION_NOT_FOUND");
    appState.selectedRegionId = null;
  }
}

export function renderRegions(result) {
  elements.regions.innerHTML = "";
  renderSelectedRegion(result);

  result.regions.forEach((region) => {
    const card = document.createElement("article");
    card.className = "region-card";
    if (region.region_id === appState.selectedRegionId) {
      card.classList.add("is-active");
    }
    card.dataset.regionId = region.region_id;

    const title = document.createElement("strong");
    title.textContent = `${region.region_id} | ${(Number(region.price_acceptance_probability) * 100).toFixed(2)}%`;
    const range = document.createElement("div");
    range.textContent = `${Number(region.lower_bound).toFixed(2)} - ${Number(region.upper_bound).toFixed(2)}`;
    card.append(title, range);

    if (
      region.coverage_count != null &&
      region.weighted_volume_contribution != null
    ) {
      const diagnostics = document.createElement("div");
      diagnostics.textContent = `coverage=${region.coverage_count} | weighted_volume=${Number(region.weighted_volume_contribution).toFixed(2)}`;
      card.appendChild(diagnostics);
    }

    card.addEventListener("click", () => {
      appState.selectedRegionId = region.region_id;
      renderRegions(result);
    });
    elements.regions.appendChild(card);
  });
}

function renderResult(result) {
  assertResultShape(result);
  appState.result = result;
  appState.selectedRegionId =
    typeof result.selected_region_id === "string"
      ? result.selected_region_id
      : null;
  renderSummary(result);
  renderHeatmap(result);
  renderRegions(result);
}

function parseInputValue() {
  const raw = elements.jsonInput.value.trim();
  if (!raw) {
    throw new Error("RESULT_SCHEMA_INVALID");
  }
  return JSON.parse(raw);
}

function bindFileInput() {
  elements.fileInput.addEventListener("change", async (event) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }
    try {
      const text = await file.text();
      elements.jsonInput.value = text;
    } catch (_error) {
      setStatus("RESULT_SCHEMA_INVALID");
    }
  });
}

function bindRenderButton() {
  elements.renderButton.addEventListener("click", () => {
    try {
      const result = parseInputValue();
      renderResult(result);
    } catch (error) {
      const code =
        error instanceof SyntaxError
          ? "RESULT_SCHEMA_INVALID"
          : ERROR_MESSAGES[error?.message]
            ? error.message
            : "RESULT_SCHEMA_INVALID";
      setStatus(code);
    }
  });
}

bindFileInput();
bindRenderButton();
