-- Equipment Database Schema - Core Tables
-- File: 001_equipment_tables.sql

-- Create equipment table
CREATE TABLE IF NOT EXISTS equipment (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    equipment_type VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    model VARCHAR(100),
    power_rating VARCHAR(50),
    dimensions VARCHAR(100),
    weight DECIMAL(6,2),
    rental_price_per_day DECIMAL(8,2),
    availability_status VARCHAR(20) DEFAULT 'available',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_equipment_type CHECK (equipment_type IN ('speaker', 'light', 'microphone', 'mixer', 'amplifier', 'cable', 'stand', 'case', 'controller', 'other')),
    CONSTRAINT valid_availability_status CHECK (availability_status IN ('available', 'rented', 'maintenance', 'retired')),
    CONSTRAINT positive_weight CHECK (weight > 0),
    CONSTRAINT positive_price CHECK (rental_price_per_day > 0)
);

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    target_audience VARCHAR(100),
    typical_event_size VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_event_size CHECK (typical_event_size IN ('small (10-50)', 'medium (50-200)', 'large (200+)', 'custom'))
);

-- Create equipment_categories junction table
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

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_equipment_type_status ON equipment(equipment_type, availability_status);
CREATE INDEX IF NOT EXISTS idx_equipment_name ON equipment(name);
CREATE INDEX IF NOT EXISTS idx_equipment_brand ON equipment(brand);
CREATE INDEX IF NOT EXISTS idx_categories_audience_size ON categories(target_audience, typical_event_size);
CREATE INDEX IF NOT EXISTS idx_equipment_categories_equipment ON equipment_categories(equipment_id);
CREATE INDEX IF NOT EXISTS idx_equipment_categories_category ON equipment_categories(category_id);

-- Create GIN index for full-text search on equipment description
CREATE INDEX IF NOT EXISTS idx_equipment_description_gin ON equipment USING gin(to_tsvector('english', description));

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_equipment_updated_at BEFORE UPDATE ON equipment
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
