import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(user_symptoms: str) -> str:
    """
    Sends symptoms to OpenAI and returns AI-generated guidance.
    """

    system_prompt = """
You are a college-student-focused wellness assistant.

IMPORTANT RULES:
- Do NOT diagnose conditions.
- Provide general educational guidance only.
- Include basic self-care advice.
- Clearly list warning signs (red flags).
- Encourage seeking professional care if symptoms worsen.
- Be calm, clear, and concise.
- Do NOT replace emergency services.

Structure your response clearly with:
1. Possible general causes (non-diagnostic)
2. Self-care suggestions
3. Red flags (when to seek urgent care)
4. When to see a doctor
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_symptoms}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content