#!/usr/bin/env python3
"""
Test script for the mock web interface (no database required)
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_mock_imports():
    """Test that the mock web app can be imported"""
    try:
        from src.web.app_mock import app
        print("✓ Mock Flask app imported successfully")
        
        # Check if app has required routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        required_routes = ['/', '/api/search', '/api/equipment/<int:equipment_id>', '/api/equipment']
        
        missing_routes = [route for route in required_routes if route not in routes]
        
        if missing_routes:
            print(f"✗ Missing routes: {missing_routes}")
            return False
        
        print("✓ Mock Flask app has all required routes")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Mock Flask app test failed: {e}")
        return False

def test_mock_data():
    """Test that mock data is available"""
    try:
        from src.web.app_mock import MOCK_EQUIPMENT, MOCK_CATEGORIES
        
        if len(MOCK_EQUIPMENT) > 0:
            print("✓ Mock equipment data available")
        else:
            print("✗ No mock equipment data")
            return False
            
        if len(MOCK_CATEGORIES) > 0:
            print("✓ Mock category data available")
        else:
            print("✗ No mock category data")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Mock data test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Mock Web Interface Components...")
    print("=" * 40)
    
    tests = [
        ("Mock Module Imports", test_mock_imports),
        ("Mock Data Availability", test_mock_data),
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
        print("✓ All tests passed! The mock web interface is ready to use.")
        print("\nTo start the mock web server:")
        print("  py web_server_mock.py")
        print("\nThen open http://localhost:5000 in your browser")
        print("\nNote: This uses mock data and doesn't require a database connection.")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
