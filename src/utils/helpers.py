"""
Utility functions for the Teenage Pregnancy Awareness System.
Contains helper functions for UI formatting and common operations.
"""

import os
import platform
from colorama import Fore, Style
from datetime import datetime

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def print_header(title):
    """Print a formatted header."""
    width = max(60, len(title) + 10)
    print("=" * width)
    print(f"{title:^{width}}")
    print("=" * width)


def print_separator(char="-", length=60):
    """Print a separator line."""
    print(char * length)


def print_section_header(title):
    """Print a section header with formatting."""
    print(f"\n{Fore.CYAN}{'=' * 50}")
    print(f"{title:^50}")
    print(f"{'=' * 50}{Style.RESET_ALL}\n")


def print_menu_option(number, description, icon=""):
    """Print a formatted menu option."""
    if icon:
        print(f"{Fore.YELLOW}{number}.{Style.RESET_ALL} {icon} {description}")
    else:
        print(f"{Fore.YELLOW}{number}.{Style.RESET_ALL} {description}")


def print_info_box(title, content, color=Fore.CYAN):
    """Print information in a formatted box."""
    box_width = 60
    print(f"\n{color}┌{'─' * (box_width - 2)}┐")
    print(f"│ {title:<{box_width - 4}} │")
    print(f"├{'─' * (box_width - 2)}┤")
    
    if isinstance(content, list):
        for line in content:
            print(f"│ {line:<{box_width - 4}} │")
    else:
        # Split long content into lines
        words = content.split()
        line = ""
        for word in words:
            if len(line + word) > (box_width - 6):
                print(f"│ {line.strip():<{box_width - 4}} │")
                line = word + " "
            else:
                line += word + " "
        if line.strip():
            print(f"│ {line.strip():<{box_width - 4}} │")
    
    print(f"└{'─' * (box_width - 2)}┘{Style.RESET_ALL}")


def print_warning(message):
    """Print a warning message."""
    print(f"\n{Fore.YELLOW}⚠️  WARNING: {message}{Style.RESET_ALL}")


def print_error(message):
    """Print an error message."""
    print(f"\n{Fore.RED}❌ ERROR: {message}{Style.RESET_ALL}")


def print_success(message):
    """Print a success message."""
    print(f"\n{Fore.GREEN}✅ SUCCESS: {message}{Style.RESET_ALL}")


def print_info(message):
    """Print an info message."""
    print(f"\n{Fore.CYAN}ℹ️  INFO: {message}{Style.RESET_ALL}")


def get_user_input(prompt, valid_options=None, input_type=str):
    """Get user input with validation."""
    while True:
        try:
            user_input = input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}").strip()
            
            if not user_input:
                print_error("Input cannot be empty. Please try again.")
                continue
            
            # Type conversion
            if input_type == int:
                user_input = int(user_input)
            elif input_type == float:
                user_input = float(user_input)
            
            # Validate against options
            if valid_options and user_input not in valid_options:
                print_error(f"Please choose from: {', '.join(map(str, valid_options))}")
                continue
            
            return user_input
            
        except ValueError:
            print_error(f"Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
            return None


def format_progress_bar(current, total, width=30):
    """Create a text-based progress bar."""
    if total == 0:
        percentage = 0
    else:
        percentage = (current / total) * 100
    
    filled = int((current / total) * width) if total > 0 else 0
    bar = "█" * filled + "░" * (width - filled)
    
    return f"[{bar}] {percentage:.1f}% ({current}/{total})"


def format_list_with_numbers(items, start_num=1):
    """Format a list with numbers."""
    formatted_items = []
    for i, item in enumerate(items, start_num):
        formatted_items.append(f"{i}. {item}")
    return formatted_items


def truncate_text(text, max_length=50):
    """Truncate text if it's too long."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_phone_number(phone):
    """Format phone number for display."""
    if not phone:
        return "Not available"
    
    # Remove any non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone


def confirm_action(message, default='n'):
    """Ask for user confirmation."""
    if default.lower() == 'y':
        prompt = f"{message} (Y/n): "
    else:
        prompt = f"{message} (y/N): "
    
    response = input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}").strip().lower()
    
    if not response:
        return default.lower() == 'y'
    
    return response in ['y', 'yes']


def pause_for_user(message="Press Enter to continue..."):
    """Pause execution and wait for user input."""
    input(f"\n{Fore.CYAN}{message}{Style.RESET_ALL}")


def print_emergency_contacts():
    """Print emergency contact information."""
    print_info_box("🆘 EMERGENCY CONTACTS", [
        "National Crisis Line: 988",
        "Teen Pregnancy Hotline: 1-800-672-2296",
        "Local Emergency: 911",
        "Crisis Text Line: Text HOME to 741741",
        "",
        "Remember: You are not alone. Help is available."
    ], Fore.RED)


def print_privacy_reminder():
    """Print privacy and safety reminder."""
    print_info_box("🔒 PRIVACY REMINDER", [
        "• This system maintains your anonymity",
        "• Never share personal identifying information",
        "• Your data is kept confidential and secure",
        "• You can exit at any time"
    ], Fore.MAGENTA)


def sanitize_input(user_input, max_length=1000):
    """Sanitize user input for safety."""
    if not isinstance(user_input, str):
        return str(user_input)
    
    # Remove potentially harmful characters
    sanitized = user_input.strip()
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized
def print_colored(text, color="white", bold=False, center=False, end="\n"):
    """Print colored text to terminal"""
    colors = {
        'black': Fore.BLACK,
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'reset': Style.RESET_ALL
    }

    color_code = colors.get(color.lower(), colors['white'])
    bold_code = Style.BRIGHT if bold else ''
    reset_code = colors['reset']

    formatted_text = f"{bold_code}{color_code}{text}{reset_code}"

    if center:
        # Get terminal width and center the text
        try:
            import shutil
            terminal_width = shutil.get_terminal_size().columns
            padding = (terminal_width - len(text)) // 2
            formatted_text = " " * padding + formatted_text
        except:
            pass  # If terminal size can't be determined, just print normally

    print(formatted_text, end=end)

def format_date(date_obj):
    """Format datetime object to readable string"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')
        except:
            return str(date_obj)

    now = datetime.now()
    diff = now - date_obj

    if diff.days > 30:
        return date_obj.strftime('%b %d, %Y')
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"

def validate_question_text(text):
    """Validate question text format"""
    if not text or len(text.strip()) < 10:
        return False, "Question must be at least 10 characters long"

    if len(text) > 1000:
        return False, "Question must be less than 1000 characters"

    # Check for inappropriate content (basic check)
    inappropriate_words = ['spam', 'test123', 'asdf']  # Add more as needed
    text_lower = text.lower()

    for word in inappropriate_words:
        if word in text_lower:
            return False, "Please ask a meaningful question"

    return True, "Valid question"

def format_category_display(category_name):
    """Format category name for display"""
    return category_name.replace('_', ' ').title()
