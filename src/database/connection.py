"""
Database connection management for the Equipment Database System
"""
import asyncio
import logging
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

import psycopg2
import psycopg2.pool
from psycopg2.extras import RealDictCursor
import asyncpg
from asyncpg import Pool, Connection

from config.database import db_config

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Synchronous database connection manager"""
    
    def __init__(self):
        self._pool: Optional[psycopg2.pool.SimpleConnectionPool] = None
        self._connection_params = db_config.to_dict()
        
    def initialize_pool(self) -> None:
        """Initialize the connection pool"""
        try:
            self._pool = psycopg2.pool.SimpleConnectionPool(
                minconn=db_config.min_connections,
                maxconn=db_config.max_connections,
                host=self._connection_params['host'],
                port=self._connection_params['port'],
                database=self._connection_params['database'],
                user=self._connection_params['username'],
                password=self._connection_params['password'],
                cursor_factory=RealDictCursor
            )
            logger.info("Database connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database connection pool: {e}")
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        if not self._pool:
            self.initialize_pool()
        return self._pool.getconn()
    
    def return_connection(self, conn) -> None:
        """Return a connection to the pool"""
        if self._pool:
            self._pool.putconn(conn)
    
    def close_pool(self) -> None:
        """Close the connection pool"""
        if self._pool:
            self._pool.closeall()
            logger.info("Database connection pool closed")
    
    def health_check(self) -> bool:
        """Check database health"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            self.return_connection(conn)
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

class AsyncDatabaseConnection:
    """Asynchronous database connection manager"""
    
    def __init__(self):
        self._pool: Optional[Pool] = None
        self._connection_params = db_config.to_dict()
    
    async def initialize_pool(self) -> None:
        """Initialize the async connection pool"""
        try:
            self._pool = await asyncpg.create_pool(
                host=self._connection_params['host'],
                port=self._connection_params['port'],
                database=self._connection_params['database'],
                user=self._connection_params['username'],
                password=self._connection_params['password'],
                min_size=db_config.min_connections,
                max_size=db_config.max_connections,
                command_timeout=db_config.connection_timeout
            )
            logger.info("Async database connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize async database connection pool: {e}")
            raise
    
    async def get_connection(self) -> Connection:
        """Get a connection from the async pool"""
        if not self._pool:
            await self.initialize_pool()
        return await self._pool.acquire()
    
    async def return_connection(self, conn: Connection) -> None:
        """Return a connection to the async pool"""
        if self._pool:
            await self._pool.release(conn)
    
    async def close_pool(self) -> None:
        """Close the async connection pool"""
        if self._pool:
            await self._pool.close()
            logger.info("Async database connection pool closed")
    
    async def health_check(self) -> bool:
        """Check database health asynchronously"""
        try:
            conn = await self.get_connection()
            result = await conn.fetchval("SELECT 1")
            await self.return_connection(conn)
            return True
        except Exception as e:
            logger.error(f"Async database health check failed: {e}")
            return False
    
    @asynccontextmanager
    async def transaction(self):
        """Context manager for database transactions"""
        conn = await self.get_connection()
        try:
            async with conn.transaction():
                yield conn
        finally:
            await self.return_connection(conn)

# Global connection instances
db_connection = DatabaseConnection()
async_db_connection = AsyncDatabaseConnection()

def get_db_connection():
    """Get the global database connection instance"""
    return db_connection

def get_async_db_connection():
    """Get the global async database connection instance"""
    return async_db_connection
