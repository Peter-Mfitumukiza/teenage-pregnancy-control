from src.utils.helpers import (
    clear_screen, print_header, print_separator, 
    print_menu_option, get_user_input, confirm_action,
    print_info_box, print_emergency_contacts
)
from src.utils.validators import validate_menu_choice
from colorama import Fore, Style
from ui.qna_ui import QnAUI
from Counseling_support import run_counseling_support

class MenuHandler:
    """Handles main menu navigation and user interactions."""
    
    def __init__(self, auth_service=None):
        self.auth_service = auth_service
        self.is_authenticated = auth_service is not None and auth_service.is_authenticated()
        self.is_guest = auth_service is None
    
    def show_main_menu(self):
        """Display main menu for authenticated users."""
        while True:
            clear_screen()
            
            if self.is_authenticated:
                user_stats = self.auth_service.get_user_stats()
                print_header(f"🌸 MAIN MENU - Welcome {user_stats['username']}")
            else:
                print_header("🌸 MAIN MENU")
            
            # Show user info
            if self.is_authenticated:
                self._show_user_dashboard()
            
            print(f"\n{Fore.CYAN}📚 WHAT WOULD YOU LIKE TO DO TODAY?{Style.RESET_ALL}")
            print_separator()
            
            print_menu_option(1, "Educational Resources", "📖")
            print_menu_option(2, "Support & Counseling", "🤝")
            print_menu_option(3, "Find Local Services", "📍")
            print_menu_option(4, "Anonymous Q&A", "💬")
            print_menu_option(5, "Take Knowledge Quiz", "🧠")
            print_menu_option(6, "My Profile & Progress", "👤")
            print_menu_option(7, "Emergency Resources", "🆘")
            print_menu_option(8, "Logout", "🚪")
            
            print_separator()
            
            choice_input = input(f"\n{Fore.YELLOW}Please select an option (1-8): {Style.RESET_ALL}").strip()
            choice, error = validate_menu_choice(choice_input, 8)
            
            if error:
                print(f"{Fore.RED}❌ {error}{Style.RESET_ALL}")
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                continue
            
            # Handle menu choices
            result = self._handle_menu_choice(choice)
            
            if result in ['logout', 'exit']:
                return result
            elif result == 'continue':
                continue
    
    def show_guest_menu(self):
        """Display limited menu for guest users."""
        while True:
            clear_screen()
            print_header("📋 GUEST MENU - Limited Access")
            
            print_info_box("🔒 GUEST LIMITATIONS", [
                "• Cannot save progress or take quizzes",
                "• Cannot ask questions in Q&A",
                "• Limited access to some features",
                "",
                "💡 Create an account for full access!"
            ], Fore.YELLOW)
            
            print(f"\n{Fore.CYAN}📚 AVAILABLE FOR GUESTS:{Style.RESET_ALL}")
            print_separator()
            
            print_menu_option(1, "View Educational Content", "📖")
            print_menu_option(2, "Browse Support Resources", "🤝")
            print_menu_option(3, "Find Local Services", "📍")
            print_menu_option(4, "View FAQ Section", "❓")
            print_menu_option(5, "Emergency Resources", "🆘")
            print_menu_option(6, "Create Account", "✨")
            print_menu_option(7, "Exit System", "🚪")
            
            print_separator()
            
            choice_input = input(f"\n{Fore.YELLOW}Please select an option (1-7): {Style.RESET_ALL}").strip()
            choice, error = validate_menu_choice(choice_input, 7)
            
            if error:
                print(f"{Fore.RED}❌ {error}{Style.RESET_ALL}")
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                continue
            
            # Handle guest menu choices
            result = self._handle_guest_choice(choice)
            
            if result in ['exit', 'account_created']:
                return result
            elif result == 'continue':
                continue
    
    def _show_user_dashboard(self):
        """Show user dashboard with progress info."""
        if not self.is_authenticated:
            return
        
        user_stats = self.auth_service.get_user_stats()
        progress = user_stats.get('progress', {})
        
        print(f"\n{Fore.GREEN}📊 YOUR DASHBOARD:{Style.RESET_ALL}")
        print(f"   Last login: {user_stats.get('last_login', 'Unknown')}")
        
        if progress:
            completed = progress.get('completed_modules', 0)
            total = progress.get('total_modules', 0)
            avg_score = progress.get('average_score', 0)
            
            if total > 0:
                completion_rate = (completed / total) * 100
                print(f"   Learning progress: {completed}/{total} modules ({completion_rate:.1f}%)")
                
                if avg_score > 0:
                    print(f"   Average quiz score: {avg_score:.1f}%")
            else:
                print(f"   {Fore.YELLOW}🎯 Ready to start your learning journey!{Style.RESET_ALL}")
    
    def _handle_menu_choice(self, choice):
        """Handle authenticated user menu choices."""
        if choice == 1:
            return self._show_educational_resources()
        elif choice == 2:
            return self._show_support_counseling()
        elif choice == 3:
            return self._show_local_services()
        elif choice == 4:
            return self._show_anonymous_qa()
        elif choice == 5:
            return self._show_knowledge_quiz()
        elif choice == 6:
            return self._show_user_profile()
        elif choice == 7:
            return self._show_emergency_resources()
        elif choice == 8:
            return self._handle_logout()
        
        return 'continue'
    
    def _handle_guest_choice(self, choice):
        """Handle guest user menu choices."""
        if choice == 1:
            return self._show_educational_resources(guest_mode=True)
        elif choice == 2:
            return self._show_support_counseling(guest_mode=True)
        elif choice == 3:
            return self._show_local_services(guest_mode=True)
        elif choice == 4:
            return self._show_faq_section()
        elif choice == 5:
            return self._show_emergency_resources()
        elif choice == 6:
            return self._create_account_from_guest()
        elif choice == 7:
            return 'exit'
        
        return 'continue'
    
    def _show_educational_resources(self, guest_mode=False):
        """Show educational resources section."""
        clear_screen()
        print_header("📖 EDUCATIONAL RESOURCES")
        
        if guest_mode:
            print_info_box("📋 GUEST ACCESS", [
                "Viewing educational content as guest",
                "Progress will not be saved",
                "Create an account to track your learning!"
            ], Fore.YELLOW)
        
        print(f"\n{Fore.CYAN}📚 SHOW AVAILABLE TOPICS:{Style.RESET_ALL}")
        print("1. 🧬 Reproductive Health Basics")
        print("2. ⚠️  Understanding Pregnancy Risks")
        print("3. 🛡️  Can fetch other topics from the database")
        # print("4. 🌸 Understanding Puberty")
        # print("5. 🏥 Sexual Health and STDs")
        # print("6. 💭 Emotional and Mental Health")
        # print("7. 🔙 Return to Main Menu")
        
        # TODO: Implement educational content display
        print(f"\n{Fore.YELLOW}🚧 Educational modules coming soon!{Style.RESET_ALL}")
        print("This feature will provide comprehensive, age-appropriate educational content.")
        
        input(f"\n{Fore.CYAN}Press Enter to return to main menu...{Style.RESET_ALL}")
        return 'continue'
    
    def _show_support_counseling(self, guest_mode=False):
        """Show support and counseling section."""
        clear_screen()
        print_header("🤝 SUPPORT & COUNSELING")
        
        print_info_box("💜 YOU ARE NOT ALONE", [
            "Support is available 24/7",
            "All services are confidential",
            "Professional help is just a call away"
        ], Fore.MAGENTA)
        
        print(f"\n{Fore.CYAN}🆘 IMMEDIATE SUPPORT:{Style.RESET_ALL}")
        print("• National Crisis Line: 988")
        print("• Teen Pregnancy Hotline: 1-800-672-2296")
        print("• Crisis Text Line: Text HOME to 741741")
        
        print(f"\n{Fore.GREEN}🏥 PROFESSIONAL SERVICES:{Style.RESET_ALL}")
        print("• Planned Parenthood: 1-800-230-PLAN")
        print("• Local Health Departments")
        print("• School Counselors")
        print("• Community Health Centers")
        
        run_counseling_support()
        # TODO: Implement support resources database
        print(f"\n{Fore.YELLOW}🚧 Detailed support directory coming soon!{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        return 'continue'
    
    def _show_local_services(self, guest_mode=False):
        """Show local services finder."""
        clear_screen()
        print_header("📍 FIND LOCAL SERVICES")
        
        print(f"\n{Fore.CYAN}Find nearby resources and support services{Style.RESET_ALL}")
        
        # TODO: Implement location-based service finder
        print(f"\n{Fore.YELLOW}🚧 Service locator coming soon!{Style.RESET_ALL}")
        print("This feature will help you find:")
        print("• Local clinics and health centers")
        print("• Counseling services")
        print("• Support groups")
        print("• NGOs and community organizations")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        return 'continue'
    def _show_anonymous_qa(self):
        """Show anonymous Q&A section - FULLY FUNCTIONAL"""
        try:
            if not self.is_authenticated:
                clear_screen()
                print_header("💬 ANONYMOUS Q&A")
                print(f"{Fore.RED}❌ Please log in to access Q&A system{Style.RESET_ALL}")
                print("Guest users can only view FAQ section.")
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                return 'continue'
            
            # Get the current user's username
            user_stats = self.auth_service.get_user_stats()
            current_username = user_stats['username']
            
            # Initialize and show the Q&A interface
            qna_ui = QnAUI(current_username)
            qna_ui.show_main_menu()
            
        except Exception as e:
            clear_screen()
            print_header("💬 ANONYMOUS Q&A - ERROR")
            print(f"{Fore.RED}❌ Error accessing Q&A system: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please try again or contact support if this persists.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        
        return 'continue'
    def _show_knowledge_quiz(self):
        """Show knowledge quiz section."""
        clear_screen()
        print_header("🧠 KNOWLEDGE QUIZ")
        
        if not self.is_authenticated:
            print(f"{Fore.RED}❌ Please log in to take quizzes{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            return 'continue'
        
        # TODO: Implement quiz system
        print(f"\n{Fore.YELLOW}🚧 Quiz system coming soon!{Style.RESET_ALL}")
        print("Features will include:")
        print("• Interactive quizzes on health topics")
        print("• Progress tracking")
        print("• Personalized feedback")
        print("• Achievement badges")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        return 'continue'
    
    def _show_user_profile(self):
        """Show user profile and settings."""
        if not self.is_authenticated:
            print(f"{Fore.RED}❌ Please log in to view profile{Style.RESET_ALL}")
            return 'continue'
        
        # Use the auth UI to show profile
        self.auth_service.auth_ui.show_user_profile() if hasattr(self.auth_service, 'auth_ui') else None
        return 'continue'
    
    def _show_emergency_resources(self):
        """Show emergency resources."""
        clear_screen()
        print_header("🆘 EMERGENCY RESOURCES")
        
        print_emergency_contacts()
        
        print(f"\n{Fore.RED}⚠️  IF YOU ARE IN IMMEDIATE DANGER:{Style.RESET_ALL}")
        print("• Call 911 immediately")
        print("• Go to the nearest emergency room")
        print("• Contact a trusted adult")
        
        print(f"\n{Fore.YELLOW}🏥 PREGNANCY-SPECIFIC RESOURCES:{Style.RESET_ALL}")
        print("• Planned Parenthood: 1-800-230-PLAN")
        print("• National Abortion Federation: 1-800-772-9100")
        print("• Option Line: 1-800-712-4357")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        return 'continue'
    
    def _show_faq_section(self):
        """Show FAQ section for guests."""
        clear_screen()
        print_header("❓ FREQUENTLY ASKED QUESTIONS")
        
        # TODO: Implement FAQ system
        print(f"\n{Fore.YELLOW}🚧 FAQ section coming soon!{Style.RESET_ALL}")
        print("Common topics will include:")
        print("• Basic reproductive health questions")
        print("• Pregnancy information and options")
        print("• Contraception methods")
        print("• Where to get help and support")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        return 'continue'
    
    def _create_account_from_guest(self):
        """Allow guest to create account."""
        from src.ui.auth_ui import AuthUI
        
        auth_ui = AuthUI()
        
        if auth_ui.handle_registration():
            self.auth_service = auth_ui.get_auth_service()
            self.is_authenticated = True
            self.is_guest = False
            return 'account_created'
        
        return 'continue'
    
    def _handle_logout(self):
        """Handle user logout."""
        if confirm_action("Are you sure you want to logout?"):
            success, message = self.auth_service.logout_user() if self.auth_service else (True, "Logged out")
            
            if success:
                print(f"\n{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}❌ {message}{Style.RESET_ALL}")
            
            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            return 'logout'
        
        return 'continue'
