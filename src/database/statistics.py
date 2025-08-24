"""
Database statistics and reporting module for the Equipment Database System
"""
import logging
from typing import Dict, Any, List

from src.database.connection import get_db_connection

logger = logging.getLogger(__name__)

class DatabaseStatistics:
    """Database statistics and reporting operations"""
    
    @staticmethod
    def get_database_statistics() -> Dict[str, Any]:
        """Get overall database statistics"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            # Equipment statistics
            cursor.execute("SELECT COUNT(*) FROM equipment")
            total_equipment = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM equipment WHERE availability_status = 'available'")
            available_equipment = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT equipment_type) FROM equipment")
            equipment_types = cursor.fetchone()[0]
            
            # Category statistics
            cursor.execute("SELECT COUNT(*) FROM categories")
            total_categories = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT target_audience) FROM categories")
            audience_types = cursor.fetchone()[0]
            
            # Package statistics
            cursor.execute("SELECT COUNT(*) FROM equipment_categories")
            total_associations = cursor.fetchone()[0]
            
            cursor.close()
            db_conn.return_connection(conn)
            
            return {
                'equipment': {
                    'total': total_equipment,
                    'available': available_equipment,
                    'types': equipment_types
                },
                'categories': {
                    'total': total_categories,
                    'audience_types': audience_types
                },
                'packages': {
                    'total_associations': total_associations
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting database statistics: {e}")
            return {}
    
    @staticmethod
    def get_equipment_type_statistics() -> Dict[str, Any]:
        """Get statistics by equipment type"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT equipment_type, 
                       COUNT(*) as total_count,
                       COUNT(CASE WHEN availability_status = 'available' THEN 1 END) as available_count,
                       AVG(rental_price_per_day) as avg_price
                FROM equipment 
                GROUP BY equipment_type
                ORDER BY total_count DESC
            """)
            
            results = cursor.fetchall()
            cursor.close()
            db_conn.return_connection(conn)
            
            type_stats = {}
            for result in results:
                type_stats[result[0]] = {
                    'total_count': result[1],
                    'available_count': result[2],
                    'avg_price': round(float(result[3] or 0), 2)
                }
            
            return type_stats
            
        except Exception as e:
            logger.error(f"Error getting equipment type statistics: {e}")
            return {}
    
    @staticmethod
    def get_category_statistics() -> Dict[str, Any]:
        """Get statistics by category"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.name, c.target_audience, c.typical_event_size,
                       COUNT(ec.equipment_id) as equipment_count,
                       COUNT(DISTINCT ec.equipment_id) as unique_equipment_count,
                       SUM(ec.quantity_in_package) as total_items
                FROM categories c
                LEFT JOIN equipment_categories ec ON c.id = ec.category_id
                GROUP BY c.id, c.name, c.target_audience, c.typical_event_size
                ORDER BY equipment_count DESC
            """)
            
            results = cursor.fetchall()
            cursor.close()
            db_conn.return_connection(conn)
            
            category_stats = []
            for result in results:
                category_stats.append({
                    'name': result[0],
                    'target_audience': result[1],
                    'typical_event_size': result[2],
                    'equipment_count': result[3],
                    'unique_equipment_count': result[4],
                    'total_items': result[5] or 0
                })
            
            return category_stats
            
        except Exception as e:
            logger.error(f"Error getting category statistics: {e}")
            return []
    
    @staticmethod
    def get_availability_statistics() -> Dict[str, Any]:
        """Get equipment availability statistics"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT availability_status,
                       COUNT(*) as count,
                       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM equipment), 2) as percentage
                FROM equipment
                GROUP BY availability_status
                ORDER BY count DESC
            """)
            
            results = cursor.fetchall()
            cursor.close()
            db_conn.return_connection(conn)
            
            availability_stats = {}
            for result in results:
                availability_stats[result[0]] = {
                    'count': result[1],
                    'percentage': result[2]
                }
            
            return availability_stats
            
        except Exception as e:
            logger.error(f"Error getting availability statistics: {e}")
            return {}
    
    @staticmethod
    def get_price_statistics() -> Dict[str, Any]:
        """Get equipment pricing statistics"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    MIN(rental_price_per_day) as min_price,
                    MAX(rental_price_per_day) as max_price,
                    AVG(rental_price_per_day) as avg_price,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY rental_price_per_day) as median_price
                FROM equipment
                WHERE rental_price_per_day IS NOT NULL
            """)
            
            result = cursor.fetchone()
            cursor.close()
            db_conn.return_connection(conn)
            
            if result:
                return {
                    'min_price': round(float(result[0] or 0), 2),
                    'max_price': round(float(result[1] or 0), 2),
                    'avg_price': round(float(result[2] or 0), 2),
                    'median_price': round(float(result[3] or 0), 2)
                }
            return {}
            
        except Exception as e:
            logger.error(f"Error getting price statistics: {e}")
            return {}
    
    @staticmethod
    def get_audience_statistics() -> Dict[str, Any]:
        """Get statistics by target audience"""
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT target_audience,
                       COUNT(*) as category_count,
                       COUNT(DISTINCT ec.equipment_id) as total_equipment_types
                FROM categories c
                LEFT JOIN equipment_categories ec ON c.id = ec.category_id
                GROUP BY target_audience
                ORDER BY category_count DESC
            """)
            
            results = cursor.fetchall()
            cursor.close()
            db_conn.return_connection(conn)
            
            audience_stats = {}
            for result in results:
                audience_stats[result[0]] = {
                    'category_count': result[1],
                    'total_equipment_types': result[2] or 0
                }
            
            return audience_stats
            
        except Exception as e:
            logger.error(f"Error getting audience statistics: {e}")
            return {}

# Global statistics instance
database_statistics = DatabaseStatistics()

def get_database_statistics() -> DatabaseStatistics:
    """Get the global database statistics instance"""
    return database_statistics
