"""
Flask web application for Equipment Database System
"""
from flask import Flask, render_template, request, jsonify
import logging
from typing import List, Dict, Any

from src.database.models.equipment import Equipment
from src.database.models.category import Category
from src.database.connection import DatabaseConnection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_db_connection():
    """Get database connection"""
    try:
        return DatabaseConnection()
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return None

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
        # Search equipment
        equipment_results = Equipment.search_equipment(query)
        
        # Search categories
        category_results = Category.search_categories(query)
        
        # Format equipment results
        equipment_data = []
        for equipment in equipment_results:
            equipment_data.append({
                'id': equipment.id,
                'name': equipment.name,
                'description': equipment.description,
                'equipment_type': equipment.equipment_type,
                'brand': equipment.brand,
                'model': equipment.model,
                'availability_status': equipment.availability_status,
                'rental_price_per_day': equipment.rental_price_per_day
            })
        
        # Format category results
        category_data = []
        for category in category_results:
            category_data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description
            })
        
        return jsonify({
            'equipment': equipment_data,
            'categories': category_data,
            'query': query,
            'total_equipment': len(equipment_data),
            'total_categories': len(category_data)
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/api/equipment/<int:equipment_id>')
def get_equipment_details(equipment_id):
    """Get detailed equipment information"""
    try:
        equipment = Equipment.get_equipment_by_id(equipment_id)
        if not equipment:
            return jsonify({'error': 'Equipment not found'}), 404
        
        equipment_data = {
            'id': equipment.id,
            'name': equipment.name,
            'description': equipment.description,
            'equipment_type': equipment.equipment_type,
            'brand': equipment.brand,
            'model': equipment.model,
            'power_rating': equipment.power_rating,
            'dimensions': equipment.dimensions,
            'weight': equipment.weight,
            'rental_price_per_day': equipment.rental_price_per_day,
            'availability_status': equipment.availability_status,
            'created_at': equipment.created_at.isoformat() if equipment.created_at else None,
            'updated_at': equipment.updated_at.isoformat() if equipment.updated_at else None
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
        if equipment_type:
            equipment_list = Equipment.get_equipment_by_type(equipment_type)
        elif availability:
            if availability == 'available':
                equipment_list = Equipment.get_available_equipment()
            else:
                equipment_list = Equipment.get_equipment_by_availability(availability)
        else:
            # Get all equipment
            equipment_list = Equipment.get_all_equipment()
        
        equipment_data = []
        for equipment in equipment_list:
            equipment_data.append({
                'id': equipment.id,
                'name': equipment.name,
                'description': equipment.description,
                'equipment_type': equipment.equipment_type,
                'brand': equipment.brand,
                'model': equipment.model,
                'availability_status': equipment.availability_status,
                'rental_price_per_day': equipment.rental_price_per_day
            })
        
        return jsonify({
            'equipment': equipment_data,
            'total': len(equipment_data)
        })
        
    except Exception as e:
        logger.error(f"List equipment error: {e}")
        return jsonify({'error': 'Failed to list equipment'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
