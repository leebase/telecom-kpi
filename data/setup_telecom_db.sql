-- Telecom Database Setup
-- Generated from data/network_performance_schema.yaml
-- Created: 2025-07-31 19:58:00

-- Table: dim_region
-- Geographical grouping for network elements
CREATE TABLE IF NOT EXISTS dim_region (
    region_id TEXT PRIMARY KEY,
    region_name TEXT
);

-- Table: dim_network_element
-- Network infrastructure inventory
CREATE TABLE IF NOT EXISTS dim_network_element (
    network_element_id INTEGER PRIMARY KEY,
    element_name TEXT,
    element_type TEXT,
    vendor TEXT,
    install_date TEXT,
    region_id INTEGER,
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id)
);

-- Table: dim_time
-- Canonical time dimension
CREATE TABLE IF NOT EXISTS dim_time (
    date_id TEXT,
    hour INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    weekday TEXT,
    is_weekend INTEGER,
    PRIMARY KEY (date_id, hour)
);

-- Table: fact_network_metrics
-- Raw counters & pre-calc KPIs per hour
CREATE TABLE IF NOT EXISTS fact_network_metrics (
    network_element_id INTEGER,
    region_id INTEGER,
    date_id TEXT,
    hour INTEGER,
    last_updated_ts TEXT,
    uptime_seconds INTEGER,
    downtime_seconds INTEGER,
    calls_attempted INTEGER,
    calls_dropped INTEGER,
    packets_sent INTEGER,
    packets_lost INTEGER,
    bandwidth_capacity_mb REAL,
    bandwidth_used_mb REAL,
    outage_minutes REAL,
    repair_minutes REAL,
    availability_percent REAL,
    dropped_call_rate REAL,
    latency_ms REAL,
    latency_ms_p95 REAL,
    packet_loss_percent REAL,
    bandwidth_utilization_percent REAL,
    mttr_hours REAL,
    FOREIGN KEY (network_element_id) REFERENCES dim_network_element(network_element_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
    FOREIGN KEY (date_id) REFERENCES dim_time(date_id)
);

-- View: vw_network_metrics_daily
-- No comment
CREATE VIEW IF NOT EXISTS vw_network_metrics_daily AS
SELECT
  date_id,
  region_id,
  AVG(latency_ms)                         AS avg_latency_ms,
  AVG(latency_ms_p95)                     AS p95_latency_ms,
  SUM(packets_lost)  / NULLIF(SUM(packets_sent),0)   * 100 AS packet_loss_percent,
  SUM(calls_dropped) / NULLIF(SUM(calls_attempted),0) * 100 AS dropped_call_rate,
  SUM(uptime_seconds) /
  (SUM(uptime_seconds) + SUM(downtime_seconds)) * 100 AS availability_percent,
  SUM(bandwidth_used_mb) / NULLIF(SUM(bandwidth_capacity_mb),0) * 100 AS bandwidth_utilization_percent,
  AVG(repair_minutes) / 60 AS mttr_hours
FROM fact_network_metrics
GROUP BY date_id, region_id
