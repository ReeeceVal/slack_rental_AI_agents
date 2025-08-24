"""
Base model class for common database operations
"""
import logging
from typing import List, Dict, Any, Optional, Union
from contextlib import contextmanager

from src.database.connection import get_db_connection

logger = logging.getLogger(__name__)

class BaseModel:
    """Base class for database models with common operations"""
    
    @staticmethod
    def _execute_query(query: str, params: Optional[tuple] = None, 
                      fetch_one: bool = False, commit: bool = False) -> Union[List[Dict[str, Any]], Dict[str, Any], bool, None]:
        """
        Execute a database query with common error handling and connection management
        
        Args:
            query: SQL query to execute
            params: Query parameters
            fetch_one: Whether to fetch one result or multiple
            commit: Whether to commit the transaction
            
        Returns:
            Query results or success status
        """
        db_conn = None
        conn = None
        cursor = None
        
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(query, params)
            
            if commit:
                conn.commit()
                return True
            
            if fetch_one:
                result = cursor.fetchone()
                return dict(result) if result else None
            else:
                results = cursor.fetchall()
                return [dict(result) for result in results]
                
        except Exception as e:
            logger.error(f"Database query execution failed: {e}")
            if conn and commit:
                conn.rollback()
            return None if not commit else False
            
        finally:
            if cursor:
                cursor.close()
            if conn and db_conn:
                db_conn.return_connection(conn)
    
    @staticmethod
    def _execute_transaction(queries: List[tuple]) -> bool:
        """
        Execute multiple queries in a single transaction
        
        Args:
            queries: List of (query, params) tuples
            
        Returns:
            Success status
        """
        db_conn = None
        conn = None
        cursor = None
        
        try:
            db_conn = get_db_connection()
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            
            for query, params in queries:
                cursor.execute(query, params)
            
            conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Transaction execution failed: {e}")
            if conn:
                conn.rollback()
            return False
            
        finally:
            if cursor:
                cursor.close()
            if conn and db_conn:
                db_conn.return_connection(conn)
    
    @staticmethod
    def _validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        Validate that required fields are present in data
        
        Args:
            data: Data dictionary to validate
            required_fields: List of required field names
            
        Returns:
            Validation result
        """
        return all(field in data and data[field] is not None for field in required_fields)
    
    @staticmethod
    def _sanitize_string(value: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize string input
        
        Args:
            value: String value to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not isinstance(value, str):
            return str(value) if value is not None else ""
        
        # Remove potentially dangerous characters
        sanitized = value.strip()
        
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
            
        return sanitized
    
    @staticmethod
    def _validate_positive_number(value: Union[int, float], field_name: str) -> bool:
        """
        Validate that a number is positive
        
        Args:
            value: Number to validate
            field_name: Name of the field for error logging
            
        Returns:
            Validation result
        """
        if value is None:
            return True  # Allow None values
        
        try:
            num_value = float(value)
            if num_value < 0:
                logger.warning(f"{field_name} must be positive, got: {value}")
                return False
            return True
        except (ValueError, TypeError):
            logger.warning(f"{field_name} must be a valid number, got: {value}")
            return False
