import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config.database import db_manager
from src.ui.auth_ui import AuthUI
from src.ui.menu_handler import MenuHandler
from src.utils.helpers import clear_screen, print_header, print_emergency_contacts
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init()


class TeenagePregnancyAwarenessSystem:
    """Main application class."""
    
    def __init__(self):
        self.auth_ui = AuthUI()
        self.menu_handler = None
        self.running = True
    
    def initialize_database(self):
        """Initialize database connection and setup."""
        print(f"{Fore.YELLOW}Initializing database connection...{Style.RESET_ALL}")
        
        if db_manager.connect():
            print(f"{Fore.GREEN}✅ Database connected successfully{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}❌ Failed to connect to database{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please ensure MySQL is running and database is configured{Style.RESET_ALL}")
            return False
    
    def run(self):
        """Main application loop."""
        try:
            # Initialize database
            if not self.initialize_database():
                print(f"\n{Fore.RED}Cannot start application without database connection.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Please check your database configuration and try again.{Style.RESET_ALL}")
                return
            
            # Show welcome screen
            self.auth_ui.show_welcome_screen()
            
            # Handle authentication
            auth_result = self.auth_ui.show_auth_menu()
            
            if auth_result == 'exit':
                return
            elif auth_result == 'guest':
                self.handle_guest_mode()
            elif auth_result:
                # User successfully authenticated
                self.handle_authenticated_user()
            
        except KeyboardInterrupt:
            self.handle_shutdown("\nApplication interrupted by user")
        except Exception as e:
            self.handle_shutdown(f"Unexpected error: {str(e)}")
        finally:
            self.cleanup()
    
    def handle_authenticated_user(self):
        """Handle main menu for authenticated users."""
        try:
            self.menu_handler = MenuHandler(self.auth_ui.get_auth_service())
            
            while self.running:
                choice = self.menu_handler.show_main_menu()
                
                if choice == 'logout' or choice == 'exit':
                    break
                elif choice == 'continue':
                    continue
                else:
                    # Handle other menu choices
                    pass
            
        except KeyboardInterrupt:
            self.handle_shutdown("\nSession interrupted by user")
    
    def handle_guest_mode(self):
        """Handle limited guest access."""
        try:
            self.menu_handler = MenuHandler(None)  # No auth service for guest
            
            while self.running:
                choice = self.menu_handler.show_guest_menu()
                
                if choice == 'exit':
                    break
                elif choice == 'continue':
                    continue
                else:
                    # Handle other guest menu choices
                    pass
            
        except KeyboardInterrupt:
            self.handle_shutdown("\nGuest session interrupted")
    
    def handle_shutdown(self, message=""):
        """Handle application shutdown."""
        self.running = False
        
        if message:
            print(f"\n{Fore.YELLOW}{message}{Style.RESET_ALL}")
        
        # Logout current user if authenticated
        if self.auth_ui.get_auth_service().is_authenticated():
            self.auth_ui.handle_logout()
        
        clear_screen()
        print_header("👋 THANK YOU FOR USING OUR SYSTEM")
        
        print(f"\n{Fore.CYAN}Remember: You are not alone. Help is always available.{Style.RESET_ALL}")
        print_emergency_contacts()
        
        print(f"\n{Fore.MAGENTA}Take care of yourself. You matter. 💜{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Stay safe and remember that support is always here when you need it.{Style.RESET_ALL}")
    
    def cleanup(self):
        """Clean up resources before exit."""
        try:
            # Close database connection
            db_manager.disconnect()
        except Exception as e:
            print(f"Warning: Error during cleanup: {str(e)}")


def main():
    """Main entry point."""
    try:
        # Set up application
        app = TeenagePregnancyAwarenessSystem()
        
        # Run application
        app.run()
        
    except Exception as e:
        print(f"\n{Fore.RED}Critical error: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}If this error persists, please contact system administrators.{Style.RESET_ALL}")
        
        # Still show emergency contacts
        print_emergency_contacts()


if __name__ == "__main__":
    main()