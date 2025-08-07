# Insight KPI Evaluator – Requirements Document

## Overview

The Insight KPI Evaluator is a reusable AI-powered module that analyzes KPI values and trends to generate executive-grade business insights. It adds a narrative layer to traditional dashboards, translating numbers into decisions and providing industry, peer, and historical benchmarking.

This feature aims to answer the question:  
**“What does this mean, and what should we do about it?”**

---

## Goals

- Provide clear, actionable insight summaries for each subject area tab (e.g., Network, Customer, Revenue, etc.)
- Detect and highlight:
  - Outliers and anomalies
  - Negative or concerning trends
  - Areas of overperformance or hidden opportunity
- Compare KPIs to:
  - Previous period
  - Peer benchmarks
  - Industry standards
- Present TL;DR narrative at top of each tab and optionally export full insights as report

---

## User Stories

### Executive View
> “As a VP of Operations, I want to immediately understand what’s going wrong or improving across my KPIs without reading every chart.”

### Analyst View
> “As a data analyst, I want an AI assistant that flags unexpected trends or correlations across metrics so I can investigate further.”

### Consultant / Pre-sales View
> “As a sales engineer, I want to preload mock data and have the evaluator generate realistic insights that support a business case.”

---

## Key Features

- ✅ **Insight Generator Engine**
  - Accepts: `kpi_name`, `current_value`, `prior_value`, `industry_avg`, `peer_avg`, `thresholds`
  - Returns: Natural-language evaluation summary (1–3 bullet insights)

- ✅ **Tab Summary Panel**
  - UI element at top of each subject area tab
  - Summarizes overall state of key metrics (“Network Health: Trending Negative due to Latency Spike”)

- ✅ **Drilldown Narrative**
  - Optional expansion with specific KPI insights (churn up 3% vs last month, NPS flat but still below industry)

- ✅ **Industry Benchmarks Engine**
  - Uses mock/real data tables for industry averages by KPI
  - Can be swapped or extended via YAML or Snowflake adapter

- ✅ **Portable & Reusable**
  - `insight_engine.py` callable from any Streamlit tab or external app
  - Decoupled from visual layout — can be integrated into other dashboards, reports, chatbots

---

## Technical Design Notes

- ⚙️ **Input Format**
  - Dict or dataframe per subject area with columns:
    ```
    kpi_name | current_value | prior_value | peer_avg | industry_avg | threshold_low | threshold_high
    ```

- 🧠 **Processing Logic**
  - Identify: % change from prior period
  - Compare: vs peer and industry
  - Classify: Performance = Good / At Risk / Needs Attention
  - Generate: Insight string using structured prompt templates

- 🖼️ **Output Options**
  - Streamlit `st.markdown` panel
  - JSON API for external use
  - PDF/Email export (future)

---

## Phase 1 MVP (Hackathon Deliverable)

- [ ] Insight Engine supporting basic change + benchmark deltas
- [ ] Hardcoded mock benchmark data
- [ ] Narrative summary at top of 2 subject area tabs
- [ ] YAML or dataframe-based KPI config
- [ ] Reusable insight generator function with clean interface

---

## Phase 2 (Post-hackathon Expansion)

- [ ] Benchmark ingestion from Snowflake or external API
- [ ] Severity classification (Green / Yellow / Red)
- [ ] Executive summary report generator (PDF, Markdown, HTML)
- [ ] Multilingual support for global clients
- [ ] Chatbot integration (ask follow-up questions on KPI drivers)

---

## Notes

- Designed to complement the modular `render_kpi()` and `render_tab()` structure
- Built to align with the “Executive Model for Prompting” and demonstrate AI value beyond code generation
- Could be packaged as a standalone module or internal SDK component for other accelerators

---