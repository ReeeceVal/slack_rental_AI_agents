-- Sample Data for Equipment Database
-- File: 003_sample_data.sql

-- Insert sample categories
INSERT INTO categories (name, description, target_audience, typical_event_size) VALUES
('Party Package', 'Complete audio and lighting setup for parties and social events. Includes speakers, lights, and basic audio equipment.', 'parties', 'small (10-50)'),
('Corporate Package', 'Professional audio-visual equipment for corporate meetings, presentations, and conferences.', 'corporate events', 'medium (50-200)'),
('Concert Package', 'High-powered audio and lighting system for live music performances and concerts.', 'concerts', 'large (200+)'),
('Wedding Package', 'Elegant audio and lighting setup for wedding ceremonies and receptions.', 'weddings', 'medium (50-200)'),
('DJ Package', 'Complete DJ setup with professional audio equipment and lighting effects.', 'parties', 'small (10-50)'),
('Conference Package', 'Comprehensive AV setup for large conferences and seminars with multiple presentation areas.', 'corporate events', 'large (200+)');

-- Insert sample equipment
INSERT INTO equipment (name, description, equipment_type, brand, model, power_rating, dimensions, weight, rental_price_per_day, availability_status) VALUES
-- Audio Equipment
('JBL Professional Speaker', 'High-quality 15-inch powered speaker with built-in amplifier. Perfect for medium to large venues. Features DSP processing and multiple input options.', 'speaker', 'JBL', 'EON615', '1000W', '15" x 15" x 12"', 15.5, 45.00, 'available'),
('Shure SM58 Microphone', 'Industry-standard dynamic microphone with cardioid pickup pattern. Excellent for vocals and speech. Includes stand mount and carrying case.', 'microphone', 'Shure', 'SM58', 'N/A', '6.5" x 1.5"', 0.3, 12.00, 'available'),
('Behringer X32 Mixer', 'Professional 32-channel digital mixing console with built-in effects and recording capabilities. Ideal for live sound and studio applications.', 'mixer', 'Behringer', 'X32', '100W', '24" x 18" x 4"', 8.2, 75.00, 'available'),
('Crown Amplifier', 'Professional power amplifier delivering 1000W RMS. Features thermal protection and high-efficiency design for reliable performance.', 'amplifier', 'Crown', 'XLS1000', '1000W', '19" x 3.5" x 12"', 5.8, 35.00, 'available'),

-- Lighting Equipment
('Chauvet LED Panel', 'Bright LED panel with RGB color mixing and multiple effect modes. Perfect for creating ambient lighting and color washes.', 'light', 'Chauvet', 'Par 56', '50W', '8" x 8" x 4"', 2.1, 18.00, 'available'),
('Martin Moving Head', 'Professional moving head light with gobo patterns and color mixing. Features silent operation and smooth pan/tilt movement.', 'light', 'Martin', 'MAC 250', '250W', '12" x 8" x 16"', 8.5, 65.00, 'available'),
('ADJ Wash Light', 'High-output wash light with zoom functionality and smooth color transitions. Ideal for stage and venue lighting.', 'light', 'ADJ', 'Vizi Wash', '200W', '10" x 10" x 6"', 4.2, 28.00, 'available'),
('Chauvet Controller', 'DMX lighting controller with 192 channels and multiple scene memories. Easy-to-use interface for lighting programming.', 'controller', 'Chauvet', 'DMX-4', 'N/A', '12" x 8" x 2"', 1.8, 22.00, 'available'),

