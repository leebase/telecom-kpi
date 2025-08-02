#!/usr/bin/env python3
"""
📊 Generate Better Customer Experience Test Data
Creates realistic customer experience data with multiple dates and regional variations
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_customer_experience_data():
    """Generate realistic customer experience data with multiple dates"""
    
    # Connect to database
    conn = sqlite3.connect('data/telecom_db.sqlite')
    
    # Get region data
    regions_df = pd.read_sql_query("SELECT region_id, region_name FROM dim_region", conn)
    
    # Generate data for the last 30 days
    end_date = datetime(2023, 8, 1)
    start_date = end_date - timedelta(days=30)
    
    data_records = []
    
    for region_id, region_name in zip(regions_df['region_id'], regions_df['region_name']):
        # Base values for each region
        base_satisfaction = {
            'North Region': 85.0,
            'South Region': 92.0,
            'East Region': 78.0,
            'West Region': 95.0,
            'Central Region': 82.0
        }[region_name]
        
        base_nps = {
            'North Region': 45.0,
            'South Region': 52.0,
            'East Region': 38.0,
            'West Region': 58.0,
            'Central Region': 42.0
        }[region_name]
        
        base_churn = {
            'North Region': 5.0,
            'South Region': 3.0,
            'East Region': 8.0,
            'West Region': 2.0,
            'Central Region': 6.0
        }[region_name]
        
        base_handling_time = {
            'North Region': 3.2,
            'South Region': 4.8,
            'East Region': 2.5,
            'West Region': 6.1,
            'Central Region': 3.8
        }[region_name]
        
        base_fcr = {
            'North Region': 85.0,
            'South Region': 92.0,
            'East Region': 78.0,
            'West Region': 95.0,
            'Central Region': 82.0
        }[region_name]
        
        base_effort = {
            'North Region': 2.5,
            'South Region': 2.1,
            'East Region': 3.2,
            'West Region': 1.8,
            'Central Region': 2.8
        }[region_name]
        
        base_clv = {
            'North Region': 2500.0,
            'South Region': 5000.0,
            'East Region': 1200.0,
            'West Region': 15000.0,
            'Central Region': 1800.0
        }[region_name]
        
        # Generate data for each day
        current_date = start_date
        while current_date <= end_date:
            # Add some daily variation (±5% for most metrics, ±10% for churn)
            day_factor = 1 + np.random.normal(0, 0.05)
            churn_factor = 1 + np.random.normal(0, 0.10)
            
            # Add trend (slight improvement over time)
            trend_factor = 1 + (current_date - start_date).days * 0.001
            
            satisfaction = max(0, min(100, base_satisfaction * day_factor * trend_factor))
            nps = max(-100, min(100, base_nps * day_factor * trend_factor))
            churn = max(0, min(20, base_churn * churn_factor))
            handling_time = max(1, min(10, base_handling_time * day_factor))
            fcr = max(0, min(100, base_fcr * day_factor * trend_factor))
            effort = max(1, min(5, base_effort * day_factor))
            clv = max(500, base_clv * day_factor * trend_factor)
            
            data_records.append({
                'customer_id': np.random.randint(1, 1000),
                'date_id': current_date.strftime('%Y-%m-%d'),
                'region_id': region_id,
                'channel_id': np.random.randint(1, 6),
                'satisfaction_score': round(satisfaction, 1),
                'nps_score': round(nps),
                'churn_probability': round(churn / 100, 3),
                'handling_time_minutes': round(handling_time, 1),
                'first_contact_resolution': round(fcr / 100, 3),
                'complaint_count': np.random.randint(0, 5),
                'escalation_count': np.random.randint(0, 3),
                'customer_effort_score': round(effort, 1),
                'lifetime_value': round(clv, 0)
            })
            
            current_date += timedelta(days=1)
    
    # Create DataFrame
    df = pd.DataFrame(data_records)
    
    # Clear existing data and insert new data
    conn.execute("DELETE FROM fact_customer_experience")
    df.to_sql('fact_customer_experience', conn, if_exists='append', index=False)
    
    # Update the view
    conn.execute("DROP VIEW IF EXISTS vw_customer_experience_daily")
    conn.execute("""
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
    GROUP BY date_id, region_id
    ORDER BY date_id, region_id
    """)
    
    print(f"✅ Generated {len(data_records)} customer experience records")
    print(f"📅 Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Verify the data
    result = conn.execute("SELECT COUNT(*) FROM fact_customer_experience").fetchone()[0]
    print(f"📊 Total records in fact_customer_experience: {result}")
    
    result = conn.execute("SELECT COUNT(*) FROM vw_customer_experience_daily").fetchone()[0]
    print(f"📊 Total records in vw_customer_experience_daily: {result}")
    
    # Show sample data
    sample = pd.read_sql_query("""
    SELECT date_id, region_id, avg_satisfaction_score, avg_nps_score, avg_churn_rate, avg_handling_time
    FROM vw_customer_experience_daily 
    ORDER BY date_id DESC, region_id 
    LIMIT 10
    """, conn)
    print("\n📋 Sample data:")
    print(sample)
    
    conn.close()

if __name__ == "__main__":
    generate_customer_experience_data() 