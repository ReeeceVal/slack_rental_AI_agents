#!/usr/bin/env python3
"""
Test Database Connection Script
This script tests the database connection and basic functionality.
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.database.connection import get_db_connection
from src.database.models.equipment import Equipment
from src.database.models.category import Category

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test basic database connection"""
    try:
        db_conn = get_db_connection()
        
        # Test health check
        if db_conn.health_check():
            logger.info("✅ Database connection successful!")
            return True
        else:
            logger.error("❌ Database health check failed!")
            return False
            
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

def test_equipment_queries():
    """Test equipment model queries"""
    try:
        logger.info("Testing equipment queries...")
        
        # Get all equipment
        equipment_list = Equipment.get_all_equipment()
        logger.info(f"✅ Found {len(equipment_list)} equipment items")
        
        # Get equipment by type
        speakers = Equipment.get_equipment_by_type('speaker')
        logger.info(f"✅ Found {len(speakers)} speakers")
        
        # Search equipment
        search_results = Equipment.search_equipment('JBL')
        logger.info(f"✅ Search for 'JBL' returned {len(search_results)} results")
        
        # Get available equipment
        available = Equipment.get_available_equipment()
        logger.info(f"✅ Found {len(available)} available equipment items")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Equipment queries failed: {e}")
        return False

def test_category_queries():
    """Test category model queries"""
    try:
        logger.info("Testing category queries...")
        
        # Get all categories
        categories = Category.get_all_categories()
        logger.info(f"✅ Found {len(categories)} categories")
        
        # Get categories by audience
        corporate_categories = Category.get_categories_by_audience('corporate events')
        logger.info(f"✅ Found {len(corporate_categories)} corporate event categories")
        
        # Get category with equipment
        if categories:
            first_category = categories[0]
            category_details = Category.get_category_with_equipment(first_category.id)
            if category_details:
                logger.info(f"✅ Category '{first_category.name}' has {len(category_details['equipment'])} equipment items")
            else:
                logger.warning(f"⚠️ Category '{first_category.name}' has no equipment")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Category queries failed: {e}")
        return False

def test_package_functionality():
    """Test package/equipment-category relationships"""
    try:
        logger.info("Testing package functionality...")
        
        # Get all categories
        categories = Category.get_all_categories()
        
        for category in categories:
            equipment_list = Equipment.get_equipment_by_category(category.id)
            logger.info(f"✅ Package '{category.name}': {len(equipment_list)} equipment items")
            
            # Show some equipment details
            for eq in equipment_list[:3]:  # Show first 3 items
                logger.info(f"   - {eq.name} ({eq.equipment_type}) - Qty: {getattr(eq, 'quantity_in_package', 1)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Package functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    logger.info("Database Connection and Functionality Test")
    logger.info("=" * 50)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Equipment Queries", test_equipment_queries),
        ("Category Queries", test_category_queries),
        ("Package Functionality", test_package_functionality),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\nRunning test: {test_name}")
        if test_func():
            passed += 1
            logger.info(f"✅ {test_name} passed")
        else:
            logger.error(f"❌ {test_name} failed")
    
    logger.info("\n" + "=" * 50)
    logger.info(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Database is working correctly.")
        return True
    else:
        logger.error("💥 Some tests failed. Please check the database setup.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
