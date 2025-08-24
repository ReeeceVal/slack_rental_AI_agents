"""
Category data model for the Equipment Database System
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.database.connection import get_db_connection

logger = logging.getLogger(__name__)

class Category:
    """Category data model and database operations"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.target_audience = kwargs.get('target_audience')
        self.typical_event_size = kwargs.get('typical_event_size')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
    
    @staticmethod
    def get_category_by_id(category_id: int) -> Optional['Category']:
        """Retrieve single category by ID"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM categories WHERE id = %s
            """, (category_id,))
            
            result = cursor.fetchone()
            cursor.close()
            db_conn.return_connection(conn)
            
            if result:
                return Category(**dict(result))
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving category by ID {category_id}: {e}")
            return None
    
    @staticmethod
    def get_all_categories() -> List['Category']:
        """Get all categories"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM categories ORDER BY name
            """)
            
            results = cursor.fetchall()
            cursor.close()
            db_conn.return_connection(conn)
            
            return [Category(**dict(result)) for result in results]
            
        except Exception as e:
            logger.error(f"Error retrieving all categories: {e}")
            return []
    
    @staticmethod
    def get_categories_by_audience(target_audience: str) -> List['Category']:
        """Get categories for specific audience"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM categories 
                WHERE target_audience = %s 
                ORDER BY name
            """, (target_audience,))
            
            results = cursor.fetchall()
            cursor.close()
            db_conn.return_connection(conn)
            
            return [Category(**dict(result)) for result in results]
            
        except Exception as e:
            logger.error(f"Error retrieving categories by audience {target_audience}: {e}")
            return []
    
    @staticmethod
    def get_category_with_equipment(category_id: int) -> Optional[Dict[str, Any]]:
        """Get category with all associated equipment"""
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
            
            # Get associated equipment
            cursor.execute("""
                SELECT e.*, ec.quantity_in_package, ec.is_required
                FROM equipment e
                JOIN equipment_categories ec ON e.id = ec.equipment_id
                WHERE ec.category_id = %s
                ORDER BY ec.is_required DESC, e.equipment_type, e.name
            """, (category_id,))
            
            equipment_results = cursor.fetchall()
            cursor.close()
            db_conn.return_connection(conn)
            
            # Build response
            category = Category(**dict(category_result))
            equipment_list = []
            
            for result in equipment_results:
                equipment_data = dict(result)
                equipment_data['quantity_in_package'] = result['quantity_in_package']
                equipment_data['is_required'] = result['is_required']
                equipment_list.append(equipment_data)
            
            return {
                'category': category.to_dict(),
                'equipment': equipment_list,
                'total_equipment_count': len(equipment_list),
                'required_equipment_count': sum(1 for eq in equipment_list if eq['is_required'])
            }
            
        except Exception as e:
            logger.error(f"Error retrieving category with equipment {category_id}: {e}")
            return None
    
    @staticmethod
    def create_category(category_data: Dict[str, Any]) -> Optional['Category']:
        """Create new category"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO categories (name, description, target_audience, typical_event_size)
                VALUES (%s, %s, %s, %s)
                RETURNING *
            """, (
                category_data['name'],
                category_data.get('description'),
                category_data.get('target_audience'),
                category_data.get('typical_event_size')
            ))
            
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
            db_conn.return_connection(conn)
            
            if result:
                return Category(**dict(result))
            return None
            
        except Exception as e:
            logger.error(f"Error creating category: {e}")
            if 'conn' in locals():
                conn.rollback()
            return None
    
    @staticmethod
    def update_category(category_id: int, update_data: Dict[str, Any]) -> bool:
        """Update category"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            # Build dynamic update query
            set_clauses = []
            values = []
            for key, value in update_data.items():
                if key != 'id' and hasattr(Category, key):
                    set_clauses.append(f"{key} = %s")
                    values.append(value)
            
            if not set_clauses:
                return False
            
            values.append(category_id)
            query = f"""
                UPDATE categories 
                SET {', '.join(set_clauses)}, updated_at = NOW()
                WHERE id = %s
            """
            
            cursor.execute(query, values)
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            db_conn.return_connection(conn)
            
            return rows_affected > 0
            
        except Exception as e:
            logger.error(f"Error updating category {category_id}: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
    
    @staticmethod
    def delete_category(category_id: int) -> bool:
        """Delete category (will cascade delete equipment associations)"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            db_conn.return_connection(conn)
            
            return rows_affected > 0
            
        except Exception as e:
            logger.error(f"Error deleting category {category_id}: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
    
    @staticmethod
    def search_categories(query: str) -> List['Category']:
        """Search categories by name and description"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM categories 
                WHERE name ILIKE %s OR description ILIKE %s
                ORDER BY name
            """, (f'%{query}%', f'%{query}%'))
            
            results = cursor.fetchall()
            cursor.close()
            db_conn.return_connection(conn)
            
            return [Category(**dict(result)) for result in results]
            
        except Exception as e:
            logger.error(f"Error searching categories with query '{query}': {e}")
            return []
    
    @staticmethod
    def get_categories_by_event_size(event_size: str) -> List['Category']:
        """Get categories by typical event size"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM categories 
                WHERE typical_event_size = %s 
                ORDER BY name
            """, (event_size,))
            
            results = cursor.fetchall()
            cursor.close()
            db_conn.return_connection(conn)
            
            return [Category(**dict(result)) for result in results]
            
        except Exception as e:
            logger.error(f"Error retrieving categories by event size {event_size}: {e}")
            return []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert category to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'target_audience': self.target_audience,
            'typical_event_size': self.typical_event_size,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __repr__(self) -> str:
        return f"Category(id={self.id}, name='{self.name}', audience='{self.target_audience}')"
