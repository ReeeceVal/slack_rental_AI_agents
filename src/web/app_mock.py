"""
Mock Flask web application for Equipment Database System (Testing Only)

This version doesn't require database connections and uses mock data for testing.
"""

from flask import Flask, render_template, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Mock data for testing
MOCK_EQUIPMENT = [
    {
        'id': 1,
        'name': 'Professional PA Speaker',
        'description': 'High-quality powered speaker system for live events',
        'equipment_type': 'speaker',
        'brand': 'JBL',
        'model': 'EON615',
        'availability_status': 'available',
        'rental_price_per_day': 75.00
    },
    {
        'id': 2,
        'name': 'Wireless Microphone System',
        'description': 'Professional wireless microphone with receiver',
        'equipment_type': 'microphone',
        'brand': 'Shure',
        'model': 'BLX24R/SM58',
        'availability_status': 'available',
        'rental_price_per_day': 45.00
    },
    {
        'id': 3,
        'name': 'LED Wash Light',
        'description': 'RGB LED wash light for stage lighting',
        'equipment_type': 'light',
        'brand': 'Chauvet',
        'model': 'Par Hex 12',
        'availability_status': 'rented',
        'rental_price_per_day': 35.00
    }
]

MOCK_CATEGORIES = [
    {
        'id': 1,
        'name': 'Party Package',
        'description': 'Complete audio and lighting setup for parties and small events'
    },
    {
        'id': 2,
        'name': 'Corporate Package',
        'description': 'Professional audio and visual equipment for corporate presentations'
    }
]

@app.route('/')
def search_page():
    """Main search page"""
    return render_template('search.html')

@app.route('/api/search')
def search_equipment():
    """Search equipment API endpoint"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    
    try:
        # Simple mock search - filter by query in name or description
        query_lower = query.lower()
        
        # Search equipment
        equipment_results = [
            eq for eq in MOCK_EQUIPMENT 
            if query_lower in eq['name'].lower() or query_lower in eq['description'].lower()
        ]
        
        # Search categories
        category_results = [
            cat for cat in MOCK_CATEGORIES 
            if query_lower in cat['name'].lower() or query_lower in cat['description'].lower()
        ]
        
        return jsonify({
            'equipment': equipment_results,
            'categories': category_results,
            'query': query,
            'total_equipment': len(equipment_results),
            'total_categories': len(category_results)
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/api/equipment/<int:equipment_id>')
def get_equipment_details(equipment_id):
    """Get detailed equipment information"""
    try:
        equipment = next((eq for eq in MOCK_EQUIPMENT if eq['id'] == equipment_id), None)
        if not equipment:
            return jsonify({'error': 'Equipment not found'}), 404
        
        # Add some mock additional details
        equipment_data = {
            **equipment,
            'power_rating': '1000W',
            'dimensions': '24" x 15" x 12"',
            'weight': '25 lbs',
            'created_at': '2024-01-15T10:00:00',
            'updated_at': '2024-01-15T10:00:00'
        }
        
        return jsonify(equipment_data)
        
    except Exception as e:
        logger.error(f"Equipment details error: {e}")
        return jsonify({'error': 'Failed to get equipment details'}), 500

@app.route('/api/equipment')
def list_equipment():
    """List all equipment with optional filtering"""
    equipment_type = request.args.get('type')
    availability = request.args.get('availability')
    
    try:
        equipment_list = MOCK_EQUIPMENT
        
        if equipment_type:
            equipment_list = [eq for eq in equipment_list if eq['equipment_type'] == equipment_type]
        elif availability:
            equipment_list = [eq for eq in equipment_list if eq['availability_status'] == availability]
        
        return jsonify({
            'equipment': equipment_list,
            'total': len(equipment_list)
        })
        
    except Exception as e:
        logger.error(f"List equipment error: {e}")
        return jsonify({'error': 'Failed to list equipment'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
