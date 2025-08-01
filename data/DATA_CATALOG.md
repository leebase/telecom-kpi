# 📊 Telecom Data Warehouse - Data Catalog

## 🎯 Overview

This catalog describes all CSV files in the Telecom Data Warehouse, providing a complete reference for data loading, analysis, and integration.

---

## 📁 Dimension Tables

### **`dim_time.csv`** - Time Dimension
**Purpose**: Master time dimension for all fact tables  
**Rows**: 24 (24 hours for 2023-08-01)  
**Columns**:
- `date_id` - Date in YYYY-MM-DD format
- `hour` - Hour of day (0-23)
- `year`, `month`, `day` - Date components
- `weekday` - Day of week name
- `is_weekend` - Boolean flag (0/1)
- `quarter` - Quarter number (1-4)
- `is_month_end`, `is_quarter_end`, `is_year_end` - End period flags

**Sample Data**:
```csv
date_id,hour,year,month,day,weekday,is_weekend,quarter,is_month_end,is_quarter_end,is_year_end
2023-08-01,0,2023,8,1,Tuesday,0,3,0,0,0
```

### **`dim_region.csv`** - Geographic Dimension
**Purpose**: Geographic regions and market information  
**Rows**: 5 regions  
**Columns**:
- `region_id` - Unique region identifier
- `region_name` - Region name
- `country` - Country name
- `timezone` - Timezone (e.g., UTC-5)
- `market_type` - Market classification (Urban, Suburban, Rural)
- `population_density` - Population density category

**Sample Data**:
```csv
region_id,region_name,country,timezone,market_type,population_density
1,North Region,USA,UTC-5,Urban,High
```

### **`dim_network_element.csv`** - Network Infrastructure
**Purpose**: Network infrastructure elements and capabilities  
**Rows**: 5 network elements  
**Columns**:
- `network_element_id` - Unique element identifier
- `element_name` - Element name/identifier
- `element_type` - Type (Tower, Switch, Router)
- `vendor` - Equipment vendor
- `install_date` - Installation date
- `region_id` - Associated region
- `location` - Physical location
- `capacity_mbps` - Capacity in Mbps
- `technology` - Technology type (4G, 5G)

**Sample Data**:
```csv
network_element_id,element_name,element_type,vendor,install_date,region_id,location,capacity_mbps,technology
1,Tower-North-001,Tower,Ericsson,2023-01-15,1,North Region,1000.0,5G
```

### **`dim_customer.csv`** - Customer Information
**Purpose**: Customer segmentation and demographics  
**Rows**: 5 customers  
**Columns**:
- `customer_id` - Unique customer identifier
- `customer_type` - Type (Consumer, Business, Enterprise)
- `segment` - Segment (Premium, Standard, Basic)
- `region_id` - Customer's region
- `acquisition_date` - Customer acquisition date
- `contract_type` - Contract type (Prepaid, Postpaid, Enterprise)
- `credit_score` - Customer credit score
- `lifetime_value` - Customer lifetime value

**Sample Data**:
```csv
customer_id,customer_type,segment,region_id,acquisition_date,contract_type,credit_score,lifetime_value
1,Consumer,Premium,1,2023-01-15,Postpaid,750,2500.0
```

### **`dim_product.csv`** - Product/Service Catalog
**Purpose**: Products and services offered  
**Rows**: 5 products  
**Columns**:
- `product_id` - Unique product identifier
- `product_name` - Product name
- `product_category` - Category (Data, Voice, Video)
- `product_type` - Type (Plan, Add-on, Service)
- `data_limit_gb` - Data limit in GB
- `price_monthly` - Monthly price
- `is_premium` - Premium flag (0/1)
- `launch_date` - Product launch date

**Sample Data**:
```csv
product_id,product_name,product_category,product_type,data_limit_gb,price_monthly,is_premium,launch_date
1,Unlimited 5G,Data,Plan,100.0,89.99,1,2023-01-01
```

### **`dim_channel.csv`** - Sales & Support Channels
**Purpose**: Customer interaction channels  
**Rows**: 5 channels  
**Columns**:
- `channel_id` - Unique channel identifier
- `channel_name` - Channel name
- `channel_type` - Type (Online, Retail, Call Center)
- `channel_category` - Category (Sales, Support, Self-Service)
- `is_digital` - Digital flag (0/1)
- `cost_per_interaction` - Cost per customer interaction

