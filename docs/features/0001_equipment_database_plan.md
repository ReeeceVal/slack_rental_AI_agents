# Feature Plan: Equipment Database and Category System

## Brief Description
Implement a PostgreSQL-based equipment database and category system that provides structured data with detailed descriptions for AI comprehension. The system will support logical grouping of equipment into packages (e.g., "party package", "corporate package") and enable intelligent equipment matching through the AI recommendation engine.

## Files and Functions to Create/Modify

### Database Schema Files
- `database/schema/001_equipment_tables.sql` - Core equipment and category table definitions
- `database/schema/002_equipment_categories.sql` - Junction table for many-to-many relationships
- `database/schema/003_sample_data.sql` - Initial equipment and category data
- `database/migrations/` - Directory for future schema migrations

### Database Connection and Models
- `src/database/connection.py` - PostgreSQL connection management
- `src/database/models/equipment.py` - Equipment data model and queries
- `src/database/models/category.py` - Category data model and queries
- `src/database/models/equipment_category.py` - Junction table model
- `src/database/repository.py` - Centralized database operations

### Configuration Files
- `config/database.py` - Database configuration settings
- `requirements.txt` - Add PostgreSQL dependencies (psycopg2-binary, SQLAlchemy)
- `.env.example` - Environment variables template for database connection

## Technical Implementation

### Phase 1: Data Layer (Database Schema and Models)

#### Database Schema Design
1. **equipment table**
   - `id` (SERIAL PRIMARY KEY)
   - `name` (VARCHAR(255) NOT NULL)
   - `description` (TEXT NOT NULL) - Detailed description for AI comprehension
   - `equipment_type` (VARCHAR(100) NOT NULL) - e.g., "speaker", "light", "microphone"
   - `brand` (VARCHAR(100))
   - `model` (VARCHAR(100))
   - `power_rating` (VARCHAR(50)) - For electrical equipment
   - `dimensions` (VARCHAR(100)) - Physical dimensions
   - `weight` (DECIMAL(6,2)) - Weight in kg
   - `rental_price_per_day` (DECIMAL(8,2))
   - `availability_status` (VARCHAR(20) DEFAULT 'available')
   - `created_at` (TIMESTAMP DEFAULT NOW())
   - `updated_at` (TIMESTAMP DEFAULT NOW())

2. **categories table**
   - `id` (SERIAL PRIMARY KEY)
   - `name` (VARCHAR(100) NOT NULL) - e.g., "party package", "corporate package"
   - `description` (TEXT) - Package description for AI understanding
   - `target_audience` (VARCHAR(100)) - e.g., "corporate events", "parties", "concerts"
   - `typical_event_size` (VARCHAR(50)) - e.g., "small (10-50)", "medium (50-200)", "large (200+)"
   - `created_at` (TIMESTAMP DEFAULT NOW())
   - `updated_at` (TIMESTAMP DEFAULT NOW())

3. **equipment_categories table** (Junction table)
   - `id` (SERIAL PRIMARY KEY)
   - `equipment_id` (INTEGER REFERENCES equipment(id) ON DELETE CASCADE)
   - `category_id` (INTEGER REFERENCES categories(id) ON DELETE CASCADE)
   - `quantity_in_package` (INTEGER DEFAULT 1) - How many of this equipment in the package
   - `is_required` (BOOLEAN DEFAULT true) - Whether this equipment is essential for the package
   - `created_at` (TIMESTAMP DEFAULT NOW())
   - UNIQUE constraint on (equipment_id, category_id)

#### Database Models and Queries
1. **Equipment Model Functions**
   - `get_equipment_by_id(id)` - Retrieve single equipment item
   - `get_equipment_by_type(equipment_type)` - Get all equipment of a specific type
   - `search_equipment(query)` - Full-text search across name and description
   - `get_available_equipment()` - Get all available equipment
   - `get_equipment_by_category(category_id)` - Get all equipment in a specific category

2. **Category Model Functions**
   - `get_category_by_id(id)` - Retrieve single category
   - `get_all_categories()` - Get all categories
   - `get_categories_by_audience(target_audience)` - Get categories for specific audience
   - `get_category_with_equipment(category_id)` - Get category with all associated equipment

3. **Equipment-Category Junction Functions**
   - `add_equipment_to_category(equipment_id, category_id, quantity, required)` - Associate equipment with category
   - `remove_equipment_from_category(equipment_id, category_id)` - Remove association
   - `get_package_details(category_id)` - Get complete package information with equipment

### Phase 2A: Database Operations Layer
- Implement connection pooling for efficient database management
- Add database health checks and connection retry logic
- Implement transaction management for complex operations
- Add database logging and monitoring

### Phase 2B: Data Access Layer
- Create repository pattern for centralized database operations
- Implement caching layer for frequently accessed equipment data
- Add data validation and sanitization
- Implement error handling and graceful degradation

## Algorithms and Logic

### Equipment Search Algorithm
1. **Full-Text Search**: Use PostgreSQL's built-in full-text search capabilities
   - Create GIN index on equipment name and description
   - Implement relevance scoring based on search term frequency
   - Support partial matches and fuzzy search

2. **Category-Based Filtering**
   - Filter equipment by category membership
   - Support multiple category selection
   - Implement exclusion logic for incompatible categories

3. **Availability Filtering**
   - Filter by current availability status
   - Consider rental duration and existing bookings
   - Implement conflict detection for overlapping rentals

### Package Recommendation Logic
1. **Category Matching**
   - Match user requirements to appropriate categories
   - Use target audience and event size for initial filtering
   - Consider equipment compatibility within packages

2. **Equipment Substitution**
   - Allow flexible equipment substitution within categories
   - Maintain package integrity while accommodating availability
   - Implement fallback options for unavailable equipment

## Database Indexes and Performance
- Primary key indexes on all tables
- GIN index on equipment description for full-text search
- Composite index on (equipment_type, availability_status)
- Composite index on (target_audience, typical_event_size)
- Foreign key indexes on junction table

## Data Integrity and Constraints
- Foreign key constraints with CASCADE delete for equipment_categories
- Check constraints for valid equipment types and status values
- Unique constraints on equipment names within the same type
- Not null constraints on essential fields
- Default values for optional fields

## Sample Data Structure
The system will include sample equipment covering:
- **Audio Equipment**: Speakers, microphones, mixers, amplifiers
- **Lighting Equipment**: LED panels, spotlights, wash lights, controllers
- **Support Equipment**: Stands, cables, cases, power distribution
- **Package Categories**: Party packages, corporate packages, concert packages, wedding packages
