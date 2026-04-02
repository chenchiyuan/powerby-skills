from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_web_result_view_assets_exist_and_define_render_contract() -> None:
    html_text = (REPO_ROOT / "web/acceptance-map/index.html").read_text(encoding="utf-8")
    js_text = (REPO_ROOT / "web/acceptance-map/app.js").read_text(encoding="utf-8")

    assert "acceptance-map-app" in html_text
    assert "result-file-input" in html_text
    assert "renderHeatmap" in js_text
    assert "renderRegions" in js_text
    assert "HEATMAP_DATA_MISSING" in js_text
    assert "RESULT_SCHEMA_INVALID" in js_text


def test_web_result_view_runtime_smoke(tmp_path: Path) -> None:
    script_path = tmp_path / "web-smoke.mjs"
    module_url = (REPO_ROOT / "web/acceptance-map/app.js").resolve().as_uri()
    script_path.write_text(
        f"""
import assert from "node:assert/strict";

class FakeClassList {{
  constructor() {{
    this.names = new Set();
  }}

  add(name) {{
    this.names.add(name);
  }}

  contains(name) {{
    return this.names.has(name);
  }}
}}

class FakeElement {{
  constructor(id = "") {{
    this.id = id;
    this.children = [];
    this.textContent = "";
    this._innerHTML = "";
    this.className = "";
    this.dataset = {{}};
    this.style = {{}};
    this.listeners = {{}};
    this.classList = new FakeClassList();
  }}

  set innerHTML(value) {{
    this._innerHTML = value;
    this.children = [];
  }}

  get innerHTML() {{
    return this._innerHTML;
  }}

  appendChild(child) {{
    this.children.push(child);
    return child;
  }}

  append(...children) {{
    this.children.push(...children);
  }}

  addEventListener(eventName, handler) {{
    this.listeners[eventName] = handler;
  }}
}}

const elements = new Map();
function ensureElement(id) {{
  if (!elements.has(id)) {{
    elements.set(id, new FakeElement(id));
  }}
  return elements.get(id);
}}

globalThis.document = {{
  getElementById(id) {{
    return ensureElement(id);
  }},
  createElement(tagName) {{
    return new FakeElement(tagName);
  }},
}};

const module = await import("{module_url}");
const status = ensureElement("status-message");
const heatmap = ensureElement("heatmap-section");
const regions = ensureElement("regions-section");

const fullResult = {{
  params: {{ include_heatmap: true }},
  regions: [
    {{
      region_id: "R-001",
      lower_bound: 100,
      upper_bound: 105,
      price_acceptance_probability: 0.6,
      coverage_count: 2,
      weighted_volume_contribution: 12.5,
    }},
    {{
      region_id: "R-002",
      lower_bound: 105,
      upper_bound: 110,
      price_acceptance_probability: 0.4,
      coverage_count: 1,
      weighted_volume_contribution: 8.5,
    }},
  ],
  heatmap: [
    {{
      index: 0,
      lower_bound: 100,
      upper_bound: 101,
      center_price: 100.5,
      price_acceptance_probability: 0,
      coverage_count: 1,
      weighted_volume_contribution: 4,
    }},
  ],
}};

module.renderHeatmap(fullResult);
assert.equal(heatmap.children.length, 1);
assert.equal(status.textContent, "结果已渲染");
assert.equal(
  heatmap.children[0].children[1].children[0].style.width,
  "0%",
);

module.renderRegions(fullResult);
assert.equal(regions.children.length, 2);
regions.children[0].listeners.click();
module.renderRegions(fullResult);
assert.equal(regions.children[0].classList.contains("is-active"), true);

const reducedResult = {{
  params: {{ include_heatmap: true }},
  regions: [
    {{
      region_id: "R-002",
      lower_bound: 105,
      upper_bound: 110,
      price_acceptance_probability: 1,
      coverage_count: 1,
      weighted_volume_contribution: 8.5,
    }},
  ],
  heatmap: [
    {{
      index: 0,
      lower_bound: 105,
      upper_bound: 106,
      center_price: 105.5,
      price_acceptance_probability: 1,
      coverage_count: 1,
      weighted_volume_contribution: 8.5,
    }},
  ],
}};

module.renderRegions(reducedResult);
assert.equal(status.textContent, "选择的区域不存在");

module.renderHeatmap({{
  params: {{ include_heatmap: false }},
  regions: fullResult.regions,
}});
assert.equal(heatmap.children.length, 1);
assert.equal(
  heatmap.children[0].textContent,
  "当前结果已关闭 heatmap，仅展示区域列表。",
);
""".strip(),
        encoding="utf-8",
    )

    subprocess.run(["node", str(script_path)], check=True, cwd=REPO_ROOT)


def test_web_result_view_rejects_partial_diagnostics_payload(tmp_path: Path) -> None:
    script_path = tmp_path / "web-invalid-diagnostics.mjs"
    module_url = (REPO_ROOT / "web/acceptance-map/app.js").resolve().as_uri()
    script_path.write_text(
        f"""
import assert from "node:assert/strict";

class FakeClassList {{
  add() {{}}
  contains() {{
    return false;
  }}
}}

class FakeElement {{
  constructor(id = "") {{
    this.id = id;
    this.children = [];
    this.textContent = "";
    this.value = "";
    this._innerHTML = "";
    this.className = "";
    this.dataset = {{}};
    this.style = {{}};
    this.listeners = {{}};
    this.classList = new FakeClassList();
  }}

  set innerHTML(value) {{
    this._innerHTML = value;
    this.children = [];
  }}

  get innerHTML() {{
    return this._innerHTML;
  }}

  appendChild(child) {{
    this.children.push(child);
    return child;
  }}

  append(...children) {{
    this.children.push(...children);
  }}

  addEventListener(eventName, handler) {{
    this.listeners[eventName] = handler;
  }}
}}

const elements = new Map();
function ensureElement(id) {{
  if (!elements.has(id)) {{
    elements.set(id, new FakeElement(id));
  }}
  return elements.get(id);
}}

globalThis.document = {{
  getElementById(id) {{
    return ensureElement(id);
  }},
  createElement(tagName) {{
    return new FakeElement(tagName);
  }},
}};

await import("{module_url}");

const status = ensureElement("status-message");
const jsonInput = ensureElement("result-json-input");
const renderButton = ensureElement("render-result-button");

jsonInput.value = JSON.stringify({{
  params: {{ include_heatmap: true }},
  regions: [
    {{
      region_id: "R-001",
      lower_bound: 100,
      upper_bound: 105,
      price_acceptance_probability: 1,
      coverage_count: 2,
    }},
  ],
  heatmap: [
    {{
      index: 0,
      lower_bound: 100,
      upper_bound: 101,
      center_price: 100.5,
      price_acceptance_probability: 1,
      coverage_count: 1,
    }},
  ],
}});

renderButton.listeners.click();
assert.equal(status.textContent, "分析结果结构非法，无法渲染");
""".strip(),
        encoding="utf-8",
    )

    subprocess.run(["node", str(script_path)], check=True, cwd=REPO_ROOT)
