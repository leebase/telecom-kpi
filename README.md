# 📊 Telecom KPI Dashboard

A **plug-and-play KPI dashboard** for telecom operators showcasing key metrics across five strategic pillars using **comprehensive CSV data warehouse** with dynamic time period filtering.

## 🚀 Features

### 📈 **Comprehensive Data Warehouse**
- **Complete star schema** with 7 dimension tables and 5 fact tables
- **CSV data foundation** - 12 CSV files with 89 rows of sample data
- **Dynamic time period filtering** (30 days, QTD, YTD, 12 months)
- **Live metric calculations** with realistic performance variations
- **Professional KPI display** with trend indicators and tooltips

### 🎯 **Strategic KPI Pillars**
- **📡 Network Performance** - Availability, latency, packet loss, bandwidth utilization
- **😊 Customer Experience** - Satisfaction scores, NPS, churn rates, response times
- **💰 Revenue & Monetization** - ARPU, EBITDA margins, acquisition costs, CLV
- **📶 Usage & Service Adoption** - Data usage, 5G adoption, feature adoption rates
- **🛠️ Operational Efficiency** - MTTR, compliance rates, system uptime, efficiency scores

### 🎨 **Professional UI/UX**
- **Responsive metric cards** with gradient backgrounds and trend arrows
- **Info tooltips** (ℹ️) for quick KPI definitions on hover
- **Time period selectors** for each tab with independent filtering
- **Print-optimized layout** for PDF export via browser print
- **Color-coded deltas** (green/red/gray) for accessibility

## 🛠️ Technology Stack

- **Frontend**: Streamlit 1.28.0+
- **Database**: SQLite with custom views
- **Data Processing**: Pandas, NumPy
- **Visualization**: Altair charts
- **Configuration**: PyYAML for schema management

## 📁 Project Structure

```
telecomdashboard/
├── app.py                          # Main Streamlit application
├── database_connection.py          # SQLite database interface
├── improved_metric_cards.py        # Metric card components
├── generate_test_data.py           # Mock data generation
├── setup_database.py              # Database schema creation
├── load_csv_data.py               # CSV data loading script
├── requirements.txt               # Python dependencies
├── data/
│   ├── telecom_db.sqlite         # SQLite database
│   ├── network_performance_schema.yaml  # Database schema
│   ├── DATA_CATALOG.md           # Complete data documentation
│   ├── dim_*.csv                 # 7 dimension table CSV files
│   ├── fact_*.csv                # 5 fact table CSV files
│   └── setup_telecom_data_warehouse_final.sql  # Complete schema
└── docs/
    ├── appRequirements.md         # Application requirements
    ├── appArchitecture.md         # Technical architecture
    └── consolidatedKPI.md        # KPI definitions
```

## 🚀 Quick Start

### 1. **Environment Setup**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **Database Setup**
```bash
# Create database and load CSV data
python setup_database.py
python load_csv_data.py
```

### 3. **Launch Dashboard**
```bash
streamlit run app.py
```

**Access at**: http://localhost:8501

## 📊 Data Warehouse Schema

### **Dimension Tables (7)**
- `dim_time` - Time dimension with 24 hours of data
- `dim_region` - Geographic regions and market information
- `dim_network_element` - Network infrastructure elements
- `dim_customer` - Customer segmentation and demographics
- `dim_product` - Product and service catalog
- `dim_channel` - Sales and support channels
- `dim_employee` - Employee information for operations

### **Fact Tables (5)**
- `fact_network_metrics` - Network performance metrics
- `fact_customer_experience` - Customer satisfaction and experience
- `fact_revenue` - Revenue and financial performance
- `fact_usage_adoption` - Service usage and adoption metrics
- `fact_operations` - Operational efficiency metrics

### **Business Views (5)**
- `vw_network_metrics_daily` - Daily network performance aggregations
- `vw_customer_experience_daily` - Daily customer experience metrics
- `vw_revenue_daily` - Daily revenue and financial metrics
- `vw_usage_adoption_daily` - Daily usage and adoption metrics
- `vw_operations_daily` - Daily operational efficiency metrics

### **CSV Data Foundation**
- **12 CSV files** with **89 rows** of sample data
- **Portable format** for easy migration to any database
- **Complete documentation** in `data/DATA_CATALOG.md`
- **Automated loading** with `load_csv_data.py`

### **Key Metrics Available**
- **Network Performance**: Availability, latency, packet loss, bandwidth utilization
- **Customer Experience**: Satisfaction scores, NPS, churn rates, response times
- **Revenue & Financial**: ARPU, EBITDA margins, acquisition costs, CLV
- **Usage & Adoption**: Data usage, 5G adoption, feature adoption rates
- **Operations**: MTTR, compliance rates, system uptime, efficiency scores

## ⏰ Time Period Filtering

