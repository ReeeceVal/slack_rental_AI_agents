-- Equipment Categories Junction Table Schema
-- File: 002_equipment_categories.sql
-- This file contains the junction table structure for many-to-many relationships
-- between equipment and categories, along with additional package metadata

-- Note: This table structure is already included in 001_equipment_tables.sql
-- This file serves as a reference and potential future migration point

-- The equipment_categories table structure (already created in 001_equipment_tables.sql):
/*
CREATE TABLE IF NOT EXISTS equipment_categories (
    id SERIAL PRIMARY KEY,
    equipment_id INTEGER NOT NULL REFERENCES equipment(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    quantity_in_package INTEGER DEFAULT 1,
    is_required BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT positive_quantity CHECK (quantity_in_package > 0),
    UNIQUE(equipment_id, category_id)
);
*/

-- Additional indexes for performance (already created in 001_equipment_tables.sql):
/*
CREATE INDEX IF NOT EXISTS idx_equipment_categories_equipment ON equipment_categories(equipment_id);
CREATE INDEX IF NOT EXISTS idx_equipment_categories_category ON equipment_categories(category_id);
*/

-- This file serves as a placeholder for future schema migrations
-- and documentation of the equipment-category relationship structure

-- Future migration considerations:
-- 1. Add package pricing information
-- 2. Add equipment compatibility rules
-- 3. Add package versioning support
-- 4. Add equipment substitution rules
