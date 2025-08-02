#!/usr/bin/env python3
"""
📊 Generate Comprehensive Telecom Test Data
Creates realistic test data for all fact tables with multiple dates and regional variations
Updates all CSV files with the new data
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_time_dimension():
    """Generate time dimension data for the last 90 days"""
    end_date = datetime(2023, 8, 1)
    start_date = end_date - timedelta(days=90)
    
    time_records = []
    current_date = start_date
    
    while current_date <= end_date:
        time_records.append({
            'date_id': current_date.strftime('%Y-%m-%d'),
            'year': current_date.year,
            'month': current_date.month,
            'day': current_date.day,
            'quarter': (current_date.month - 1) // 3 + 1,
            'is_month_end': 1 if current_date.month != (current_date + timedelta(days=1)).month else 0,
            'is_quarter_end': 1 if current_date.month in [3, 6, 9, 12] and current_date.day >= 28 else 0,
            'is_year_end': 1 if current_date.month == 12 and current_date.day >= 28 else 0
        })
        current_date += timedelta(days=1)
    
    return pd.DataFrame(time_records)

def generate_customer_experience_data():
    """Generate realistic customer experience data with multiple dates"""
    
    # Get region data
    regions_df = pd.read_csv('data/dim_region.csv')
    
    # Generate data for the last 30 days
    end_date = datetime(2023, 8, 1)
    start_date = end_date - timedelta(days=30)
    
    data_records = []
    
    for _, region in regions_df.iterrows():
        region_id = region['region_id']
        region_name = region['region_name']
        
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
    
    return pd.DataFrame(data_records)

def generate_network_metrics_data():
    """Generate realistic network metrics data with multiple dates"""
    
    regions_df = pd.read_csv('data/dim_region.csv')
    end_date = datetime(2023, 8, 1)
    start_date = end_date - timedelta(days=30)
    
    data_records = []
    
    for _, region in regions_df.iterrows():
        region_id = region['region_id']
        region_name = region['region_name']
        
        # Base values for each region
        base_availability = {
            'North Region': 99.5,
            'South Region': 99.8,
            'East Region': 99.2,
            'West Region': 99.9,
            'Central Region': 99.3
        }[region_name]
        
        base_latency = {
            'North Region': 45.0,
            'South Region': 38.0,
            'East Region': 52.0,
            'West Region': 35.0,
            'Central Region': 48.0
        }[region_name]
        
        base_packet_loss = {
            'North Region': 0.1,
            'South Region': 0.05,
            'East Region': 0.2,
            'West Region': 0.02,
            'Central Region': 0.15
        }[region_name]
        
        base_bandwidth = {
            'North Region': 65.0,
            'South Region': 72.0,
            'East Region': 58.0,
            'West Region': 78.0,
            'Central Region': 62.0
        }[region_name]
        
        base_mttr = {
            'North Region': 2.5,
            'South Region': 1.8,
            'East Region': 3.2,
            'West Region': 1.5,
            'Central Region': 2.8
        }[region_name]
        
        base_dropped_calls = {
            'North Region': 0.2,
            'South Region': 0.1,
            'East Region': 0.4,
            'West Region': 0.05,
            'Central Region': 0.3
        }[region_name]
        
        # Generate data for each day
        current_date = start_date
        while current_date <= end_date:
            # Add daily variation
            day_factor = 1 + np.random.normal(0, 0.02)
            
            # Add slight trend
            trend_factor = 1 + (current_date - start_date).days * 0.0005
            
            availability = max(95, min(100, base_availability * day_factor * trend_factor))
            latency = max(20, min(80, base_latency * day_factor))
            packet_loss = max(0, min(1, base_packet_loss * day_factor))
            bandwidth = max(40, min(90, base_bandwidth * day_factor * trend_factor))
            mttr = max(0.5, min(6, base_mttr * day_factor))
            dropped_calls = max(0, min(2, base_dropped_calls * day_factor))
            
            data_records.append({
                'network_element_id': np.random.randint(1, 6),
                'date_id': current_date.strftime('%Y-%m-%d'),
                'region_id': region_id,
                'uptime_seconds': int(availability * 86400 / 100),
                'downtime_seconds': int((100 - availability) * 86400 / 100),
                'latency_ms': round(latency, 1),
                'packet_loss_percent': round(packet_loss, 2),
                'bandwidth_utilization_percent': round(bandwidth, 1),
                'mttr_hours': round(mttr, 1),
                'dropped_call_rate': round(dropped_calls, 2)
            })
            
            current_date += timedelta(days=1)
    
    return pd.DataFrame(data_records)

def generate_revenue_data():
    """Generate realistic revenue data with multiple dates"""
    
    regions_df = pd.read_csv('data/dim_region.csv')
    end_date = datetime(2023, 8, 1)
    start_date = end_date - timedelta(days=30)
    
    data_records = []
    
    for _, region in regions_df.iterrows():
        region_id = region['region_id']
        region_name = region['region_name']
        
        # Base values for each region
        base_arpu = {
            'North Region': 76.0,
            'South Region': 89.0,
            'East Region': 65.0,
            'West Region': 95.0,
            'Central Region': 72.0
        }[region_name]
        
        base_ebitda = {
            'North Region': 32.0,
            'South Region': 35.0,
            'East Region': 28.0,
            'West Region': 38.0,
            'Central Region': 30.0
        }[region_name]
        
        base_cac = {
            'North Region': 170.0,
            'South Region': 200.0,
            'East Region': 150.0,
            'West Region': 220.0,
            'Central Region': 160.0
        }[region_name]
        
        base_clv = {
            'North Region': 2600.0,
            'South Region': 3200.0,
            'East Region': 2000.0,
            'West Region': 4000.0,
            'Central Region': 2400.0
        }[region_name]
        
        base_growth = {
            'North Region': 9.8,
            'South Region': 12.5,
            'East Region': 7.2,
            'West Region': 15.0,
            'Central Region': 8.5
        }[region_name]
        
        base_profit = {
            'North Region': 19.9,
            'South Region': 22.1,
            'East Region': 17.5,
            'West Region': 25.8,
            'Central Region': 18.7
        }[region_name]
        
        # Generate data for each day
        current_date = start_date
        while current_date <= end_date:
            # Add daily variation
            day_factor = 1 + np.random.normal(0, 0.03)
            
            # Add slight trend
            trend_factor = 1 + (current_date - start_date).days * 0.001
            
            arpu = max(50, base_arpu * day_factor * trend_factor)
            ebitda = max(20, min(50, base_ebitda * day_factor * trend_factor))
            cac = max(100, base_cac * day_factor)
            clv = max(1000, base_clv * day_factor * trend_factor)
            growth = max(5, min(25, base_growth * day_factor * trend_factor))
            profit = max(10, min(35, base_profit * day_factor * trend_factor))
            
            data_records.append({
                'customer_id': np.random.randint(1, 1000),
                'date_id': current_date.strftime('%Y-%m-%d'),
                'region_id': region_id,
                'revenue_amount': round(arpu * np.random.randint(80, 120), 2),
                'arpu': round(arpu, 2),
                'customer_acquisition_cost': round(cac, 0),
                'customer_lifetime_value': round(clv, 0),
                'ebitda_margin': round(ebitda, 1),
                'profit_margin': round(profit, 1),
                'subscriber_count': np.random.randint(1000, 5000),
                'subscriber_growth_rate': round(growth / 100, 3)
            })
            
            current_date += timedelta(days=1)
    
    return pd.DataFrame(data_records)

def generate_usage_adoption_data():
    """Generate realistic usage and adoption data with multiple dates"""
    
    regions_df = pd.read_csv('data/dim_region.csv')
    end_date = datetime(2023, 8, 1)
    start_date = end_date - timedelta(days=30)
    
    data_records = []
    
    for _, region in regions_df.iterrows():
        region_id = region['region_id']
        region_name = region['region_name']
        
        # Base values for each region
        base_data_usage = {
            'North Region': 11.5,
            'South Region': 14.2,
            'East Region': 9.8,
            'West Region': 16.5,
            'Central Region': 10.2
        }[region_name]
        
        base_5g_adoption = {
            'North Region': 71.0,
            'South Region': 78.0,
            'East Region': 65.0,
            'West Region': 82.0,
            'Central Region': 68.0
        }[region_name]
        
        base_feature_adoption = {
            'North Region': 70.4,
            'South Region': 75.2,
            'East Region': 65.8,
            'West Region': 80.1,
            'Central Region': 68.9
        }[region_name]
        
        base_service_penetration = {
            'North Region': 86.2,
            'South Region': 89.5,
            'East Region': 82.1,
            'West Region': 92.8,
            'Central Region': 84.7
        }[region_name]
        
        base_app_usage = {
            'North Region': 82.6,
            'South Region': 87.3,
            'East Region': 78.9,
            'West Region': 90.2,
            'Central Region': 81.4
        }[region_name]
        
        base_premium_adoption = {
            'North Region': 56.2,
            'South Region': 62.8,
            'East Region': 48.5,
            'West Region': 68.9,
            'Central Region': 52.1
        }[region_name]
        
        # Generate data for each day
        current_date = start_date
        while current_date <= end_date:
            # Add daily variation
            day_factor = 1 + np.random.normal(0, 0.04)
            
            # Add slight trend
            trend_factor = 1 + (current_date - start_date).days * 0.001
            
            data_usage = max(5, base_data_usage * day_factor * trend_factor)
            five_g_adoption = max(40, min(95, base_5g_adoption * day_factor * trend_factor))
            feature_adoption = max(50, min(90, base_feature_adoption * day_factor * trend_factor))
            service_penetration = max(70, min(98, base_service_penetration * day_factor * trend_factor))
            app_usage = max(60, min(95, base_app_usage * day_factor * trend_factor))
            premium_adoption = max(30, min(80, base_premium_adoption * day_factor * trend_factor))
            
            data_records.append({
                'customer_id': np.random.randint(1, 1000),
                'date_id': current_date.strftime('%Y-%m-%d'),
                'region_id': region_id,
                'data_usage_gb': round(data_usage, 1),
                'five_g_adoption': round(five_g_adoption / 100, 3),
                'feature_adoption_rate': round(feature_adoption / 100, 3),
                'service_penetration': round(service_penetration / 100, 3),
                'app_usage_rate': round(app_usage / 100, 3),
                'premium_service_adoption': round(premium_adoption / 100, 3),
                'active_subscribers': np.random.randint(500, 2000)
            })
            
            current_date += timedelta(days=1)
    
    return pd.DataFrame(data_records)

def generate_operations_data():
    """Generate realistic operations data with multiple dates"""
    
    regions_df = pd.read_csv('data/dim_region.csv')
    end_date = datetime(2023, 8, 1)
    start_date = end_date - timedelta(days=30)
    
    data_records = []
    
    for _, region in regions_df.iterrows():
        region_id = region['region_id']
        region_name = region['region_name']
        
        # Base values for each region
        base_response_time = {
            'North Region': 2.3,
            'South Region': 1.8,
            'East Region': 2.8,
            'West Region': 1.5,
            'Central Region': 2.5
        }[region_name]
        
        base_compliance = {
            'North Region': 98.7,
            'South Region': 99.2,
            'East Region': 98.5,
            'West Region': 99.5,
            'Central Region': 98.8
        }[region_name]
        
        base_resolution = {
            'North Region': 94.6,
            'South Region': 95.8,
            'East Region': 93.5,
            'West Region': 96.8,
            'Central Region': 94.2
        }[region_name]
        
        base_uptime = {
            'North Region': 99.91,
            'South Region': 99.88,
            'East Region': 99.95,
            'West Region': 99.96,
            'Central Region': 99.85
        }[region_name]
        
        base_efficiency = {
            'North Region': 86.7,
            'South Region': 84.7,
            'East Region': 89.1,
            'West Region': 91.2,
            'Central Region': 81.4
        }[region_name]
        
        base_capex = {
            'North Region': 18.4,
            'South Region': 19.1,
            'East Region': 17.8,
            'West Region': 16.5,
            'Central Region': 20.3
        }[region_name]
        
        base_productivity = {
            'North Region': 85.5,
            'South Region': 82.3,
            'East Region': 87.6,
            'West Region': 90.1,
            'Central Region': 79.8
        }[region_name]
        
        base_automation = {
            'North Region': 75.0,
            'South Region': 68.0,
            'East Region': 82.0,
            'West Region': 88.0,
            'Central Region': 62.0
        }[region_name]
        
        # Generate data for each day
        current_date = start_date
        while current_date <= end_date:
            # Add daily variation
            day_factor = 1 + np.random.normal(0, 0.03)
            
            # Add slight trend
            trend_factor = 1 + (current_date - start_date).days * 0.0005
            
            response_time = max(1, min(5, base_response_time * day_factor))
            compliance = max(95, min(100, base_compliance * day_factor * trend_factor))
            resolution = max(90, min(98, base_resolution * day_factor * trend_factor))
            uptime = max(99.5, min(99.99, base_uptime * day_factor * trend_factor))
            efficiency = max(75, min(95, base_efficiency * day_factor * trend_factor))
            capex = max(10, min(25, base_capex * day_factor))
            productivity = max(70, min(95, base_productivity * day_factor * trend_factor))
            automation = max(50, min(95, base_automation * day_factor * trend_factor))
            
            data_records.append({
                'employee_id': np.random.randint(1, 100),
                'date_id': current_date.strftime('%Y-%m-%d'),
                'region_id': region_id,
                'service_response_time_hours': round(response_time, 1),
                'regulatory_compliance_rate': round(compliance / 100, 3),
                'support_ticket_resolution_rate': round(resolution / 100, 3),
                'system_uptime_percentage': round(uptime, 2),
                'operational_efficiency_score': round(efficiency, 1),
                'capex_to_revenue_ratio': round(capex, 1),
                'employee_productivity_score': round(productivity, 1),
                'automation_rate': round(automation / 100, 3)
            })
            
            current_date += timedelta(days=1)
    
    return pd.DataFrame(data_records)

def update_csv_files():
    """Update all CSV files with the new generated data"""
    
    print("🔄 Updating CSV files with new test data...")
    
    # Generate new data
    time_df = generate_time_dimension()
    customer_df = generate_customer_experience_data()
    network_df = generate_network_metrics_data()
    revenue_df = generate_revenue_data()
    usage_df = generate_usage_adoption_data()
    operations_df = generate_operations_data()
    
    # Update CSV files
    csv_files = [
        ('data/dim_time.csv', time_df),
        ('data/fact_customer_experience.csv', customer_df),
        ('data/fact_network_metrics.csv', network_df),
        ('data/fact_revenue.csv', revenue_df),
        ('data/fact_usage_adoption.csv', usage_df),
        ('data/fact_operations.csv', operations_df)
    ]
    
    for file_path, df in csv_files:
        df.to_csv(file_path, index=False)
        print(f"✅ Updated {file_path} with {len(df)} records")
    
    print(f"\n📊 Summary:")
    print(f"📅 Time dimension: {len(time_df)} days")
    print(f"😊 Customer experience: {len(customer_df)} records")
    print(f"📡 Network metrics: {len(network_df)} records")
    print(f"💰 Revenue: {len(revenue_df)} records")
    print(f"📶 Usage adoption: {len(usage_df)} records")
    print(f"🛠️ Operations: {len(operations_df)} records")

def update_database():
    """Update the SQLite database with the new CSV data"""
    
    print("\n🗄️ Updating SQLite database...")
    
    # Connect to database
    conn = sqlite3.connect('data/telecom_db.sqlite')
    
    # Load CSV files into database
    csv_files = [
        ('data/fact_customer_experience.csv', 'fact_customer_experience'),
        ('data/fact_network_metrics.csv', 'fact_network_metrics'),
        ('data/fact_revenue.csv', 'fact_revenue'),
        ('data/fact_usage_adoption.csv', 'fact_usage_adoption'),
        ('data/fact_operations.csv', 'fact_operations')
    ]
    
    for csv_file, table_name in csv_files:
        df = pd.read_csv(csv_file)
        conn.execute(f"DELETE FROM {table_name}")
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"✅ Updated {table_name} with {len(df)} records")
    
    # Update views
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
    
    print("✅ Updated vw_customer_experience_daily view")
    
    conn.close()

def main():
    """Main function to generate and update all test data"""
    
    print("🚀 Generating comprehensive telecom test data...")
    print("=" * 60)
    
    # Update CSV files
    update_csv_files()
    
    # Update database
    update_database()
    
    print("\n🎉 All test data has been updated successfully!")
    print("📊 The dashboard now has realistic multi-day data with regional variations")

if __name__ == "__main__":
    main() 