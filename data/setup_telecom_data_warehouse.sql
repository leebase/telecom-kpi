-- 🏗️ Telecom Data Warehouse Setup Script
-- Comprehensive star schema for all 5 strategic KPI pillars
-- SQLite compatible implementation

-- ========================================
-- DIMENSION TABLES
-- ========================================

-- Time Dimension
CREATE TABLE IF NOT EXISTS dim_time (
    date_id TEXT,
    hour INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    weekday TEXT,
    is_weekend INTEGER,
    quarter INTEGER,
    is_month_end INTEGER,
    is_quarter_end INTEGER,
    is_year_end INTEGER,
    PRIMARY KEY (date_id, hour)
);

-- Geographic Dimension
CREATE TABLE IF NOT EXISTS dim_region (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT,
    country TEXT,
    timezone TEXT,
    market_type TEXT,
    population_density TEXT
);

-- Network Infrastructure Dimension
CREATE TABLE IF NOT EXISTS dim_network_element (
    network_element_id INTEGER PRIMARY KEY,
    element_type TEXT,
    element_name TEXT,
    location TEXT,
    capacity_mbps REAL,
    technology TEXT,
    vendor TEXT,
    installation_date TEXT
);

-- Customer Dimension
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INTEGER PRIMARY KEY,
    customer_type TEXT,
    segment TEXT,
    region_id INTEGER,
    acquisition_date TEXT,
    contract_type TEXT,
    credit_score INTEGER,
    lifetime_value REAL,
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id)
);

-- Product/Service Dimension
CREATE TABLE IF NOT EXISTS dim_product (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    product_category TEXT,
    product_type TEXT,
    data_limit_gb REAL,
    price_monthly REAL,
    is_premium INTEGER,
    launch_date TEXT
);

-- Channel Dimension
CREATE TABLE IF NOT EXISTS dim_channel (
    channel_id INTEGER PRIMARY KEY,
    channel_name TEXT,
    channel_type TEXT,
    channel_category TEXT,
    is_digital INTEGER,
    cost_per_interaction REAL
);

-- Employee Dimension
CREATE TABLE IF NOT EXISTS dim_employee (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT,
    department TEXT,
    role TEXT,
    hire_date TEXT,
    region_id INTEGER,
    is_active INTEGER,
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id)
);

-- ========================================
-- FACT TABLES
-- ========================================

