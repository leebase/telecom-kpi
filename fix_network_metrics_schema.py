#!/usr/bin/env python3
"""
🔧 Fix Network Metrics Schema
Updates the fact_network_metrics table schema to match the CSV structure
"""

import sqlite3

def fix_network_metrics_schema():
    """Fix the fact_network_metrics table schema"""
    
    conn = sqlite3.connect('data/telecom_db.sqlite')
    
    # Drop the existing table
    conn.execute("DROP TABLE IF EXISTS fact_network_metrics")
    
    # Create the table with the correct schema (no composite primary key)
    conn.execute("""
    CREATE TABLE fact_network_metrics (
        network_element_id INTEGER,
        date_id TEXT,
        region_id INTEGER,
        uptime_seconds INTEGER,
        downtime_seconds INTEGER,
        latency_ms REAL,
        packet_loss_percent REAL,
        bandwidth_utilization_percent REAL,
        mttr_hours REAL,
        dropped_call_rate REAL,
        FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
        FOREIGN KEY (date_id) REFERENCES dim_time(date_id)
    )
    """)
    
    print("✅ Updated fact_network_metrics table schema")
    
    # Update the view
    conn.execute("DROP VIEW IF EXISTS vw_network_metrics_daily")
    conn.execute("""
    CREATE VIEW vw_network_metrics_daily AS
    SELECT
        date_id,
        region_id,
        CAST(uptime_seconds AS REAL) / (CAST(uptime_seconds AS REAL) + CAST(downtime_seconds AS REAL)) * 100 AS availability_percent,
        AVG(latency_ms) AS avg_latency_ms,
        AVG(packet_loss_percent) AS avg_packet_loss_percent,
        AVG(bandwidth_utilization_percent) AS avg_bandwidth_utilization_percent,
        AVG(mttr_hours) AS avg_mttr_hours,
        AVG(dropped_call_rate) AS avg_dropped_call_rate,
        COUNT(DISTINCT network_element_id) AS active_elements,
        COUNT(DISTINCT date_id) AS days_with_data
    FROM fact_network_metrics
    GROUP BY date_id, region_id
    ORDER BY date_id, region_id
    """)
    
    print("✅ Updated vw_network_metrics_daily view")
    
    conn.close()

if __name__ == "__main__":
    fix_network_metrics_schema() 