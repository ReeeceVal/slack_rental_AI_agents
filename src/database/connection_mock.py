"""
Mock Database Connection for demonstration purposes
This allows testing the system architecture without requiring PostgreSQL drivers
"""
import logging
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class MockDatabaseConnection:
    """Mock database connection manager for demonstration"""
    
    def __init__(self):
        self._connected = False
        logger.info("Mock database connection initialized")
        
    def initialize_pool(self) -> None:
        """Initialize the mock connection pool"""
        self._connected = True
        logger.info("Mock database connection pool initialized successfully")
    
    def get_connection(self):
        """Get a mock connection"""
        if not self._connected:
            self.initialize_pool()
        return MockConnection()
    
    def return_connection(self, conn) -> None:
        """Return a mock connection to the pool"""
        logger.debug("Mock connection returned to pool")
    
    def close_pool(self) -> None:
        """Close the mock connection pool"""
        self._connected = False
        logger.info("Mock database connection pool closed")
    
    def health_check(self) -> bool:
        """Check mock database health"""
        return self._connected

class MockAsyncDatabaseConnection:
    """Mock async database connection manager"""
    
    def __init__(self):
        self._connected = False
        logger.info("Mock async database connection initialized")
    
    async def initialize_pool(self) -> None:
        """Initialize the mock async connection pool"""
        self._connected = True
        logger.info("Mock async database connection pool initialized successfully")
    
    async def get_connection(self):
        """Get a mock async connection"""
        if not self._connected:
            await self.initialize_pool()
        return MockAsyncConnection()
    
    async def return_connection(self, conn) -> None:
        """Return a mock async connection to the pool"""
        logger.debug("Mock async connection returned to pool")
    
    async def close_pool(self) -> None:
        """Close the mock async connection pool"""
        self._connected = False
        logger.info("Mock async database connection pool closed")
    
    async def health_check(self) -> bool:
        """Check mock async database health"""
        return self._connected
    
    @asynccontextmanager
    async def transaction(self):
        """Context manager for mock database transactions"""
        conn = await self.get_connection()
        try:
            yield conn
        finally:
            await self.return_connection(conn)

class MockConnection:
    """Mock database connection"""
    
    def cursor(self):
        return MockCursor()
    
    def commit(self):
        logger.debug("Mock transaction committed")
    
    def rollback(self):
        logger.debug("Mock transaction rolled back")

class MockAsyncConnection:
    """Mock async database connection"""
    
    async def fetchval(self, query, *args):
        logger.debug(f"Mock async query: {query}")
        return 1
    
    async def fetch(self, query, *args):
        logger.debug(f"Mock async query: {query}")
        return []

class MockCursor:
    """Mock database cursor"""
    
    def execute(self, query, params=None):
        logger.debug(f"Mock query executed: {query}")
        if params:
            logger.debug(f"With parameters: {params}")
    
    def fetchone(self):
        return None
    
    def fetchall(self):
        return []
    
    def close(self):
        logger.debug("Mock cursor closed")
    
    @property
    def rowcount(self):
        return 0

# Global mock connection instances
mock_db_connection = MockDatabaseConnection()
mock_async_db_connection = MockAsyncDatabaseConnection()

def get_mock_db_connection():
    """Get the global mock database connection instance"""
    return mock_db_connection

def get_mock_async_db_connection():
    """Get the global mock async database connection instance"""
    return mock_async_db_connection
