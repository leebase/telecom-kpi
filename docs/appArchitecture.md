# 🏗️ App Architecture: Telecom KPI Dashboard MVP

## 🧱 Stack Overview

- **Frontend**: Streamlit (Python)
- **Backend (Mock)**: Python test data generators (`generate_test_data.py`)
- **Charting**: Streamlit native + Altair (optional)
- **Deployment**: Local Streamlit or Streamlit Cloud

---

## 📁 Project Structure

```bash
vibe-telecom-dashboard/
│
├── app.py                      # Main Streamlit app
├── generate_test_data.py      # Data generator for mock values
├── kpi_components.py          # Modular render functions for each KPI/chart type
├── data/                      # (Optional) CSVs for mock data
├── README.md
└── requirements.txt