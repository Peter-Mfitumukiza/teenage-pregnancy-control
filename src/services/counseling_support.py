from datetime import datetime
from colorama import Fore, Style
from config.database import db_manager
from src.models.counseling_session import CounselingSession

class CounselingSupport:
    
    def __init__(self):
        # Ensure database connection is established
        if not db_manager.connection or not db_manager.connection.is_connected():
            db_manager.connect()
        
        # Create counseling sessions table if it doesn't exist
        self._create_sessions_table()
    
    def _create_sessions_table(self):
        """Create counseling sessions table if it doesn't exist."""
        create_query = """
        CREATE TABLE IF NOT EXISTS counseling_sessions (
            session_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(20) NOT NULL,
            client_name VARCHAR(255) NOT NULL,
            topic TEXT NOT NULL,
            preferred_date DATE NOT NULL,
            status ENUM('scheduled', 'completed', 'cancelled', 'rescheduled') DEFAULT 'scheduled',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
        """
        
        try:
            db_manager.execute_query(create_query)
        except Exception as e:
            print(f"Note: Counseling sessions table may already exist: {e}")
    
    def display_topics(self):
        """Display available support topics."""
        print(f"\n{Fore.CYAN}📋 Available Support Topics:{Style.RESET_ALL}")
        print("=" * 40)
        
        topics = [
            "1. 🤱 Coping with teenage pregnancy",
            "2. 🧠 Mental health and stress management",
            "3. 👨‍👩‍👧‍👦 Talking to parents and family",
            "4. 🥗 Nutrition during pregnancy",
            "5. 📚 Educational support options",
            "6. 💰 Financial planning and resources",
            "7. 🏥 Healthcare navigation",
            "8. 👥 Peer support and relationships",
            "9. 📋 Other (please specify)"
        ]
        
        for topic in topics:
            print(f"   {topic}")
        
        print("\n" + "=" * 40)
    
    def book_session(self, username):
        """Book a new counseling session."""
        print(f"\n{Fore.GREEN}--- 📅 Book a Counseling Session ---{Style.RESET_ALL}")
        
        # Get client information
        name = input("Enter your first name (or press Enter to stay anonymous): ").strip()
        if not name:
            name = "Anonymous"
        
        print(f"\n{Fore.CYAN}What would you like help with?{Style.RESET_ALL}")
        self.display_topics()
        
        topic = input("\nEnter the topic you need help with: ").strip()
        if not topic:
            print(f"{Fore.RED}❌ Topic is required.{Style.RESET_ALL}")
            return False
        
        # Get preferred date
        print(f"\n{Fore.CYAN}When would you prefer to have the session?{Style.RESET_ALL}")
        date_input = input("Enter preferred date (YYYY-MM-DD, e.g., 2025-07-28): ").strip()
        
        # Validate date format
        try:
            preferred_date = datetime.strptime(date_input, '%Y-%m-%d').date()
        except ValueError:
            print(f"{Fore.RED}❌ Invalid date format. Please use YYYY-MM-DD{Style.RESET_ALL}")
            return False
        
        # Optional notes
        notes = input("Any additional notes or specific concerns (optional): ").strip()
        if not notes:
            notes = None
        
        # Create the session
        success, message = CounselingSession.create_session(
            username, name, topic, preferred_date, notes
        )
        
        if success:
            print(f"\n{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📞 You will be contacted soon to confirm the appointment.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}❌ {message}{Style.RESET_ALL}")
        
        return success
    
    def view_sessions(self, username):
        """View all sessions for a user."""
        print(f"\n{Fore.GREEN}--- 📋 Your Booked Sessions ---{Style.RESET_ALL}")
        
        sessions = CounselingSession.get_user_sessions(username)
        
        if not sessions:
            print(f"{Fore.YELLOW}📝 No sessions booked yet.{Style.RESET_ALL}")
            print("Book your first session to get started with counseling support!")
            return []
        
        print(f"\nFound {len(sessions)} session(s):")
        print("=" * 80)
        
        for idx, session in enumerate(sessions, start=1):
            status_color = {
                'scheduled': Fore.BLUE,
                'completed': Fore.GREEN,
                'cancelled': Fore.RED,
                'rescheduled': Fore.YELLOW
            }.get(session.status, Fore.WHITE)
            
            print(f"\n{Fore.CYAN}{idx}. Session #{session.session_id}{Style.RESET_ALL}")
            print(f"   👤 Name: {session.name}")
            print(f"   📝 Topic: {session.topic}")
            print(f"   📅 Date: {session.preferred_date}")
            print(f"   {status_color}📊 Status: {session.status.title()}{Style.RESET_ALL}")
            
            if session.notes:
                print(f"   📄 Notes: {session.notes}")
            
            print(f"   🕒 Booked: {session.created_at.strftime('%Y-%m-%d %H:%M') if session.created_at else 'Unknown'}")
        
        print("\n" + "=" * 80)
        return sessions
    
    def edit_session(self, username):
        """Edit a counseling session."""
        print(f"\n{Fore.YELLOW}--- ✏️ Edit a Counseling Session ---{Style.RESET_ALL}")
        
        sessions = self.view_sessions(username)
        if not sessions:
            return False
        
        # Get session selection
        try:
            session_choice = input(f"\n{Fore.YELLOW}Enter the session number to edit (1-{len(sessions)}): {Style.RESET_ALL}").strip()
            session_index = int(session_choice) - 1
            
            if session_index < 0 or session_index >= len(sessions):
                print(f"{Fore.RED}❌ Invalid session number.{Style.RESET_ALL}")
                return False
            
            selected_session = sessions[session_index]
            
        except ValueError:
            print(f"{Fore.RED}❌ Please enter a valid number.{Style.RESET_ALL}")
            return False
        
        # Check if session can be edited
        if selected_session.status == 'completed':
            print(f"{Fore.RED}❌ Cannot edit completed sessions.{Style.RESET_ALL}")
            return False
        
        print(f"\n{Fore.CYAN}Editing Session #{selected_session.session_id}{Style.RESET_ALL}")
        print("Press Enter to keep current value, or type new value:")
        
        # Get new values
        new_name = input(f"Name [{selected_session.name}]: ").strip()
        if not new_name:
            new_name = selected_session.name
        
        new_topic = input(f"Topic [{selected_session.topic}]: ").strip()
        if not new_topic:
            new_topic = selected_session.topic
        
        new_date_input = input(f"Date [{selected_session.preferred_date}]: ").strip()
        if new_date_input:
            try:
                new_date = datetime.strptime(new_date_input, '%Y-%m-%d').date()
            except ValueError:
                print(f"{Fore.RED}❌ Invalid date format. Keeping original date.{Style.RESET_ALL}")
                new_date = selected_session.preferred_date
        else:
            new_date = selected_session.preferred_date
        
        new_notes = input(f"Notes [{selected_session.notes or 'None'}]: ").strip()
        if not new_notes:
            new_notes = selected_session.notes
        
        # Update the session
        success, message = selected_session.update_session(
            name=new_name,
            topic=new_topic,
            preferred_date=new_date,
            notes=new_notes
        )
        
        if success:
            print(f"\n{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}❌ {message}{Style.RESET_ALL}")
        
        return success
    
    def delete_session(self, username):
        """Delete a counseling session."""
        print(f"\n{Fore.RED}--- 🗑️ Delete a Counseling Session ---{Style.RESET_ALL}")
        
        sessions = self.view_sessions(username)
        if not sessions:
            return False
        
        # Get session selection
        try:
            session_choice = input(f"\n{Fore.YELLOW}Enter the session number to delete (1-{len(sessions)}): {Style.RESET_ALL}").strip()
            session_index = int(session_choice) - 1
            
            if session_index < 0 or session_index >= len(sessions):
                print(f"{Fore.RED}❌ Invalid session number.{Style.RESET_ALL}")
                return False
            
            selected_session = sessions[session_index]
            
        except ValueError:
            print(f"{Fore.RED}❌ Please enter a valid number.{Style.RESET_ALL}")
            return False
        
        # Confirm deletion
        print(f"\n{Fore.YELLOW}⚠️ Are you sure you want to delete this session?{Style.RESET_ALL}")
        print(f"   Session #{selected_session.session_id}")
        print(f"   Topic: {selected_session.topic}")
        print(f"   Date: {selected_session.preferred_date}")
        
        confirm = input(f"\n{Fore.RED}Type 'DELETE' to confirm: {Style.RESET_ALL}").strip()
        
        if confirm != 'DELETE':
            print(f"{Fore.CYAN}❌ Deletion cancelled.{Style.RESET_ALL}")
            return False
        
        # Delete the session
        success, message = selected_session.delete_session()
        
        if success:
            print(f"\n{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}❌ {message}{Style.RESET_ALL}")
        
        return success


