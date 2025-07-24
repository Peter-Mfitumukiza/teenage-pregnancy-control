# Create this as src/admin_tool.py - Simple tool for experts to answer questions

import sys
sys.path.append('.')

from config.database import db_manager
from datetime import datetime

class AdminTool:
    def __init__(self):
        self.db_manager = db_manager
        if not self.db_manager.connection or not self.db_manager.connection.is_connected():
            self.db_manager.connect()
    
    def show_pending_questions(self):
        """Show all pending questions that need answers"""
        query = """
            SELECT question_id, username, question_text, category, created_at
            FROM anonymous_questions 
            WHERE is_answered = FALSE 
            ORDER BY created_at ASC
        """
        
        questions = self.db_manager.execute_query(query)
        
        if not questions:
            print("No pending questions.")
            return
        
        print(f"\n{'='*80}")
        print("PENDING QUESTIONS NEEDING EXPERT ANSWERS")
        print(f"{'='*80}")
        
        for i, q in enumerate(questions, 1):
            print(f"\n{i}. Question ID: {q['question_id']}")
            print(f"   Category: {q['category'].title()}")
            print(f"   Asked: {q['created_at']}")
            print(f"   Question: {q['question_text']}")
            print("-" * 80)
        
        return questions
    
    def add_expert_answer(self, question_id, answer_text):
        """Add an expert answer to a question"""
        try:
            # Add the answer
            answer_query = """
                INSERT INTO anonymous_answers (question_id, answer_text, is_verified, helpful_votes)
                VALUES (%s, %s, %s, %s)
            """
            
            result = self.db_manager.execute_query(answer_query, (question_id, answer_text, True, 0))
            
            if result is not None:
                # Mark question as answered
                update_query = "UPDATE anonymous_questions SET is_answered = TRUE WHERE question_id = %s"
                self.db_manager.execute_query(update_query, (question_id,))
                
                print(f"✅ Expert answer added to question {question_id}")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error adding answer: {e}")
            return False
    
    def run_interactive_mode(self):
        """Run interactive mode for experts to answer questions"""
        print("Welcome to the Expert Q&A Admin Tool")
        print("=====================================")
        
        while True:
            print("\nOptions:")
            print("1. View pending questions")
            print("2. Answer a question")
            print("3. Exit")
            
            choice = input("\nEnter choice (1-3): ").strip()
            
            if choice == '1':
                self.show_pending_questions()
                
            elif choice == '2':
                questions = self.show_pending_questions()
                if questions:
                    try:
                        q_id = int(input("\nEnter question ID to answer: "))
                        
                        # Verify question exists and is pending
                        valid_ids = [q['question_id'] for q in questions]
                        if q_id not in valid_ids:
                            print("❌ Invalid question ID")
                            continue
                        
                        print("\nEnter your expert answer (press Enter twice when done):")
                        answer_lines = []
                        while True:
                            line = input()
                            if line == "" and answer_lines:
                                break
                            answer_lines.append(line)
                        
                        answer_text = "\n".join(answer_lines).strip()
                        
                        if len(answer_text) < 10:
                            print("❌ Answer too short. Please provide a detailed response.")
                            continue
                        
                        if self.add_expert_answer(q_id, answer_text):
                            print("✅ Answer added successfully!")
                        else:
                            print("❌ Failed to add answer")
                            
                    except ValueError:
                        print("❌ Please enter a valid question ID")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                        
            elif choice == '3':
                print("Goodbye!")
                break
                
            else:
                print("❌ Invalid choice")

if __name__ == "__main__":
    admin = AdminTool()
    admin.run_interactive_mode()
