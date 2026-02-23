def intake_questions(user_text: str) -> list[str]:
    """
    Simple rule-based intake. Can be used for future enhancements.
    """
    text = user_text.lower()

    questions = []
    questions.append("How long have you had these symptoms (hours/days/weeks)?")
    questions.append("How severe is it on a 1–10 scale?")
    questions.append("Do you have any red flags: trouble breathing, chest pain, fainting, confusion, severe dehydration?")

    if "throat" in text or "sore throat" in text:
        questions.append("Any fever? If yes, what's the highest temperature?")
        questions.append("Any trouble swallowing?")

    if "stomach" in text or "nausea" in text:
        questions.append("Can you keep fluids down?")
        questions.append("Any severe abdominal pain?")

    if "headache" in text:
        questions.append("Is this a new/worst-ever headache? Any vision changes or neck stiffness?")

    if "back" in text or "pain" in text:
        questions.append("Did this start after lifting/exercise? Any numbness/weakness down your legs?")

    return questions[:6]