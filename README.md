# 📊 Telecom KPI Dashboard

A **production-ready KPI dashboard** for telecom operators with **comprehensive CSV data warehouse** and **modular theming system**. Provides real-time insights into network performance, customer experience, revenue, usage, and operational efficiency with dynamic time period filtering and professional UI/UX.

## 🎯 Features

### ✅ **Comprehensive Data Warehouse Architecture**
- **Complete Star Schema** - 7 dimension tables and 5 fact tables
- **CSV Data Foundation** - 12 CSV files with 89 rows of sample data
- **Dynamic Time Period Filtering** - User-selectable periods (30 days, QTD, YTD, 12 months)
- **Live Metric Calculations** - Real-time aggregations and delta calculations

### ✅ **Modular Theming System**
- **Multiple Professional Themes** - Cognizant and Verizon themes included
- **Dynamic Theme Switching** - Real-time theme changes without page reload
- **Customizable Components** - KPI cards, charts, and layouts adapt to theme
- **Extensible Architecture** - Easy to add new themes with CSS and Python modules
- **Theme-Aware Charts** - Altair charts automatically adapt to theme colors
- **Professional Branding** - Logo integration and brand-specific styling

### ✅ **Strategic KPI Pillars**
- **📡 Network Performance** - Availability, latency, packet loss, bandwidth utilization
- **😊 Customer Experience** - Satisfaction, NPS, churn rate, support metrics
- **💰 Revenue & Monetization** - ARPU, EBITDA, CLV, growth metrics
- **📶 Usage & Service Adoption** - Data usage, 5G adoption, feature penetration
- **🛠️ Operational Efficiency** - Response times, compliance, uptime metrics

### ✅ **Professional UI/UX**
- **Responsive Metric Cards** - Gradient backgrounds with trend arrows
- **Info Tooltips** (ℹ️) - Quick KPI definitions on hover
- **Time Period Selectors** - Independent filtering per tab
- **Print-Optimized Layout** - PDF export via browser print
- **Color-Coded Deltas** - Green/red/gray for accessibility
- **Real-Time Timestamps** - Last update indicators

## 🎨 Available Themes

### **Cognizant Theme**
- **Color Scheme**: Professional blue/cyan palette
- **Design**: Clean, modern corporate aesthetic
- **Features**: Dark mode support, professional typography
- **Branding**: Cognizant logo integration

