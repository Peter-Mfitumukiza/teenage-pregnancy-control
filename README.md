# Teenage Pregnancy Awareness and Support System

A Python-based application designed to provide education, support, and resources for teenagers regarding reproductive health and pregnancy awareness. This system prioritizes user privacy and anonymity while delivering age-appropriate, medically accurate information.

## 🌟 Features

### Core Functionality

- **Anonymous User System**: Complete anonymity with secure user IDs
- **Educational Resources**: Interactive lessons on reproductive health, contraception, and pregnancy risks
- **Support Network**: Access to counseling resources and support services
- **Local Services Finder**: Location-based resource discovery
- **Anonymous Q&A**: Safe space for asking questions and getting answers
- **Knowledge Quizzes**: Interactive assessments to reinforce learning
- **Progress Tracking**: Monitor learning journey and achievements

### Security & Privacy

- 🔒 Complete user anonymity
- 🛡️ Secure session management
- 📊 Encrypted sensitive data storage
- 🚫 No personal identifying information collected
- ✅ Safe content filtering

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd teenage-pregnancy-control
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python src/main.py
   ```

## 📂 Project Structure

```
teenage_pregnancy_awareness_system/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── config/
│   ├── __init__.py
│   ├── database.py          # Database connection management
│   └── settings.py          # Application settings
│
├── src/
│   ├── main.py              # Application entry point
│   │
│   ├── models/              # Data models
│   │   ├── user.py          # User model and operations
│   │   ├── educational_content.py
│   │   ├── resources.py
│   │   └── quiz.py
│   │
│   ├── services/            # Business logic
│   │   ├── auth_service.py  # Authentication management
│   │   ├── education_service.py
│   │   ├── support_service.py
│   │   ├── quiz_service.py
│   │   └── messaging_service.py
│   │
│   ├── ui/                  # User interface
│   │   ├── auth_ui.py       # Authentication interface
│   │   ├── menu_handler.py  # Main menu navigation
│   │   ├── education_ui.py
│   │   ├── support_ui.py
│   │   └── quiz_ui.py
│   │
│   └── utils/               # Utility functions
│       ├── validators.py    # Input validation
│       ├── security.py      # Security utilities
│       └── helpers.py       # UI helpers
│
├── database/
│   ├── migrations/
│        └── create_tables.sql
│  

```

## 🔧 Configuration

### Database Configuration
Edit `.env` file with your MySQL credentials:
```
DB_HOST=localhost
DB_NAME=teenage_pregnancy_awareness
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=3306
```

### Security Settings
Ensure you set secure keys in your `.env` file:
```
SESSION_SECRET_KEY=your_unique_secret_key
ENCRYPTION_KEY=your_encryption_key
```

## 🎯 Usage

### For Users (Teenagers)
1. **Starting the Application**: Run `python src/main.py`
2. **Registration**: Create an anonymous account with just your age
3. **Navigation**: Use the numbered menu system to explore features
4. **Learning**: Access educational modules and track your progress
5. **Support**: Find local resources and get help when needed

### For Developers
1. **Adding Educational Content**: Update `database/sample_data/educational_content.sql`
2. **Adding Support Resources**: Update `database/sample_data/resources.sql`
3. **Creating New Features**: Follow the MVC pattern in the existing structure
4. **Testing**: Run tests with `pytest tests/`

## 🛡️ Privacy & Security

This application prioritizes user privacy and safety:

- **Anonymous by Design**: Only age is collected, no personal information
- **Secure Sessions**: Encrypted session management
- **Safe Content**: Content filtering and validation
- **Emergency Resources**: Always available crisis contact information
- **Data Protection**: Secure storage and transmission of all data


## 🤝 Contributing

This is a collaborative project for social awareness. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 📄 License

This project is created for educational and social awareness purposes. Please use responsibly and ensure all content remains appropriate for teenage users.

## 🙏 Acknowledgments

- Healthcare professionals who provided content guidance
- Community organizations supporting teenage pregnancy awareness
- Educational institutions promoting reproductive health education

---

**Remember**: This system is designed to support and educate, not replace professional medical advice. Always consult healthcare providers for medical concerns.