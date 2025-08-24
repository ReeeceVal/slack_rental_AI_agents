"""
Equipment-Category junction table model for the Equipment Database System
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from src.database.connection import get_db_connection

logger = logging.getLogger(__name__)

class EquipmentCategory:
    """Equipment-Category junction table model and operations"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.equipment_id = kwargs.get('equipment_id')
        self.category_id = kwargs.get('category_id')
        self.quantity_in_package = kwargs.get('quantity_in_package', 1)
        self.is_required = kwargs.get('is_required', True)
        self.created_at = kwargs.get('created_at')
    
    @staticmethod
    def add_equipment_to_category(equipment_id: int, category_id: int, 
                                 quantity: int = 1, required: bool = True) -> bool:
        """Associate equipment with category"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            # Check if association already exists
            cursor.execute("""
                SELECT id FROM equipment_categories 
                WHERE equipment_id = %s AND category_id = %s
            """, (equipment_id, category_id))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing association
                cursor.execute("""
                    UPDATE equipment_categories 
                    SET quantity_in_package = %s, is_required = %s
                    WHERE equipment_id = %s AND category_id = %s
                """, (quantity, required, equipment_id, category_id))
            else:
                # Create new association
                cursor.execute("""
                    INSERT INTO equipment_categories (equipment_id, category_id, quantity_in_package, is_required)
                    VALUES (%s, %s, %s, %s)
                """, (equipment_id, category_id, quantity, required))
            
            conn.commit()
            cursor.close()
            db_conn.return_connection(conn)
            
            logger.info(f"Equipment {equipment_id} associated with category {category_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error associating equipment {equipment_id} with category {category_id}: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
    
    @staticmethod
    def remove_equipment_from_category(equipment_id: int, category_id: int) -> bool:
        """Remove association between equipment and category"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM equipment_categories 
                WHERE equipment_id = %s AND category_id = %s
            """, (equipment_id, category_id))
            
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            db_conn.return_connection(conn)
            
            if rows_affected > 0:
                logger.info(f"Equipment {equipment_id} removed from category {category_id}")
                return True
            else:
                logger.warning(f"No association found between equipment {equipment_id} and category {category_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error removing equipment {equipment_id} from category {category_id}: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
    
    @staticmethod
    def get_package_details(category_id: int) -> Optional[Dict[str, Any]]:
        """Get complete package information with equipment"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            # Get category details
            cursor.execute("""
                SELECT * FROM categories WHERE id = %s
            """, (category_id,))
            
            category_result = cursor.fetchone()
            if not category_result:
                cursor.close()
                db_conn.return_connection(conn)
                return None
            
            # Get all equipment in the package with quantities and requirements
            cursor.execute("""
                SELECT e.*, ec.quantity_in_package, ec.is_required,
                       c.name as category_name, c.description as category_description
                FROM equipment e
                JOIN equipment_categories ec ON e.id = ec.equipment_id
                JOIN categories c ON ec.category_id = c.id
                WHERE ec.category_id = %s
                ORDER BY ec.is_required DESC, e.equipment_type, e.name
            """, (category_id,))
            
            equipment_results = cursor.fetchall()
            cursor.close()
            db_conn.return_connection(conn)
            
            # Calculate package statistics
            total_items = sum(result['quantity_in_package'] for result in equipment_results)
            required_items = sum(result['quantity_in_package'] for result in equipment_results if result['is_required'])
            total_value = sum(result['rental_price_per_day'] * result['quantity_in_package'] for result in equipment_results)
            
            # Group equipment by type
            equipment_by_type = {}
            for result in equipment_results:
                eq_type = result['equipment_type']
                if eq_type not in equipment_by_type:
                    equipment_by_type[eq_type] = []
                
                equipment_data = dict(result)
                equipment_data['quantity_in_package'] = result['quantity_in_package']
                equipment_data['is_required'] = result['is_required']
                equipment_by_type[eq_type].append(equipment_data)
            
            return {
                'category': {
                    'id': category_result['id'],
                    'name': category_result['name'],
                    'description': category_result['description'],
                    'target_audience': category_result['target_audience'],
                    'typical_event_size': category_result['typical_event_size']
                },
                'equipment': equipment_results,
                'equipment_by_type': equipment_by_type,
                'statistics': {
                    'total_equipment_types': len(equipment_by_type),
                    'total_items': total_items,
                    'required_items': required_items,
                    'optional_items': total_items - required_items,
                    'estimated_daily_cost': round(total_value, 2)
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting package details for category {category_id}: {e}")
            return None
    
    @staticmethod
    def get_equipment_categories(equipment_id: int) -> List[Dict[str, Any]]:
        """Get all categories that an equipment item belongs to"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.*, ec.quantity_in_package, ec.is_required
                FROM categories c
                JOIN equipment_categories ec ON c.id = ec.category_id
                WHERE ec.equipment_id = %s
                ORDER BY c.name
            """, (equipment_id,))
            
            results = cursor.fetchall()
            cursor.close()
            db_conn.return_connection(conn)
            
            return [dict(result) for result in results]
            
        except Exception as e:
            logger.error(f"Error getting categories for equipment {equipment_id}: {e}")
            return []
    
    @staticmethod
    def update_package_quantity(equipment_id: int, category_id: int, 
                               new_quantity: int) -> bool:
        """Update quantity of equipment in a package"""
        try:
            if new_quantity <= 0:
                logger.error(f"Invalid quantity {new_quantity} for equipment {equipment_id}")
                return False
            
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE equipment_categories 
                SET quantity_in_package = %s
                WHERE equipment_id = %s AND category_id = %s
            """, (new_quantity, equipment_id, category_id))
            
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            db_conn.return_connection(conn)
            
            if rows_affected > 0:
                logger.info(f"Updated quantity for equipment {equipment_id} in category {category_id} to {new_quantity}")
                return True
            else:
                logger.warning(f"No association found to update for equipment {equipment_id} in category {category_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating quantity for equipment {equipment_id} in category {category_id}: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
    
    @staticmethod
    def update_package_requirement(equipment_id: int, category_id: int, 
                                  is_required: bool) -> bool:
        """Update whether equipment is required in a package"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE equipment_categories 
                SET is_required = %s
                WHERE equipment_id = %s AND category_id = %s
            """, (is_required, equipment_id, category_id))
            
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            db_conn.return_connection(conn)
            
            if rows_affected > 0:
                requirement_text = "required" if is_required else "optional"
                logger.info(f"Updated equipment {equipment_id} in category {category_id} to {requirement_text}")
                return True
            else:
                logger.warning(f"No association found to update for equipment {equipment_id} in category {category_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating requirement for equipment {equipment_id} in category {category_id}: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
    
    @staticmethod
    def get_package_compatibility(equipment_id: int) -> List[Dict[str, Any]]:
        """Get compatibility information for an equipment item"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            # Get all categories this equipment belongs to
            cursor.execute("""
                SELECT c.*, ec.quantity_in_package, ec.is_required
                FROM categories c
                JOIN equipment_categories ec ON c.id = ec.category_id
                WHERE ec.equipment_id = %s
                ORDER BY c.name
            """, (equipment_id,))
            
            category_results = cursor.fetchall()
            
            # Get equipment details
            cursor.execute("""
                SELECT * FROM equipment WHERE id = %s
            """, (equipment_id,))
            
            equipment_result = cursor.fetchone()
            cursor.close()
            db_conn.return_connection(conn)
            
            if not equipment_result:
                return []
            
            compatibility_info = []
            for cat_result in category_results:
                compatibility_info.append({
                    'category': {
                        'id': cat_result['id'],
                        'name': cat_result['name'],
                        'description': cat_result['description'],
                        'target_audience': cat_result['target_audience'],
                        'typical_event_size': cat_result['typical_event_size']
                    },
                    'package_details': {
                        'quantity_in_package': cat_result['quantity_in_package'],
                        'is_required': cat_result['is_required']
                    },
                    'equipment': dict(equipment_result)
                })
            
            return compatibility_info
            
        except Exception as e:
            logger.error(f"Error getting compatibility for equipment {equipment_id}: {e}")
            return []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'category_id': self.category_id,
            'quantity_in_package': self.quantity_in_package,
            'is_required': self.is_required,
            'created_at': self.created_at
        }
    
    def __repr__(self) -> str:
        return f"EquipmentCategory(equipment_id={self.equipment_id}, category_id={self.category_id}, quantity={self.quantity_in_package}, required={self.is_required})"