**Sample Data**:
```csv
channel_id,channel_name,channel_type,channel_category,is_digital,cost_per_interaction
1,Online Store,Online,Sales,1,5.0
```

### **`dim_employee.csv`** - Employee Information
**Purpose**: Employee data for operational metrics  
**Rows**: 5 employees  
**Columns**:
- `employee_id` - Unique employee identifier
- `employee_name` - Employee name
- `department` - Department (Network Ops, Customer Service, Sales)
- `role` - Job role
- `hire_date` - Hire date
- `region_id` - Assigned region
- `is_active` - Active employee flag (0/1)

**Sample Data**:
```csv
employee_id,employee_name,department,role,hire_date,region_id,is_active
1,John Smith,Network Ops,Network Engineer,2023-01-15,1,1
```

---

## 📈 Fact Tables

### **`fact_network_metrics.csv`** - Network Performance
**Purpose**: Network performance metrics by element, region, and time  
**Rows**: 5 records  
**Key Metrics**:
- `uptime_seconds`, `downtime_seconds` - Availability data
- `calls_attempted`, `calls_dropped` - Call quality metrics
- `packets_sent`, `packets_lost` - Network integrity
- `bandwidth_capacity_mb`, `bandwidth_used_mb` - Capacity utilization
- `latency_ms`, `latency_ms_p95` - Performance metrics
- `repair_minutes` - MTTR (Mean Time To Repair)

**Sample Data**:
```csv
network_element_id,region_id,date_id,hour,uptime_seconds,downtime_seconds,calls_attempted,calls_dropped,packets_sent,packets_lost,bandwidth_capacity_mb,bandwidth_used_mb,outage_minutes,repair_minutes,latency_ms,latency_ms_p95,last_updated_ts
1,1,2023-08-01,0,86158,242,758,7,183726,230,1000,575,4.033333333333333,138,35.0,45.0,2023-08-01 00:00:00
```

### **`fact_customer_experience.csv`** - Customer Experience
**Purpose**: Customer satisfaction and experience metrics  
**Rows**: 5 records  
**Key Metrics**:
- `satisfaction_score` - Customer satisfaction (1-100)
- `nps_score` - Net Promoter Score (-100 to 100)
- `churn_probability` - Churn risk (0-1)
- `handling_time_minutes` - Support efficiency
- `first_contact_resolution` - FCR rate (0-1)
- `customer_effort_score` - Customer effort (1-7)
- `lifetime_value` - Customer lifetime value

**Sample Data**:
```csv
customer_id,date_id,region_id,channel_id,satisfaction_score,nps_score,churn_probability,handling_time_minutes,first_contact_resolution,complaint_count,escalation_count,customer_effort_score,lifetime_value
1,2023-08-01,1,1,85.0,45,0.05,3.2,0.85,1,0,2.5,2500.0
```

### **`fact_revenue.csv`** - Revenue & Financial Performance
**Purpose**: Revenue and financial performance metrics  
**Rows**: 5 records  
**Key Metrics**:
- `revenue_amount` - Revenue amount
- `arpu` - Average Revenue Per User
- `customer_acquisition_cost` - CAC
- `customer_lifetime_value` - CLV
- `ebitda_margin` - EBITDA margin percentage
- `profit_margin` - Profit margin percentage
- `subscriber_growth_rate` - Growth rate

**Sample Data**:
```csv
customer_id,product_id,date_id,region_id,channel_id,revenue_amount,arpu,customer_acquisition_cost,customer_lifetime_value,churn_revenue_loss,upsell_revenue,cross_sell_revenue,ebitda_margin,profit_margin,subscriber_count,subscriber_growth_rate
1,1,2023-08-01,1,1,89.99,89.99,125.0,2500.0,0.0,15.0,8.0,32.5,18.7,1,0.08
```

### **`fact_usage_adoption.csv`** - Usage & Service Adoption
**Purpose**: Service usage and adoption metrics  
**Rows**: 5 records  
**Key Metrics**:
- `data_usage_gb` - Data usage in GB
- `voice_minutes` - Voice minutes used
- `sms_count` - SMS count
- `feature_adoption_rate` - Feature adoption (0-1)
- `five_g_adoption` - 5G adoption rate (0-1)
- `service_penetration` - Service penetration (0-1)
- `app_usage_rate` - App usage rate (0-1)
- `premium_service_adoption` - Premium adoption (0-1)

