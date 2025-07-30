# 📡 Telecom KPI Dashboard MVP

A **plug-and-play KPI dashboard** for telecom operators showcasing key metrics across five strategic pillars: Network, Customer, Revenue, Usage, and Operations. Built with Streamlit and designed for executive presentations and hackathon demos.

## 🎯 Features

### 📊 **5 Strategic KPI Pillars**
- **📡 Network Performance** - Uptime, latency, bandwidth, dropped calls, packet loss, MTTR
- **😊 Customer Experience** - CSAT, NPS, churn rate, handling time, first contact resolution
- **💰 Revenue & Monetization** - ARPU, CLV, CAC, subscriber growth, EBITDA margin
- **📶 Usage & Adoption** - Data usage, throughput, feature adoption, 5G adoption
- **🛠️ Operational Efficiency** - Response time, compliance, capex ratio

### 🎨 **Professional UI Components**
- **Metric Cards** with big numbers and trend deltas (▲ 3.2%)
- **Interactive Charts** (line, bar, area, histogram) using Altair
- **ℹ️ Popup tooltips** for quick KPI definitions on hover
- **📋 Info icons** for detailed explanations and live documentation
- **📘 Expandable sections** with definitions, formulae, and business impact

### 🛠️ **Technical Features**
- **Synthetic but realistic data** for immediate visual impact
- **Modular component architecture** for easy customization
- **Snowflake-ready schema** for future integration
- **Responsive design** optimized for executive presentations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone or download the project**
```bash
# If you have the files locally, navigate to the project directory
cd telecomdashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the dashboard**
```bash
streamlit run app.py
```

4. **Open your browser**
Navigate to `http://localhost:8501`

## 📁 Project Structure

```
telecomdashboard/
├── app.py                      # Main Streamlit application
├── kpi_components.py          # Reusable KPI render functions
├── generate_test_data.py      # Synthetic data generator
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🎛️ Dashboard Navigation

### **Tab 1: Network Performance**
- Network Availability: 99.87% (▲ 0.12%)
- Latency: 45.2 ms (▼ 2.1 ms)
- Bandwidth Utilization: 78.3% (▲ 3.2%)
- Dropped Call Rate: 1.2% (▼ 0.3%)
- Packet Loss Rate: 0.08% (▼ 0.02%)
- MTTR: 2.3 hours (▼ 0.5 hours)

### **Tab 2: Customer Experience**
- Customer Satisfaction: 4.2/5.0 (▲ 0.3)
- Net Promoter Score: 42 (▲ 5)
- Customer Churn Rate: 2.1% (▼ 0.4%)
- Average Handling Time: 4.2 min (▼ 0.8 min)
- First Contact Resolution: 78% (▲ 3%)
- Customer Lifetime Value: $1,247 (▲ $89)

### **Tab 3: Revenue & Monetization**
- Average Revenue Per User: $42.17 (▲ $3.25)
- Customer Lifetime Value: $1,247 (▲ $89)
- Customer Acquisition Cost: $156 (▼ $12)
- Subscriber Growth Rate: 8.3% (▲ 1.2%)
- EBITDA Margin: 32.4% (▲ 2.1%)
- Monthly Recurring Revenue: $2.4M (▲ $180K)

### **Tab 4: Usage & Adoption**
- Data Usage per Subscriber: 8.7 GB (▲ 1.2 GB)
- Average Data Throughput: 45.2 Mbps (▲ 3.8 Mbps)
- Feature Adoption Rate: 67% (▲ 8%)
- 5G Adoption Rate: 34% (▲ 12%)
- Active Subscribers: 1.2M (▲ 45K)
- Peak Usage Time: 8-10 PM (Stable)

### **Tab 5: Operational Efficiency**
- Service Response Time: 2.1 hours (▼ 0.5 hours)
- Regulatory Compliance Rate: 98.7% (▲ 0.3%)
- Capex to Revenue Ratio: 18.2% (▼ 1.1%)
- Network Efficiency Score: 87.3 (▲ 2.1)
- Support Ticket Resolution: 94.2% (▲ 1.8%)
- System Uptime: 99.92% (▲ 0.05%)

## 🔧 Customization

### **Adding New KPIs**
1. Add the KPI to the appropriate tab in `app.py`
2. Create corresponding data in `generate_test_data.py`
3. Add tooltip content in `kpi_components.py`

### **Modifying Data**
Edit the functions in `generate_test_data.py` to change:
- Data trends and patterns
- Regional variations
- Time series characteristics

### **Styling Changes**
Modify the CSS in `app.py` to customize:
- Color schemes
- Layout spacing
- Typography

## 🎯 Target Users

- **Telecom executives** (CEO, CTO, COO)
- **Business analysts** and finance leads
- **Network operations managers**
- **Hackathon judges** and product reviewers

## 🚀 Deployment Options

### **Local Development**
```bash
streamlit run app.py
```

### **Streamlit Cloud**
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

## 🔮 Future Enhancements

- **Real-time data integration** with Snowflake
- **Advanced filtering** by region, time period, customer segment
- **Export functionality** for reports and presentations
- **Alert system** for KPI thresholds
- **Mobile-responsive** design improvements

## 📊 Data Schema (Snowflake-Ready)

The dashboard is designed to work with these data tables:
- `customers` - Customer demographics and behavior
- `subscriptions` - Plan details and usage
- `calls` - Call quality and network performance
- `support_tickets` - Customer service metrics
- `network_events` - Infrastructure monitoring
- `revenue_snapshots` - Financial performance data

## 🤝 Contributing

This is a hackathon MVP designed for rapid prototyping. For production use:
1. Replace synthetic data with real data sources
2. Add proper error handling and validation
3. Implement user authentication and access controls
4. Add comprehensive testing

## 📄 License

This project is designed for educational and demonstration purposes.

---

**Built with ❤️ for telecom executives and hackathon judges** 