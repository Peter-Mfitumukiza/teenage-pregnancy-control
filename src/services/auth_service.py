from src.models.user import User
from src.utils.validators import validate_age_input, validate_username_input
import json
import os

class AuthService:
    """Handles simple username-based authentication."""
    
    def __init__(self):
        self.current_user = None
        self.session_file = "current_session.json"
    
    def register_user(self, username, age_input):
        """Register a new user with username and age."""
        # Validate age
        age, age_error = validate_age_input(age_input)
        if age_error:
            return False, age_error
        
        # Validate username
        username_clean, username_error = validate_username_input(username)
        if username_error:
            return False, username_error
        
        # Create new user
        user, message = User.create_user(username_clean, age)
        
        if user:
            self.current_user = user
            self._save_session()
            return True, f"Welcome {username_clean}! {message}"
        else:
            return False, message
    
    def login_user(self, username):
        """Login an existing user with their username."""
        if not username or len(username.strip()) < 3:
            return False, "Please provide a valid username"
        
        username = username.strip()
        
        # Find user
        user = User.get_user(username)
        
        if user:
            user.update_last_login()
            self.current_user = user
            self._save_session()
            return True, f"Welcome back {username}! Last login: {user.last_login.strftime('%Y-%m-%d %H:%M')}"
        else:
            return False, "Username not found. Please check your username or create a new account."
    
    def logout_user(self):
        """Logout the current user."""
        if self.current_user:
            username = self.current_user.username
            self.current_user = None
            self._clear_session()
            return True, f"Goodbye {username}! Your session has ended safely."
        else:
            return False, "No user is currently logged in."
    
    def is_authenticated(self):
        """Check if a user is currently authenticated."""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get the currently authenticated user."""
        return self.current_user
    
    def restore_session(self):
        """Restore user session from saved file."""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                
                username = session_data.get('username')
                if username:
                    user = User.get_user(username)
                    if user:
                        self.current_user = user
                        return True, f"Welcome back {username}!"
            
            return False, "No saved session found"
            
        except Exception as e:
            return False, f"Error restoring session: {str(e)}"
    
    def _save_session(self):
        """Save current session to file."""
        try:
            if self.current_user:
                session_data = {
                    'username': self.current_user.username,
                    'age': self.current_user.age
                }
                
                with open(self.session_file, 'w') as f:
                    json.dump(session_data, f)
                    
        except Exception as e:
            print(f"Warning: Could not save session: {str(e)}")
    
    def _clear_session(self):
        """Clear saved session file."""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
        except Exception as e:
            print(f"Warning: Could not clear session file: {str(e)}")
    
    def delete_account(self):
        """Delete/deactivate the current user account."""
        if not self.current_user:
            return False, "No user is currently logged in"
        
        username = self.current_user.username
        success = self.current_user.deactivate()
        
        if success:
            self.logout_user()
            return True, f"Account '{username}' has been deactivated successfully"
        else:
            return False, "Failed to deactivate account"
    
    def get_user_stats(self):
        """Get statistics for the current user."""
        if not self.current_user:
            return None
        
        progress = self.current_user.get_progress_summary()
        
        return {
            'username': self.current_user.username,
            'age': self.current_user.age,
            'member_since': self.current_user.created_at.strftime("%B %Y") if self.current_user.created_at else "Unknown",
            'last_login': self.current_user.last_login.strftime("%Y-%m-%d %H:%M") if self.current_user.last_login else "Never",
            'progress': progress
        }
    
    def suggest_usernames(self, base_name):
        """Suggest available usernames if the desired one is taken."""
        suggestions = []
        
        # Try variations
        for i in range(1, 6):
            suggestion = f"{base_name}{i}"
            if not User.username_exists(suggestion):
                suggestions.append(suggestion)
        
        # Try with underscores
        for suffix in ['_teen', '_user', '_2024']:
            suggestion = f"{base_name}{suffix}"
            if not User.username_exists(suggestion) and len(suggestions) < 5:
                suggestions.append(suggestion)
        
        return suggestions[:3]  # Return top 3 suggestions