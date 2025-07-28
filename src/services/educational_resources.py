from datetime import datetime
from colorama import Fore, Style
from config.database import db_manager
from src.models.educational_module import EducationalModule
from src.models.user_progress import UserProgress


class EducationalResources:
    
    def __init__(self):
        # Ensure database connection is established
        if not db_manager.connection or not db_manager.connection.is_connected():
            db_manager.connect()
        
        # Create default modules if they don't exist
        EducationalModule.create_default_modules()
    
    def display_topics_menu(self):
        """Display available educational topics."""
        print(f"\n{Fore.CYAN}📚 AVAILABLE EDUCATIONAL TOPICS:{Style.RESET_ALL}")
        print("=" * 50)
        
        modules = EducationalModule.get_all_modules()
        
        if not modules:
            print(f"{Fore.YELLOW}No topics available yet.{Style.RESET_ALL}")
            return []
        
        current_category = ""
        for module in modules:
            if module.category != current_category:
                current_category = module.category
                category_display = module.category.replace('_', ' ').title()
                print(f"\n{Fore.GREEN}📖 {category_display.upper()}:{Style.RESET_ALL}")
            
            difficulty_color = {
                'beginner': Fore.GREEN,
                'intermediate': Fore.YELLOW,
                'advanced': Fore.RED
            }.get(module.difficulty_level, Fore.WHITE)
            
            print(f"   {module.module_id}. {module.title} {difficulty_color}[{module.difficulty_level}]{Style.RESET_ALL}")
        
        return modules
    
    def view_topic_content(self, module_id):
        """Display content for a specific topic."""
        module = EducationalModule.get_module_by_id(module_id)
        
        if not module:
            print(f"{Fore.RED}❌ Topic not found.{Style.RESET_ALL}")
            return False
        
        print(f"\n{Fore.CYAN}📖 {module.title.upper()}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Category: {module.category.replace('_', ' ').title()}{Style.RESET_ALL}")
        
        difficulty_color = {
            'beginner': Fore.GREEN,
            'intermediate': Fore.YELLOW,
            'advanced': Fore.RED
        }.get(module.difficulty_level, Fore.WHITE)
        print(f"{difficulty_color}Difficulty: {module.difficulty_level.title()}{Style.RESET_ALL}")
        
        print("=" * 60)
        print(f"\n{module.content}")
        print("\n" + "=" * 60)
        
        return True
    
    def mark_topic_completed(self, username, module_id):
        """Mark a topic as completed for a user."""
        if not username or username == "Anonymous":
            return False
        
        return UserProgress.mark_completed(username, module_id)
    
    def show_user_progress(self, username):
        """Display user's progress."""
        progress = UserProgress.get_user_progress(username)
        
        print(f"\n{Fore.GREEN}📊 YOUR LEARNING PROGRESS:{Style.RESET_ALL}")
        print(f"   Completed: {progress['completed']}/{progress['total']} modules")
        print(f"   Progress: {progress['percentage']:.1f}%")
        
        if progress['average_score'] > 0:
            print(f"   Average Score: {progress['average_score']:.1f}%")
        
        if progress['completed'] > 0:
            completed_modules = UserProgress.get_completed_modules(username, 3)
            if completed_modules:
                print(f"\n{Fore.CYAN}✅ Recently Completed:{Style.RESET_ALL}")
                for module in completed_modules:
                    date_str = module['completion_date'].strftime('%Y-%m-%d') if module['completion_date'] else 'Unknown'
                    score_str = f" (Score: {module['score']}%)" if module['score'] and module['score'] > 0 else ""
                    print(f"   • {module['title']} ({date_str}){score_str}")
    
    def get_topics_by_category(self, category):
        """Get all topics in a specific category."""
        return EducationalModule.get_modules_by_category(category)
    
    def get_all_categories(self):
        """Get all available categories."""
        return EducationalModule.get_all_categories()


