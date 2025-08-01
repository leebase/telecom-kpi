# 🏗️ Telecom KPI Dashboard - Technical Architecture

## 🎯 Overview

The Telecom KPI Dashboard is a **database-driven Streamlit application** that provides real-time insights into telecom network performance and business metrics. Built with a modular architecture for scalability and maintainability.

## 🛠️ Technology Stack

### **Frontend & Framework**
- **Streamlit 1.28.0+** - Web application framework
- **HTML/CSS** - Custom styling for metric cards
- **JavaScript** - Browser-based interactions (tooltips, print)

### **Database & Data Layer**
- **SQLite 3** - Embedded database for data storage
- **Pandas** - Data manipulation and analysis
- **PyYAML** - Schema configuration management
- **Custom Views** - `vw_network_metrics_daily` for KPI calculations

### **Data Processing**
- **NumPy** - Numerical operations and calculations
- **Pandas** - DataFrame operations and time series analysis
- **Custom Aggregations** - Time period filtering and metric calculations

### **Visualization**
- **Altair** - Declarative statistical visualizations
- **Streamlit Components** - Native UI elements
- **Custom CSS** - Professional styling and layouts

## 📁 Project Structure

```
telecomdashboard/
├── app.py                          # Main Streamlit application
├── database_connection.py          # SQLite database interface
├── improved_metric_cards.py        # Metric card components
├── generate_test_data.py           # Mock data generation (legacy)
├── setup_database.py              # Database schema creation
├── load_data.py                   # Data loading utilities
├── requirements.txt               # Python dependencies
├── data/
│   ├── telecom_db.sqlite         # SQLite database
│   ├── network_performance_schema.yaml  # Database schema
│   ├── setup_telecom_db.sql     # Generated SQL DDL
│   └── fact_network_metrics_preview.csv # Sample data
└── docs/
    ├── appRequirements.md         # Application requirements
    ├── appArchitecture.md         # This file
    └── consolidatedKPI.md        # KPI definitions
```

## 🗄️ Database Architecture

### **Star Schema Design**
```
fact_network_metrics (Fact Table)
├── network_element_id (FK → dim_network_element)
├── region_id (FK → dim_region)
├── date_id (FK → dim_time)
├── hour
├── uptime_seconds
├── downtime_seconds
├── latency_ms
├── packet_loss_percent
├── bandwidth_utilization_percent
└── mttr_hours

dim_region (Dimension Table)
├── region_id (PK)
└── region_name

dim_network_element (Dimension Table)
├── network_element_id (PK)
└── element_type

dim_time (Dimension Table)
├── date_id (PK)
├── hour (PK)
├── year
├── month
├── day
├── weekday
└── is_weekend
```

### **Views**
- **`vw_network_metrics_daily`** - Daily aggregated metrics for KPI calculations
  - Calculates availability percentages
  - Aggregates latency and performance metrics
  - Provides clean interface for dashboard queries

## 🔄 Data Flow

### **1. Database Setup**
```python
# setup_database.py
1. Parse YAML schema → Generate SQL DDL
2. Create SQLite database → Execute DDL
3. Load dimension data → Insert reference data
4. Load fact data → Insert network metrics
```

### **2. Dashboard Queries**
```python
# database_connection.py
1. User selects time period → Convert to days
2. Query database → Get aggregated metrics
3. Calculate deltas → Compare with baseline
4. Format data → Return to UI components
```

### **3. UI Rendering**
```python
# improved_metric_cards.py
1. Receive metric data → Format values
2. Create HTML cards → Apply styling
3. Render with Streamlit → Display to user
```

## 🎨 Component Architecture

### **Core Components**

#### **1. Database Connection (`database_connection.py`)**
```python
class TelecomDatabase:
    - get_network_metrics(days)
    - get_customer_metrics(days)
    - get_revenue_metrics(days)
    - get_usage_metrics(days)
    - get_operations_metrics(days)
```

