# 📊 Final Curated KPI Set for Plug-and-Play Telecom Dashboard

**Purpose**: This KPI set is designed for rapid MVP development in a vibe coding hackathon. Each metric is selected for clarity, business value, and relevance across mobile, broadband, ISP, and carrier networks. The dashboard is mock-data ready but structured to accommodate real Snowflake-based pipelines in the future.

---

## 🛰️ 1. Network Performance & Reliability

| KPI | Definition | Why It Matters |
|------|------------|----------------|
| **Network Availability (Uptime)** | Percentage of time the network is operational | Core reliability metric; ensures SLA compliance |
| **Latency** | Average round-trip time for data packets (ms) | Critical for real-time apps (VoIP, gaming, etc.) |
| **Bandwidth Utilization** | Percentage of total network capacity being used | Indicates congestion risk and capacity needs |
| **Dropped Call Rate (DCR)** | Percentage of calls terminated unexpectedly | Measures call stability; key voice QoS metric |
| **Packet Loss Rate** | Percentage of packets lost in transmission | Impacts streaming, calls, and network integrity |
| **Mean Time to Repair (MTTR)** | Average time to resolve network outages | Reflects operational responsiveness |

---

## 🤝 2. Customer Experience & Retention

| KPI | Definition | Why It Matters |
|------|------------|----------------|
| **Customer Satisfaction (CSAT)** | Post-interaction score (usually 1–5 scale) | Measures short-term service experience quality |
| **Net Promoter Score (NPS)** | % Promoters − % Detractors (from 0–10 scale) | Tracks loyalty and referral potential |
| **Customer Churn Rate** | % of customers who cancel service | Indicates dissatisfaction and financial risk |
| **Average Handling Time (AHT)** | Average duration of customer support interactions | Key efficiency metric for support teams |
| **First Contact Resolution (FCR)** | % of issues resolved in one interaction | Ties to lower costs and higher satisfaction |

---

## 💸 3. Revenue & Monetization

| KPI | Definition | Why It Matters |
|------|------------|----------------|
| **Average Revenue Per User (ARPU)** | Average monthly revenue per subscriber | Core monetization KPI |
| **Customer Lifetime Value (CLV)** | Total expected profit per user over time | Guides acquisition and retention spend |
| **Customer Acquisition Cost (CAC)** | Average cost to acquire a new customer | Measures marketing and sales efficiency |
| **Subscriber Growth Rate** | Net % increase in subscriber base | Reflects market momentum |
| **EBITDA Margin** | Profitability before non-cash expenses | Financial health metric watched by investors |

---

## 📶 4. Usage & Service Adoption

| KPI | Definition | Why It Matters |
|------|------------|----------------|
| **Data Usage per Subscriber** | Average GB/month per user | Helps with pricing, planning, and segmenting |
| **Average Data Throughput** | Average data speed (Mbps) | Directly affects user experience and NPS |
| **Feature Adoption Rate** | % of users adopting new features | Signals product innovation success |
| **5G Adoption Rate** | % of subscribers using 5G services | Tracks modernization and premium plan uptake |

---

## 🧱 5. Operational Efficiency

| KPI | Definition | Why It Matters |
|------|------------|----------------|
| **Service Response Time** | Time from issue reported to first action taken | Drives customer satisfaction and NPS |
| **Regulatory Compliance Rate** | % of audits or checks passed successfully | Avoids fines and reputational damage |
| **Capex to Revenue Ratio** | % of revenue reinvested in infrastructure | Shows commitment to network quality/growth |

---

## 🧪 Developer Notes

- Each KPI maps to mockable synthetic data models
- Suggested mock data tables:
  - `customers`
  - `subscriptions`
  - `calls`
  - `support_tickets`
  - `network_events`
  - `revenue_snapshots`
- Use Python scripts or Snowflake CTEs to generate realistic fake data
- KPI groups can be shown in Streamlit using **tabs**, **accordions**, or **metric cards**

---

## 📎 Next Steps

- [ ] Generate `appRequirements.md` using this KPI set  
- [ ] Generate `appArchitecture.md` for Streamlit + Snowflake backend  
- [ ] Build mock data pipeline (`generate_test_data.py`)  
- [ ] Start Vibe Coding MVP 🎛️