"""
Centralized database repository for the Equipment Database System
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from src.database.models.equipment import Equipment
from src.database.models.category import Category
from src.database.models.equipment_category import EquipmentCategory
from src.database.statistics import get_database_statistics
from src.database.connection import get_db_connection

logger = logging.getLogger(__name__)

class EquipmentRepository:
    """Centralized repository for all equipment database operations"""
    
    def __init__(self):
        self.db_connection = get_db_connection()
        self.statistics = get_database_statistics()
    
    # Equipment Operations
    def get_equipment(self, equipment_id: int) -> Optional[Equipment]:
        """Get equipment by ID"""
        return Equipment.get_equipment_by_id(equipment_id)
    
    def get_equipment_by_type(self, equipment_type: str) -> List[Equipment]:
        """Get equipment by type"""
        return Equipment.get_equipment_by_type(equipment_type)
    
    def search_equipment(self, query: str) -> List[Equipment]:
        """Search equipment by query"""
        return Equipment.search_equipment(query)
    
    def get_available_equipment(self) -> List[Equipment]:
        """Get all available equipment"""
        return Equipment.get_available_equipment()
    
    def create_equipment(self, equipment_data: Dict[str, Any]) -> Optional[Equipment]:
        """Create new equipment"""
        return Equipment.create_equipment(equipment_data)
    
    def update_equipment(self, equipment_id: int, update_data: Dict[str, Any]) -> bool:
        """Update equipment"""
        return Equipment.update_equipment(equipment_id, update_data)
    
    def delete_equipment(self, equipment_id: int) -> bool:
        """Delete equipment"""
        return Equipment.delete_equipment(equipment_id)
    
    # Category Operations
    def get_category(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        return Category.get_category_by_id(category_id)
    
    def get_all_categories(self) -> List[Category]:
        """Get all categories"""
        return Category.get_all_categories()
    
    def get_categories_by_audience(self, target_audience: str) -> List[Category]:
        """Get categories by audience"""
        return Category.get_categories_by_audience(target_audience)
    
    def get_category_with_equipment(self, category_id: int) -> Optional[Dict[str, Any]]:
        """Get category with all equipment"""
        return Category.get_category_with_equipment(category_id)
    
    def create_category(self, category_data: Dict[str, Any]) -> Optional[Category]:
        """Create new category"""
        return Category.create_category(category_data)
    
    def update_category(self, category_id: int, update_data: Dict[str, Any]) -> bool:
        """Update category"""
        return Category.update_category(category_id, update_data)
    
    def delete_category(self, category_id: int) -> bool:
        """Delete category"""
        return Category.delete_category(category_id)
    
    # Package Operations
    def get_package_details(self, category_id: int) -> Optional[Dict[str, Any]]:
        """Get complete package details"""
        return EquipmentCategory.get_package_details(category_id)
    
    def add_equipment_to_package(self, equipment_id: int, category_id: int, 
                                 quantity: int = 1, required: bool = True) -> bool:
        """Add equipment to package"""
        return EquipmentCategory.add_equipment_to_category(equipment_id, category_id, quantity, required)
    
    def remove_equipment_from_package(self, equipment_id: int, category_id: int) -> bool:
        """Remove equipment from package"""
        return EquipmentCategory.remove_equipment_from_category(equipment_id, category_id)
    
    def update_package_quantity(self, equipment_id: int, category_id: int, 
                               new_quantity: int) -> bool:
        """Update equipment quantity in package"""
        return EquipmentCategory.update_package_quantity(equipment_id, category_id, new_quantity)
    
    def update_package_requirement(self, equipment_id: int, category_id: int, 
                                  is_required: bool) -> bool:
        """Update whether equipment is required in package"""
        return EquipmentCategory.update_package_requirement(equipment_id, category_id, is_required)
    
    # Advanced Search and Recommendation Operations
    def search_packages(self, query: str) -> List[Dict[str, Any]]:
        """Search packages by name and description"""
        categories = Category.search_categories(query)
        package_results = []
        
        for category in categories:
            package_details = self.get_package_details(category.id)
            if package_details:
                package_results.append(package_details)
        
        return package_results
    
    def get_packages_by_audience_and_size(self, target_audience: str, 
                                         event_size: str) -> List[Dict[str, Any]]:
        """Get packages filtered by audience and event size"""
        categories = Category.get_categories_by_audience(target_audience)
        filtered_categories = [cat for cat in categories if cat.typical_event_size == event_size]
        
        package_results = []
        for category in filtered_categories:
            package_details = self.get_package_details(category.id)
            if package_details:
                package_results.append(package_details)
        
        return package_results
    
    def get_equipment_compatibility(self, equipment_id: int) -> List[Dict[str, Any]]:
        """Get compatibility information for equipment"""
        return EquipmentCategory.get_package_compatibility(equipment_id)
    
    def get_equipment_in_packages(self, equipment_id: int) -> List[Dict[str, Any]]:
        """Get all packages that contain specific equipment"""
        return EquipmentCategory.get_equipment_categories(equipment_id)
    
    # Bulk Operations
    def create_package_from_equipment_list(self, category_data: Dict[str, Any], 
                                          equipment_list: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Create a new package with multiple equipment items"""
        try:
            # Create the category first
            category = self.create_category(category_data)
            if not category:
                return None
            
            # Add equipment to the category
            for equipment_item in equipment_list:
                equipment_id = equipment_item['equipment_id']
                quantity = equipment_item.get('quantity', 1)
                required = equipment_item.get('required', True)
                
                success = self.add_equipment_to_package(
                    equipment_id, category.id, quantity, required
                )
                
                if not success:
                    logger.warning(f"Failed to add equipment {equipment_id} to category {category.id}")
            
            # Return the complete package details
            return self.get_package_details(category.id)
            
        except Exception as e:
            logger.error(f"Error creating package from equipment list: {e}")
            return None
    
    def duplicate_package(self, source_category_id: int, new_category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Duplicate an existing package with new category details"""
        try:
            # Get source package details
            source_package = self.get_package_details(source_category_id)
            if not source_package:
                return None
            
            # Create new category
            new_category = self.create_category(new_category_data)
            if not new_category:
                return None
            
            # Copy equipment associations
            for equipment_item in source_package['equipment']:
                equipment_id = equipment_item['id']
                quantity = equipment_item['quantity_in_package']
                required = equipment_item['is_required']
                
                success = self.add_equipment_to_package(
                    equipment_id, new_category.id, quantity, required
                )
                
                if not success:
                    logger.warning(f"Failed to copy equipment {equipment_id} to new category {new_category.id}")
            
            # Return the new package details
            return self.get_package_details(new_category.id)
            
        except Exception as e:
            logger.error(f"Error duplicating package {source_category_id}: {e}")
            return None
    
    # Statistics and Reporting
    def get_database_statistics(self) -> Dict[str, Any]:
        """Get overall database statistics"""
        return self.statistics.get_database_statistics()
    
    def get_equipment_type_statistics(self) -> Dict[str, Any]:
        """Get statistics by equipment type"""
        return self.statistics.get_equipment_type_statistics()
    
    def get_category_statistics(self) -> Dict[str, Any]:
        """Get statistics by category"""
        return self.statistics.get_category_statistics()
    
    def get_availability_statistics(self) -> Dict[str, Any]:
        """Get equipment availability statistics"""
        return self.statistics.get_availability_statistics()
    
    def get_price_statistics(self) -> Dict[str, Any]:
        """Get equipment pricing statistics"""
        return self.statistics.get_price_statistics()
    
    def get_audience_statistics(self) -> Dict[str, Any]:
        """Get statistics by target audience"""
        return self.statistics.get_audience_statistics()
    
    def health_check(self) -> bool:
        """Check database health"""
        return self.db_connection.health_check()

# Global repository instance
equipment_repository = EquipmentRepository()

def get_equipment_repository() -> EquipmentRepository:
    """Get the global equipment repository instance"""
    return equipment_repository
