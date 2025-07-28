from config.database import db_manager


class UserProgress:
    """Model for tracking user progress on educational modules."""
    
    def __init__(self, username=None, module_id=None, completed=False, score=0):
        self.username = username
        self.module_id = module_id
        self.completed = completed
        self.completion_date = None
        self.score = score
    
    @classmethod
    def mark_completed(cls, username, module_id, score=0):
        """Mark a module as completed for a user."""
        # Check if progress record exists
        check_query = """
        SELECT progress_id FROM user_progress 
        WHERE username = %s AND module_id = %s
        """
        
        try:
            result = db_manager.execute_query(check_query, (username, module_id))
            
            if result and len(result) > 0:
                # Update existing record
                update_query = """
                UPDATE user_progress 
                SET completed = TRUE, completion_date = NOW(), score = %s
                WHERE username = %s AND module_id = %s
                """
                db_manager.execute_query(update_query, (score, username, module_id))
            else:
                # Create new record
                insert_query = """
                INSERT INTO user_progress (username, module_id, completed, completion_date, score)
                VALUES (%s, %s, TRUE, NOW(), %s)
                """
                db_manager.execute_query(insert_query, (username, module_id, score))
            
            return True
        except Exception as e:
            print(f"Error marking module as completed: {e}")
            return False
    
    @classmethod
    def get_user_progress(cls, username):
        """Get user's learning progress summary."""
        progress_query = """
        SELECT 
            (SELECT COUNT(*) FROM educational_modules) as total_modules,
            COUNT(CASE WHEN completed = TRUE THEN 1 END) as completed_modules,
            AVG(CASE WHEN completed = TRUE AND score > 0 THEN score END) as average_score
        FROM user_progress 
        WHERE username = %s
        """
        
        try:
            result = db_manager.execute_query(progress_query, (username,))
            
            if result and len(result) > 0:
                data = result[0]
                total = data['total_modules'] or 0
                completed = data['completed_modules'] or 0
                avg_score = data['average_score'] or 0
                
                return {
                    "total": total,
                    "completed": completed,
                    "percentage": (completed / total * 100) if total > 0 else 0,
                    "average_score": float(avg_score) if avg_score else 0
                }
            
            return {"total": 0, "completed": 0, "percentage": 0, "average_score": 0}
        except Exception as e:
            print(f"Error getting user progress: {e}")
            return {"total": 0, "completed": 0, "percentage": 0, "average_score": 0}
    
    @classmethod
    def get_completed_modules(cls, username, limit=3):
        """Get recently completed modules for a user."""
        query = """
        SELECT em.title, up.completion_date, up.score
        FROM user_progress up
        JOIN educational_modules em ON up.module_id = em.module_id
        WHERE up.username = %s AND up.completed = TRUE
        ORDER BY up.completion_date DESC
        LIMIT %s
        """
        
        try:
            result = db_manager.execute_query(query, (username, limit))
            return result if result else []
        except Exception as e:
            print(f"Error getting completed modules: {e}")
            return []