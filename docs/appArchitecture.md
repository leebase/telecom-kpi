# 🏗️ App Architecture: Telecom KPI Dashboard

## 📋 Overview

This **comprehensive data warehouse-driven** telecom KPI dashboard provides real-time insights into network performance, customer experience, revenue, usage, and operational efficiency. Built with a **modular theming system** for professional branding and extensible architecture for enterprise deployment.

## 🛠️ Technology Stack

### **Frontend Framework**
- **Streamlit 1.28.0+** - Interactive web application framework
- **Altair** - Declarative statistical visualization library
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical operations and calculations

### **Database & Data Layer**
- **SQLite** - Local database for development and testing
- **Enterprise Database Adapters** - 🚧 *Future Feature: PostgreSQL and Snowflake support with connection pooling*
- **CSV Data Foundation** - 12 files with 89 rows of sample data
- **Business Views** - 5 daily aggregation views for KPI calculations
- **Connection Pool Management** - Thread-safe connection handling with validation and cleanup
- **PyYAML** - Schema definition and configuration management

### **Theming System**
- **Modular CSS** - External stylesheets for each theme
- **Dynamic Theme Switching** - Real-time theme changes
- **Logo Integration** - Base64-encoded logos for branding
- **Theme-Aware Components** - All UI elements adapt to theme

### **Performance & Reliability Layer**
- **Smart Caching System** - TTL-based caching with automatic cleanup and debug logging
- **Circuit Breaker Pattern** - AI service protection with state management (CLOSED/OPEN/HALF_OPEN)
- **Exponential Backoff Retry** - Intelligent retry logic with jitter for external API calls
- **Connection Pooling** - Enterprise database connection management with min/max limits
- **Graceful Degradation** - Fallback responses and error recovery mechanisms

### **Development Tools**
- **Python 3.8+** - Core programming language
- **Virtual Environment** - Dependency isolation
- **Git** - Version control and collaboration

## 📁 Project Structure

```
telecomdashboard/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
├── CHANGELOG.md                   # Version history
├── client_onboarding_guide.md     # Client deployment guide
├── data/                          # Data warehouse files
│   ├── telecom_db.sqlite         # SQLite database
│   ├── dim_*.csv                 # Dimension tables (7 files)
│   ├── fact_*.csv                # Fact tables (5 files)
│   ├── DATA_CATALOG.md           # Data documentation
│   ├── load_csv_data.py          # Data loading script
│   └── setup_telecom_data_warehouse_final.sql  # Complete schema
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

## 🗄️ Database Architecture

### **Complete Star Schema Design**

#### **Dimension Tables (7)**
1. **`dim_time`** - Date/time dimensions with hour-level granularity
2. **`dim_region`** - Geographic regions and market information
3. **`dim_network_element`** - Network infrastructure elements
4. **`dim_customer`** - Customer segmentation and demographics
5. **`dim_product`** - Product and service catalog
6. **`dim_channel`** - Sales and support channels
7. **`dim_employee`** - Employee information for operations

#### **Fact Tables (5)**
1. **`fact_network_metrics`** - Network performance metrics (availability, latency, etc.)
2. **`fact_customer_experience`** - Customer satisfaction and experience metrics
3. **`fact_revenue`** - Revenue and financial performance data
4. **`fact_usage_adoption`** - Service usage and adoption statistics
5. **`fact_operations`** - Operational efficiency and compliance metrics

#### **Business Views (5)**
1. **`vw_network_metrics_daily`** - Daily network performance aggregations
2. **`vw_customer_experience_daily`** - Daily customer experience metrics
3. **`vw_revenue_daily`** - Daily revenue and financial calculations
4. **`vw_usage_adoption_daily`** - Daily usage and adoption statistics
5. **`vw_operations_daily`** - Daily operational efficiency metrics

### **CSV Data Foundation**
- **12 CSV files** with **89 rows** of realistic sample data
- **Portable format** for easy migration to any database system
- **Complete documentation** in `data/DATA_CATALOG.md`
- **Automated loading** with `load_csv_data.py`

## 🎨 Theming System Architecture

### **Core Components**

#### **Theme Manager (`theme_manager.py`)**
- **Central Registry** - Manages all available themes
- **Dynamic Loading** - Loads theme CSS and assets on demand
- **Theme Switching** - Handles real-time theme changes
- **Component Coordination** - Ensures all components adapt to theme

#### **Theme Switcher (`theme_switcher.py`)**
- **Streamlit UI Component** - Sidebar theme selection interface
- **Real-time Updates** - Instant theme changes without page reload
- **Theme Persistence** - Maintains selection across sessions
- **User Experience** - Intuitive theme switching controls

#### **Individual Theme Modules**
- **`cognizant_theme.py`** - Cognizant theme implementation
- **`verizon_theme.py`** - Verizon theme implementation
- **CSS Loading** - External stylesheet management
- **Logo Integration** - Base64-encoded logo handling
- **Color Coordination** - Theme-specific color schemes

### **Theme Features**

#### **Dynamic CSS Loading**
- **External Stylesheets** - Each theme has dedicated CSS file
- **Real-time Application** - CSS changes applied immediately
- **Component Styling** - KPI cards, charts, and layouts adapt
- **Print Optimization** - Theme-aware print layouts

#### **Logo Integration**
- **Base64 Encoding** - Logos embedded directly in HTML
- **Header Branding** - Professional logo display in headers
- **Theme-Specific Assets** - Each theme has its own logo
- **Responsive Design** - Logos scale appropriately

#### **Color Coordination**
- **Theme-Aware Charts** - Altair charts use theme colors
- **Component Adaptation** - All UI elements match theme
- **Accessibility** - High contrast for color-blind users
- **Professional Appearance** - Brand-consistent styling

### **Theme Development Process**

#### **1. CSS Creation**
```css
/* styles/[theme_name]/[theme_name].css */
:root {
  --primary-color: #brand-color;
  --secondary-color: #accent-color;
  /* Theme-specific variables */
}
```

#### **2. Python Module**
```python
# [theme_name]_theme.py
def get_[theme_name]_css():
    # Load and return CSS content
    