def display_educational_menu():
    """Display the educational resources menu."""
    print(f"\n{Fore.CYAN}=== 📖 EDUCATIONAL RESOURCES ==={Style.RESET_ALL}")
    print("1. Browse All Topics")
    print("2. View Specific Topic")
    print("3. View My Progress")
    print("4. Search Topics by Category")
    print("5. Return to Main Menu")


def run_educational_resources(username=None, guest_mode=False):
    """Main function to run the educational resources system."""
    resources = EducationalResources()
    
    try:
        while True:
            display_educational_menu()
            
            if guest_mode:
                print(f"{Fore.YELLOW}📋 Guest Mode: Progress will not be saved{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.YELLOW}Choose an option (1-5): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                # Browse all topics
                modules = resources.display_topics_menu()
                if modules:
                    topic_choice = input(f"\n{Fore.YELLOW}Enter module number to view (or press Enter to continue): {Style.RESET_ALL}").strip()
                    if topic_choice.isdigit():
                        module_id = int(topic_choice)
                        # Check if module exists
                        valid_ids = [module.module_id for module in modules]
                        if module_id in valid_ids:
                            if resources.view_topic_content(module_id):
                                if not guest_mode and username:
                                    mark_complete = input(f"\n{Fore.GREEN}Mark this topic as completed? (y/n): {Style.RESET_ALL}").strip().lower()
                                    if mark_complete == 'y':
                                        if resources.mark_topic_completed(username, module_id):
                                            print(f"{Fore.GREEN}✅ Topic marked as completed!{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}❌ Invalid module number.{Style.RESET_ALL}")
                        
                        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '2':
                # View specific topic
                module_id = input(f"{Fore.YELLOW}Enter module ID: {Style.RESET_ALL}").strip()
                if module_id.isdigit():
                    if resources.view_topic_content(int(module_id)):
                        if not guest_mode and username:
                            mark_complete = input(f"\n{Fore.GREEN}Mark this topic as completed? (y/n): {Style.RESET_ALL}").strip().lower()
                            if mark_complete == 'y':
                                if resources.mark_topic_completed(username, int(module_id)):
                                    print(f"{Fore.GREEN}✅ Topic marked as completed!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ Invalid module ID.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Please enter a valid number.{Style.RESET_ALL}")
                
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '3':
                # View progress
                if guest_mode:
                    print(f"{Fore.YELLOW}📋 Progress tracking not available for guests.{Style.RESET_ALL}")
                    print("Create an account to track your learning progress!")
                elif username:
                    resources.show_user_progress(username)
                
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '4':
                # Search by category
                categories = resources.get_all_categories()
                if categories:
                    print(f"\n{Fore.CYAN}📚 Available Categories:{Style.RESET_ALL}")
                    for i, category in enumerate(categories, 1):
                        category_display = category.replace('_', ' ').title()
                        print(f"{i}. {category_display}")
                    
                    cat_choice = input(f"\n{Fore.YELLOW}Enter category number: {Style.RESET_ALL}").strip()
                    if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
                        selected_category = categories[int(cat_choice) - 1]
                        modules = resources.get_topics_by_category(selected_category)
                        
                        if modules:
                            category_display = selected_category.replace('_', ' ').title()
                            print(f"\n{Fore.GREEN}📖 Topics in {category_display}:{Style.RESET_ALL}")
                            for module in modules:
                                difficulty_color = {
                                    'beginner': Fore.GREEN,
                                    'intermediate': Fore.YELLOW,
                                    'advanced': Fore.RED
                                }.get(module.difficulty_level, Fore.WHITE)
                                print(f"   {module.module_id}. {module.title} {difficulty_color}[{module.difficulty_level}]{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}No topics found in this category.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ Invalid category selection.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}No categories available.{Style.RESET_ALL}")
                
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '5':
                print(f"{Fore.GREEN}Thanks for learning! Stay informed and stay safe! 🌸{Style.RESET_ALL}")
                break
            
            else:
                print(f"{Fore.RED}❌ Invalid choice. Please select 1-5.{Style.RESET_ALL}")
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
    except Exception as e:
        print(f"{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")
        input(f"{Fore.CYAN}Press Enter to return to main menu...{Style.RESET_ALL}")
