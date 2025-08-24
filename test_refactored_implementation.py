#!/usr/bin/env python3
"""
Test script to verify the refactored Equipment Database System implementation
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

def test_base_model():
    """Test BaseModel functionality"""
    try:
        from src.database.models.base import BaseModel
        
        logger.info("✓ BaseModel imported successfully")
        
        # Test validation methods
        test_data = {'name': 'Test', 'description': 'Test Description'}
        required_fields = ['name', 'description']
        
        if BaseModel._validate_required_fields(test_data, required_fields):
            logger.info("✓ Required field validation working")
        else:
            logger.error("✗ Required field validation failed")
            return False
        
        # Test string sanitization
        sanitized = BaseModel._sanitize_string("  Test String  ", 10)
        if sanitized == "Test Strin":
            logger.info("✓ String sanitization working")
        else:
            logger.error(f"✗ String sanitization failed: expected 'Test Strin', got '{sanitized}'")
            return False
        
        # Test positive number validation
        if BaseModel._validate_positive_number(5, 'test_field'):
            logger.info("✓ Positive number validation working")
        else:
            logger.error("✗ Positive number validation failed")
            return False
        
        if not BaseModel._validate_positive_number(-1, 'test_field'):
            logger.info("✓ Negative number validation working")
        else:
            logger.error("✗ Negative number validation failed")
            return False
        
        return True
        
    except ImportError as e:
        logger.error(f"✗ Failed to import BaseModel: {e}")
        return False

def test_equipment_model_refactoring():
    """Test refactored Equipment model"""
    try:
        from src.database.models.equipment import Equipment
        
        logger.info("✓ Refactored Equipment model imported successfully")
        
        # Test validation
        valid_data = {
            'name': 'Test Speaker',
            'description': 'Test speaker description',
            'equipment_type': 'speaker',
            'rental_price_per_day': 25.00
        }
        
        if Equipment.validate_equipment_data(valid_data):
            logger.info("✓ Equipment data validation working")
        else:
            logger.error("✗ Equipment data validation failed")
            return False
        
        # Test invalid data validation
        invalid_data = {
            'name': 'Test Speaker',
            'description': 'Test speaker description',
            'equipment_type': 'invalid_type',  # Invalid type
            'rental_price_per_day': -25.00    # Negative price
        }
        
        if not Equipment.validate_equipment_data(invalid_data):
            logger.info("✓ Invalid data validation working")
        else:
            logger.error("✗ Invalid data validation failed")
            return False
        
        # Test model instantiation
        equipment = Equipment(**valid_data)
        if equipment.name == 'Test Speaker':
            logger.info("✓ Equipment model instantiation working")
        else:
            logger.error("✗ Equipment model instantiation failed")
            return False
        
        return True
        
    except ImportError as e:
        logger.error(f"✗ Failed to import refactored Equipment model: {e}")
        return False

def test_statistics_module():
    """Test new statistics module"""
    try:
        from src.database.statistics import get_database_statistics
        
        stats = get_database_statistics()
        logger.info("✓ Statistics module imported successfully")
        
        # Test statistics instance
        if hasattr(stats, 'get_database_statistics'):
            logger.info("✓ Statistics module has required methods")
        else:
            logger.error("✗ Statistics module missing required methods")
            return False
        
        return True
        
    except ImportError as e:
        logger.error(f"✗ Failed to import statistics module: {e}")
        return False

def test_repository_refactoring():
    """Test refactored repository"""
    try:
        from src.database.repository import get_equipment_repository
        
        repo = get_equipment_repository()
        logger.info("✓ Refactored repository imported successfully")
        
        # Test statistics delegation
        if hasattr(repo, 'get_category_statistics'):
            logger.info("✓ Repository has new statistics methods")
        else:
            logger.error("✗ Repository missing new statistics methods")
            return False
        
        return True
        
    except ImportError as e:
        logger.error(f"✗ Failed to import refactored repository: {e}")
        return False

def test_import_cleanup():
    """Test that unused imports have been removed"""
    try:
        # Check that models no longer import async connections
        with open('src/database/models/equipment.py', 'r') as f:
            content = f.read()
            if 'get_async_db_connection' in content:
                logger.error("✗ Equipment model still imports async connection")
                return False
        
        with open('src/database/models/category.py', 'r') as f:
            content = f.read()
            if 'get_async_db_connection' in content:
                logger.error("✗ Category model still imports async connection")
                return False
        
        with open('src/database/models/equipment_category.py', 'r') as f:
            content = f.read()
            if 'get_async_db_connection' in content:
                logger.error("✗ EquipmentCategory model still imports async connection")
                return False
        
        logger.info("✓ All unused async imports removed")
        return True
        
    except Exception as e:
        logger.error(f"✗ Error checking import cleanup: {e}")
        return False

def test_schema_files():
    """Test that all schema files exist"""
    schema_files = [
        'database/schema/001_equipment_tables.sql',
        'database/schema/002_equipment_categories.sql',
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

def main():
    """Run all refactoring tests"""
    logger.info("Starting Equipment Database System refactoring tests...")
    logger.info("=" * 60)
    
    tests = [
        ("Base Model", test_base_model),
        ("Equipment Model Refactoring", test_equipment_model_refactoring),
        ("Statistics Module", test_statistics_module),
        ("Repository Refactoring", test_repository_refactoring),
        ("Import Cleanup", test_import_cleanup),
        ("Schema Files", test_schema_files),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\nRunning test: {test_name}")
        logger.info("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"✗ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("REFACTORING TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All refactoring tests passed! Implementation is ready.")
        return 0
    else:
        logger.error("❌ Some refactoring tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
