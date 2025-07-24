import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'teenage-pc-mfitumukizapeter255-fa99.d.aivencloud.com')
        self.database = os.getenv('DB_NAME', 'defaultdb')
        self.user = os.getenv('DB_USER', 'avnadmin')
        self.password = os.getenv('DB_PASSWORD', 'AVNS_LxwVa_57ZXqckNMOgt2')
        self.port = os.getenv('DB_PORT', 16835)
        self.connection = None
    
    def connect(self):
        """Establish database connection."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                autocommit=True
            )
            
            if self.connection.is_connected():
                print("✓ Successfully connected to MySQL database")
                return True
                
        except Error as e:
            print(f"✗ Error connecting to MySQL database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a query and return results."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                return cursor.rowcount
                
        except Error as e:
            print(f"✗ Error executing query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def execute_many(self, query, data_list):
        """Execute query with multiple data sets."""
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, data_list)
            return cursor.rowcount
        except Error as e:
            print(f"✗ Error executing batch query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()


# Global database instance
db_manager = DatabaseManager()