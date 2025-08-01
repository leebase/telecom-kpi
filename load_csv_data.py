#!/usr/bin/env python3
"""
📊 Telecom Data Warehouse - CSV Data Loader
Loads all dimension and fact table CSV files into SQLite database
"""

import sqlite3
import pandas as pd
import os
from pathlib import Path

def load_csv_to_sqlite(csv_file, table_name, db_path):
    """Load CSV file into SQLite table"""
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        print(f"📁 Loading {csv_file} ({len(df)} rows) into {table_name}")
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        
        # Load data into table
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # Verify data was loaded
        result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"✅ Successfully loaded {result} rows into {table_name}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error loading {csv_file}: {e}")
        return False

def main():
    """Main function to load all CSV files"""
    print("🚀 Telecom Data Warehouse - CSV Data Loader")
    print("=" * 50)
    
    # Database path
    db_path = "data/telecom_db.sqlite"
    
    # CSV files to load (in order to respect foreign key constraints)
    csv_files = [
        # Dimension tables first
        ("data/dim_time.csv", "dim_time"),
        ("data/dim_region.csv", "dim_region"),
        ("data/dim_network_element.csv", "dim_network_element"),
        ("data/dim_customer.csv", "dim_customer"),
        ("data/dim_product.csv", "dim_product"),
        ("data/dim_channel.csv", "dim_channel"),
        ("data/dim_employee.csv", "dim_employee"),
        
        # Fact tables
        ("data/fact_network_metrics.csv", "fact_network_metrics"),
        ("data/fact_customer_experience.csv", "fact_customer_experience"),
        ("data/fact_revenue.csv", "fact_revenue"),
        ("data/fact_usage_adoption.csv", "fact_usage_adoption"),
        ("data/fact_operations.csv", "fact_operations"),
    ]
    
    # Track success/failure
    success_count = 0
    total_count = len(csv_files)
    
    # Load each CSV file
    for csv_file, table_name in csv_files:
        if os.path.exists(csv_file):
            if load_csv_to_sqlite(csv_file, table_name, db_path):
                success_count += 1
        else:
            print(f"⚠️  File not found: {csv_file}")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Data Loading Summary:")
    print(f"✅ Successfully loaded: {success_count}/{total_count} files")
    print(f"❌ Failed: {total_count - success_count} files")
    
    # Verify database state
    if success_count > 0:
        print("\n🔍 Database Verification:")
        conn = sqlite3.connect(db_path)
        
        # Check table counts
        tables = [
            "dim_time", "dim_region", "dim_network_element", 
            "dim_customer", "dim_product", "dim_channel", "dim_employee",
            "fact_network_metrics", "fact_customer_experience", 
            "fact_revenue", "fact_usage_adoption", "fact_operations"
        ]
        
        for table in tables:
            try:
                count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                print(f"📋 {table}: {count} rows")
            except Exception as e:
                print(f"❌ {table}: Error - {e}")
        
        # Check views
        views = [
            "vw_network_metrics_daily", "vw_customer_experience_daily",
            "vw_revenue_daily", "vw_usage_adoption_daily", "vw_operations_daily"
        ]
        
        print("\n🔍 View Verification:")
        for view in views:
            try:
                count = conn.execute(f"SELECT COUNT(*) FROM {view}").fetchone()[0]
                print(f"📊 {view}: {count} rows")
            except Exception as e:
                print(f"❌ {view}: Error - {e}")
        
        conn.close()
    
    print("\n🎉 CSV Data Loading Complete!")

if __name__ == "__main__":
    main() 