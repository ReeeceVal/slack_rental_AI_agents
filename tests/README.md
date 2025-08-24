# Tests Directory

This directory contains all the testing and development files that were moved from the root directory to reduce clutter.

## Test Files

- `test_database_connection.py` - Database connection tests
- `test_implementation.py` - Main implementation tests
- `test_mock_implementation.py` - Mock implementation tests
- `test_refactored_implementation.py` - Refactored implementation tests
- `test_web_interface.py` - Web interface tests
- `test_web_interface_mock.py` - Mock web interface tests

## Development Files

- `web_server_mock.py` - Mock web server for testing
- `demo_system.py` - Demo system implementation
- `*.log` - Various log files

## Running Tests

To run tests, you can use:
```bash
py -m pytest tests/
```

Or run individual test files:
```bash
py tests/test_database_connection.py
```

## Note

These files were moved here to clean up the root directory while keeping them accessible for future development and testing needs.