-- Support Equipment
('Ultimate Support Stand', 'Heavy-duty speaker stand with adjustable height from 4 to 8 feet. Features safety locking mechanism and rubber feet.', 'stand', 'Ultimate Support', 'TS-90B', 'N/A', '8" x 8" x 96"', 12.0, 15.00, 'available'),
('Pro Co Cable', 'Professional XLR cable with gold-plated connectors and heavy-duty shielding. Available in 25ft and 50ft lengths.', 'cable', 'Pro Co', 'XLR-25', 'N/A', '0.25" x 25ft', 0.8, 8.00, 'available'),
('SKB Case', 'Heavy-duty flight case with foam padding and wheels. Perfect for protecting and transporting audio equipment.', 'case', 'SKB', '4U Rack', 'N/A', '19" x 14" x 7"', 8.5, 12.00, 'available'),
('Furman Power Conditioner', 'Professional power conditioner with surge protection and voltage regulation. Features 8 outlets and circuit breaker protection.', 'other', 'Furman', 'PL-8C', 'N/A', '19" x 1.75" x 8"', 2.3, 18.00, 'available');

-- Associate equipment with categories
INSERT INTO equipment_categories (equipment_id, category_id, quantity_in_package, is_required) VALUES
-- Party Package
(1, 1, 2, true),   -- 2 JBL Speakers
(2, 1, 2, true),   -- 2 SM58 Microphones
(5, 1, 4, true),   -- 4 LED Panels
(9, 1, 2, true),   -- 2 Speaker Stands
(10, 1, 4, true),  -- 4 XLR Cables
(11, 1, 1, false), -- 1 Equipment Case

-- Corporate Package
(1, 2, 2, true),   -- 2 JBL Speakers
(2, 2, 4, true),   -- 4 SM58 Microphones
(3, 2, 1, true),   -- 1 X32 Mixer
(5, 2, 6, true),   -- 6 LED Panels
(9, 2, 2, true),   -- 2 Speaker Stands
(10, 2, 8, true),  -- 8 XLR Cables
(12, 2, 1, true),  -- 1 Power Conditioner

-- Concert Package
(1, 3, 4, true),   -- 4 JBL Speakers
(2, 3, 6, true),   -- 6 SM58 Microphones
(3, 3, 1, true),   -- 1 X32 Mixer
(4, 3, 2, true),   -- 2 Crown Amplifiers
(6, 3, 8, true),   -- 8 Moving Heads
(7, 3, 6, true),   -- 6 Wash Lights
(8, 3, 1, true),   -- 1 DMX Controller
(9, 3, 4, true),   -- 4 Speaker Stands
(10, 3, 12, true), -- 12 XLR Cables
(11, 3, 2, true),  -- 2 Equipment Cases
(12, 3, 2, true),  -- 2 Power Conditioners

-- Wedding Package
(1, 4, 2, true),   -- 2 JBL Speakers
(2, 4, 2, true),   -- 2 SM58 Microphones
(5, 4, 8, true),   -- 8 LED Panels
(7, 4, 4, true),   -- 4 Wash Lights
(9, 4, 2, true),   -- 2 Speaker Stands
(10, 4, 6, true),  -- 6 XLR Cables
(11, 4, 1, true),  -- 1 Equipment Case

-- DJ Package
(1, 5, 2, true),   -- 2 JBL Speakers
(2, 5, 1, true),   -- 1 SM58 Microphone
(3, 5, 1, true),   -- 1 X32 Mixer
(5, 5, 6, true),   -- 6 LED Panels
(6, 5, 2, true),   -- 2 Moving Heads
(9, 5, 2, true),   -- 2 Speaker Stands
(10, 5, 4, true),  -- 4 XLR Cables

-- Conference Package
(1, 6, 4, true),   -- 4 JBL Speakers
(2, 6, 8, true),   -- 8 SM58 Microphones
(3, 6, 1, true),   -- 1 X32 Mixer
(5, 6, 12, true),  -- 12 LED Panels
(7, 6, 8, true),   -- 8 Wash Lights
(9, 6, 4, true),   -- 4 Speaker Stands
(10, 6, 16, true), -- 16 XLR Cables
(11, 6, 2, true),  -- 2 Equipment Cases
(12, 6, 3, true);  -- 3 Power Conditioners
