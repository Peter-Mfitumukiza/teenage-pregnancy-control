"""
Validation utilities for the Teenage Pregnancy Awareness System.
Contains functions to validate user inputs and data.
"""

import re
from typing import Tuple, Union
import html

def validate_username_input(username: str) -> Tuple[Union[str, None], Union[str, None]]:
    """
    Validate username input for user registration.
    
    Args:
        username: The username input from user
        
    Returns:
        Tuple of (clean_username, error_message). If valid, error_message is None.
    """
    if not username:
        return None, "Username cannot be empty"
    
    # Clean the username
    username = username.strip().lower()
    
    # Check length
    if len(username) < 3:
        return None, "Username must be at least 3 characters long"
    elif len(username) > 20:
        return None, "Username must be 20 characters or less"
    
    # Check characters (letters, numbers, underscore only)
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return None, "Username can only contain letters, numbers, and underscores"
    
    # Must start with letter
    if not username[0].isalpha():
        return None, "Username must start with a letter"
    
    # Check for inappropriate words (basic filter)
    try:
        age = int(age_input)
        
        if age < 13:
            return None, "This system is designed for teenagers aged 13-19. Please seek age-appropriate resources."
        elif age > 19:
            return None, "This system is designed for teenagers aged 13-19. You may find adult-focused resources more helpful."
        else:
            return age, None
            
    except (ValueError, TypeError):
        return None, "Please enter a valid age as a number."


def validate_user_id(user_id: str) -> Tuple[bool, str]:
    """
    Validate user ID format.
    
    Args:
        user_id: The user ID to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not user_id:
        return False, "User ID cannot be empty"
    
    if len(user_id) < 8:
        return False, "User ID must be at least 8 characters long"
    
    # Check if it contains only valid characters (letters, numbers, hyphens)
    if not re.match(r'^[a-zA-Z0-9-]+$', user_id):
        return False, "User ID contains invalid characters"
    
    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format (for resource contacts).
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return True, ""  # Email is optional
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(email_pattern, email):
        return True, ""
    else:
        return False, "Please enter a valid email address"


def validate_phone_number(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not phone:
        return True, ""  # Phone is optional
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check for valid lengths (10 digits for US, 11 if includes country code)
    if len(digits_only) == 10 or (len(digits_only) == 11 and digits_only[0] == '1'):
        return True, ""
    else:
        return False, "Please enter a valid phone number (10 digits)"


def validate_question_text(question: str) -> Tuple[bool, str]:
    """
    Validate question text for the Q&A system.
    
    Args:
        question: Question text to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not question or not question.strip():
        return False, "Question cannot be empty"
    
    question = question.strip()
    
    if len(question) < 10:
        return False, "Please provide a more detailed question (at least 10 characters)"
    
    if len(question) > 1000:
        return False, "Question is too long (maximum 1000 characters)"
    
    # Check for potentially inappropriate content (basic filter)
    inappropriate_words = ['spam', 'test', 'asdf', 'qwerty']
    if any(word in question.lower() for word in inappropriate_words):
        return False, "Please ask a meaningful question"
    
    return True, ""


def validate_answer_text(answer: str) -> Tuple[bool, str]:
    """
    Validate answer text for the Q&A system.
    
    Args:
        answer: Answer text to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not answer or not answer.strip():
        return False, "Answer cannot be empty"
    
    answer = answer.strip()
    
    if len(answer) < 5:
        return False, "Please provide a more detailed answer (at least 5 characters)"
    
    if len(answer) > 2000:
        return False, "Answer is too long (maximum 2000 characters)"
    
    return True, ""


def validate_quiz_answer(answer: str) -> Tuple[bool, str]:
    """
    Validate quiz answer selection.
    
    Args:
        answer: The selected answer (should be A, B, C, or D)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not answer:
        return False, "Please select an answer"
    
    answer = answer.upper().strip()
    
    if answer not in ['A', 'B', 'C', 'D']:
        return False, "Please select A, B, C, or D"
    
    return True, ""


def validate_location_input(location: str) -> Tuple[bool, str]:
    """
    Validate location input for finding local services.
    
    Args:
        location: Location string (city, zip code, etc.)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not location or not location.strip():
        return False, "Location cannot be empty"
    
    location = location.strip()
    
    if len(location) < 2:
        return False, "Please enter a valid location (city name or zip code)"
    
    if len(location) > 100:
        return False, "Location name is too long"
    
    # Check if it's a valid zip code (5 digits) or city name (letters and spaces)
    if location.isdigit() and len(location) == 5:
        return True, ""  # Valid zip code
    elif re.match(r'^[a-zA-Z\s,.-]+$', location):
        return True, ""  # Valid city name
    else:
        return False, "Please enter a valid city name or 5-digit zip code"


def validate_resource_name(name: str) -> Tuple[bool, str]:
    """
    Validate resource name.
    
    Args:
        name: Resource name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Resource name cannot be empty"
    
    name = name.strip()
    
    if len(name) < 3:
        return False, "Resource name must be at least 3 characters long"
    
    if len(name) > 255:
        return False, "Resource name is too long (maximum 255 characters)"
    
    return True, ""


