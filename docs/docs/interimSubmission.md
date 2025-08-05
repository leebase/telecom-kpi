# Interim Submission: Hackathon Project Entry

## 1) Project Overview

**Submission Type**  
Team

**Team Name**  
Cengage Snowflake Managed Services Vibers

**Team Members

Project Lead: Lee Harrington - jerry.harrington@cognizant.com
Arun Kumar - ArunKumar.Arivazhagan@cognizant.com 
Guru T - guru.t@cognizang.com

**Project Title**  
Telecom KPI Control Tower: Plug-and-Play Insights for Network, Customer, and Revenue Performance

---

## 2) Project Details & Innovation

**Use case for Coding**  
Telco leaders lack a trusted, near-real-time view across OSS/BSS, CRM, billing, and NOC. Decisions slow, CX degrades, and pre-sales drags because data is fragmented. We built a plug-and-play KPI control tower that boots instantly with realistic synthetic data for stakeholder demos and accepts real data later with zero structural changes. It presents the five pillars that matter most—Network, Customer, Revenue, Usage, Ops—so executives can “see the business on one page” on day 1 and connect to Snowflake on day 2.

**Solution & Benefits**  
- Five KPI pillars with bold metric cards, deltas, and trend charts  
- Realistic synthetic data for immediate demo value; no backend required  
- Declarative KPI definitions and YAML semantic layer; UI updates cascade from one place  
- Azure App Services-ready; Snowflake/API adapters by config  
Benefits:  
- Executive-ready demo in under 60 minutes  
- Reusable across telcos and portable to adjacent verticals  
- Covers ARPU, DCR, Latency, NPS, Churn, MTTR, etc.  
- Day-1 sales enablement; day-2 data integration

**Innovativeness**  
We blended human expertise with AI acceleration—without “checking our brains at the door.”  
- Team-led data and design: We applied our own knowledge and experience, KPI rigor, and product UX judgment to define what matters and how it should look.  
- AI as a multiplier, not a crutch: We used AI to research and draft KPI candidates and to generate realistic distributions—but we curated, challenged, and refined everything.  
- Declarative semantic layer (YAML): Our team designed the semantic model, formulas, and star/gold patterns; AI helped scaffold tests and boilerplate.  
- Narrative-first build: We started with the executive story and decision moments, then shaped data and visuals to serve that story.

**Our Executive Model for Prompting (original to this team)**  
Conceived and authored by Lee Harrington to drive exec-grade outputs:  
1) Hire an expert: Define the ideal agent you’d trust with P&L impact  
2) Orient deeply: Provide industry, business, and operational context  
3) Assign precisely: Scope, format, constraints, and acceptance criteria  
4) Micro-manage: Review, challenge, iterate—executive name goes on the line

**User Experience**  
- Tabbed navigation by pillar (Network, Customer, Revenue, Usage, Ops)  
- Big, color-cued metric cards with week-over-week deltas  
- Trend and distribution charts for fast pattern detection  
- Inline KPI definitions for business users and analysts  
- Streamlit-native responsive layout

---

## 3) Impact & Implementation

**Business Opportunity / Market Potential**  
- Universal telco pain: fragmented KPI visibility across systems  
- GSI/Snowflake-aligned: “day-1 demo, day-2 data” accelerates PoCs and pipelines  
- Repeatable across hundreds of telcos; adaptable to utilities, cloud, transport  
- Services pull-through: ingestion, semantic modeling, governance, FinOps, MLOps

**Ease of Implementation**  
- Python + Streamlit; single config controls data provider (synthetic/Snowflake/API)  
- No hardcoded sources; adapters pattern for clean swaps  
- Helper functions (render_metric, render_chart, render_tab) simplify changes  
- Deployable in under an hour in a clean environment

**Scalable / Reusable**  
- Modular pillars/KPIs, declarative YAML semantic layer  
- Aligns with Snowflake best practices (staging → gold, semantic KPIs)  
- Add a KPI in minutes; reuse across clients with minimal changes  
- Portable to other industries by swapping semantic/KPI YAML

**Financial Feasibility**  
- Zero-license MVP (Streamlit + Python), synthetic data (no ETL)  
- Pay-as-you-go when connecting to Snowflake  
- Low engineering lift to move from demo to PoC to production

---

## 4) Resources & Links

**SharePoint URL of Uploaded Code as Zip file**  
[Paste SharePoint link]

**SharePoint URL of Uploaded Video Recording**  
[Paste SharePoint link]

---

## 5) Azure Deployment (Non-Lovable)

**Who needs Azure DevOps access to manage code check-in?**  
Lee Harrington (jerry.harrington@cognizant.com)
Guru T (guru.t@cognizang.com)


**Who needs access to Deploy the App to Azure App Services?**  
Lee Harrington (jerry.harrington@cognizant.com)
Guru T (guru.t@cognizang.com)


---

## 6) Lovable Deployments

**Need more Lovable token credits?**  
Yes

**Select team members who need additional token credits**  
[Names or N/A]