def create_[theme_name]_header():
    # Create theme-specific header with logo
```

#### **3. Asset Integration**
- Add logo to `styles/[theme_name]/logojpg.jpg`
- Ensure logo is appropriate size and format
- Test logo display in header

#### **4. Theme Registration**
```python
# theme_manager.py
self.themes["theme_name"] = {
    "css_function": get_theme_name_css,
    "header_function": create_theme_name_header,
    "colors": theme_colors
}
```

## 🔄 Data Flow

### **Database Integration**
1. **CSV Loading** - `load_csv_data.py` loads CSV files into SQLite
2. **View Creation** - Business views aggregate data for KPIs
3. **Real-time Queries** - `database_connection.py` executes queries
4. **Data Processing** - Pandas processes results for visualization

### **Theme Integration**
1. **Theme Selection** - User selects theme via `theme_switcher.py`
2. **CSS Loading** - `theme_manager.py` loads theme CSS
3. **Component Adaptation** - All components apply theme styling
4. **Real-time Updates** - Changes applied without page reload

### **Component Rendering**
1. **Data Retrieval** - Database queries fetch KPI data
2. **Metric Calculation** - Pandas calculates deltas and trends
3. **Chart Generation** - Altair creates theme-aware visualizations
4. **Card Rendering** - HTML cards with theme-specific styling

## 🧩 Component Architecture

### **Performance & Reliability Components**

#### **Caching System (`database_connection.py`)**
```python
@cache_with_ttl(ttl_seconds=300)  # 5-minute cache
def get_network_metrics(self, days: int = 30):
    # Automatic cache expiration and cleanup
```

- **TTL Management**: Automatic cache expiration prevents stale data
- **Memory Control**: LRU-style cleanup limits cache size to 100 items
- **Debug Logging**: Cache hits/misses tracked for performance monitoring
- **Thread Safety**: Concurrent access handling with proper locking

#### **Circuit Breaker Pattern (`llm_service.py`)**
```python
class CircuitBreaker:
    - CLOSED: Normal operation
    - OPEN: Rejecting requests (5 failures → 60s timeout)
    - HALF_OPEN: Testing service recovery
