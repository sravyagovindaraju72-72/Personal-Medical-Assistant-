# List of emergency keywords
EMERGENCY_WORDS = [
    'chest pain', 'heart attack', 'cant breathe', "can't breathe",
    'difficulty breathing', 'shortness of breath', 'stroke', 'seizure', 
    'suicidal', 'kill myself', 'self harm', 'severe bleeding', 
    'unresponsive', 'loss of consciousness', 'fainting', 'passed out',
    'anaphylaxis', 'overdose', 'poisoning', 'choking',
    'facial drooping', 'slurred speech', 'confused', 'disoriented',
    'severe allergic reaction', 'swelling throat', 'blue lips',
    'crushing chest', 'heart racing', 'irregular heartbeat',
    'thoughts of suicide', 'want to die', 'hurt myself',
    'vomiting blood', 'coughing blood', 'severe head injury',
    'broken bone', 'compound fracture'
]

def check_for_emergency(symptom_text):
    """
    Checks if symptom contains emergency keywords.
    
    Args:
        symptom_text: User's symptom description
        
    Returns:
        True if emergency keyword found, False if safe
    """
    symptom_lower = symptom_text.lower()
    
    for keyword in EMERGENCY_WORDS:
        if keyword in symptom_lower:
            return True
    
    return False