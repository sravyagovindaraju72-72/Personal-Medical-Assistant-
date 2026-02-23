# Symptom Wellness Advisor

AI-powered wellness recommendation tool that provides natural remedies, OTC medications, exercises, and product suggestions based on symptoms.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key

1. Copy `.env.example` to `.env`:
```bash
   cp .env.example .env
```

2. Add your OpenAI API key to `.env`:
```
   OPENAI_API_KEY=sk-your-actual-key-here
```

3. Get your API key from: https://platform.openai.com/api-keys

### 3. Run the Application
```bash
streamlit run app/main.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure
```
├── app/
│   └── main.py                 # Main Streamlit application
├── core/
│   ├── ai_client.py           # OpenAI API integration
│   ├── input_validator.py     # Input validation and sanitization
│   ├── response_parser.py     # AI response parsing
│   └── amazon_links.py        # Amazon link generation
├── .env.example               # Environment variable template
├── .env                       # Your actual API key (not committed)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Features

- ✅ Input validation and sanitization
- ✅ AI-powered symptom analysis
- ✅ Structured recommendations (teas, medications, exercises, products)
- ✅ Amazon product links
- ✅ Mobile-responsive design
- ✅ Medical disclaimers and safety warnings

## Team Responsibilities

- **Tyler**: AI integration and prompt engineering
- **Brigette**: Input validation, parsing, Amazon links
- **Sharika**: UI/UX design and Streamlit interface

## Important Notes

- This tool provides **general wellness information only**
- NOT a substitute for professional medical advice
- Always consult healthcare providers for medical concerns
- For emergencies, call 911

## Testing

Test with various symptoms:
- Common: "headache", "sore throat", "stomachache"
- Specific: "tension headache", "lower back pain when sitting"
- Vague: "feeling tired", "not sleeping well"

Verify:
- Input validation catches empty/invalid inputs
- AI returns structured JSON recommendations
- Amazon links work for all products
- UI displays all categories properly