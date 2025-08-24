# Equipment Database and Category System

A PostgreSQL-based equipment database and category system that provides structured data with detailed descriptions for AI comprehension. The system supports logical grouping of equipment into packages (e.g., "party package", "corporate package") and enables intelligent equipment matching through AI recommendation engines.

## Features

- **Equipment Management**: Complete CRUD operations for equipment items with detailed metadata
- **Category System**: Flexible package categorization with target audience and event size specifications
- **Package Management**: Create, modify, and manage equipment packages with quantities and requirements
- **Full-Text Search**: PostgreSQL-powered search across equipment names and descriptions
- **Connection Pooling**: Efficient database connection management with health checks
- **Async Support**: Both synchronous and asynchronous database operations
- **Comprehensive API**: Centralized repository pattern for all database operations

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Application  │    │   Repository    │    │   Database     │
│      Layer     │◄──►│      Layer      │◄──►│     Layer      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Connection    │
                       │     Pool       │
                       └─────────────────┘
```

## Database Schema

### Core Tables

1. **equipment**: Equipment items with detailed specifications
2. **categories**: Package categories with target audience and event size
3. **equipment_categories**: Junction table for many-to-many relationships

### Key Features

- Full-text search capabilities with GIN indexes
- Automatic timestamp management
- Data integrity constraints
- Performance-optimized indexes

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd slack_MVP
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

4. **Create database**
   ```sql
   CREATE DATABASE equipment_db;
   ```

5. **Initialize schema**
   ```bash
   # Run the schema files in order:
   psql -d equipment_db -f database/schema/001_equipment_tables.sql
   psql -d equipment_db -f database/schema/003_sample_data.sql
   ```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | `equipment_db` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | (required) |
| `DB_MIN_CONNECTIONS` | Min connection pool size | `1` |
| `DB_MAX_CONNECTIONS` | Max connection pool size | `10` |
| `DB_CONNECTION_TIMEOUT` | Connection timeout (seconds) | `30` |

## Usage

### Web Interface

The system includes a simple web interface for searching equipment and categories:

#### Quick Start (Mock Data - No Database Required)

1. **Start the mock web server**
   ```bash
   py web_server_mock.py
   ```

2. **Access the web interface**
   - Open your browser and go to `http://localhost:5000`
   - Use the search bar to find equipment and categories
   - Click on equipment cards to view detailed information
   - Switch between Equipment and Categories tabs to view different result types

#### Production Setup (With Database)

1. **Install all dependencies**
   ```bash
   py -m pip install -r requirements.txt
   ```

2. **Start the production web server**
   ```bash
   py web_server.py
   ```

#### Web Interface Features
- Full-text search across equipment names and descriptions
- Real-time search results with loading indicators
- Responsive design for mobile and desktop
- Equipment details modal with complete information
- Tabbed interface for equipment and category results
- Mock data available for testing without database setup

### Basic Operations

```python
from src.database import get_equipment_repository

# Get repository instance
repo = get_equipment_repository()

# Get equipment by ID
equipment = repo.get_equipment(1)

# Search equipment
results = repo.search_equipment("speaker")

# Get package details
package = repo.get_package_details(1)

# Create new equipment
new_equipment = repo.create_equipment({
    'name': 'New Speaker',
    'description': 'High-quality speaker',
    'equipment_type': 'speaker',
    'brand': 'Brand Name',
    'rental_price_per_day': 50.00
})
```

### Package Management

```python
# Add equipment to package
repo.add_equipment_to_package(
    equipment_id=1,
    category_id=1,
    quantity=2,
    required=True
)

# Get package statistics
stats = repo.get_database_statistics()
```

### Advanced Search

```python
# Search packages by audience and event size
packages = repo.get_packages_by_audience_and_size(
    target_audience='corporate events',
    event_size='medium (50-200)'
)

# Get equipment compatibility
compatibility = repo.get_equipment_compatibility(equipment_id=1)
```

## API Reference

### Equipment Model

- `get_equipment_by_id(id)`: Retrieve single equipment item
- `get_equipment_by_type(type)`: Get equipment by type
- `search_equipment(query)`: Full-text search
- `get_available_equipment()`: Get available equipment
- `create_equipment(data)`: Create new equipment
- `update_equipment(id, data)`: Update equipment
- `delete_equipment(id)`: Delete equipment

### Category Model

- `get_category_by_id(id)`: Retrieve single category
- `get_all_categories()`: Get all categories
- `get_categories_by_audience(audience)`: Filter by audience
- `get_category_with_equipment(id)`: Get category with equipment
- `create_category(data)`: Create new category
- `update_category(id, data)`: Update category
- `delete_category(id)`: Delete category

### Package Operations

- `get_package_details(category_id)`: Complete package information
- `add_equipment_to_package(equipment_id, category_id, quantity, required)`: Add equipment
- `remove_equipment_from_package(equipment_id, category_id)`: Remove equipment
- `update_package_quantity(equipment_id, category_id, quantity)`: Update quantity
- `update_package_requirement(equipment_id, category_id, required)`: Update requirement

## Sample Data

The system includes sample data for:

- **Audio Equipment**: Speakers, microphones, mixers, amplifiers
- **Lighting Equipment**: LED panels, spotlights, wash lights, controllers
- **Support Equipment**: Stands, cables, cases, power distribution
- **Package Categories**: Party, corporate, concert, wedding, DJ, conference packages

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

### Database Migrations

The system includes a migrations directory for future schema changes. Use Alembic for managing database migrations:

```bash
# Initialize Alembic (first time)
alembic init migrations

# Create migration
alembic revision -m "Description of changes"

# Apply migrations
alembic upgrade head
```

## Performance Considerations

- **Indexes**: Optimized database indexes for common queries
- **Connection Pooling**: Efficient connection management
- **Full-Text Search**: GIN indexes for fast text search
- **Query Optimization**: Structured queries with proper JOINs

## Security

- **Parameterized Queries**: SQL injection prevention
- **Connection Security**: Secure database connections
- **Environment Variables**: Secure credential management
- **Input Validation**: Data validation and sanitization

## Troubleshooting

### Common Issues

1. **Connection Errors**: Check database credentials and network connectivity
2. **Schema Errors**: Ensure all schema files are run in correct order
3. **Permission Errors**: Verify database user has appropriate permissions

### Logging

The system includes comprehensive logging. Check log files for detailed error information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Add your license information here]

## Support

For support and questions, please [create an issue](link-to-issues) or contact the development team.
