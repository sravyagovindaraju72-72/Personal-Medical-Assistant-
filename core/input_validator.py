import re

def validate_symptom_input(user_input: str) -> dict:
    """
    Validates and cleans user symptom input.
    
    Args:
        user_input: Raw text from user
        
    Returns:
        dict with 'valid' (bool), 'cleaned_input' (str), and 'error_message' (str)
    """
    
    # Remove leading/trailing whitespace
    cleaned = user_input.strip()
    
    # Check if empty
    if not cleaned:
        return {
            'valid': False,
            'cleaned_input': '',
            'error_message': 'Please describe your symptom'
        }
    
    # Check if too short (less than 2 characters)
    if len(cleaned) < 2:
        return {
            'valid': False,
            'cleaned_input': cleaned,
            'error_message': 'Please provide more detail about your symptom'
        }
    
    # Check if too long (more than 500 characters)
    if len(cleaned) > 500:
        return {
            'valid': False,
            'cleaned_input': cleaned,
            'error_message': 'Please keep your description under 500 characters'
        }
    
    # Check if only numbers
    if cleaned.isdigit():
        return {
            'valid': False,
            'cleaned_input': cleaned,
            'error_message': 'Please describe your symptom in words'
        }
    
    # Check if only special characters
    if re.match(r'^[^a-zA-Z0-9]+$', cleaned):
        return {
            'valid': False,
            'cleaned_input': cleaned,
            'error_message': 'Please describe your symptom using letters'
        }
    
    # Remove dangerous HTML/script tags (basic security)
    cleaned = re.sub(r'<script.*?</script>', '', cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r'<.*?>', '', cleaned)
    
    # Remove SQL injection attempts (basic)
    sql_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'SELECT', '--', ';--']
    for keyword in sql_keywords:
        cleaned = cleaned.replace(keyword, '')
    
    # Clean up extra spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Remove excessive punctuation (e.g., "headache!!!!!!!" -> "headache!")
    cleaned = re.sub(r'([!?.])\1{2,}', r'\1', cleaned)
    
    # Valid input
    return {
        'valid': True,
        'cleaned_input': cleaned,
        'error_message': ''
    }