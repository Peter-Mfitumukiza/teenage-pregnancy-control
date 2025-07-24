from datetime import datetime
from config.database import db_manager


class User:
    """Represents a user with simple username authentication."""
    
    def __init__(self, username=None, age=None):
        self.username = username
        self.age = age
        self.created_at = None
        self.last_login = None
        self.is_active = True
    
    @classmethod
    def create_user(cls, username, age):
        """Create a new user with username and age."""
        # Validate inputs
        if not cls.validate_age(age):
            return None, "Age must be between 13 and 19"
        
        if not cls.validate_username(username):
            return None, "Username must be 3-20 characters, letters and numbers only"
        
        # Check if username already exists
        if cls.username_exists(username):
            return None, "Username already taken. Please choose a different one."
        
        user = cls(username=username, age=age)
        
        query = """
        INSERT INTO users (username, age, created_at, last_login, is_active)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        try:
            current_time = datetime.now()
            result = db_manager.execute_query(
                query, 
                (user.username, user.age, current_time, current_time, user.is_active)
            )
            
            if result is not None:
                user.created_at = current_time
                user.last_login = current_time
                return user, "Account created successfully!"
            else:
                return None, "Failed to create account"
                
        except Exception as e:
            return None, f"Error creating account: {str(e)}"
    
    @classmethod
    def get_user(cls, username):
        """Get a user by username."""
        query = "SELECT * FROM users WHERE username = %s AND is_active = TRUE"
        
        try:
            result = db_manager.execute_query(query, (username,))
            
            if result and len(result) > 0:
                user_data = result[0]
                user = cls(user_data['username'], user_data['age'])
                user.created_at = user_data['created_at']
                user.last_login = user_data['last_login']
                user.is_active = user_data['is_active']
                return user
            else:
                return None
                
        except Exception as e:
            print(f"Error retrieving user: {str(e)}")
            return None
    
    @classmethod
    def username_exists(cls, username):
        """Check if username already exists."""
        query = "SELECT COUNT(*) as count FROM users WHERE username = %s"
        
        try:
            result = db_manager.execute_query(query, (username,))
            return result[0]['count'] > 0 if result else False
        except Exception as e:
            print(f"Error checking username: {str(e)}")
            return True  # Assume exists on error to be safe
    
    def update_last_login(self):
        """Update the user's last login timestamp."""
        query = "UPDATE users SET last_login = %s WHERE username = %s"
        
        try:
            current_time = datetime.now()
            result = db_manager.execute_query(query, (current_time, self.username))
            
            if result is not None:
                self.last_login = current_time
                return True
            return False
            
        except Exception as e:
            print(f"Error updating last login: {str(e)}")
            return False
    
    def deactivate(self):
        """Deactivate the user account."""
        query = "UPDATE users SET is_active = FALSE WHERE username = %s"
        
        try:
            result = db_manager.execute_query(query, (self.username,))
            
            if result is not None:
                self.is_active = False
                return True
            return False
            
        except Exception as e:
            print(f"Error deactivating user: {str(e)}")
            return False
    
    def get_progress_summary(self):
        """Get user's learning progress summary."""
        query = """
        SELECT 
            COUNT(*) as total_modules,
            SUM(completed) as completed_modules,
            AVG(score) as average_score
        FROM user_progress 
        WHERE username = %s
        """
        
        try:
            result = db_manager.execute_query(query, (self.username,))
            
            if result and len(result) > 0:
                return result[0]
            else:
                return {
                    'total_modules': 0,
                    'completed_modules': 0,
                    'average_score': 0
                }
                
        except Exception as e:
            print(f"Error getting progress summary: {str(e)}")
            return None
    
    @staticmethod
    def validate_age(age):
        """Validate if the age is within the allowed range."""
        try:
            age = int(age)
            return 13 <= age <= 19
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_username(username):
        """Validate username format."""
        if not username:
            return False
        
        # Remove whitespace
        username = username.strip()
        
        # Check length (3-20 characters)
        if len(username) < 3 or len(username) > 20:
            return False
        
        # Check characters (letters, numbers, underscore only)
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False
        
        # Must start with letter
        if not username[0].isalpha():
            return False
        
        return True
    
    @staticmethod
    def get_user_count():
        """Get total number of active users."""
        query = "SELECT COUNT(*) as count FROM users WHERE is_active = TRUE"
        
        try:
            result = db_manager.execute_query(query)
            return result[0]['count'] if result else 0
        except Exception as e:
            print(f"Error getting user count: {str(e)}")
            return 0
    
    def __str__(self):
        return f"User(Username: {self.username}, Age: {self.age}, Active: {self.is_active})"