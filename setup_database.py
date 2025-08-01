import yaml
import sqlite3
import os
from datetime import datetime

def load_schema(yaml_file):
    """Load the YAML schema file"""
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

def generate_sqlite_schema(schema_data, yaml_file):
    """Generate SQLite DDL from the YAML schema"""
    sql_statements = []
    
    # Get the database and schema
    database = schema_data['databases'][0]
    schema = database['schemas'][0]
    
    sql_statements.append(f"-- Telecom Database Setup")
    sql_statements.append(f"-- Generated from {yaml_file}")
    sql_statements.append(f"-- Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sql_statements.append("")
    
    # Create tables
    for table in schema['tables']:
        if 'view' in table:
            # Handle views
            sql_statements.append(f"-- View: {table['name']}")
            sql_statements.append(f"-- {table.get('comment', 'No comment')}")
            # Fix schema reference for SQLite
            view_sql = table['view'].replace('sch_gold.fact_network_metrics', 'fact_network_metrics')
            sql_statements.append(f"CREATE VIEW IF NOT EXISTS {table['name']} AS")
            sql_statements.append(view_sql)
            sql_statements.append("")
        else:
            # Handle tables
            sql_statements.append(f"-- Table: {table['name']}")
            sql_statements.append(f"-- {table.get('comment', 'No comment')}")
            
            columns = []
            primary_keys = []
            foreign_keys = []
            
            for column in table['columns']:
                col_name = column['name']
                col_type = column['types']['sqlite']
                
                # Handle primary key
                if column.get('primary_key'):
                    primary_keys.append(col_name)
                    # Don't add PRIMARY KEY here for composite keys
                    col_def = f"{col_name} {col_type}"
                else:
                    col_def = f"{col_name} {col_type}"
                
                # Handle foreign key
                if 'foreign_key' in column:
                    fk = column['foreign_key']
                    foreign_keys.append({
                        'column': col_name,
                        'ref_table': fk['table'],
                        'ref_column': fk['column']
                    })
                
                columns.append(col_def)
            
            # Create table statement
            table_sql = f"CREATE TABLE IF NOT EXISTS {table['name']} (\n"
            table_sql += ",\n".join(f"    {col}" for col in columns)
            
            # Add composite primary key if multiple primary keys
            if len(primary_keys) > 1:
                table_sql += f",\n    PRIMARY KEY ({', '.join(primary_keys)})"
            elif len(primary_keys) == 1:
                # Replace the column definition with PRIMARY KEY
                for i, col in enumerate(columns):
                    if primary_keys[0] in col:
                        columns[i] = f"{primary_keys[0]} {col_type} PRIMARY KEY"
                        break
                table_sql = f"CREATE TABLE IF NOT EXISTS {table['name']} (\n"
                table_sql += ",\n".join(f"    {col}" for col in columns)
            
            # Add foreign key constraints
            for fk in foreign_keys:
                table_sql += f",\n    FOREIGN KEY ({fk['column']}) REFERENCES {fk['ref_table']}({fk['ref_column']})"
            
            table_sql += "\n);"
            sql_statements.append(table_sql)
            sql_statements.append("")
    
    return "\n".join(sql_statements)

def create_database(db_path, sql_statements):
    """Create the SQLite database and execute the SQL statements"""
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute SQL statements
    try:
        cursor.executescript(sql_statements)
        conn.commit()
        print(f"✅ Successfully created database: {db_path}")
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Created tables: {[table[0] for table in tables]}")
        
    except sqlite3.Error as e:
        print(f"❌ Error creating database: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    """Main function to set up the database"""
    yaml_file = "data/network_performance_schema.yaml"
    db_path = "data/telecom_db.sqlite"
    
    print("🔧 Setting up Telecom Database...")
    print(f"📄 Reading schema from: {yaml_file}")
    
    # Load and parse schema
    schema_data = load_schema(yaml_file)
    
    # Generate SQL statements
    sql_statements = generate_sqlite_schema(schema_data, yaml_file)
    
    # Save SQL to file for reference
    sql_file = "data/setup_telecom_db.sql"
    with open(sql_file, 'w') as f:
        f.write(sql_statements)
    print(f"💾 SQL statements saved to: {sql_file}")
    
    # Create database
    create_database(db_path, sql_statements)
    
    print("\n🎉 Database setup complete!")
    print(f"📊 Database file: {db_path}")
    print(f"📝 SQL file: {sql_file}")

if __name__ == "__main__":
    main() 