# src/ui/qna_ui.py
import os
import textwrap
from datetime import datetime
from typing import List, Dict
from services.qna_service import QnAService
from utils.helpers import clear_screen, print_colored, get_user_input, format_date

class QnAUI:
    def __init__(self, username: str):
        self.username = username
        self.qna_service = QnAService()
        self.colors = {
            'header': '\033[95m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'end': '\033[0m',
            'bold': '\033[1m',
            'underline': '\033[4m'
        }
    
    def display_header(self):
        """Display Q&A system header"""
        clear_screen()
        print("=" * 70)
        print_colored("💬 ANONYMOUS Q&A", "cyan", bold=True)
        print("=" * 70)
        print_colored("🔒 ANONYMOUS & SAFE", "green")
        print()
        print_colored("Ask questions without revealing identity", "blue")
        print_colored("Get answers from community and experts", "blue")
        print_colored("All conversations are confidential", "blue")
        print()
    
    def show_main_menu(self):
        """Display main Q&A menu"""
        while True:
            self.display_header()
            
            # Get and display stats
            stats = self.qna_service.get_question_stats()
            if stats:
                print_colored("📊 System Statistics:", "yellow", bold=True)
                print(f"   • Total Questions: {stats.get('total_questions', 0)}")
                print(f"   • Answered Questions: {stats.get('answered_questions', 0)}")
                print(f"   • Pending Questions: {stats.get('pending_questions', 0)}")
                print(f"   • Active Users: {stats.get('active_users', 0)}")
                print()
            
            print_colored("🌟 Q&A system features:", "yellow")
            print("• Ask anonymous questions")
            print("• Browse frequently asked questions")
            print("• Get expert and peer responses")
            print("• Rate helpful answers")
            print()
            
            print_colored("Choose an option:", "cyan", bold=True)
            print("1. 🤔 Ask a Question")
            print("2. 📖 Browse Questions & Answers")
            print("3. 🔍 Search Questions")
            print("4. 📋 My Questions")
            print("5. 📊 Browse by Category")
            print("6. ℹ️  How Q&A Works")
            print("0. ⬅️  Back to Main Menu")
            print()
            
            choice = get_user_input("Enter your choice (0-6): ").strip()
            
            if choice == '1':
                self.ask_question()
            elif choice == '2':
                self.browse_questions()
            elif choice == '3':
                self.search_questions()
            elif choice == '4':
                self.view_my_questions()
            elif choice == '5':
                self.browse_by_category()
            elif choice == '6':
                self.show_how_it_works()
            elif choice == '0':
                break
            else:
                print_colored("❌ Invalid choice. Please try again.", "red")
                input("\nPress Enter to continue...")
    
    def ask_question(self):
        """Interface for asking a new question"""
        clear_screen()
        print_colored("🤔 Ask Your Question", "cyan", bold=True)
        print("=" * 50)
        print()
        
        print_colored("Guidelines for asking questions:", "yellow")
        print("• Be specific and clear")
        print("• Ask one question at a time")
        print("• Avoid sharing personal identifying information")
        print("• Use appropriate language")
        print("• Remember: all questions are anonymous")
        print()
        
        # Get categories for selection
        categories = self.qna_service.get_categories()
        if categories:
            print_colored("📂 Available Categories:", "blue", bold=True)
            for i, cat in enumerate(categories, 1):
                count_text = f"({cat['question_count']} questions)" if cat['question_count'] > 0 else "(new)"
                print(f"{i}. {cat['name'].title()} - {cat['description']} {count_text}")
            print()
            
            while True:
                try:
                    cat_choice = int(get_user_input("Select category (number): "))
                    if 1 <= cat_choice <= len(categories):
                        selected_category = categories[cat_choice - 1]['name']
                        break
                    else:
                        print_colored("❌ Invalid category. Please try again.", "red")
                except ValueError:
                    print_colored("❌ Please enter a valid number.", "red")
        else:
            selected_category = 'general'
        
        print()
        print_colored(f"📝 Category: {selected_category.title()}", "green")
        print_colored("Type your question (10-1000 characters):", "blue")
        print("─" * 50)
        
        question_text = ""
        while len(question_text.strip()) < 10:
            question_text = get_user_input("Your question: ").strip()
            if len(question_text) < 10:
                print_colored("❌ Question too short. Please provide more details (minimum 10 characters).", "red")
            elif len(question_text) > 1000:
                print_colored("❌ Question too long. Please keep it under 1000 characters.", "red")
                question_text = ""
        
        print()
        print_colored("Question Preview:", "yellow", bold=True)
        print("─" * 50)
        wrapped_text = textwrap.fill(question_text, width=60)
        print(wrapped_text)
        print("─" * 50)
        print(f"Category: {selected_category.title()}")
        print(f"Characters: {len(question_text)}")
        print()
        
        confirm = get_user_input("Submit this question? (y/n): ").lower().strip()
        
        if confirm == 'y':
            if self.qna_service.submit_question(self.username, question_text, selected_category):
                print_colored("✅ Question submitted successfully!", "green", bold=True)
                print_colored("Your question will be reviewed and answered by our community and experts.", "blue")
                print_colored("Check 'My Questions' section for updates.", "blue")
            else:
                print_colored("❌ Failed to submit question. Please try again.", "red")
        else:
            print_colored("❌ Question cancelled.", "yellow")
        
        input("\nPress Enter to continue...")
    
    def browse_questions(self):
        """Browse answered questions"""
        while True:
            clear_screen()
            print_colored("📖 Browse Questions & Answers", "cyan", bold=True, center=True)
            print("=" * 60)
            print()
            
            questions = self.qna_service.browse_questions(limit=15)
            
            if not questions:
                print_colored("📝 No answered questions available yet.", "yellow", center=True)
                print_colored("Be the first to ask a question!", "blue", center=True)
                input("\nPress Enter to continue...")
                return
            
            print_colored(f"📋 Showing {len(questions)} most popular questions:", "blue", bold=True)
            print()
            
            for i, q in enumerate(questions, 1):
                answer_count = q['answer_count'] or 0
                category = q['category'].title()
                date_str = format_date(q['created_at'])
                
                print(f"{i:2d}. [{category}] ", end="")
                
                # Truncate long questions
                question_preview = q['question_text'][:80] + "..." if len(q['question_text']) > 80 else q['question_text']
                print_colored(question_preview, "white", bold=True)
                
                print(f"    💬 {answer_count} answer{'s' if answer_count != 1 else ''} • 📅 {date_str}")
                print()
            
            print_colored("Options:", "cyan", bold=True)
            print("• Enter question number to view full Q&A")
            print("• Press 'r' to refresh")
            print("• Press '0' to go back")
            print()
            
            choice = get_user_input("Your choice: ").strip().lower()
            
            if choice == '0':
                break
            elif choice == 'r':
                continue
            else:
                try:
                    q_num = int(choice)
                    if 1 <= q_num <= len(questions):
                        self.view_question_detail(questions[q_num - 1]['id'])
                    else:
                        print_colored("❌ Invalid question number.", "red")
                        input("Press Enter to continue...")
                except ValueError:
                    print_colored("❌ Please enter a valid number or 'r' to refresh.", "red")
                    input("Press Enter to continue...")
    
    def view_question_detail(self, question_id: int):
        """View detailed question with all answers"""
        question_data = self.qna_service.get_question_with_answers(question_id)
        
        if not question_data:
            print_colored("❌ Question not found or not available.", "red")
            input("Press Enter to continue...")
            return
        
        while True:
            clear_screen()
            print_colored("📖 Question & Answers", "cyan", bold=True, center=True)
            print("=" * 70)
            print()
            
            # Display question
            print_colored("❓ QUESTION:", "blue", bold=True)
            print_colored(f"Category: {question_data['category'].title()}", "yellow")
            print_colored(f"Asked: {format_date(question_data['created_at'])}", "yellow")
            print("─" * 50)
            wrapped_question = textwrap.fill(question_data['question_text'], width=65)
            print_colored(wrapped_question, "white", bold=True)
            print("─" * 50)
            print()
            
            # Display answers
            answers = question_data.get('answers', [])
            if answers:
                print_colored(f"💬 ANSWERS ({len(answers)}):", "green", bold=True)
                print()
                
                for i, answer in enumerate(answers, 1):
                    expert_badge = "👨‍⚕️ EXPERT" if answer['is_verified'] else "👥 COMMUNITY"
                    helpful_count = answer['helpful_count'] or 0
                    date_str = format_date(answer['created_at'])
                    
                    print_colored(f"Answer #{i} • {expert_badge} • 👍 {helpful_count} helpful • {date_str}", "cyan")
                    print("─" * 60)
                    
                    wrapped_answer = textwrap.fill(answer['answer_text'], width=65)
                    print(wrapped_answer)
                    print("─" * 60)
                    print()
            else:
                print_colored("📝 No answers available yet.", "yellow")
                print()
            
            print_colored("Options:", "cyan", bold=True)
            if answers:
                print("• Enter answer number (1-{}) to mark as helpful".format(len(answers)))
            print("• Press 'h' to mark this entire Q&A as helpful")
            print("• Press 'r' to report inappropriate content")
            print("• Press 'b' to go back to browse")
            print()
            
            choice = get_user_input("Your choice: ").strip().lower()
            
            # Check if user entered a number for individual answer voting
            if choice.isdigit() and answers:
                answer_num = int(choice)
                if 1 <= answer_num <= len(answers):
                    selected_answer = answers[answer_num - 1]
                    if self.mark_individual_answer_helpful(selected_answer['id'], self.username):
                        print_colored(f"✅ Thank you! Answer #{answer_num} has been marked as helpful.", "green")
                    else:
                        print_colored("ℹ️  Unable to vote on this answer.", "yellow")
                    input("Press Enter to continue...")
                    # Refresh to show updated count
                    question_data = self.qna_service.get_question_with_answers(question_id)
                    continue
                else:
                    print_colored("❌ Invalid answer number.", "red")
                    input("Press Enter to continue...")
                    continue
            elif choice == 'h':
                if self.qna_service.mark_answer_helpful(question_id, self.username):
                    print_colored("✅ Thank you for your feedback! This Q&A has been marked as helpful.", "green")
                else:
                    print_colored("ℹ️  You've already rated this Q&A, or there was an error.", "yellow")
                input("Press Enter to continue...")
                # Refresh the question data to show updated helpful count
                question_data = self.qna_service.get_question_with_answers(question_id)
                continue  # Redisplay with updated counts
            elif choice == 'r':
                print_colored("📝 Thank you for reporting. This content will be reviewed by moderators.", "yellow")
                input("Press Enter to continue...")
            elif choice == 'b':
                break
            else:
                break
    
    def mark_individual_answer_helpful(self, answer_id: int, username: str) -> bool:
        """Mark a specific answer as helpful"""
        try:
            # Update the specific answer's helpful count
            update_query = "UPDATE anonymous_answers SET helpful_votes = helpful_votes + 1 WHERE answer_id = %s"
            result = self.qna_service.db_manager.execute_query(update_query, (answer_id,))
            return result is not None
        except Exception as e:
            print(f"Error marking individual answer helpful: {e}")
            return False
    
    def search_questions(self):
        """Search for questions"""
        clear_screen()
        print_colored("🔍 Search Questions", "cyan", bold=True)
        print("=" * 50)
        print()
        
        search_term = get_user_input("Enter search term: ").strip()
        
        if len(search_term) < 3:
            print_colored("❌ Please enter at least 3 characters to search.", "red")
            input("Press Enter to continue...")
            return
        
        print_colored(f"🔍 Searching for: '{search_term}'", "blue")
        results = self.qna_service.search_questions(search_term)
        
        if not results:
            print_colored("📝 No questions found matching your search.", "yellow")
            print_colored("Try different keywords or browse all questions.", "blue")
            input("\nPress Enter to continue...")
            return
        
        print_colored(f"📋 Found {len(results)} matching questions:", "green", bold=True)
        print()
        
        for i, q in enumerate(results, 1):
            answer_count = q['answer_count'] or 0
            category = q['category'].title()
            date_str = format_date(q['created_at'])
            
            print(f"{i:2d}. [{category}] ", end="")
            question_preview = q['question_text'][:70] + "..." if len(q['question_text']) > 70 else q['question_text']
            print_colored(question_preview, "white", bold=True)
            print(f"    💬 {answer_count} answers • 📅 {date_str}")
            print()
        
        print_colored("Enter question number to view, or press Enter to go back:", "cyan")
        choice = get_user_input("Your choice: ").strip()
        
        if choice.isdigit():
            q_num = int(choice)
            if 1 <= q_num <= len(results):
                self.view_question_detail(results[q_num - 1]['id'])
    
    def view_my_questions(self):
        """View user's submitted questions"""
        clear_screen()
        print_colored("📋 My Questions", "cyan", bold=True)
        print("=" * 50)
        print()
        
        questions = self.qna_service.get_user_questions(self.username)
        
        if not questions:
            print_colored("📝 You haven't asked any questions yet.", "yellow")
            print_colored("Click 'Ask a Question' to get started!", "blue")
            input("\nPress Enter to continue...")
            return
        
        print_colored(f"📋 Your {len(questions)} questions:", "blue", bold=True)
        print()
        
        for i, q in enumerate(questions, 1):
            status_color = "green" if q['status'] == 'answered' else "yellow"
            status_symbol = "✅" if q['status'] == 'answered' else "⏳"
            answer_count = q['answer_count'] or 0
            date_str = format_date(q['created_at'])
            
            print(f"{i:2d}. {status_symbol} ", end="")
            print_colored(q['status'].title(), status_color, bold=True, end=" ")
            print(f"[{q['category'].title()}]")
            
            question_preview = q['question_text'][:60] + "..." if len(q['question_text']) > 60 else q['question_text']
            print(f"    {question_preview}")
            print(f"    💬 {answer_count} answers • 📅 {date_str}")
            print()
        
        if any(q['status'] == 'answered' for q in questions):
            print_colored("Enter question number to view answers, or press Enter to go back:", "cyan")
            choice = get_user_input("Your choice: ").strip()
            
            if choice.isdigit():
                q_num = int(choice)
                if 1 <= q_num <= len(questions) and questions[q_num - 1]['status'] == 'answered':
                    self.view_question_detail(questions[q_num - 1]['id'])
                elif 1 <= q_num <= len(questions):
                    print_colored("⏳ This question hasn't been answered yet.", "yellow")
                    input("Press Enter to continue...")
        else:
            input("Press Enter to continue...")
