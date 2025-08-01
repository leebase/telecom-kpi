import pandas as pd
import sqlite3
import os
from datetime import datetime, timedelta

def create_dimension_data():
    """Create dimension data for regions, network elements, and time"""
    
    # Create region dimension data
    regions_data = [
        {'region_id': 1, 'region_name': 'North Region'},
        {'region_id': 2, 'region_name': 'South Region'},
        {'region_id': 3, 'region_name': 'East Region'},
        {'region_id': 4, 'region_name': 'West Region'},
        {'region_id': 5, 'region_name': 'Central Region'}
    ]
    
    # Create network element dimension data
    network_elements_data = [
        {'network_element_id': 1, 'element_name': 'Router-North-01', 'element_type': 'Router', 'vendor': 'Cisco', 'install_date': '2023-01-15', 'region_id': 1},
        {'network_element_id': 2, 'element_name': 'Switch-South-01', 'element_type': 'Switch', 'vendor': 'Juniper', 'install_date': '2023-02-20', 'region_id': 2},
        {'network_element_id': 3, 'element_name': 'Router-East-01', 'element_type': 'Router', 'vendor': 'Cisco', 'install_date': '2023-03-10', 'region_id': 3},
        {'network_element_id': 4, 'element_name': 'Switch-West-01', 'element_type': 'Switch', 'vendor': 'Juniper', 'install_date': '2023-04-05', 'region_id': 4},
        {'network_element_id': 5, 'element_name': 'Router-Central-01', 'element_type': 'Router', 'vendor': 'Cisco', 'install_date': '2023-05-12', 'region_id': 5}
    ]
    
    # Create time dimension data for the date range in the CSV
    time_data = []
    start_date = datetime(2023, 8, 1)
    end_date = datetime(2023, 8, 31)  # Assuming one month of data
    
    current_date = start_date
    while current_date <= end_date:
        for hour in range(24):
            time_data.append({
                'date_id': current_date.strftime('%Y-%m-%d'),
                'hour': hour,
                'year': current_date.year,
                'month': current_date.month,
                'day': current_date.day,
                'weekday': current_date.strftime('%A'),
                'is_weekend': 1 if current_date.weekday() >= 5 else 0
            })
        current_date += timedelta(days=1)
    
    return regions_data, network_elements_data, time_data

def load_data_to_sqlite():
    """Load CSV data and dimension data into SQLite database"""
    
    db_path = "data/telecom_db.sqlite"
    csv_path = "data/fact_network_metrics_preview.csv"
    
    print("📊 Loading data into SQLite database...")
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        print("Please run setup_database.py first to create the database.")
        return
    
    # Check if CSV file exists
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create dimension data
        regions_data, network_elements_data, time_data = create_dimension_data()
        
        # Load dimension tables
        print("📋 Loading dimension tables...")
        
        # Load regions
        cursor.executemany(
            "INSERT OR REPLACE INTO dim_region (region_id, region_name) VALUES (?, ?)",
            [(r['region_id'], r['region_name']) for r in regions_data]
        )
        print(f"✅ Loaded {len(regions_data)} regions")
        
        # Load network elements
        cursor.executemany(
            "INSERT OR REPLACE INTO dim_network_element (network_element_id, element_name, element_type, vendor, install_date, region_id) VALUES (?, ?, ?, ?, ?, ?)",
            [(ne['network_element_id'], ne['element_name'], ne['element_type'], ne['vendor'], ne['install_date'], ne['region_id']) for ne in network_elements_data]
        )
        print(f"✅ Loaded {len(network_elements_data)} network elements")
        
        # Load time dimension
        cursor.executemany(
            "INSERT OR REPLACE INTO dim_time (date_id, hour, year, month, day, weekday, is_weekend) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [(t['date_id'], t['hour'], t['year'], t['month'], t['day'], t['weekday'], t['is_weekend']) for t in time_data]
        )
        print(f"✅ Loaded {len(time_data)} time records")
        
        # Load fact table data from CSV
        print("📈 Loading fact table data from CSV...")
        
        # Read CSV data
        df = pd.read_csv(csv_path)
        
        # Add last_updated_ts column
        df['last_updated_ts'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Convert DataFrame to list of tuples for insertion
        fact_data = []
        for _, row in df.iterrows():
            fact_data.append((
                row['network_element_id'],
                row['network_element_id'],  # Using network_element_id as region_id for simplicity
                row['date_id'],
                row['hour'],
                row['last_updated_ts'],
                row['uptime_seconds'],
                row['downtime_seconds'],
                row['calls_attempted'],
                row['calls_dropped'],
                row['packets_sent'],
                row['packets_lost'],
                row['bandwidth_capacity_mb'],
                row['bandwidth_used_mb'],
                row['outage_minutes'],
                row['repair_minutes'],
                row['availability_percent'],
                row['dropped_call_rate'],
                row['latency_ms'],
                row.get('latency_ms_p95', row['latency_ms']),  # Use latency_ms if p95 not available
                row['packet_loss_percent'],
                row['bandwidth_utilization_percent'],
                row['mttr_hours']
            ))
        
        # Insert fact data
        cursor.executemany("""
            INSERT OR REPLACE INTO fact_network_metrics (
                network_element_id, region_id, date_id, hour, last_updated_ts,
                uptime_seconds, downtime_seconds, calls_attempted, calls_dropped,
                packets_sent, packets_lost, bandwidth_capacity_mb, bandwidth_used_mb,
                outage_minutes, repair_minutes, availability_percent, dropped_call_rate,
                latency_ms, latency_ms_p95, packet_loss_percent, bandwidth_utilization_percent, mttr_hours
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, fact_data)
        
        print(f"✅ Loaded {len(fact_data)} fact records")
        
        # Commit changes
        conn.commit()
        
        # Verify data loaded
        print("\n📊 Data verification:")
        
        # Check record counts
        cursor.execute("SELECT COUNT(*) FROM dim_region")
        region_count = cursor.fetchone()[0]
        print(f"   Regions: {region_count}")
        
        cursor.execute("SELECT COUNT(*) FROM dim_network_element")
        element_count = cursor.fetchone()[0]
        print(f"   Network Elements: {element_count}")
        
        cursor.execute("SELECT COUNT(*) FROM dim_time")
        time_count = cursor.fetchone()[0]
        print(f"   Time Records: {time_count}")
        
        cursor.execute("SELECT COUNT(*) FROM fact_network_metrics")
        fact_count = cursor.fetchone()[0]
        print(f"   Fact Records: {fact_count}")
        
        # Test the view
        cursor.execute("SELECT COUNT(*) FROM vw_network_metrics_daily")
        view_count = cursor.fetchone()[0]
        print(f"   Daily Aggregates: {view_count}")
        
        print("\n🎉 Data loading complete!")
        print(f"📊 Database: {db_path}")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    """Main function to load data"""
    print("🚀 Telecom Database Data Loading")
    print("=" * 40)
    load_data_to_sqlite()

if __name__ == "__main__":
    main() 