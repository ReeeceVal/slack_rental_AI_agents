#!/usr/bin/env python3
"""
Test script to verify the Equipment Database System implementation with mock connections
"""
import os
import sys
import logging
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_mock_database_connection():
    """Test mock database connection functionality"""
    try:
        from src.database.connection_mock import get_mock_db_connection
        
        db_conn = get_mock_db_connection()
        logger.info("✓ Mock database connection module imported successfully")
        
        # Test connection initialization
        db_conn.initialize_pool()
        logger.info("✓ Mock database connection pool initialized")
        
        # Test health check
        health = db_conn.health_check()
        logger.info(f"✓ Database health check: {health}")
        
        return True
        
    except ImportError as e:
        logger.error(f"✗ Failed to import mock database connection: {e}")
        return False

def test_models_import():
    """Test model imports"""
    try:
        from src.database.models.equipment import Equipment
        from src.database.models.category import Category
        from src.database.models.equipment_category import EquipmentCategory
        
        logger.info("✓ All database models imported successfully")
        
        # Test model instantiation
        equipment = Equipment(name="Test Equipment", equipment_type="speaker")
        category = Category(name="Test Category", target_audience="test")
        
        logger.info("✓ Model instantiation successful")
        logger.info(f"  - Equipment: {equipment}")
        logger.info(f"  - Category: {category}")
        
        return True
        
    except ImportError as e:
        logger.error(f"✗ Failed to import models: {e}")
        return False

def test_repository_import():
    """Test repository import"""
    try:
        from src.database.repository import get_equipment_repository
        
        repo = get_equipment_repository()
        logger.info("✓ Equipment repository imported and instantiated successfully")
        return True
        
    except ImportError as e:
        logger.error(f"✗ Failed to import repository: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    try:
        from config.database import db_config
        
        logger.info(f"✓ Database configuration loaded: {db_config}")
        logger.info(f"  - Host: {db_config.host}")
        logger.info(f"  - Port: {db_config.port}")
        logger.info(f"  - Database: {db_config.database}")
        
        return True
        
    except ImportError as e:
        logger.error(f"✗ Failed to import configuration: {e}")
        return False

def test_schema_files():
    """Test that schema files exist and are readable"""
    schema_files = [
        'database/schema/001_equipment_tables.sql',
        'database/schema/003_sample_data.sql'
    ]
    
    all_exist = True
    for schema_file in schema_files:
        if os.path.exists(schema_file):
            logger.info(f"✓ Schema file exists: {schema_file}")
        else:
            logger.error(f"✗ Schema file missing: {schema_file}")
            all_exist = False
    
    return all_exist

def test_requirements():
    """Test that requirements.txt exists"""
    if os.path.exists('requirements.txt'):
        logger.info("✓ Requirements file exists")
        return True
    else:
        logger.error("✗ Requirements file missing")
        return False

def test_directory_structure():
    """Test that all required directories exist"""
    required_dirs = [
        'src',
        'src/database',
        'src/database/models',
        'config',
        'database',
        'database/schema',
        'database/migrations'
    ]
    
    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            logger.info(f"✓ Directory exists: {directory}")
        else:
            logger.error(f"✗ Directory missing: {directory}")
            all_exist = False
    
    return all_exist

def test_mock_operations():
    """Test basic mock operations"""
    try:
        from src.database.connection_mock import get_mock_db_connection
        
        db_conn = get_mock_db_connection()
        
        # Test getting a connection
        conn = db_conn.get_connection()
        logger.info("✓ Mock connection retrieved successfully")
        
        # Test cursor operations
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM equipment WHERE id = %s", (1,))
        logger.info("✓ Mock cursor operations successful")
        
        # Test transaction operations
        conn.commit()
        conn.rollback()
        logger.info("✓ Mock transaction operations successful")
        
        # Clean up
        cursor.close()
        db_conn.return_connection(conn)
        logger.info("✓ Mock connection cleanup successful")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Mock operations test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("Starting Equipment Database System implementation tests (Mock Mode)...")
    logger.info("=" * 70)
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("Requirements File", test_requirements),
        ("Schema Files", test_schema_files),
        ("Configuration", test_configuration),
        ("Mock Database Connection", test_mock_database_connection),
        ("Mock Operations", test_mock_operations),
        ("Models Import", test_models_import),
        ("Repository Import", test_repository_import),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\nRunning test: {test_name}")
        logger.info("-" * 50)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"✗ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("TEST SUMMARY")
    logger.info("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Implementation is ready.")
        logger.info("\n📋 NEXT STEPS:")
        logger.info("1. Install PostgreSQL on your system")
        logger.info("2. Install Microsoft Visual C++ Build Tools (for Windows)")
        logger.info("3. Run: py -m pip install -r requirements.txt")
        logger.info("4. Create database and run schema files")
        logger.info("5. Update .env file with database credentials")
        return 0
    else:
        logger.error("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
