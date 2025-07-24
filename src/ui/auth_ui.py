from src.services.auth_service import AuthService
from src.utils.helpers import clear_screen, print_header, print_separator
import colorama
from colorama import Fore, Style

# Initialize colorama for cross-platform colored output
colorama.init()


class AuthUI:
    """Handles simple authentication user interface."""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    def show_welcome_screen(self):
        """Display the welcome screen with privacy information."""
        clear_screen()
        print_header("🌸 TEENAGE PREGNANCY AWARENESS & SUPPORT SYSTEM 🌸")
        
        print(f"\n{Fore.CYAN}Welcome to a safe, confidential space for education and support{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}🔒 PRIVACY COMMITMENT:{Style.RESET_ALL}")
        print("   • Choose any username you like (no real names required)")
        print("   • We only collect your age for appropriate content")
        print("   • All interactions are confidential")
        print("   • You can leave at any time")
        
        print(f"\n{Fore.GREEN}🎯 WHAT YOU'LL FIND HERE:{Style.RESET_ALL}")
        print("   • Educational resources on reproductive health")
        print("   • Support and counseling information")
        print("   • Local services and resources")
        print("   • Anonymous Q&A community")
        print("   • Interactive knowledge quizzes")
        
        print_separator()
        print(f"{Fore.MAGENTA}This system is designed for teenagers aged 13-19{Style.RESET_ALL}")
        print_separator()
        
        # Check for existing session
        success, message = self.auth_service.restore_session()
        if success:
            print(f"\n{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
            choice = input(f"\n{Fore.YELLOW}Continue with saved session? (y/n): {Style.RESET_ALL}").strip().lower()
            if choice == 'y':
                return 'restored'
            else:
                self.auth_service.logout_user()
        
        return None
    
    def show_auth_menu(self):
        """Display authentication menu and handle user choice."""
        # Check for restored session first
        welcome_result = self.show_welcome_screen()
        if welcome_result == 'restored':
            return True
        
        while True:
            print(f"\n{Fore.CYAN}GETTING STARTED:{Style.RESET_ALL}")
            print("1. 👤 Create New Account")
            print("2. 🔑 Login with Username")
            print("3. 📋 Continue as Guest (Limited Access)")
            print("4. 🚪 Exit System")
            
            choice = input(f"\n{Fore.YELLOW}Please select an option (1-4): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                if self.handle_registration():
                    return True  # Successfully registered and logged in
            elif choice == '2':
                if self.handle_login():
                    return True  # Successfully logged in
            elif choice == '3':
                return self.handle_guest_access()
            elif choice == '4':
                return self.handle_exit()
            else:
                print(f"{Fore.RED}❌ Invalid option. Please choose 1-4.{Style.RESET_ALL}")
    
    def handle_registration(self):
        """Handle new user registration."""
        clear_screen()
        print_header("👤 CREATE NEW ACCOUNT")
        
        print(f"\n{Fore.CYAN}Create your account with a username and age{Style.RESET_ALL}")
        print("Your username can be anything you like - no real names required!")
        
        while True:
            print(f"\n{Fore.YELLOW}📝 ACCOUNT SETUP:{Style.RESET_ALL}")
            
            # Get username
            username = input(f"\n{Fore.YELLOW}Choose a username (3-20 characters): {Style.RESET_ALL}").strip()
            if not username:
                print(f"{Fore.RED}Username is required.{Style.RESET_ALL}")
                continue
            
            # Get age
            age_input = input(f"{Fore.YELLOW}Your age (13-19): {Style.RESET_ALL}").strip()
            if not age_input:
                print(f"{Fore.RED}Age is required.{Style.RESET_ALL}")
                continue
            
            # Try to create account
            success, message = self.auth_service.register_user(username, age_input)
            
            if success:
                print(f"\n{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
                print(f"\n{Fore.CYAN}💡 Remember your username: {Fore.YELLOW}{username}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}You'll use it to login next time!{Style.RESET_ALL}")
                
                input(f"\n{Fore.CYAN}Press Enter to continue to the main system...{Style.RESET_ALL}")
                return True
            else:
                print(f"\n{Fore.RED}❌ {message}{Style.RESET_ALL}")
                
                # If username is taken, suggest alternatives
                if "already taken" in message.lower():
                    suggestions = self.auth_service.suggest_usernames(username)
                    if suggestions:
                        print(f"\n{Fore.YELLOW}💡 Try these available usernames:{Style.RESET_ALL}")
                        for i, suggestion in enumerate(suggestions, 1):
                            print(f"   {i}. {suggestion}")
                
                retry = input(f"\n{Fore.YELLOW}Would you like to try again? (y/n): {Style.RESET_ALL}").strip().lower()
                if retry != 'y':
                    return False
    
    def handle_login(self):
        """Handle user login."""
        clear_screen()
        print_header("🔑 LOGIN TO YOUR ACCOUNT")
        
        print(f"\n{Fore.CYAN}Enter your username to access your account{Style.RESET_ALL}")
        
        while True:
            username = input(f"\n{Fore.YELLOW}Username: {Style.RESET_ALL}").strip()
            
            if not username:
                print(f"{Fore.RED}Please enter your username.{Style.RESET_ALL}")
                continue
            
            success, message = self.auth_service.login_user(username)
            
            if success:
                print(f"\n{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                return True
            else:
                print(f"\n{Fore.RED}❌ {message}{Style.RESET_ALL}")
                
                options = input(f"\n{Fore.YELLOW}What would you like to do?{Style.RESET_ALL}\n"
                              "1. Try again\n"
                              "2. Create new account\n"
                              "3. Return to main menu\n"
                              f"{Fore.YELLOW}Choice (1-3): {Style.RESET_ALL}").strip()
                
                if options == '1':
                    continue
                elif options == '2':
                    return self.handle_registration()
                else:
                    return False
    
    def handle_guest_access(self):
        """Handle guest access with limited features."""
        clear_screen()
        print_header("📋 GUEST ACCESS")
        
        print(f"\n{Fore.YELLOW}⚠️  GUEST ACCESS LIMITATIONS:{Style.RESET_ALL}")
        print("   • Cannot save progress")
        print("   • Cannot take quizzes")
        print("   • Cannot ask questions in Q&A")
        print("   • Limited access to some resources")
        
        print(f"\n{Fore.CYAN}You can still access:{Style.RESET_ALL}")
        print("   • Educational content")
        print("   • Support resources directory")
        print("   • View FAQ section")
        
        choice = input(f"\n{Fore.YELLOW}Continue as guest? (y/n): {Style.RESET_ALL}").strip().lower()
        
        if choice == 'y':
            print(f"\n{Fore.GREEN}✅ Continuing as guest...{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            return 'guest'
        
        return False
    
    def handle_exit(self):
        """Handle system exit."""
        clear_screen()
        print_header("🚪 THANK YOU")
        
        print(f"\n{Fore.CYAN}Thank you for considering our support system.{Style.RESET_ALL}")
        print("Remember, help is always available when you need it.")
        
        print(f"\n{Fore.YELLOW}🆘 EMERGENCY RESOURCES:{Style.RESET_ALL}")
        print("   • National Crisis Line: 988")
        print("   • Teen Pregnancy Hotline: 1-800-672-2296")
        print("   • Local Emergency: 911")
        
        print(f"\n{Fore.MAGENTA}Take care of yourself. You matter. 💜{Style.RESET_ALL}")
        return 'exit'
    
    def show_user_profile(self):
        """Show current user profile information."""
        if not self.auth_service.is_authenticated():
            print(f"{Fore.RED}❌ No user is currently logged in.{Style.RESET_ALL}")
            return
        
        clear_screen()
        print_header("👤 YOUR PROFILE")
        
        stats = self.auth_service.get_user_stats()
        
        if stats:
            print(f"\n{Fore.CYAN}📊 ACCOUNT INFORMATION:{Style.RESET_ALL}")
            print(f"   Username: {stats['username']}")
            print(f"   Age: {stats['age']} years old")
            print(f"   Member since: {stats['member_since']}")
            print(f"   Last login: {stats['last_login']}")
            
            if stats['progress']:
                progress = stats['progress']
                print(f"\n{Fore.GREEN}📈 LEARNING PROGRESS:{Style.RESET_ALL}")
                print(f"   Total modules: {progress.get('total_modules', 0)}")
                print(f"   Completed: {progress.get('completed_modules', 0)}")
                if progress.get('average_score'):
                    print(f"   Average quiz score: {progress.get('average_score', 0):.1f}%")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def handle_logout(self):
        """Handle user logout."""
        if not self.auth_service.is_authenticated():
            return False, "No user is currently logged in"
        
        success, message = self.auth_service.logout_user()
        
        if success:
            print(f"\n{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}❌ {message}{Style.RESET_ALL}")
        
        return success, message
    
    def get_auth_service(self):
        """Get the authentication service instance."""
        return self.auth_service