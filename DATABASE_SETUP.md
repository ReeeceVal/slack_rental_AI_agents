# Equipment Database Setup Guide

This guide will walk you through setting up the complete equipment database system with PostgreSQL, including schema creation, sample data, and testing.

## Prerequisites

### 1. PostgreSQL Installation
- **Windows**: Download and install from [PostgreSQL Downloads](https://www.postgresql.org/download/windows/)
- **macOS**: Use Homebrew: `brew install postgresql`
- **Linux**: `sudo apt-get install postgresql postgresql-contrib` (Ubuntu/Debian)

### 2. Python Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Quick Setup

### Step 1: Configure Environment Variables
1. Copy the environment template:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` with your PostgreSQL credentials:
   ```bash
   # Database Configuration
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=equipment_db
   DB_USER=postgres
   DB_PASSWORD=your_actual_password
   ```

### Step 2: Run Database Setup
Execute the setup script to create the database and populate it with sample data:
```bash
python setup_database.py
```

This script will:
- Create the `equipment_db` database if it doesn't exist
- Execute the schema files to create all tables
- Populate the database with sample equipment and categories
- Verify the setup was successful

### Step 3: Test the Setup
Run the connection test to verify everything is working:
```bash
python test_database_connection.py
```

## Manual Setup (Alternative)

If you prefer to set up the database manually:

### 1. Create Database
```sql
CREATE DATABASE equipment_db;
```

### 2. Execute Schema Files
Connect to the `equipment_db` database and run the SQL files in order:

```bash
psql -h localhost -U postgres -d equipment_db -f database/schema/001_equipment_tables.sql
psql -h localhost -U postgres -d equipment_db -f database/schema/003_sample_data.sql
```

## Database Schema Overview

### Core Tables

#### 1. `equipment` Table
Stores individual equipment items with detailed specifications:
- **id**: Unique identifier
- **name**: Equipment name (e.g., "JBL Professional Speaker")
- **description**: Detailed description for AI comprehension
- **equipment_type**: Category (speaker, light, microphone, etc.)
- **brand**: Manufacturer (JBL, Shure, Behringer, etc.)
- **model**: Specific model number
- **power_rating**: Electrical power requirements
- **dimensions**: Physical dimensions
- **weight**: Weight in kilograms
- **rental_price_per_day**: Daily rental cost
- **availability_status**: Current status (available, rented, maintenance, retired)

#### 2. `categories` Table
Defines equipment packages and their characteristics:
- **id**: Unique identifier
- **name**: Package name (e.g., "Party Package", "Corporate Package")
- **description**: Package description
- **target_audience**: Intended use (parties, corporate events, concerts, weddings)
- **typical_event_size**: Event size range (small, medium, large)

#### 3. `equipment_categories` Table
Junction table linking equipment to categories with package-specific details:
- **equipment_id**: Reference to equipment table
- **category_id**: Reference to categories table
- **quantity_in_package**: How many of this equipment in the package
- **is_required**: Whether this equipment is essential for the package

### Sample Data Included

The system comes pre-populated with:

#### Equipment Categories
- **Party Package**: Audio and lighting for small social events
- **Corporate Package**: Professional AV for business meetings
- **Concert Package**: High-powered system for live music
- **Wedding Package**: Elegant setup for ceremonies
- **DJ Package**: Complete DJ equipment setup
- **Conference Package**: Multi-area presentation system

#### Equipment Types
- **Audio**: Speakers, microphones, mixers, amplifiers
- **Lighting**: LED panels, moving heads, wash lights, controllers
- **Support**: Stands, cables, cases, power distribution

## Testing the System

### 1. Basic Connection Test
```python
from src.database.connection import get_db_connection

db_conn = get_db_connection()
if db_conn.health_check():
    print("Database connection successful!")
```

### 2. Equipment Queries
```python
from src.database.models.equipment import Equipment

# Get all equipment
all_equipment = Equipment.get_all_equipment()

# Search for specific equipment
speakers = Equipment.search_equipment("JBL speaker")

# Get equipment by type
lights = Equipment.get_equipment_by_type("light")
```

### 3. Category and Package Queries
```python
from src.database.models.category import Category

# Get all packages
packages = Category.get_all_categories()

# Get package details with equipment
party_package = Category.get_category_with_equipment(1)

# Get equipment in a specific package
from src.database.models.equipment import Equipment
party_equipment = Equipment.get_equipment_by_category(1)
```

## Troubleshooting

### Common Issues

#### 1. Connection Refused
- Ensure PostgreSQL is running
- Check if the port (5432) is correct
- Verify firewall settings

#### 2. Authentication Failed
- Check username and password in `.env`
- Ensure the user has permission to create databases
- Try connecting with `psql` to verify credentials

#### 3. Database Already Exists
- The setup script will handle this automatically
- If manual setup, drop the database first: `DROP DATABASE equipment_db;`

#### 4. Permission Denied
- Ensure the PostgreSQL user has `CREATEDB` privilege
- Run as a user with appropriate permissions

### Verification Commands

Check if the database was created:
```bash
psql -h localhost -U postgres -l | grep equipment_db
```

Verify tables exist:
```bash
psql -h localhost -U postgres -d equipment_db -c "\dt"
```

Check sample data:
```bash
psql -h localhost -U postgres -d equipment_db -c "SELECT COUNT(*) FROM equipment;"
psql -h localhost -U postgres -d equipment_db -c "SELECT COUNT(*) FROM categories;"
```

## Next Steps

Once the database is set up and tested:

1. **Run the Web Application**:
   ```bash
   python web_server.py
   ```

2. **Access the Web Interface**: Open `http://localhost:5000` in your browser

3. **Test Equipment Search**: Use the search interface to find equipment and packages

4. **Explore the API**: The system provides RESTful endpoints for equipment and category management

## Support

If you encounter issues:
1. Check the logs for detailed error messages
2. Verify PostgreSQL is running and accessible
3. Ensure all environment variables are set correctly
4. Run the test script to identify specific problems

The system is designed to be robust and provide clear error messages to help with troubleshooting.
