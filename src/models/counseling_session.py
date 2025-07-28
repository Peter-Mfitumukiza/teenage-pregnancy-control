from datetime import datetime
from colorama import Fore, Style
from config.database import db_manager

class CounselingSession:
    """Model for counseling sessions."""
    
    def __init__(self, session_id=None, username=None, name=None, topic=None, 
                 preferred_date=None, status='scheduled', notes=None):
        self.session_id = session_id
        self.username = username
        self.name = name
        self.topic = topic
        self.preferred_date = preferred_date
        self.status = status
        self.notes = notes
        self.created_at = None
        self.updated_at = None
    
    @classmethod
    def create_session(cls, username, name, topic, preferred_date, notes=None):
        """Create a new counseling session."""
        insert_query = """
        INSERT INTO counseling_sessions (username, client_name, topic, preferred_date, status, notes)
        VALUES (%s, %s, %s, %s, 'scheduled', %s)
        """
        
        try:
            # If name is empty, use "Anonymous"
            display_name = name.strip() if name and name.strip() else "Anonymous"
            
            result = db_manager.execute_query(
                insert_query, 
                (username, display_name, topic, preferred_date, notes)
            )
            
            if result is not None:
                return True, "Session booked successfully!"
            return False, "Failed to book session"
        except Exception as e:
            return False, f"Error booking session: {str(e)}"
    
    @classmethod
    def get_user_sessions(cls, username):
        """Get all sessions for a specific user."""
        query = """
        SELECT session_id, username, client_name, topic, preferred_date, status, notes, created_at, updated_at
        FROM counseling_sessions 
        WHERE username = %s 
        ORDER BY preferred_date DESC, created_at DESC
        """
        
        try:
            result = db_manager.execute_query(query, (username,))
            sessions = []
            
            if result:
                for row in result:
                    session = cls(
                        session_id=row['session_id'],
                        username=row['username'],
                        name=row['client_name'],
                        topic=row['topic'],
                        preferred_date=row['preferred_date'],
                        status=row['status'],
                        notes=row['notes']
                    )
                    session.created_at = row['created_at']
                    session.updated_at = row['updated_at']
                    sessions.append(session)
            
            return sessions
        except Exception as e:
            print(f"Error retrieving sessions: {e}")
            return []
    
    @classmethod
    def get_all_sessions(cls):
        """Get all sessions (for admin/counselor view)."""
        query = """
        SELECT session_id, username, client_name, topic, preferred_date, status, notes, created_at, updated_at
        FROM counseling_sessions 
        ORDER BY preferred_date DESC, created_at DESC
        """
        
        try:
            result = db_manager.execute_query(query)
            sessions = []
            
            if result:
                for row in result:
                    session = cls(
                        session_id=row['session_id'],
                        username=row['username'],
                        name=row['client_name'],
                        topic=row['topic'],
                        preferred_date=row['preferred_date'],
                        status=row['status'],
                        notes=row['notes']
                    )
                    session.created_at = row['created_at']
                    session.updated_at = row['updated_at']
                    sessions.append(session)
            
            return sessions
        except Exception as e:
            print(f"Error retrieving all sessions: {e}")
            return []
    
    @classmethod
    def get_session_by_id(cls, session_id):
        """Get a specific session by ID."""
        query = """
        SELECT session_id, username, client_name, topic, preferred_date, status, notes, created_at, updated_at
        FROM counseling_sessions 
        WHERE session_id = %s
        """
        
        try:
            result = db_manager.execute_query(query, (session_id,))
            
            if result and len(result) > 0:
                row = result[0]
                session = cls(
                    session_id=row['session_id'],
                    username=row['username'],
                    name=row['client_name'],
                    topic=row['topic'],
                    preferred_date=row['preferred_date'],
                    status=row['status'],
                    notes=row['notes']
                )
                session.created_at = row['created_at']
                session.updated_at = row['updated_at']
                return session
            
            return None
        except Exception as e:
            print(f"Error retrieving session: {e}")
            return None
    
    def update_session(self, name=None, topic=None, preferred_date=None, notes=None):
        """Update session details."""
        update_query = """
        UPDATE counseling_sessions 
        SET client_name = %s, topic = %s, preferred_date = %s, notes = %s, updated_at = NOW()
        WHERE session_id = %s
        """
        
        try:
            # Use current values if new ones not provided
            new_name = name if name is not None else self.name
            new_topic = topic if topic is not None else self.topic
            new_date = preferred_date if preferred_date is not None else self.preferred_date
            new_notes = notes if notes is not None else self.notes
            
            result = db_manager.execute_query(
                update_query, 
                (new_name, new_topic, new_date, new_notes, self.session_id)
            )
            
            if result is not None:
                # Update local attributes
                self.name = new_name
                self.topic = new_topic
                self.preferred_date = new_date
                self.notes = new_notes
                return True, "Session updated successfully!"
            return False, "Failed to update session"
        except Exception as e:
            return False, f"Error updating session: {str(e)}"
    
    def delete_session(self):
        """Delete the session."""
        delete_query = "DELETE FROM counseling_sessions WHERE session_id = %s"
        
        try:
            result = db_manager.execute_query(delete_query, (self.session_id,))
            
            if result is not None and result > 0:
                return True, "Session deleted successfully!"
            return False, "Session not found or already deleted"
        except Exception as e:
            return False, f"Error deleting session: {str(e)}"
    
    def update_status(self, new_status):
        """Update session status."""
        status_query = """
        UPDATE counseling_sessions 
        SET status = %s, updated_at = NOW()
        WHERE session_id = %s
        """
        
        try:
            result = db_manager.execute_query(status_query, (new_status, self.session_id))
            
            if result is not None:
                self.status = new_status
                return True, f"Status updated to {new_status}"
            return False, "Failed to update status"
        except Exception as e:
            return False, f"Error updating status: {str(e)}"
