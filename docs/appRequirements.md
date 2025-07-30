# 📄 App Requirements: Telecom KPI Dashboard MVP

## 🎯 Purpose

This MVP provides a **plug-and-play KPI dashboard** for telecom operators, showcasing key metrics across five strategic pillars: Network, Customer, Revenue, Usage, and Operations. It uses **synthetic but realistic data** to simulate the visual impact of a real dashboard and is designed to support future integration with Snowflake or other data sources.

## 🧑‍💼 Target Users

- Telecom executives (CEO, CTO, COO)
- Business analysts and finance leads
- Network operations managers
- Hackathon judges and product reviewers

## 🛠️ Core Functionality

### ✅ High-Level Layout

- **Top Tabs** for each KPI pillar:
  - 📡 Network Performance
  - 😊 Customer Experience
  - 💰 Revenue & Monetization
  - 📶 Usage & Adoption
  - 🛠️ Operational Efficiency

- Each tab contains:
  - 📊 **Metric Cards** (big numbers with trend deltas)
  - 📈 **Charts** (line, bar, area, or distribution depending on metric)
  - 📘 **Expanders** with definitions, formulae, and explanations
  - ℹ️ **Popup tooltips** for quick KPI definitions on hover
  - 📋 **Info icons** for detailed explanations and live documentation

### ✅ Visual Goals

- Realistic-looking data
- Attractive, professional layout
- Executable without any backend data source
- Easy to swap in real data later

### ✅ Developer Goals

- Each KPI display is powered by a **reusable component function**
- Chart styling, metric formatting, and data simulation logic are modular
- Layout code is lightweight — logic lives in helper modules
- **Live documentation** via tooltips and info icons for immediate user guidance

---

## 🧪 Example KPI Render Types

| Type | Function | Example |
|------|----------|---------|
| Metric Card | `render_metric(label, value, delta)` | ARPU = $42.17 (▲ 3.2%) |
| Line Chart | `render_line_chart(df, title)` | Latency trend (ms over 30 days) |
| Bar Chart | `render_bar_chart(df, title)` | Churn by region |
| Area Chart | `render_area_chart(df, title)` | Subscriber growth |
| Histogram | `render_distribution(df, title)` | Data usage per subscriber |
| Expander | `render_kpi_expander(name, definition, chart_fn)` | DCR with explanation + chart |
| Tooltip | `render_kpi_tooltip(label, definition)` | Quick hover definitions |
| Info Icon | `render_info_icon(kpi_name, detailed_help)` | Clickable help popups |

---

## 🔜 Next Steps

- Implement layout using `Streamlit` with synthetic data
- Use helper functions to simulate KPIs for visual realism
- Prepare Snowflake-ready schema for later drop-in