The dashboard supports **dynamic time period filtering** with realistic data variations:

| Period | Days | Performance Variation |
|--------|------|---------------------|
| **Last 30 Days** | 30 | Baseline performance |
| **QTD** | 90 | 2-5% degradation |
| **YTD** | 365 | 5-10% degradation |
| **Last 12 Months** | 365 | Same as YTD |

### **Example Variations**
- **30 Days**: 99.77% availability, 41.0ms latency
- **QTD**: 97.77% availability, 43.1ms latency  
- **YTD**: 94.78% availability, 45.1ms latency

## 🎨 Dashboard Features

### **Metric Cards**
- **Professional styling** with gradient backgrounds
- **Trend indicators** (▲▼●) with color coding
- **Info tooltips** for KPI definitions
- **Real-time timestamps** showing last update
- **Responsive layout** (3x2 grid per tab)

### **Navigation**
- **Tab-based interface** for each KPI pillar
- **Independent time period selectors** per tab
- **Consistent styling** across all sections
- **Print-optimized** for PDF export

### **Data Integration**
- **Real-time database queries** for all metrics
- **Error handling** with graceful fallbacks
- **Performance optimizations** for large datasets
- **Scalable architecture** for production deployment

## 🔧 Customization

### **Adding New KPIs**
1. Update `database_connection.py` with new query methods
2. Add metric definitions in `improved_metric_cards.py`
3. Update the relevant tab in `app.py`
4. Add corresponding CSV data if needed

### **Modifying Time Periods**
1. Edit the time period mapping in `app.py`
2. Update database queries in `database_connection.py`
3. Adjust performance variations as needed

### **Data Customization**
1. **CSV Files**: Modify dimension and fact table CSV files
2. **Schema**: Update `network_performance_schema.yaml`
3. **Loading**: Use `load_csv_data.py` to reload data
4. **Documentation**: Update `data/DATA_CATALOG.md`

### **Styling Changes**
1. Modify CSS in `improved_metric_cards.py`
2. Update color schemes and gradients
3. Adjust card layouts and spacing

## 📈 Target Users

- **Telecom Executives** (CEO, CTO, COO) - Strategic overview
- **Business Analysts** - Detailed KPI analysis
- **Network Operations** - Performance monitoring
- **Finance Teams** - Revenue and cost metrics
- **Product Managers** - Service adoption insights

## 🚀 Deployment Options

### **Local Development**
```bash
streamlit run app.py
```

### **Streamlit Cloud**
1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy with automatic updates

### **Enterprise Deployment**
- **Snowflake Integration**: Replace SQLite with Snowflake
- **Docker Containerization**: Package with Docker
- **Kubernetes**: Scale with K8s deployment
- **Custom Authentication**: Add SSO integration

## 🔮 Future Enhancements

### **Planned Features**
- **Real-time data streaming** from network APIs
- **Advanced analytics** with machine learning insights
- **Custom dashboard builder** for user-defined KPIs
- **Mobile-responsive design** for tablet/phone access
- **Multi-tenant architecture** for multiple operators

### **Integration Opportunities**
- **Snowflake Data Warehouse** - Replace SQLite with CSV loading
- **PostgreSQL/MySQL** - Enterprise database migration
- **Tableau/Power BI** - Enhanced visualizations
- **Slack/Teams** - Automated alerts and notifications
- **Jira/ServiceNow** - Incident management integration

## 📋 Data Schema

### **Complete Data Warehouse Schema**
The project includes a comprehensive star schema with:

- **7 Dimension Tables**: Time, Region, Network Element, Customer, Product, Channel, Employee
- **5 Fact Tables**: Network Metrics, Customer Experience, Revenue, Usage Adoption, Operations
- **5 Business Views**: Daily aggregations for each strategic pillar
- **12 CSV Files**: Complete data foundation with 89 sample records

### **Schema Documentation**
- **`data/DATA_CATALOG.md`** - Complete data documentation
- **`data/network_performance_schema.yaml`** - Full schema definition
- **`load_csv_data.py`** - Automated data loading script

### **Sample Schema Structure**
```yaml
databases:
  - name: "telecom_dw"
    schemas:
      - name: "sch_gold"
        tables:
          - name: "dim_time"           # Time dimension
          - name: "dim_region"         # Geographic dimension
          - name: "dim_customer"       # Customer dimension
          - name: "fact_network_metrics"    # Network performance
          - name: "fact_revenue"       # Financial metrics
          # ... additional tables
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-kpi`
3. **Commit changes**: `git commit -am 'Add new KPI metric'`
4. **Push branch**: `git push origin feature/new-kpi`
5. **Submit pull request**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the documentation in `/docs/`
2. Review the database schema and data loading scripts
3. Test with the provided sample data
4. Open an issue on GitHub

---

**Built with ❤️ for telecom operators who need real-time insights into their network performance and business metrics.** 