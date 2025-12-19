"""
Database Connector Service
==========================
Handles database connections and operations.
"""

import pandas as pd
from sqlalchemy import create_engine, inspect
from typing import List
from app.models.schemas import DatabaseConnectionSchema
from app.utils.logger import app_logger
from fastapi import HTTPException


class DatabaseConnector:
    """
    Service for database connection and operations.
    """
    
    @staticmethod
    def build_connection_string(config: DatabaseConnectionSchema) -> str:
        """
        Build database connection string from configuration
        
        Args:
            config: Database connection configuration
        
        Returns:
            Connection string
        """
        if config.db_type == 'postgresql':
            return (
                f"postgresql://{config.username}:{config.password}@"
                f"{config.host}:{config.port}/{config.database}"
            )
        elif config.db_type == 'mysql':
            return (
                f"mysql+pymysql://{config.username}:{config.password}@"
                f"{config.host}:{config.port}/{config.database}"
            )
        else:
            raise ValueError(f"Unsupported database type: {config.db_type}")
    
    @staticmethod
    def test_connection(connection_string: str) -> bool:
        """
        Test database connection
        
        Args:
            connection_string: Database connection string
        
        Returns:
            True if connection successful
        
        Raises:
            HTTPException: If connection fails
        """
        try:
            engine = create_engine(connection_string)
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            return True
        except Exception as e:
            app_logger.error(f"Database connection failed: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Database connection failed: {str(e)}"
            )
    
    @staticmethod
    def get_tables(connection_string: str) -> List[str]:
        """
        Get list of tables in database
        
        Args:
            connection_string: Database connection string
        
        Returns:
            List of table names
        """
        try:
            engine = create_engine(connection_string)
            inspector = inspect(engine)
            return inspector.get_table_names()
        except Exception as e:
            app_logger.error(f"Error getting tables: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Error getting tables: {str(e)}"
            )
    
    @staticmethod
    def read_table(connection_string: str, table: str) -> pd.DataFrame:
        """
        Read table from database into DataFrame
        
        Args:
            connection_string: Database connection string
            table: Table name
        
        Returns:
            DataFrame with table data
        
        Raises:
            HTTPException: If reading fails
        """
        try:
            engine = create_engine(connection_string)
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(query, engine)
            app_logger.info(f"Read {len(df)} rows from table '{table}'")
            return df
        except Exception as e:
            app_logger.error(f"Error reading table '{table}': {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Error reading table: {str(e)}"
            )
    
    @staticmethod
    def write_table(
        df: pd.DataFrame,
        connection_string: str,
        table: str,
        if_exists: str = 'replace'
    ) -> int:
        """
        Write DataFrame to database table
        
        Args:
            df: DataFrame to write
            connection_string: Database connection string
            table: Table name
            if_exists: What to do if table exists ('fail', 'replace', 'append')
        
        Returns:
            Number of rows written
        
        Raises:
            HTTPException: If writing fails
        """
        try:
            engine = create_engine(connection_string)
            rows_written = df.to_sql(
                table,
                engine,
                if_exists=if_exists,
                index=False
            )
            app_logger.info(f"Wrote {len(df)} rows to table '{table}' (mode: {if_exists})")
            return len(df)
        except Exception as e:
            app_logger.error(f"Error writing to table '{table}': {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Error writing to table: {str(e)}"
            )
