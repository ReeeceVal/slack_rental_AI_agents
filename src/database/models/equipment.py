"""
Equipment data model for the Equipment Database System
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.database.models.base import BaseModel

logger = logging.getLogger(__name__)

class Equipment(BaseModel):
    """Equipment data model and database operations"""
    
    # Valid equipment types
    VALID_EQUIPMENT_TYPES = {
        'speaker', 'light', 'microphone', 'mixer', 'amplifier', 
        'cable', 'stand', 'case', 'controller', 'other'
    }
    
    # Valid availability statuses
    VALID_AVAILABILITY_STATUSES = {
        'available', 'rented', 'maintenance', 'retired'
    }
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.equipment_type = kwargs.get('equipment_type')
        self.brand = kwargs.get('brand')
        self.model = kwargs.get('model')
        self.power_rating = kwargs.get('power_rating')
        self.dimensions = kwargs.get('dimensions')
        self.weight = kwargs.get('weight')
        self.rental_price_per_day = kwargs.get('rental_price_per_day')
        self.availability_status = kwargs.get('availability_status', 'available')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
    
    @classmethod
    def validate_equipment_data(cls, data: Dict[str, Any]) -> bool:
        """Validate equipment data before database operations"""
        # Check required fields
        required_fields = ['name', 'description', 'equipment_type']
        if not cls._validate_required_fields(data, required_fields):
            logger.error("Missing required fields for equipment")
            return False
        
        # Validate equipment type
        if data['equipment_type'] not in cls.VALID_EQUIPMENT_TYPES:
            logger.error(f"Invalid equipment type: {data['equipment_type']}")
            return False
        
        # Validate availability status if provided
        if 'availability_status' in data and data['availability_status'] not in cls.VALID_AVAILABILITY_STATUSES:
            logger.error(f"Invalid availability status: {data['availability_status']}")
            return False
        
        # Validate numeric fields
        if 'weight' in data and not cls._validate_positive_number(data['weight'], 'weight'):
            return False
        
        if 'rental_price_per_day' in data and not cls._validate_positive_number(data['rental_price_per_day'], 'rental_price_per_day'):
            return False
        
        # Sanitize string fields
        if 'name' in data:
            data['name'] = cls._sanitize_string(data['name'], 255)
        
        if 'description' in data:
            data['description'] = cls._sanitize_string(data['description'])
        
        if 'brand' in data:
            data['brand'] = cls._sanitize_string(data['brand'], 100)
        
        if 'model' in data:
            data['model'] = cls._sanitize_string(data['model'], 100)
        
        return True
    
    @staticmethod
    def get_equipment_by_id(equipment_id: int) -> Optional['Equipment']:
        """Retrieve single equipment item by ID"""
        result = Equipment._execute_query(
            "SELECT * FROM equipment WHERE id = %s",
            (equipment_id,),
            fetch_one=True
        )
        
        if result:
            return Equipment(**result)
        return None
    
    @staticmethod
    def get_equipment_by_type(equipment_type: str) -> List['Equipment']:
        """Get all equipment of a specific type"""
        results = Equipment._execute_query(
            "SELECT * FROM equipment WHERE equipment_type = %s ORDER BY name",
            (equipment_type,)
        )
        
        if results:
            return [Equipment(**result) for result in results]
        return []
    
    @staticmethod
    def search_equipment(query: str) -> List['Equipment']:
        """Full-text search across name and description"""
        results = Equipment._execute_query(
            """
            SELECT *, ts_rank(to_tsvector('english', name || ' ' || description), plainto_tsquery('english', %s)) as rank
            FROM equipment 
            WHERE to_tsvector('english', name || ' ' || description) @@ plainto_tsquery('english', %s)
            ORDER BY rank DESC, name
            """,
            (query, query)
        )
        
        if results:
            return [Equipment(**result) for result in results]
        return []
    
    @staticmethod
    def get_available_equipment() -> List['Equipment']:
        """Get all available equipment"""
        results = Equipment._execute_query(
            "SELECT * FROM equipment WHERE availability_status = 'available' ORDER BY name"
        )
        
        if results:
            return [Equipment(**result) for result in results]
        return []
    
    @staticmethod
    def get_equipment_by_category(category_id: int) -> List['Equipment']:
        """Get all equipment in a specific category"""
        results = Equipment._execute_query(
            """
            SELECT e.*, ec.quantity_in_package, ec.is_required
            FROM equipment e
            JOIN equipment_categories ec ON e.id = ec.equipment_id
            WHERE ec.category_id = %s
            ORDER BY ec.is_required DESC, e.name
            """,
            (category_id,)
        )
        
        if results:
            equipment_list = []
            for result in results:
                equipment = Equipment(**result)
                equipment.quantity_in_package = result['quantity_in_package']
                equipment.is_required = result['is_required']
                equipment_list.append(equipment)
            return equipment_list
        return []
    
    @staticmethod
    def get_all_equipment() -> List['Equipment']:
        """Get all equipment items"""
        results = Equipment._execute_query(
            "SELECT * FROM equipment ORDER BY name"
        )
        
        if results:
            return [Equipment(**result) for result in results]
        return []
    
    @staticmethod
    def get_equipment_by_availability(availability_status: str) -> List['Equipment']:
        """Get equipment by availability status"""
        if availability_status not in Equipment.VALID_AVAILABILITY_STATUSES:
            logger.error(f"Invalid availability status: {availability_status}")
            return []
        
        results = Equipment._execute_query(
            "SELECT * FROM equipment WHERE availability_status = %s ORDER BY name",
            (availability_status,)
        )
        
        if results:
            return [Equipment(**result) for result in results]
        return []
    
    @staticmethod
    def create_equipment(equipment_data: Dict[str, Any]) -> Optional['Equipment']:
        """Create new equipment item"""
        # Validate input data
        if not Equipment.validate_equipment_data(equipment_data):
            logger.error("Invalid equipment data provided")
            return None
        
        result = Equipment._execute_query(
            """
            INSERT INTO equipment (name, description, equipment_type, brand, model, 
                                power_rating, dimensions, weight, rental_price_per_day, availability_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
            """,
            (
                equipment_data['name'],
                equipment_data['description'],
                equipment_data['equipment_type'],
                equipment_data.get('brand'),
                equipment_data.get('model'),
                equipment_data.get('power_rating'),
                equipment_data.get('dimensions'),
                equipment_data.get('weight'),
                equipment_data.get('rental_price_per_day'),
                equipment_data.get('availability_status', 'available')
            ),
            fetch_one=True,
            commit=True
        )
        
        if result:
            return Equipment(**result)
        return None
    
    @staticmethod
    def update_equipment(equipment_id: int, update_data: Dict[str, Any]) -> bool:
        """Update equipment item"""
        # Validate update data
        if not Equipment.validate_equipment_data(update_data):
            logger.error("Invalid update data provided")
            return False
        
        # Build dynamic update query
        set_clauses = []
        values = []
        for key, value in update_data.items():
            if key != 'id' and hasattr(Equipment, key):
                set_clauses.append(f"{key} = %s")
                values.append(value)
        
        if not set_clauses:
            return False
        
        values.append(equipment_id)
        query = f"""
            UPDATE equipment 
            SET {', '.join(set_clauses)}, updated_at = NOW()
            WHERE id = %s
        """
        
        return Equipment._execute_query(query, tuple(values), commit=True)
    
    @staticmethod
    def delete_equipment(equipment_id: int) -> bool:
        """Delete equipment item"""
        return Equipment._execute_query(
            "DELETE FROM equipment WHERE id = %s",
            (equipment_id,),
            commit=True
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert equipment to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'equipment_type': self.equipment_type,
            'brand': self.brand,
            'model': self.model,
            'power_rating': self.power_rating,
            'dimensions': self.dimensions,
            'weight': self.weight,
            'rental_price_per_day': self.rental_price_per_day,
            'availability_status': self.availability_status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __repr__(self) -> str:
        return f"Equipment(id={self.id}, name='{self.name}', type='{self.equipment_type}')"