### **Verizon Theme**
- **Color Scheme**: Verizon red (#cd040b) with dark backgrounds
- **Design**: Telecom industry-focused styling
- **Features**: High contrast, accessibility-friendly
- **Branding**: Verizon logo integration

### **Adding New Themes**
The dashboard supports easy theme addition through the modular system:
- Create theme CSS file in `styles/[theme_name]/`
- Add theme Python module in `[theme_name]_theme.py`
- Register theme in `theme_manager.py`
- Include logo and assets in theme directory

## 🚀 Quick Start

### **Prerequisites**
```bash
python 3.8+
pip install -r requirements.txt
```

### **Installation**
```bash
# Clone the repository
git clone <repository-url>
cd telecomdashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **Database Setup**
```bash
# Load comprehensive data warehouse
python load_csv_data.py

# Verify database creation
ls data/telecom_db.sqlite
```

### **Run the Application**
```bash
streamlit run app.py
```

Access the dashboard at `http://localhost:8501`

## 📁 Project Structure

```
telecomdashboard/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                      # This file
├── CHANGELOG.md                   # Version history
├── client_onboarding_guide.md     # Client deployment guide
├── data/                          # Data warehouse files
│   ├── telecom_db.sqlite         # SQLite database
│   ├── dim_*.csv                 # Dimension tables (7 files)
│   ├── fact_*.csv                # Fact tables (5 files)
│   ├── DATA_CATALOG.md           # Data documentation
│   └── load_csv_data.py          # Data loading script
├── docs/                          # Documentation
│   ├── appRequirements.md        # Detailed requirements
│   ├── appArchitecture.md        # Technical architecture
│   ├── consolidatedKPI.md        # KPI definitions
│   ├── THEME_GUIDE.md           # Theme development guide
│   └── ux-design1.html          # Design reference
├── styles/                        # Theming system
│   ├── cognizant/                # Cognizant theme
│   │   ├── cognizant.css         # Theme stylesheet
│   │   └── logojpg.jpg          # Theme logo
│   └── verizon/                  # Verizon theme
│       ├── verizon.css           # Theme stylesheet
│       └── logojpg.jpg          # Theme logo
├── components/                    # Modular components
│   ├── kpi_components.py         # Chart rendering functions
│   ├── improved_metric_cards.py  # KPI card components
│   ├── database_connection.py    # Database interface
│   ├── theme_manager.py          # Theme management system
│   ├── theme_switcher.py        # Theme switching UI
│   ├── cognizant_theme.py       # Cognizant theme module
│   └── verizon_theme.py         # Verizon theme module
└── scripts/                      # Data generation
    ├── generate_comprehensive_data.py
    └── fix_network_metrics_schema.py
```

## 🎨 Theming System Architecture

### **Core Components**
- **`theme_manager.py`** - Central theme registry and management
- **`theme_switcher.py`** - Streamlit UI for theme selection
- **`[theme]_theme.py`** - Individual theme modules (CSS, headers, colors)
- **`styles/[theme]/`** - Theme-specific assets and stylesheets

### **Theme Features**
- **Dynamic CSS Loading** - External stylesheets with theme-specific styling
- **Logo Integration** - Base64-encoded logos for header branding
- **Color Coordination** - Theme-aware chart colors and component styling
- **Responsive Design** - Mobile-friendly layouts for all themes
- **Print Optimization** - Theme-aware print layouts

### **Adding a New Theme**
1. Create `styles/[theme_name]/[theme_name].css`
2. Create `[theme_name]_theme.py` with theme functions
3. Add logo to `styles/[theme_name]/logojpg.jpg`
4. Register theme in `theme_manager.py`
5. Test theme switching functionality

## 📊 Data Warehouse Schema

### **Dimension Tables (7)**
- `dim_time` - Date/time dimensions
- `dim_region` - Geographic regions
- `dim_network_element` - Network infrastructure
- `dim_customer` - Customer segments
- `dim_product` - Service offerings
- `dim_channel` - Distribution channels
- `dim_employee` - Staff information

### **Fact Tables (5)**
- `fact_network_metrics` - Network performance data
- `fact_customer_experience` - Customer satisfaction metrics
- `fact_revenue` - Financial performance data
- `fact_usage_adoption` - Service usage statistics
- `fact_operations` - Operational efficiency metrics

### **Business Views (5)**
- `vw_network_metrics_daily` - Daily network aggregations
- `vw_customer_experience_daily` - Daily customer metrics
- `vw_revenue_daily` - Daily revenue calculations
- `vw_usage_adoption_daily` - Daily usage statistics
- `vw_operations_daily` - Daily operational metrics

## ⚙️ Configuration

### **Time Period Filtering**
| Period | Days | Performance Variation |
|--------|------|---------------------|
| **Last 30 Days** | 30 | Baseline performance |
| **QTD** | 90 | 2-5% degradation |
| **YTD** | 365 | 5-10% degradation |
| **Last 12 Months** | 365 | Same as YTD |

### **Theme Configuration**
- **Default Theme**: Cognizant
- **Available Themes**: Cognizant, Verizon
- **Theme Switching**: Real-time via sidebar
- **Theme Persistence**: Maintains selection across sessions

## 🎯 Key Metrics Available

### **Network Performance**
- Network Availability: 99.77%
- Average Latency: 41.0ms
- Packet Loss Rate: 0.0%
- Bandwidth Utilization: 63.48%
- MTTR: 2.15 hours
- Dropped Call Rate: 0.0%

### **Customer Experience**
- Customer Satisfaction: 4.2/5.0
- Net Promoter Score: 42
- Customer Churn Rate: 2.1%
- Average Handling Time: 4.2 min
- First Contact Resolution: 78.5%
- Customer Lifetime Value: $1,250

### **Revenue & Monetization**
- ARPU: $42.17
- EBITDA Margin: 28.5%
- Customer Acquisition Cost: $125
- Customer Lifetime Value: $1,850
- Revenue Growth: 12.3%
- Profit Margin: 18.7%

### **Usage & Service Adoption**
- Data Usage per Subscriber: 8.5 GB
- 5G Adoption Rate: 45.2%
- Feature Adoption Rate: 32.8%
- Service Penetration: 78.5%
- App Usage Rate: 65.3%
- Premium Service Adoption: 28.7%

### **Operational Efficiency**
- Service Response Time: 2.1 hours
- Regulatory Compliance Rate: 98.7%
- Support Ticket Resolution: 94.2%
- System Uptime: 99.92%
- Operational Efficiency Score: 87.3
- Capex to Revenue Ratio: 18.2%

## 🔧 Customization

### **Data Customization**
- **CSV Files**: Modify `data/*.csv` files for custom data
- **Database**: Use `load_csv_data.py` to reload custom data
- **Views**: Update SQL views in `data/setup_telecom_data_warehouse_final.sql`

### **Theme Customization**
- **CSS Styling**: Modify `styles/[theme]/[theme].css`
- **Logo Integration**: Replace `styles/[theme]/logojpg.jpg`
- **Color Schemes**: Update theme color variables
- **Component Styling**: Customize KPI cards and charts

### **KPI Customization**
- **Metric Definitions**: Update `docs/consolidatedKPI.md`
- **Chart Types**: Modify `kpi_components.py`
- **Card Layouts**: Customize `improved_metric_cards.py`

## 🚀 Deployment

### **Local Development**
```bash
streamlit run app.py
```

### **Production Deployment**
1. **Database Migration**: Load CSV data to PostgreSQL/MySQL/Snowflake
2. **Environment Setup**: Configure production database connection
3. **Theme Deployment**: Ensure all theme assets are accessible
4. **Performance Optimization**: Enable caching and monitoring

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

## 🔗 Integration Opportunities

### **Data Warehouse Integration**
- **Snowflake**: Migrate CSV data to Snowflake data warehouse
- **PostgreSQL/MySQL**: Enterprise database deployment
- **Real-time APIs**: Live network performance data feeds

### **Visualization Integration**
- **Tableau**: Export data for advanced visualizations
- **Power BI**: Microsoft BI integration
- **Custom Dashboards**: Embed in existing systems

### **Enterprise Integration**
- **SSO Authentication**: Single sign-on for enterprise users
- **Slack/Teams**: Automated alerts and notifications
- **Jira/ServiceNow**: Incident management integration

## 📈 Future Enhancements

### **Immediate Roadmap**
- **Real-time Data Streaming** - Live network API integration
- **Advanced Analytics** - Machine learning insights
- **Custom Dashboards** - User-defined KPI configurations
- **Mobile Optimization** - Tablet/phone responsive design

### **Long-term Vision**
- **Multi-tenant Architecture** - Support for multiple telecom operators
- **Advanced Theming** - AI-powered theme generation
- **Predictive Analytics** - Proactive issue detection
- **API Ecosystem** - RESTful APIs for external integrations

## 🤝 Contributing

### **Theme Development**
1. Follow the theme architecture in `docs/THEME_GUIDE.md`
2. Create theme assets in `styles/[theme_name]/`
3. Implement theme module in `[theme_name]_theme.py`
4. Test theme switching and print functionality

### **Data Enhancement**
1. Update CSV files with realistic telecom data
2. Modify database schema as needed
3. Update business views for new metrics
4. Test data loading and visualization

### **Feature Development**
1. Follow modular component architecture
2. Maintain theme compatibility
3. Update documentation for new features
4. Test print functionality with changes

## 📄 License

This project is designed as a telecom KPI dashboard accelerator for enterprise clients.

## 📞 Support

For technical support and customization requests, refer to `client_onboarding_guide.md` for comprehensive deployment and customization guidance.

---

**This dashboard provides telecom operators with real-time insights into network performance and business metrics, enabling data-driven decision-making and operational excellence with professional theming and comprehensive data analytics.** 