```

- **Failure Threshold**: 5 consecutive failures trigger circuit opening
- **Recovery Timeout**: 60-second wait before testing service recovery
- **Graceful Fallback**: Structured error responses during outages
- **State Persistence**: Circuit state maintained across requests

#### **Connection Pooling (`enterprise_database_adapter.py`)**
```python
ConnectionPool(
    min_connections=2,
    max_connections=10,
    connection_validation=True
)
```

- **Pool Management**: Min/max connection limits prevent exhaustion
- **Connection Health**: Automatic validation and cleanup of stale connections
- **Thread Safety**: Concurrent pool access with proper synchronization
- **Enterprise Ready**: PostgreSQL and Snowflake adapter support

### **Core Components**

#### **Metric Cards (`improved_metric_cards.py`)**
- **Theme-Aware Styling** - Cards adapt to selected theme
- **Responsive Layout** - 3x2 grid per tab
- **Trend Indicators** - Color-coded deltas (▲▼●)
- **Info Tooltips** - Hover definitions for KPIs
- **Real-time Updates** - Timestamps and live data

#### **Chart Components (`kpi_components.py`)**
- **Theme-Aware Colors** - Charts use theme color schemes
- **Multiple Chart Types** - Bar, line, area, distribution charts
- **Interactive Features** - Hover tooltips and zoom
- **Print Optimization** - Charts render properly in print mode

#### **Database Interface (`database_connection.py`)**
- **Connection Management** - SQLite database connections
- **Query Execution** - Real-time data retrieval
- **Error Handling** - Graceful fallbacks for data issues
- **Performance Optimization** - Efficient query patterns

### **Theme Components**

#### **Theme Manager (`theme_manager.py`)**
- **Theme Registry** - Central management of all themes
- **CSS Loading** - Dynamic stylesheet application
- **Header Generation** - Theme-specific headers with logos
- **Color Coordination** - Theme color scheme management

#### **Theme Switcher (`theme_switcher.py`)**
- **UI Component** - Streamlit sidebar theme selection
- **Real-time Switching** - Instant theme changes
- **State Management** - Theme selection persistence
- **User Experience** - Intuitive theme switching

## ⚙️ Configuration Management

### **Environment Configuration**
- **Database Path** - Configurable SQLite database location
- **Theme Default** - Default theme selection
- **Print Settings** - Print mode configuration
- **Development Mode** - Debug and development settings

### **Theme Configuration**
- **Available Themes** - List of registered themes
- **Default Theme** - Initial theme selection
- **Theme Assets** - CSS and logo file paths
- **Color Schemes** - Theme-specific color variables

### **Data Configuration**
- **CSV File Paths** - Location of data files
- **Database Schema** - Table and view definitions
- **Query Timeouts** - Database query performance settings
- **Cache Settings** - Data caching configuration

## 🔧 Simulated Time Period Filtering

### **Implementation Details**
- **Scaling Factors** - Performance variations based on time period
- **Query Modification** - WHERE clauses adjusted for period
- **Metric Calculation** - Deltas calculated for each period
- **User Interface** - Period selectors in each tab

### **Period Variations**
| Period | Days | Network Performance | Customer Experience | Revenue |
|--------|------|-------------------|-------------------|---------|
| **30 Days** | 30 | Baseline | Baseline | Baseline |
| **QTD** | 90 | -2% to -5% | -1% to -3% | +5% to +10% |
| **YTD** | 365 | -5% to -10% | -2% to -5% | +10% to +20% |
| **12 Months** | 365 | Same as YTD | Same as YTD | Same as YTD |

## 🚀 Production Considerations

### **Database Migration**
- **PostgreSQL/MySQL** - Enterprise database deployment
- **Snowflake** - Cloud data warehouse integration
- **Data Loading** - CSV to enterprise database migration
- **Performance Optimization** - Query optimization for large datasets

### **Theme Customization**
- **Client Branding** - Custom themes for specific clients
- **Logo Integration** - Client logo and branding
- **Color Schemes** - Brand-specific color palettes
- **Print Optimization** - Client-specific print layouts

### **Deployment Architecture**
- **Docker Containerization** - Portable deployment
- **Kubernetes Scaling** - Enterprise scaling
- **Load Balancing** - High availability setup
- **Monitoring** - Application performance monitoring

### **Security Considerations**
- **Authentication** - SSO integration for enterprise users
- **Data Encryption** - Sensitive data protection
- **Access Control** - Role-based access to KPIs
- **Audit Logging** - User activity tracking

## 📈 Performance & Scalability

### **Database Performance**
- **Indexing Strategy** - Optimized database indexes
- **Query Optimization** - Efficient SQL queries
- **Connection Pooling** - Database connection management
- **Caching** - Data caching for improved performance

### **Application Performance**
- **Streamlit Optimization** - Efficient component rendering
- **Theme Switching** - Fast theme changes without reload
- **Chart Rendering** - Optimized Altair chart generation
- **Print Mode** - Efficient print layout generation

### **Scalability Considerations**
- **Multi-tenant Architecture** - Support for multiple clients
- **Horizontal Scaling** - Load balancer deployment
- **Data Volume** - Handling large datasets
- **User Concurrency** - Multiple simultaneous users

## 🔮 Future Enhancements

### **Immediate Roadmap**
- **Real-time Data Streaming** - Live network API integration
- **Advanced Analytics** - Machine learning insights
- **Custom Dashboards** - User-defined KPI configurations
- **Mobile Optimization** - Tablet/phone responsive design
- **Additional Themes** - More telecom operator themes

### **Long-term Vision**
- **Multi-tenant Architecture** - Support for multiple telecom operators
- **Advanced Theming** - AI-powered theme generation
- **Predictive Analytics** - Proactive issue detection
- **API Ecosystem** - RESTful APIs for external integrations
- **Custom Branding** - Client-specific theme development

---

**This architecture provides a robust foundation for a production-ready telecom KPI dashboard with comprehensive data analytics, modular theming, and enterprise-grade scalability.**