**Sample Data**:
```csv
customer_id,product_id,date_id,region_id,data_usage_gb,voice_minutes,sms_count,feature_adoption_rate,five_g_adoption,service_penetration,app_usage_rate,premium_service_adoption,peak_usage_time,average_session_duration,active_subscribers
1,1,2023-08-01,1,8.5,120,45,0.75,0.85,0.92,0.88,0.65,8-10 PM,45.2,1
```

### **`fact_operations.csv`** - Operational Efficiency
**Purpose**: Operational efficiency and performance metrics  
**Rows**: 5 records  
**Key Metrics**:
- `service_response_time_hours` - Response time
- `regulatory_compliance_rate` - Compliance rate (0-1)
- `support_ticket_resolution_rate` - Resolution rate (0-1)
- `system_uptime_percentage` - System uptime
- `operational_efficiency_score` - Efficiency score (0-100)
- `capex_to_revenue_ratio` - CapEx to revenue ratio
- `employee_productivity_score` - Productivity score (0-100)
- `automation_rate` - Process automation (0-1)

**Sample Data**:
```csv
employee_id,region_id,date_id,channel_id,service_response_time_hours,regulatory_compliance_rate,support_ticket_resolution_rate,system_uptime_percentage,operational_efficiency_score,capex_to_revenue_ratio,employee_productivity_score,cost_per_customer,automation_rate,training_completion_rate,incident_count,resolution_time_hours
1,1,2023-08-01,3,2.1,0.987,0.942,99.92,87.3,18.2,85.5,12.5,0.75,0.92,2,3.5
```

---

## 🔄 Data Loading

### **Automated Loading Script**
Use `load_csv_data.py` to load all CSV files into SQLite:

```bash
python load_csv_data.py
```

### **Manual Loading**
Load individual files using pandas:

```python
import pandas as pd
import sqlite3

# Load CSV into database
df = pd.read_csv('data/dim_region.csv')
conn = sqlite3.connect('data/telecom_db.sqlite')
df.to_sql('dim_region', conn, if_exists='replace', index=False)
conn.close()
```

---

## 📊 Business Views

The data warehouse includes 5 business semantic views:

1. **`vw_network_metrics_daily`** - Daily network performance aggregations
2. **`vw_customer_experience_daily`** - Daily customer experience metrics
3. **`vw_revenue_daily`** - Daily revenue and financial metrics
4. **`vw_usage_adoption_daily`** - Daily usage and adoption metrics
5. **`vw_operations_daily`** - Daily operational efficiency metrics

---

## 🎯 Data Quality

### **Validation Rules**
- All foreign key relationships are maintained
- Date formats are consistent (YYYY-MM-DD)
- Numeric values are properly formatted
- Boolean flags use 0/1 values
- Percentage values are in decimal format (0-1)

### **Data Completeness**
- **Dimension Tables**: 100% populated
- **Fact Tables**: Sample data for demonstration
- **Views**: Automatically generated from fact tables

---

## 🚀 Usage Examples

### **Load into Different Databases**

**PostgreSQL**:
```sql
COPY dim_region FROM 'data/dim_region.csv' WITH CSV HEADER;
```

**Snowflake**:
```sql
COPY INTO dim_region FROM @stage/dim_region.csv FILE_FORMAT = (TYPE = CSV);
```

**MySQL**:
```sql
LOAD DATA INFILE 'data/dim_region.csv' INTO TABLE dim_region FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES;
```

---

## 📋 File Summary

| File | Type | Rows | Purpose |
|------|------|------|---------|
| `dim_time.csv` | Dimension | 24 | Time master data |
| `dim_region.csv` | Dimension | 5 | Geographic regions |
| `dim_network_element.csv` | Dimension | 5 | Network infrastructure |
| `dim_customer.csv` | Dimension | 5 | Customer information |
| `dim_product.csv` | Dimension | 5 | Product catalog |
| `dim_channel.csv` | Dimension | 5 | Sales channels |
| `dim_employee.csv` | Dimension | 5 | Employee data |
| `fact_network_metrics.csv` | Fact | 5 | Network performance |
| `fact_customer_experience.csv` | Fact | 5 | Customer experience |
| `fact_revenue.csv` | Fact | 5 | Revenue metrics |
| `fact_usage_adoption.csv` | Fact | 5 | Usage metrics |
| `fact_operations.csv` | Fact | 5 | Operations metrics |

**Total**: 12 files, 89 rows of sample data 