-- Network Performance Facts
CREATE TABLE IF NOT EXISTS fact_network_metrics (
    network_element_id INTEGER,
    region_id INTEGER,
    date_id TEXT,
    hour INTEGER,
    uptime_seconds REAL,
    downtime_seconds REAL,
    calls_attempted INTEGER,
    calls_dropped INTEGER,
    packets_sent INTEGER,
    packets_lost INTEGER,
    bandwidth_capacity_mb REAL,
    bandwidth_used_mb REAL,
    outage_minutes REAL,
    repair_minutes REAL,
    latency_ms REAL,
    latency_ms_p95 REAL,
    last_updated_ts TEXT,
    PRIMARY KEY (network_element_id, region_id, date_id, hour),
    FOREIGN KEY (network_element_id) REFERENCES dim_network_element(network_element_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
    FOREIGN KEY (date_id, hour) REFERENCES dim_time(date_id, hour)
);

-- Customer Experience Facts
CREATE TABLE IF NOT EXISTS fact_customer_experience (
    customer_id INTEGER,
    date_id TEXT,
    region_id INTEGER,
    channel_id INTEGER,
    satisfaction_score REAL,
    nps_score INTEGER,
    churn_probability REAL,
    handling_time_minutes REAL,
    first_contact_resolution REAL,
    complaint_count INTEGER,
    escalation_count INTEGER,
    customer_effort_score REAL,
    lifetime_value REAL,
    PRIMARY KEY (customer_id, date_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (date_id) REFERENCES dim_time(date_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
    FOREIGN KEY (channel_id) REFERENCES dim_channel(channel_id)
);

-- Revenue and Monetization Facts
CREATE TABLE IF NOT EXISTS fact_revenue (
    customer_id INTEGER,
    product_id INTEGER,
    date_id TEXT,
    region_id INTEGER,
    channel_id INTEGER,
    revenue_amount REAL,
    arpu REAL,
    customer_acquisition_cost REAL,
    customer_lifetime_value REAL,
    churn_revenue_loss REAL,
    upsell_revenue REAL,
    cross_sell_revenue REAL,
    ebitda_margin REAL,
    profit_margin REAL,
    subscriber_count INTEGER,
    subscriber_growth_rate REAL,
    PRIMARY KEY (customer_id, product_id, date_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (date_id) REFERENCES dim_time(date_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
    FOREIGN KEY (channel_id) REFERENCES dim_channel(channel_id)
);

-- Usage and Adoption Facts
CREATE TABLE IF NOT EXISTS fact_usage_adoption (
    customer_id INTEGER,
    product_id INTEGER,
    date_id TEXT,
    region_id INTEGER,
    data_usage_gb REAL,
    voice_minutes REAL,
    sms_count INTEGER,
    feature_adoption_rate REAL,
    five_g_adoption REAL,
    service_penetration REAL,
    app_usage_rate REAL,
    premium_service_adoption REAL,
    peak_usage_time TEXT,
    average_session_duration REAL,
    active_subscribers INTEGER,
    PRIMARY KEY (customer_id, product_id, date_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (date_id) REFERENCES dim_time(date_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id)
);

-- Operational Efficiency Facts
CREATE TABLE IF NOT EXISTS fact_operations (
    employee_id INTEGER,
    region_id INTEGER,
    date_id TEXT,
    channel_id INTEGER,
    service_response_time_hours REAL,
    regulatory_compliance_rate REAL,
    support_ticket_resolution_rate REAL,
    system_uptime_percentage REAL,
    operational_efficiency_score REAL,
    capex_to_revenue_ratio REAL,
    employee_productivity_score REAL,
    cost_per_customer REAL,
    automation_rate REAL,
    training_completion_rate REAL,
    incident_count INTEGER,
    resolution_time_hours REAL,
    PRIMARY KEY (employee_id, region_id, date_id),
    FOREIGN KEY (employee_id) REFERENCES dim_employee(employee_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
    FOREIGN KEY (date_id) REFERENCES dim_time(date_id),
    FOREIGN KEY (channel_id) REFERENCES dim_channel(channel_id)
);

-- ========================================
-- BUSINESS SEMANTIC VIEWS
-- ========================================

-- Network Performance Views
DROP VIEW IF EXISTS vw_network_metrics_daily;
CREATE VIEW vw_network_metrics_daily AS
SELECT
    date_id,
    region_id,
    AVG(CAST(latency_ms AS REAL)) AS avg_latency_ms,
    AVG(CAST(latency_ms_p95 AS REAL)) AS p95_latency_ms,
    SUM(CAST(packets_lost AS REAL)) / NULLIF(SUM(CAST(packets_sent AS REAL)), 0) * 100 AS packet_loss_percent,
    SUM(CAST(calls_dropped AS REAL)) / NULLIF(SUM(CAST(calls_attempted AS REAL)), 0) * 100 AS dropped_call_rate,
    SUM(CAST(uptime_seconds AS REAL)) / (SUM(CAST(uptime_seconds AS REAL)) + SUM(CAST(downtime_seconds AS REAL))) * 100 AS availability_percent,
    SUM(CAST(bandwidth_used_mb AS REAL)) / NULLIF(SUM(CAST(bandwidth_capacity_mb AS REAL)), 0) * 100 AS bandwidth_utilization_percent,
    AVG(CAST(repair_minutes AS REAL)) / 60 AS mttr_hours,
    COUNT(DISTINCT network_element_id) AS active_elements,
    COUNT(DISTINCT region_id) AS active_regions
FROM fact_network_metrics
GROUP BY date_id, region_id;

-- Customer Experience Views
DROP VIEW IF EXISTS vw_customer_experience_daily;
CREATE VIEW vw_customer_experience_daily AS
SELECT
    date_id,
    region_id,
    AVG(satisfaction_score) AS avg_satisfaction_score,
    AVG(nps_score) AS avg_nps_score,
    AVG(churn_probability) * 100 AS avg_churn_rate,
    AVG(handling_time_minutes) AS avg_handling_time,
    AVG(first_contact_resolution) * 100 AS first_contact_resolution_rate,
    AVG(customer_effort_score) AS avg_customer_effort_score,
    AVG(lifetime_value) AS avg_lifetime_value,
    COUNT(DISTINCT customer_id) AS active_customers
FROM fact_customer_experience
GROUP BY date_id, region_id;

-- Revenue Views
DROP VIEW IF EXISTS vw_revenue_daily;
CREATE VIEW vw_revenue_daily AS
SELECT
    date_id,
    region_id,
    SUM(revenue_amount) AS total_revenue,
    AVG(arpu) AS avg_arpu,
    AVG(customer_acquisition_cost) AS avg_cac,
    AVG(customer_lifetime_value) AS avg_clv,
    AVG(ebitda_margin) AS avg_ebitda_margin,
    AVG(profit_margin) AS avg_profit_margin,
    SUM(subscriber_count) AS total_subscribers,
    AVG(subscriber_growth_rate) AS avg_growth_rate
FROM fact_revenue
GROUP BY date_id, region_id;

-- Usage and Adoption Views
DROP VIEW IF EXISTS vw_usage_adoption_daily;
CREATE VIEW vw_usage_adoption_daily AS
SELECT
    date_id,
    region_id,
    AVG(data_usage_gb) AS avg_data_usage,
    AVG(feature_adoption_rate) * 100 AS avg_feature_adoption,
    AVG(five_g_adoption) * 100 AS avg_five_g_adoption,
    AVG(service_penetration) * 100 AS avg_service_penetration,
    AVG(app_usage_rate) * 100 AS avg_app_usage,
    AVG(premium_service_adoption) * 100 AS avg_premium_adoption,
    SUM(active_subscribers) AS total_active_subscribers
FROM fact_usage_adoption
GROUP BY date_id, region_id;

-- Operations Views
DROP VIEW IF EXISTS vw_operations_daily;
CREATE VIEW vw_operations_daily AS
SELECT
    date_id,
    region_id,
    AVG(service_response_time_hours) AS avg_response_time,
    AVG(regulatory_compliance_rate) * 100 AS avg_compliance_rate,
    AVG(support_ticket_resolution_rate) * 100 AS avg_resolution_rate,
    AVG(system_uptime_percentage) AS avg_uptime,
    AVG(operational_efficiency_score) AS avg_efficiency_score,
    AVG(capex_to_revenue_ratio) AS avg_capex_ratio,
    AVG(employee_productivity_score) AS avg_productivity,
    AVG(automation_rate) * 100 AS avg_automation_rate
FROM fact_operations
GROUP BY date_id, region_id;

-- ========================================
-- SAMPLE DATA INSERTION
-- ========================================

-- Insert sample time data
INSERT OR REPLACE INTO dim_time (date_id, hour, year, month, day, weekday, is_weekend, quarter, is_month_end, is_quarter_end, is_year_end) VALUES
('2023-08-01', 0, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 1, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 2, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 3, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 4, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 5, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 6, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 7, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 8, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 9, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 10, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 11, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 12, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 13, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 14, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 15, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 16, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 17, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 18, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 19, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 20, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 21, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 22, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0),
('2023-08-01', 23, 2023, 8, 1, 'Tuesday', 0, 3, 0, 0, 0);

-- Insert sample region data
INSERT OR REPLACE INTO dim_region (region_id, region_name, country, timezone, market_type, population_density) VALUES
(1, 'North Region', 'USA', 'UTC-5', 'Urban', 'High'),
(2, 'South Region', 'USA', 'UTC-6', 'Suburban', 'Medium'),
(3, 'East Region', 'USA', 'UTC-4', 'Urban', 'High'),
(4, 'West Region', 'USA', 'UTC-8', 'Mixed', 'Medium'),
(5, 'Central Region', 'USA', 'UTC-6', 'Rural', 'Low');

-- Insert sample network element data
INSERT OR REPLACE INTO dim_network_element (network_element_id, element_type, element_name, location, capacity_mbps, technology, vendor, installation_date) VALUES
(1, 'Tower', 'Tower-North-001', 'North Region', 1000.0, '5G', 'Ericsson', '2023-01-15'),
(2, 'Switch', 'Switch-South-001', 'South Region', 500.0, '4G', 'Cisco', '2023-02-20'),
(3, 'Router', 'Router-East-001', 'East Region', 750.0, '5G', 'Nokia', '2023-03-10'),
(4, 'Tower', 'Tower-West-001', 'West Region', 1200.0, '5G', 'Ericsson', '2023-01-25'),
(5, 'Switch', 'Switch-Central-001', 'Central Region', 400.0, '4G', 'Cisco', '2023-04-05');

-- Insert sample customer data
INSERT OR REPLACE INTO dim_customer (customer_id, customer_type, segment, region_id, acquisition_date, contract_type, credit_score, lifetime_value) VALUES
(1, 'Consumer', 'Premium', 1, '2023-01-15', 'Postpaid', 750, 2500.0),
(2, 'Business', 'Standard', 2, '2023-02-20', 'Enterprise', 800, 5000.0),
(3, 'Consumer', 'Basic', 3, '2023-03-10', 'Prepaid', 650, 1200.0),
(4, 'Enterprise', 'Premium', 4, '2023-01-25', 'Enterprise', 900, 15000.0),
(5, 'Consumer', 'Standard', 5, '2023-04-05', 'Postpaid', 700, 1800.0);

-- Insert sample product data
INSERT OR REPLACE INTO dim_product (product_id, product_name, product_category, product_type, data_limit_gb, price_monthly, is_premium, launch_date) VALUES
(1, 'Unlimited 5G', 'Data', 'Plan', 100.0, 89.99, 1, '2023-01-01'),
(2, 'Business Pro', 'Data', 'Plan', 200.0, 149.99, 1, '2023-02-01'),
(3, 'Basic 4G', 'Data', 'Plan', 10.0, 29.99, 0, '2023-03-01'),
(4, 'Enterprise Suite', 'Data', 'Plan', 500.0, 299.99, 1, '2023-01-15'),
(5, 'Standard 5G', 'Data', 'Plan', 50.0, 59.99, 0, '2023-04-01');

-- Insert sample channel data
INSERT OR REPLACE INTO dim_channel (channel_id, channel_name, channel_type, channel_category, is_digital, cost_per_interaction) VALUES
(1, 'Online Store', 'Online', 'Sales', 1, 5.0),
(2, 'Retail Store', 'Retail', 'Sales', 0, 25.0),
(3, 'Call Center', 'Call Center', 'Support', 0, 15.0),
(4, 'Mobile App', 'Online', 'Self-Service', 1, 2.0),
(5, 'Partner Store', 'Partner', 'Sales', 0, 20.0);

-- Insert sample employee data
INSERT OR REPLACE INTO dim_employee (employee_id, employee_name, department, role, hire_date, region_id, is_active) VALUES
(1, 'John Smith', 'Network Ops', 'Network Engineer', '2023-01-15', 1, 1),
(2, 'Sarah Johnson', 'Customer Service', 'Support Specialist', '2023-02-20', 2, 1),
(3, 'Mike Davis', 'Sales', 'Account Manager', '2023-03-10', 3, 1),
(4, 'Lisa Wilson', 'Network Ops', 'Network Manager', '2023-01-25', 4, 1),
(5, 'Tom Brown', 'Customer Service', 'Team Lead', '2023-04-05', 5, 1);

-- Insert sample network metrics data (using existing data structure)
INSERT OR REPLACE INTO fact_network_metrics (network_element_id, region_id, date_id, hour, uptime_seconds, downtime_seconds, calls_attempted, calls_dropped, packets_sent, packets_lost, bandwidth_capacity_mb, bandwidth_used_mb, outage_minutes, repair_minutes, latency_ms, latency_ms_p95, last_updated_ts) VALUES
(1, 1, '2023-08-01', 0, 86158, 242, 758, 7, 183726, 230, 1000, 575, 4.033333333333333, 138, 35.0, 45.0, '2023-08-01 00:00:00'),
(2, 2, '2023-08-01', 0, 85920, 480, 642, 12, 156789, 312, 800, 420, 8.0, 180, 42.0, 52.0, '2023-08-01 00:00:00'),
(3, 3, '2023-08-01', 0, 86340, 60, 892, 3, 201234, 156, 1200, 680, 1.0, 90, 38.0, 48.0, '2023-08-01 00:00:00'),
(4, 4, '2023-08-01', 0, 86400, 0, 1023, 0, 245678, 0, 1500, 890, 0.0, 0, 32.0, 40.0, '2023-08-01 00:00:00'),
(5, 5, '2023-08-01', 0, 85680, 720, 445, 15, 98765, 445, 600, 280, 12.0, 240, 55.0, 65.0, '2023-08-01 00:00:00');

-- Insert sample customer experience data
INSERT OR REPLACE INTO fact_customer_experience (customer_id, date_id, region_id, channel_id, satisfaction_score, nps_score, churn_probability, handling_time_minutes, first_contact_resolution, complaint_count, escalation_count, customer_effort_score, lifetime_value) VALUES
(1, '2023-08-01', 1, 1, 85.0, 45, 0.05, 3.2, 0.85, 1, 0, 2.5, 2500.0),
(2, '2023-08-01', 2, 3, 92.0, 52, 0.03, 4.8, 0.92, 0, 0, 2.1, 5000.0),
(3, '2023-08-01', 3, 4, 78.0, 38, 0.08, 2.5, 0.78, 2, 1, 3.2, 1200.0),
(4, '2023-08-01', 4, 2, 95.0, 58, 0.02, 6.1, 0.95, 0, 0, 1.8, 15000.0),
(5, '2023-08-01', 5, 3, 82.0, 42, 0.06, 3.8, 0.82, 1, 0, 2.8, 1800.0);

-- Insert sample revenue data
INSERT OR REPLACE INTO fact_revenue (customer_id, product_id, date_id, region_id, channel_id, revenue_amount, arpu, customer_acquisition_cost, customer_lifetime_value, churn_revenue_loss, upsell_revenue, cross_sell_revenue, ebitda_margin, profit_margin, subscriber_count, subscriber_growth_rate) VALUES
(1, 1, '2023-08-01', 1, 1, 89.99, 89.99, 125.0, 2500.0, 0.0, 15.0, 8.0, 32.5, 18.7, 1, 0.08),
(2, 2, '2023-08-01', 2, 3, 149.99, 149.99, 200.0, 5000.0, 0.0, 25.0, 12.0, 35.2, 22.1, 1, 0.12),
(3, 3, '2023-08-01', 3, 4, 29.99, 29.99, 75.0, 1200.0, 0.0, 5.0, 3.0, 28.1, 15.3, 1, 0.05),
(4, 4, '2023-08-01', 4, 2, 299.99, 299.99, 350.0, 15000.0, 0.0, 45.0, 20.0, 38.5, 25.8, 1, 0.15),
(5, 5, '2023-08-01', 5, 3, 59.99, 59.99, 100.0, 1800.0, 0.0, 10.0, 6.0, 30.2, 17.5, 1, 0.09);

-- Insert sample usage adoption data
INSERT OR REPLACE INTO fact_usage_adoption (customer_id, product_id, date_id, region_id, data_usage_gb, voice_minutes, sms_count, feature_adoption_rate, five_g_adoption, service_penetration, app_usage_rate, premium_service_adoption, peak_usage_time, average_session_duration, active_subscribers) VALUES
(1, 1, '2023-08-01', 1, 8.5, 120, 45, 0.75, 0.85, 0.92, 0.88, 0.65, '8-10 PM', 45.2, 1),
(2, 2, '2023-08-01', 2, 12.3, 180, 67, 0.82, 0.78, 0.89, 0.92, 0.78, '9-11 PM', 52.8, 1),
(3, 3, '2023-08-01', 3, 4.2, 85, 23, 0.45, 0.35, 0.72, 0.65, 0.28, '7-9 PM', 28.5, 1),
(4, 4, '2023-08-01', 4, 25.7, 300, 120, 0.95, 0.92, 0.98, 0.96, 0.88, '10-12 PM', 78.3, 1),
(5, 5, '2023-08-01', 5, 6.8, 95, 34, 0.58, 0.62, 0.81, 0.72, 0.42, '8-10 PM', 35.7, 1);

-- Insert sample operations data
INSERT OR REPLACE INTO fact_operations (employee_id, region_id, date_id, channel_id, service_response_time_hours, regulatory_compliance_rate, support_ticket_resolution_rate, system_uptime_percentage, operational_efficiency_score, capex_to_revenue_ratio, employee_productivity_score, cost_per_customer, automation_rate, training_completion_rate, incident_count, resolution_time_hours) VALUES
(1, 1, '2023-08-01', 3, 2.1, 0.987, 0.942, 99.92, 87.3, 18.2, 85.5, 12.5, 0.75, 0.92, 2, 3.5),
(2, 2, '2023-08-01', 3, 2.8, 0.992, 0.958, 99.88, 84.7, 19.1, 82.3, 14.2, 0.68, 0.89, 3, 4.2),
(3, 3, '2023-08-01', 4, 1.9, 0.985, 0.935, 99.95, 89.1, 17.8, 87.6, 11.8, 0.82, 0.94, 1, 2.8),
(4, 4, '2023-08-01', 2, 2.3, 0.995, 0.968, 99.96, 91.2, 16.5, 90.1, 10.5, 0.88, 0.97, 0, 2.1),
(5, 5, '2023-08-01', 3, 3.2, 0.978, 0.925, 99.85, 81.4, 20.3, 79.8, 15.8, 0.62, 0.86, 4, 5.1);

-- ========================================
-- VERIFICATION QUERIES
-- ========================================

-- Verify data insertion
SELECT 'Time Dimension' as table_name, COUNT(*) as record_count FROM dim_time
UNION ALL
SELECT 'Region Dimension', COUNT(*) FROM dim_region
UNION ALL
SELECT 'Network Element Dimension', COUNT(*) FROM dim_network_element
UNION ALL
SELECT 'Customer Dimension', COUNT(*) FROM dim_customer
UNION ALL
SELECT 'Product Dimension', COUNT(*) FROM dim_product
UNION ALL
SELECT 'Channel Dimension', COUNT(*) FROM dim_channel
UNION ALL
SELECT 'Employee Dimension', COUNT(*) FROM dim_employee
UNION ALL
SELECT 'Network Metrics Facts', COUNT(*) FROM fact_network_metrics
UNION ALL
SELECT 'Customer Experience Facts', COUNT(*) FROM fact_customer_experience
UNION ALL
SELECT 'Revenue Facts', COUNT(*) FROM fact_revenue
UNION ALL
SELECT 'Usage Adoption Facts', COUNT(*) FROM fact_usage_adoption
UNION ALL
SELECT 'Operations Facts', COUNT(*) FROM fact_operations;

-- Test view functionality
SELECT 'Network Metrics Daily View' as view_name, COUNT(*) as record_count FROM vw_network_metrics_daily
UNION ALL
SELECT 'Customer Experience Daily View', COUNT(*) FROM vw_customer_experience_daily
UNION ALL
SELECT 'Revenue Daily View', COUNT(*) FROM vw_revenue_daily
UNION ALL
SELECT 'Usage Adoption Daily View', COUNT(*) FROM vw_usage_adoption_daily
UNION ALL
SELECT 'Operations Daily View', COUNT(*) FROM vw_operations_daily; 