#### **2. Metric Cards (`improved_metric_cards.py`)**
```python
def create_metric_card():
    - Format values and deltas
    - Generate HTML with CSS
    - Handle tooltips and styling

def render_metric_grid():
    - Create responsive 3x2 grid
    - Manage unique keys per tab
    - Handle error states
```

#### **3. Main Application (`app.py`)**
```python
def main():
    - Configure page settings
    - Apply custom CSS
    - Create tab navigation
    - Handle time period selection
    - Render metric grids per tab
```

## ⏰ Time Period Filtering

### **Implementation Strategy**
Since we have limited historical data (single day), we implement **simulated time period filtering**:

```python
# Time period mapping
time_periods = {
    "Last 30 Days": 30,    # Baseline performance
    "QTD": 90,             # 2-5% degradation
    "YTD": 365,            # 5-10% degradation
    "Last 12 Months": 365  # Same as YTD
}
```

### **Performance Variations**
- **30 Days**: Uses actual data values
- **90 Days (QTD)**: Applies 2-5% performance degradation
- **365 Days (YTD)**: Applies 5-10% performance degradation

## 🔧 Configuration Management

### **Schema Definition (`network_performance_schema.yaml`)**
```yaml
databases:
  - name: "telecom_db"
    schemas:
      - name: "sch_gold"
        tables:
          - name: "fact_network_metrics"
            columns:
              - name: "network_element_id"
                type: "INTEGER"
              # ... additional columns
```

### **Environment Configuration**
- **Virtual Environment**: `venv/` for dependency isolation
- **Requirements**: `requirements.txt` for package management
- **Database Path**: Configurable in `database_connection.py`

## 🚀 Deployment Architecture

### **Development Environment**
```bash
# Local development
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### **Production Considerations**
- **Database**: Replace SQLite with PostgreSQL/MySQL
- **Caching**: Implement Redis for query caching
- **Load Balancing**: Multiple Streamlit instances
- **Monitoring**: Add logging and metrics collection

## 🔒 Security & Performance

### **Security Measures**
- **Input Validation**: Sanitize user inputs
- **SQL Injection Prevention**: Use parameterized queries
- **Error Handling**: Graceful fallbacks for database errors
- **Access Control**: Future SSO integration

### **Performance Optimizations**
- **Database Indexing**: Optimize query performance
- **Connection Pooling**: Reuse database connections
- **Caching**: Cache frequently accessed metrics
- **Lazy Loading**: Load data on demand

## 🔮 Scalability Considerations

### **Horizontal Scaling**
- **Multiple Streamlit Instances**: Behind load balancer
- **Database Clustering**: Read replicas for queries
- **CDN Integration**: Static asset delivery

### **Vertical Scaling**
- **Database Optimization**: Query tuning and indexing
- **Memory Management**: Efficient data structures
- **Caching Strategy**: Redis for metric caching

## 🧪 Testing Strategy

### **Unit Testing**
- **Database Queries**: Test metric calculations
- **Component Functions**: Test card rendering
- **Data Validation**: Test input/output formats

### **Integration Testing**
- **End-to-End**: Full dashboard functionality
- **Database Integration**: Real data loading
- **UI Components**: Cross-browser compatibility

## 📊 Monitoring & Analytics

### **Application Metrics**
- **Response Times**: Dashboard load performance
- **Error Rates**: Database and UI errors
- **User Interactions**: Time period selections

### **Business Metrics**
- **KPI Accuracy**: Data quality validation
- **User Engagement**: Dashboard usage patterns
- **Performance Trends**: Metric changes over time

## 🔄 Future Enhancements

### **Immediate Roadmap**
1. **Real-time Data Integration**: Live network APIs
2. **Advanced Analytics**: ML-powered insights
3. **Custom Dashboards**: User-defined KPIs
4. **Mobile Optimization**: Responsive design improvements

### **Long-term Vision**
1. **Multi-tenant Architecture**: Multiple operators
2. **Advanced Visualizations**: Interactive charts
3. **Alert System**: KPI threshold notifications
4. **API Integration**: Third-party data sources

---

**This architecture provides a solid foundation for a production-ready telecom KPI dashboard with real-time data integration and enterprise-grade scalability.**