#!/usr/bin/env python3
"""
Simple test script for the web interface
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        from src.web.app import app
        print("✓ Flask app imported successfully")
        
        from src.database.models.equipment import Equipment
        print("✓ Equipment model imported successfully")
        
        from src.database.models.category import Category
        print("✓ Category model imported successfully")
        
        from src.database.connection import DatabaseConnection
        print("✓ Database connection imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_flask_app():
    """Test Flask app configuration"""
    try:
        from src.web.app import app
        
        # Check if app has required routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        required_routes = ['/', '/api/search', '/api/equipment/<int:equipment_id>', '/api/equipment']
        
        missing_routes = [route for route in required_routes if route not in routes]
        
        if missing_routes:
            print(f"✗ Missing routes: {missing_routes}")
            return False
        
        print("✓ Flask app has all required routes")
        return True
        
    except Exception as e:
        print(f"✗ Flask app test failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        from src.database.connection import DatabaseConnection
        
        # Try to create a connection
        connection = DatabaseConnection()
        print("✓ Database connection test successful")
        return True
        
    except Exception as e:
        print(f"✗ Database connection test failed: {e}")
        print("  This is expected if the database is not running or configured")
        return False

def main():
    """Run all tests"""
    print("Testing Web Interface Components...")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_imports),
        ("Flask App", test_flask_app),
        ("Database Connection", test_database_connection),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"  {test_name} failed")
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! The web interface is ready to use.")
        print("\nTo start the web server:")
        print("  py web_server.py")
        print("\nThen open http://localhost:5000 in your browser")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
