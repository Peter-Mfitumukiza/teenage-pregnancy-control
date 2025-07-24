# Replace your entire src/services/qna_service.py with this updated version

import mysql.connector
from typing import List, Dict, Optional
from datetime import datetime
from config.database import db_manager
from utils.validators import validate_input
from utils.security import sanitize_text

class QnAService:
    def __init__(self):
        self.db_manager = db_manager
        # Ensure database connection
        if not self.db_manager.connection or not self.db_manager.connection.is_connected():
            self.db_manager.connect()
    
    def get_connection(self):
        """Get database connection"""
        if not self.db_manager.connection or not self.db_manager.connection.is_connected():
            self.db_manager.connect()
        return self.db_manager.connection
    
    def submit_question(self, username: str, question_text: str, category: str = 'general') -> bool:
        """Submit a new anonymous question"""
        try:
            # Validate and sanitize input
            if not validate_input(question_text, min_length=10, max_length=1000):
                return False
            
            question_text = sanitize_text(question_text)
            
            # Validate category
            valid_categories = ['general', 'health', 'emotional_support', 'resources', 'other']
            if category not in valid_categories:
                category = 'general'
            
            query = """
                INSERT INTO anonymous_questions (username, question_text, category, is_answered)
                VALUES (%s, %s, %s, %s)
            """
            
            result = self.db_manager.execute_query(query, (username, question_text, category, False))
            
            if result is not None:
                # Update system stats
                self._update_system_stat('total_questions_asked', 1)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error submitting question: {e}")
            return False
    
    def get_user_questions(self, username: str) -> List[Dict]:
        """Get all questions submitted by a user"""
        try:
            query = """
                SELECT q.question_id, q.question_text, q.category, q.is_answered, q.created_at,
                       COUNT(a.answer_id) as answer_count
                FROM anonymous_questions q
                LEFT JOIN anonymous_answers a ON q.question_id = a.question_id
                WHERE q.username = %s
                GROUP BY q.question_id, q.question_text, q.category, q.is_answered, q.created_at
                ORDER BY q.created_at DESC
            """
            
            questions = self.db_manager.execute_query(query, (username,))
            
            if questions:
                # Convert is_answered boolean to status string for compatibility
                for q in questions:
                    q['status'] = 'answered' if q['is_answered'] else 'pending'
                    q['answer_count'] = q['answer_count'] or 0
                    q['id'] = q['question_id']  # Add this line for compatibility
                return questions
            
            return []
            
        except Exception as e:
            print(f"Error getting user questions: {e}")
            return []
    
    def browse_questions(self, category: str = None, limit: int = 20) -> List[Dict]:
        """Browse answered questions"""
        try:
            if category and category != 'all':
                query = """
                    SELECT q.question_id, q.question_text, q.category, q.created_at,
                           COUNT(a.answer_id) as answer_count,
                           MAX(a.created_at) as last_answered
                    FROM anonymous_questions q
                    LEFT JOIN anonymous_answers a ON q.question_id = a.question_id
                    WHERE q.is_answered = TRUE AND q.category = %s
                    GROUP BY q.question_id, q.question_text, q.category, q.created_at
                    ORDER BY answer_count DESC, q.created_at DESC
                    LIMIT %s
                """
                questions = self.db_manager.execute_query(query, (category, limit))
            else:
                query = """
                    SELECT q.question_id, q.question_text, q.category, q.created_at,
                           COUNT(a.answer_id) as answer_count,
                           MAX(a.created_at) as last_answered
                    FROM anonymous_questions q
                    LEFT JOIN anonymous_answers a ON q.question_id = a.question_id
                    WHERE q.is_answered = TRUE
                    GROUP BY q.question_id, q.question_text, q.category, q.created_at
                    ORDER BY answer_count DESC, q.created_at DESC
                    LIMIT %s
                """
                questions = self.db_manager.execute_query(query, (limit,))
            
            if questions:
                # Add id field for compatibility
                for q in questions:
                    q['id'] = q['question_id']
                    q['answer_count'] = q['answer_count'] or 0
                return questions
            
            return []
            
        except Exception as e:
            print(f"Error browsing questions: {e}")
            return []
    
    def get_question_with_answers(self, question_id: int) -> Optional[Dict]:
        """Get a specific question with all its answers"""
        try:
            print(f"DEBUG: Getting question {question_id} with its answers")
            
            # Get question details
            question_query = """
                SELECT question_id, question_text, category, is_answered, created_at
                FROM anonymous_questions
                WHERE question_id = %s
            """
            
            questions = self.db_manager.execute_query(question_query, (question_id,))
            
            if not questions:
                print(f"DEBUG: No question found with ID {question_id}")
                return None
            
            question = questions[0]
            print(f"DEBUG: Found question: {question['question_text'][:50]}...")
            
            # Only show answers if the question is answered
            if not question['is_answered']:
                print(f"DEBUG: Question {question_id} is not answered yet")
                question['id'] = question['question_id']
                question['status'] = 'pending'
                question['answers'] = []
                return question
            
            # Get answers for THIS SPECIFIC question only
            answers_query = """
                SELECT answer_id, answer_text, is_verified, helpful_votes, created_at
                FROM anonymous_answers
                WHERE question_id = %s
                ORDER BY is_verified DESC, helpful_votes DESC, created_at ASC
            """
            
            answers = self.db_manager.execute_query(answers_query, (question_id,))
            print(f"DEBUG: Found {len(answers) if answers else 0} answers for question {question_id}")
            
            # Convert field names for compatibility
            question['id'] = question['question_id']
            question['status'] = 'answered' if question['is_answered'] else 'pending'
            
            if answers:
                for i, answer in enumerate(answers):
                    answer['id'] = answer['answer_id']
                    answer['answered_by'] = 'expert' if answer['is_verified'] else 'community'
                    answer['helpful_count'] = answer['helpful_votes'] or 0
                    print(f"DEBUG: Answer {i+1}: {answer['answer_text'][:30]}... (by {answer['answered_by']})")
            else:
                answers = []
            
            question['answers'] = answers
            return question
            
        except Exception as e:
            print(f"Error getting question with answers: {e}")
            return None
    
    def get_categories(self) -> List[Dict]:
        """Get all available question categories"""
        categories = [
            {
                'name': 'general',
                'description': 'General questions about reproductive health',
                'color_code': '#3498db'
            },
            {
                'name': 'health',
                'description': 'Questions about sexual and reproductive health',
                'color_code': '#f39c12'
            },
            {
                'name': 'emotional_support',
                'description': 'Questions about emotional and psychological support',
                'color_code': '#9b59b6'
            },
            {
                'name': 'resources',
                'description': 'Questions about available support and resources',
                'color_code': '#1abc9c'
            },
            {
                'name': 'other',
                'description': 'Other questions not covered in specific categories',
                'color_code': '#95a5a6'
            }
        ]
        
        # Add question counts
        try:
            for category in categories:
                query = "SELECT COUNT(*) as count FROM anonymous_questions WHERE category = %s AND is_answered = TRUE"
                result = self.db_manager.execute_query(query, (category['name'],))
                category['question_count'] = result[0]['count'] if result else 0
            
        except Exception as e:
            print(f"Error getting category counts: {e}")
            # Set default counts if query fails
            for category in categories:
                category['question_count'] = 0
        
        return categories
    
    def search_questions(self, search_term: str, category: str = None) -> List[Dict]:
        """Search for questions by keyword"""
        try:
            search_term = f"%{search_term}%"
            
            if category and category != 'all':
                query = """
                    SELECT q.question_id, q.question_text, q.category, q.created_at,
                           COUNT(a.answer_id) as answer_count
                    FROM anonymous_questions q
                    LEFT JOIN anonymous_answers a ON q.question_id = a.question_id
                    WHERE q.is_answered = TRUE 
                    AND (q.question_text LIKE %s OR a.answer_text LIKE %s)
                    AND q.category = %s
                    GROUP BY q.question_id, q.question_text, q.category, q.created_at
                    ORDER BY answer_count DESC, q.created_at DESC
                """
                results = self.db_manager.execute_query(query, (search_term, search_term, category))
            else:
                query = """
                    SELECT q.question_id, q.question_text, q.category, q.created_at,
                           COUNT(a.answer_id) as answer_count
                    FROM anonymous_questions q
                    LEFT JOIN anonymous_answers a ON q.question_id = a.question_id
                    WHERE q.is_answered = TRUE 
                    AND (q.question_text LIKE %s OR a.answer_text LIKE %s)
                    GROUP BY q.question_id, q.question_text, q.category, q.created_at
                    ORDER BY answer_count DESC, q.created_at DESC
                """
                results = self.db_manager.execute_query(query, (search_term, search_term))
            
            if results:
                # Add id field for compatibility
                for r in results:
                    r['id'] = r['question_id']
                    r['answer_count'] = r['answer_count'] or 0
                return results
            
            return []
            
        except Exception as e:
            print(f"Error searching questions: {e}")
            return []
    
    def mark_answer_helpful(self, question_id: int, username: str) -> bool:
        """Mark an answer as helpful (increase helpful votes)"""
        try:
            # Check if user already voted for this question (simple prevention of multiple votes)
            check_query = """
                SELECT COUNT(*) as voted 
                FROM anonymous_answers a
                JOIN anonymous_questions q ON a.question_id = q.question_id
                WHERE a.question_id = %s AND q.username = %s
            """
            
            result = self.db_manager.execute_query(check_query, (question_id, username))
            
            # Don't let users vote on their own questions' answers
            if result and result[0]['voted'] > 0:
                # This is their own question, don't allow voting
                own_question_check = "SELECT username FROM anonymous_questions WHERE question_id = %s"
                question_owner = self.db_manager.execute_query(own_question_check, (question_id,))
                if question_owner and question_owner[0]['username'] == username:
                    return False  # Can't vote on own question
            
            # For now, allow multiple helpful votes (in production, you'd track individual votes)
            # Update all answers for this question (increase helpful count)
            update_query = """
                UPDATE anonymous_answers 
                SET helpful_votes = helpful_votes + 1 
                WHERE question_id = %s
            """
            result = self.db_manager.execute_query(update_query, (question_id,))
            
            return result is not None
            
        except Exception as e:
            print(f"Error marking answer helpful: {e}")
            return False
    
    def get_question_stats(self) -> Dict:
        """Get statistics about the Q&A system"""
        try:
            stats_query = """
                SELECT 
                    (SELECT COUNT(*) FROM anonymous_questions) as total_questions,
                    (SELECT COUNT(*) FROM anonymous_questions WHERE is_answered = TRUE) as answered_questions,
                    (SELECT COUNT(*) FROM anonymous_questions WHERE is_answered = FALSE) as pending_questions,
                    (SELECT COUNT(*) FROM anonymous_answers) as total_answers,
                    (SELECT COUNT(DISTINCT username) FROM anonymous_questions) as active_users
            """
            
            result = self.db_manager.execute_query(stats_query)
            
            return result[0] if result else {}
            
        except Exception as e:
            print(f"Error getting question stats: {e}")
            return {}
    
    def _update_system_stat(self, stat_name: str, increment: int = 1):
        """Update system statistics"""
        try:
            query = """
                INSERT INTO system_stats (stat_name, stat_value) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE 
                stat_value = stat_value + %s
            """
            
            self.db_manager.execute_query(query, (stat_name, increment, increment))
            
        except Exception as e:
            print(f"Error updating system stats: {e}")
    
    def close_connection(self):
        """Close database connection"""
        self.db_manager.disconnect()
