#!/usr/bin/env python3
"""
Web Server Entry Point for Equipment Database System

This script runs the Flask web application for searching equipment in the database.
"""

import os
import sys
import logging
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.web.app import app
from src.database.connection import DatabaseConnection

def setup_logging():
    """Configure logging for the web server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('web_server.log')
        ]
    )

def test_database_connection():
    """Test database connection before starting the server"""
    try:
        connection = DatabaseConnection()
        logging.info("Database connection successful")
        return True
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        logging.error("Please check your database configuration and ensure the database is running")
        return False

def main():
    """Main entry point for the web server"""
    setup_logging()
    
    logging.info("Starting Equipment Database Web Server...")
    
    # Test database connection
    if not test_database_connection():
        logging.error("Cannot start server without database connection")
        sys.exit(1)
    
    # Get configuration from environment variables
    host = os.getenv('WEB_HOST', '0.0.0.0')
    port = int(os.getenv('WEB_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logging.info(f"Server configuration: host={host}, port={port}, debug={debug}")
    
    try:
        # Start the Flask application
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=debug
        )
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
    except Exception as e:
        logging.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
