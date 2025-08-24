#!/usr/bin/env python3
"""
Simple script to run the web server
"""
import subprocess
import sys
import os

def main():
    """Run the web server"""
    print("Starting Equipment Database Web Server...")
    print("Make sure your database is running first!")
    print("Use 'py setup_database.py' if you need to set up the database.")
    print()
    
    try:
        # Run the web server
        subprocess.run([sys.executable, "web_server.py"], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Error running server: {e}")
        print("Check that all dependencies are installed:")
        print("  py -m pip install -r requirements_web_only.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
