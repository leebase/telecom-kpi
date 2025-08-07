import sqlite3
import pandas as pd
import os
from datetime import datetime

def setup_benchmark_tables():
    """Set up benchmark tables in the SQLite database"""
    
    # Connect to the database
    db_path = "data/telecom_db.sqlite"
    conn = sqlite3.connect(db_path)
    
    # Create benchmark targets table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS benchmark_targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kpi_name TEXT UNIQUE NOT NULL,
            peer_avg REAL,
            industry_avg REAL,
            unit TEXT,
            direction TEXT,
            threshold_low REAL,
            threshold_high REAL,
            last_updated TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Load data from CSV if it exists
    csv_path = "data/benchmark_targets.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # Clear existing data
        conn.execute("DELETE FROM benchmark_targets")
        
        # Insert data from CSV
        for _, row in df.iterrows():
            conn.execute('''
                INSERT INTO benchmark_targets 
                (kpi_name, peer_avg, industry_avg, unit, direction, threshold_low, threshold_high, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['kpi_name'],
                row['peer_avg'],
                row['industry_avg'],
                row['unit'],
                row['direction'],
                row['threshold_low'],
                row['threshold_high'],
                row['last_updated']
            ))
        
        print(f"✅ Loaded {len(df)} benchmark targets from CSV")
    else:
        print("⚠️  CSV file not found, creating empty table")
    
    # Create benchmark history table for tracking changes
    conn.execute('''
        CREATE TABLE IF NOT EXISTS benchmark_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kpi_name TEXT NOT NULL,
            old_peer_avg REAL,
            new_peer_avg REAL,
            old_industry_avg REAL,
            new_industry_avg REAL,
            changed_by TEXT,
            change_reason TEXT,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Benchmark tables created successfully")

def export_benchmarks_to_csv():
    """Export current benchmarks from database to CSV"""
    db_path = "data/telecom_db.sqlite"
    conn = sqlite3.connect(db_path)
    
    df = pd.read_sql_query("SELECT * FROM benchmark_targets", conn)
    
    # Remove the id column for CSV export
    df = df.drop('id', axis=1)
    df = df.drop('created_at', axis=1)
    
    csv_path = "data/benchmark_targets.csv"
    df.to_csv(csv_path, index=False)
    
    conn.close()
    print(f"✅ Exported {len(df)} benchmarks to {csv_path}")

def import_benchmarks_from_csv():
    """Import benchmarks from CSV to database"""
    csv_path = "data/benchmark_targets.csv"
    if not os.path.exists(csv_path):
        print("❌ CSV file not found")
        return
    
    db_path = "data/telecom_db.sqlite"
    conn = sqlite3.connect(db_path)
    
    df = pd.read_csv(csv_path)
    
    # Clear existing data
    conn.execute("DELETE FROM benchmark_targets")
    
    # Insert data from CSV
    for _, row in df.iterrows():
        conn.execute('''
            INSERT INTO benchmark_targets 
            (kpi_name, peer_avg, industry_avg, unit, direction, threshold_low, threshold_high, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['kpi_name'],
            row['peer_avg'],
            row['industry_avg'],
            row['unit'],
            row['direction'],
            row['threshold_low'],
            row['threshold_high'],
            row['last_updated']
        ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Imported {len(df)} benchmarks from CSV")

if __name__ == "__main__":
    print("Setting up benchmark tables...")
    setup_benchmark_tables()
    
    print("\nAvailable functions:")
    print("- setup_benchmark_tables(): Create tables and load initial data")
    print("- export_benchmarks_to_csv(): Export current DB data to CSV")
    print("- import_benchmarks_from_csv(): Import CSV data to DB")