def display_counseling_menu():
    """Display the counseling support menu."""
    print(f"\n{Fore.MAGENTA}=== 🤝 COUNSELING & SUPPORT ==={Style.RESET_ALL}")
    print("1. 📋 View Support Topics")
    print("2. 📅 Book a Counseling Session")
    print("3. 📝 View My Sessions")
    print("4. ✏️ Edit a Session")
    print("5. 🗑️ Delete a Session")
    print("6. 🔙 Return to Main Menu")


def run_counseling_support(username=None):
    """Main function to run the counseling support system."""
    if not username:
        print(f"{Fore.RED}❌ Authentication required for counseling services.{Style.RESET_ALL}")
        return
    
    support = CounselingSupport()
    
    try:
        while True:
            display_counseling_menu()
            choice = input(f"\n{Fore.YELLOW}Choose an option (1-6): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                support.display_topics()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '2':
                support.book_session(username)
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '3':
                support.view_sessions(username)
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '4':
                support.edit_session(username)
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '5':
                support.delete_session(username)
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '6':
                print(f"{Fore.GREEN}Thank you for using counseling support! 🌸{Style.RESET_ALL}")
                break
            
            else:
                print(f"{Fore.RED}❌ Invalid choice. Please select 1-6.{Style.RESET_ALL}")
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
    except Exception as e:
        print(f"{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")
        input(f"{Fore.CYAN}Press Enter to return to main menu...{Style.RESET_ALL}")