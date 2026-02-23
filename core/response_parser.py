import json
import re

def parse_ai_response(ai_response: str) -> dict:
    """
    Parses the AI response string into a structured dictionary.
    Handles both JSON and plain text responses.
    
    Args:
        ai_response: Raw response from OpenAI
        
    Returns:
        Dict with parsed recommendations or error info
    """
    
    # Check for error responses
    if ai_response.startswith("ERROR:"):
        return {
            'error': True,
            'message': ai_response.replace("ERROR: ", ""),
            'recommendations': None
        }
    
    try:
        # Try to extract JSON from the response
        # Sometimes AI wraps JSON in markdown code blocks
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(0)
            recommendations = json.loads(json_str)
            
            return {
                'error': False,
                'message': '',
                'recommendations': recommendations
            }
        else:
            # No JSON found - return plain text response
            return {
                'error': False,
                'message': 'Response not in expected format',
                'recommendations': None,
                'raw_response': ai_response
            }
            
    except json.JSONDecodeError as e:
        # JSON parsing failed
        return {
            'error': True,
            'message': f'Could not parse AI response: {str(e)}',
            'recommendations': None,
            'raw_response': ai_response
        }
    except Exception as e:
        # Other errors
        return {
            'error': True,
            'message': f'Unexpected error: {str(e)}',
            'recommendations': None
        }


def validate_recommendations_structure(recommendations: dict) -> bool:
    """
    Validates that recommendations have the expected structure.
    
    Args:
        recommendations: Dict to validate
        
    Returns:
        True if valid structure, False otherwise
    """
    
    if not recommendations or not isinstance(recommendations, dict):
        return False
    
    # Check for required keys
    required_keys = ['teas', 'medications', 'exercises', 'products']
    
    for key in required_keys:
        if key not in recommendations:
            return False
        if not isinstance(recommendations[key], list):
            return False
    
    return True