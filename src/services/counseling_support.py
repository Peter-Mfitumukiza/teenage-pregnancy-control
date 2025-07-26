import sqlite3

class CounselingSupport:
    def __init__(self):
        self.conn = sqlite3.connect('support_system.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                topic TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def display_topics(self):
        print("\nAvailable Support Topics:")
        topics = [
            "1. Coping with teenage pregnancy",
            "2. Mental health and stress",
            "3. Talking to parents",
            "4. Nutrition during pregnancy",
            "5. Educational support options"
        ]
        for topic in topics:
            print(topic)

    def book_session(self):
        print("\n--- Book a Counseling Session ---")
        name = input("Enter your first name (or press Enter to stay anonymous): ")
        if not name.strip():
            name = "Anonymous"
        topic = input("Enter the topic you need help with: ")
        date = input("Enter preferred date (e.g., 2025-07-28): ")

        self.cursor.execute('''
            INSERT INTO sessions (name, topic, date) VALUES (?, ?, ?)
        ''', (name, topic, date))
        self.conn.commit()
        print("✅ Session booked successfully!")

    def view_sessions(self):
        print("\n--- Booked Sessions ---")
        self.cursor.execute('SELECT name, topic, date FROM sessions ORDER BY date')
        sessions = self.cursor.fetchall()
        if sessions:
            for idx, session in enumerate(sessions, start=1):
                print(f"{idx}. Name: {session[0]}, Topic: {session[1]}, Date: {session[2]}")
        else:
            print("No sessions booked yet.")

    def edit_session(self):
        print("\n--- Edit a Counseling Session ---")
        self.view_sessions()
        session_id = input("Enter the session number to edit: ")

        try:
            self.cursor.execute('SELECT * FROM sessions')
            sessions = self.cursor.fetchall()
            session = sessions[int(session_id) - 1]
        except:
            print("❌ Invalid session number.")
            return

        new_name = input(f"Enter new name [{session[1]}]: ") or session[1]
        new_topic = input(f"Enter new topic [{session[2]}]: ") or session[2]
        new_date = input(f"Enter new date [{session[3]}]: ") or session[3]

        self.cursor.execute('''
            UPDATE sessions SET name = ?, topic = ?, date = ? WHERE id = ?
        ''', (new_name, new_topic, new_date, session[0]))
        self.conn.commit()
        print("✅ Session updated successfully!")

    def delete_session(self):
        print("\n--- Delete a Counseling Session ---")
        self.view_sessions()
        session_id = input("Enter the session number to delete: ")

        try:
            self.cursor.execute('SELECT * FROM sessions')
            sessions = self.cursor.fetchall()
            session = sessions[int(session_id) - 1]
        except:
            print("❌ Invalid session number.")
            return

        confirm = input(f"Are you sure you want to delete session for {session[1]}? (y/n): ")
        if confirm.lower() == 'y':
            self.cursor.execute('DELETE FROM sessions WHERE id = ?', (session[0],))
            self.conn.commit()
            print("✅ Session deleted.")
        else:
            print("❌ Deletion cancelled.")

# -------- MENU & PROGRAM RUNNER --------
def display_menu():
    print("\n=== COUNSELING & SUPPORT ===")
    print("1. View Support Topics")
    print("2. Book a Counseling Session")
    print("3. View Booked Sessions")
    print("4. Edit a Session")
    print("5. Delete a Session")
    print("6. Exit")

def run_counseling_support():
    support = CounselingSupport()

    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            support.display_topics()
        elif choice == '2':
            support.book_session()
        elif choice == '3':
            support.view_sessions()
        elif choice == '4':
            support.edit_session()
        elif choice == '5':
            support.delete_session()
        elif choice == '6':
            print("Exiting Counseling Support...")
            break
        else:
            print("Invalid choice. Please try again.")
