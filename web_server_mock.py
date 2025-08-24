#!/usr/bin/env python3
"""
Mock Web Server Entry Point for Equipment Database System (Testing Only)

This script runs the Flask web application with mock data for testing.
"""

import os
import sys
import logging
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.web.app_mock import app

def setup_logging():
    """Configure logging for the web server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('web_server_mock.log')
        ]
    )

def main():
    """Main entry point for the mock web server"""
    setup_logging()
    
    logging.info("Starting Equipment Database Mock Web Server...")
    logging.info("This server uses mock data and doesn't require a database connection")
    
    # Get configuration from environment variables
    host = os.getenv('WEB_HOST', '0.0.0.0')
    port = int(os.getenv('WEB_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    logging.info(f"Server configuration: host={host}, port={port}, debug={debug}")
    logging.info("Mock data includes sample equipment and categories")
    
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
