#!/usr/bin/env python3
"""
Database Setup Script for Equipment Database System
This script sets up the complete database with schema and sample data.
"""

import os
import sys
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config.database import db_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (not to specific database)
        conn = psycopg2.connect(
            host=db_config.host,
            port=db_config.port,
            user=db_config.username,
            password=db_config.password,
            database='postgres'  # Connect to default postgres database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_config.database,))
        exists = cursor.fetchone()
        
        if not exists:
            logger.info(f"Creating database: {db_config.database}")
            cursor.execute(f"CREATE DATABASE {db_config.database}")
            logger.info(f"Database '{db_config.database}' created successfully")
        else:
            logger.info(f"Database '{db_config.database}' already exists")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        return False

def execute_sql_file(file_path: str, connection_params: dict):
    """Execute SQL file with the given connection parameters"""
    try:
        # Read SQL file
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Connect to the target database
        conn = psycopg2.connect(**connection_params)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Execute SQL content
        logger.info(f"Executing SQL file: {file_path}")
        cursor.execute(sql_content)
        
        cursor.close()
        conn.close()
        logger.info(f"Successfully executed: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error executing {file_path}: {e}")
        return False

def setup_database():
    """Main setup function"""
    logger.info("Starting database setup...")
    
    # Step 1: Create database if it doesn't exist
    if not create_database():
        logger.error("Failed to create database. Exiting.")
        return False
    
    # Step 2: Connect to the target database
    try:
        conn = psycopg2.connect(
            host=db_config.host,
            port=db_config.port,
            database=db_config.database,
            user=db_config.username,
            password=db_config.password
        )
        conn.close()
        logger.info("Successfully connected to target database")
    except Exception as e:
        logger.error(f"Failed to connect to target database: {e}")
        return False
    
    # Step 3: Execute schema files
    connection_params = {
        'host': db_config.host,
        'port': db_config.port,
        'database': db_config.database,
        'user': db_config.username,
        'password': db_config.password
    }
    
    schema_files = [
        'database/schema/001_equipment_tables.sql',
        'database/schema/003_sample_data.sql'
    ]
    
    for schema_file in schema_files:
        if not execute_sql_file(schema_file, connection_params):
            logger.error(f"Failed to execute {schema_file}")
            return False
    
    logger.info("Database setup completed successfully!")
    return True

def verify_setup():
    """Verify that the database setup was successful"""
    try:
        conn = psycopg2.connect(
            host=db_config.host,
            port=db_config.port,
            database=db_config.database,
            user=db_config.username,
            password=db_config.password
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('equipment', 'categories', 'equipment_categories')
            ORDER BY table_name
        """)
        
        tables = [row['table_name'] for row in cursor.fetchall()]
        logger.info(f"Found tables: {tables}")
        
        # Check data exists
        cursor.execute("SELECT COUNT(*) as count FROM equipment")
        equipment_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM categories")
        categories_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM equipment_categories")
        relationships_count = cursor.fetchone()['count']
        
        logger.info(f"Equipment count: {equipment_count}")
        logger.info(f"Categories count: {categories_count}")
        logger.info(f"Equipment-category relationships: {relationships_count}")
        
        cursor.close()
        conn.close()
        
        return len(tables) == 3 and equipment_count > 0 and categories_count > 0
        
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return False

def main():
    """Main function"""
    logger.info("Equipment Database Setup")
    logger.info("=" * 50)
    
    # Check if we can connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            host=db_config.host,
            port=db_config.port,
            user=db_config.username,
            password=db_config.password,
            database='postgres'
        )
        conn.close()
        logger.info("PostgreSQL connection test successful")
    except Exception as e:
        logger.error(f"Cannot connect to PostgreSQL: {e}")
        logger.error("Please ensure PostgreSQL is running and credentials are correct")
        return False
    
    # Setup database
    if setup_database():
        logger.info("Database setup completed successfully!")
        
        # Verify setup
        if verify_setup():
            logger.info("Database verification successful!")
            logger.info("\nSetup Summary:")
            logger.info("- Database created/verified")
            logger.info("- Tables created with proper schema")
            logger.info("- Sample data populated")
            logger.info("- Indexes and constraints applied")
            logger.info("\nYou can now run the application!")
        else:
            logger.error("Database verification failed!")
            return False
    else:
        logger.error("Database setup failed!")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