def sanitize_text_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize text input by removing potentially harmful content.
    
    Args:
        text: Text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Strip whitespace
    text = text.strip()
    
    # Remove potentially harmful HTML/script tags
    text = re.sub(r'<[^>]*>', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + '...'
    
    return text


def is_safe_content(text: str) -> Tuple[bool, str]:
    """
    Check if content is safe and appropriate.
    
    Args:
        text: Text content to check
        
    Returns:
        Tuple of (is_safe, reason_if_unsafe)
    """
    if not text:
        return True, ""
    
    text_lower = text.lower()
    
    # Check for obviously inappropriate content
    harmful_patterns = [
        r'\b(suicide|kill\s+myself|end\s+it\s+all)\b',
        r'\b(self\s*harm|cutting|hurt\s+myself)\b',
        r'\b(drug\s+dealer|buy\s+drugs|sell\s+drugs)\b',
        r'\b(prostitution|escort\s+service)\b'
    ]
    
    for pattern in harmful_patterns:
        if re.search(pattern, text_lower):
            return False, "Content may contain harmful or inappropriate material"
    
    return True, ""


def validate_menu_choice(choice: str, max_option: int) -> Tuple[Union[int, None], str]:
    """
    Validate menu choice input.
    
    Args:
        choice: User's menu choice
        max_option: Maximum valid option number
        
    Returns:
        Tuple of (choice_number, error_message)
    """
    if not choice:
        return None, "Please make a selection"
    
    try:
        choice_num = int(choice.strip())
        
        if 1 <= choice_num <= max_option:
            return choice_num, ""
        else:
            return None, f"Please choose a number between 1 and {max_option}"
            
    except ValueError:
        return None, "Please enter a valid number"


def validate_username_input(username: str) -> Tuple[str, str]:
    """
    Validate username input for user registration.
    
    Args:
        username: The username input from user (string)
        
    Returns:
        Tuple of (username, error_message). If valid, error_message is None.
    """
    if not username:
        return None, "Username cannot be empty"
    
    # Must be 3-20 characters
    if len(username) < 3 or len(username) > 20:
        return None, "Username can only contain letters, numbers, and underscores"
    
    # Must start with letter
    if not username[0].isalpha():
        return None, "Username must start with a letter"
    
    # Check for inappropriate words (basic filter)
    inappropriate_words = ['admin', 'root', 'test', 'user', 'guest', 'anonymous']
    if any(word in username for word in inappropriate_words):
        return None, "Please choose a different username"
    
    return username, None


def validate_age_input(age_input: Union[str, int]) -> Tuple[Union[int, None], Union[str, None]]:
    """
    Validate age input for user registration.
    
    Args:
        age_input: The age input from user (string or integer)
        
    Returns:
        Tuple of (age, error_message). If valid, error_message is None.
    """
    try:
        age = int(age_input)
        
        if age < 13:
            return None, "This system is designed for teenagers aged 13-19. Please seek age-appropriate resources."
        elif age > 19:
            return None, "This system is designed for teenagers aged 13-19. You may find adult-focused resources more helpful."
        else:
            return age, None
            
    except (ValueError, TypeError):
        return None, "Please enter a valid age as a number."


def validate_user_id(user_id: str) -> Tuple[bool, str]:
    """
    Validate user ID format.
    
    Args:
        user_id: The user ID to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not user_id:
        return False, "User ID cannot be empty"
    
    if len(user_id) < 8:
        return False, "User ID must be at least 8 characters long"
    
    # Check if it contains only valid characters (letters, numbers, hyphens)
    if not re.match(r'^[a-zA-Z0-9-]+$', user_id):
        return False, "User ID contains invalid characters"
    
    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format (for resource contacts).
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return True, ""  # Email is optional
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(email_pattern, email):
        return True, ""
    else:
        return False, "Please enter a valid email address"


def validate_phone_number(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not phone:
        return True, ""  # Phone is optional
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check for valid lengths (10 digits for US, 11 if includes country code)
    if len(digits_only) == 10 or (len(digits_only) == 11 and digits_only[0] == '1'):
        return True, ""
    else:
        return False, "Please enter a valid phone number (10 digits)"


def validate_question_text(question: str) -> Tuple[bool, str]:
    """
    Validate question text for the Q&A system.
    
    Args:
        question: Question text to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not question or not question.strip():
        return False, "Question cannot be empty"
    
    question = question.strip()
    
    if len(question) < 10:
        return False, "Please provide a more detailed question (at least 10 characters)"
    
    if len(question) > 1000:
        return False, "Question is too long (maximum 1000 characters)"
    
    # Check for potentially inappropriate content (basic filter)
    inappropriate_words = ['spam', 'test', 'asdf', 'qwerty']
    if any(word in question.lower() for word in inappropriate_words):
        return False, "Please ask a meaningful question"
    
    return True, ""


def validate_answer_text(answer: str) -> Tuple[bool, str]:
    """
    Validate answer text for the Q&A system.
    
    Args:
        answer: Answer text to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not answer or not answer.strip():
        return False, "Answer cannot be empty"
    
    answer = answer.strip()
    
    if len(answer) < 5:
        return False, "Please provide a more detailed answer (at least 5 characters)"
    
    if len(answer) > 2000:
        return False, "Answer is too long (maximum 2000 characters)"
    
    return True, ""


def validate_quiz_answer(answer: str) -> Tuple[bool, str]:
    """
    Validate quiz answer selection.
    
    Args:
        answer: The selected answer (should be A, B, C, or D)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not answer:
        return False, "Please select an answer"
    
    answer = answer.upper().strip()
    
    if answer not in ['A', 'B', 'C', 'D']:
        return False, "Please select A, B, C, or D"
    
    return True, ""


def validate_location_input(location: str) -> Tuple[bool, str]:
    """
    Validate location input for finding local services.
    
    Args:
        location: Location string (city, zip code, etc.)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not location or not location.strip():
        return False, "Location cannot be empty"
    
    location = location.strip()
    
    if len(location) < 2:
        return False, "Please enter a valid location (city name or zip code)"
    
    if len(location) > 100:
        return False, "Location name is too long"
    
    # Check if it's a valid zip code (5 digits) or city name (letters and spaces)
    if location.isdigit() and len(location) == 5:
        return True, ""  # Valid zip code
    elif re.match(r'^[a-zA-Z\s,.-]+$', location):
        return True, ""  # Valid city name
    else:
        return False, "Please enter a valid city name or 5-digit zip code"


def validate_resource_name(name: str) -> Tuple[bool, str]:
    """
    Validate resource name.
    
    Args:
        name: Resource name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Resource name cannot be empty"
    
    name = name.strip()
    
    if len(name) < 3:
        return False, "Resource name must be at least 3 characters long"
    
    if len(name) > 255:
        return False, "Resource name is too long (maximum 255 characters)"
    
    return True, ""


def sanitize_text_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize text input by removing potentially harmful content.
    
    Args:
        text: Text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Strip whitespace
    text = text.strip()
    
    # Remove potentially harmful HTML/script tags
    text = re.sub(r'<[^>]*>', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + '...'
    
    return text


def is_safe_content(text: str) -> Tuple[bool, str]:
    """
    Check if content is safe and appropriate.
    
    Args:
        text: Text content to check
        
    Returns:
        Tuple of (is_safe, reason_if_unsafe)
    """
    if not text:
        return True, ""
    
    text_lower = text.lower()
    
    # Check for obviously inappropriate content
    harmful_patterns = [
        r'\b(suicide|kill\s+myself|end\s+it\s+all)\b',
        r'\b(self\s*harm|cutting|hurt\s+myself)\b',
        r'\b(drug\s+dealer|buy\s+drugs|sell\s+drugs)\b',
        r'\b(prostitution|escort\s+service)\b'
    ]
    
    for pattern in harmful_patterns:
        if re.search(pattern, text_lower):
            return False, "Content may contain harmful or inappropriate material"
    
    return True, ""


def validate_menu_choice(choice: str, max_option: int) -> Tuple[Union[int, None], str]:
    """
    Validate menu choice input.
    
    Args:
        choice: User's menu choice
        max_option: Maximum valid option number
        
    Returns:
        Tuple of (choice_number, error_message)
    """
    if not choice:
        return None, "Please make a selection"
    
    try:
        choice_num = int(choice.strip())
        
        if 1 <= choice_num <= max_option:
            return choice_num, ""
        else:
            return None, f"Please choose a number between 1 and {max_option}"
            
    except ValueError:
        return None, "Please enter a valid number"
def validate_input(text, min_length=1, max_length=1000):
    """Validate user input text"""
    if not text or not isinstance(text, str):
        return False
    
    text = text.strip()
    
    if len(text) < min_length or len(text) > max_length:
        return False
    
    # Check for potentially harmful content
    dangerous_patterns = [
        r'<script',
        r'javascript:',
        r'<iframe',
        r'<object',
        r'<embed'
    ]
    
    text_lower = text.lower()
    for pattern in dangerous_patterns:
        if re.search(pattern, text_lower):
            return False
    
    return True

def validate_category(category, valid_categories):
    """Validate if category is in allowed list"""
    if not category or category not in valid_categories:
        return False
    return True

def is_safe_content(text):
    """Check if content is appropriate for teenagers"""
    # Add your content filtering logic here
    inappropriate_keywords = [
        'explicit_content',  # Add actual keywords based on your policy
        'inappropriate_term'
    ]
    
    text_lower = text.lower()
    for keyword in inappropriate_keywords:
        if keyword in text_lower:
            return False
    
    return True
