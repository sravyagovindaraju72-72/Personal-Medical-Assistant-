import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
from core.ai_client import get_ai_response
from core.input_validator import validate_symptom_input
from core.response_parser import parse_ai_response, validate_recommendations_structure
from core.amazon_links import add_amazon_links_to_recommendations
from core.red_flag_detector import check_for_emergency 

# Must be first Streamlit call
st.set_page_config(
    page_title="Mend — Natural Relief", 
    page_icon="🌱", 
    layout="centered"
)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# ===========================
# MEND THEME CSS
# ===========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;600&display=swap');

/* Force light theme background everywhere */
html, body, [class*="css"], .stApp, .main, section[data-testid="stSidebar"] {
    font-family: 'Lato', sans-serif !important;
    background-color: #FAF6EF !important;
    color: #2C1A0E !important;
}

/* Override Streamlit dark mode defaults */
.stApp {
    background-color: #FAF6EF !important;
}

.block-container {
    max-width: 720px;
    padding-top: 2rem;
    background-color: #FAF6EF !important;
}

/* Force all text to dark color */
p, span, div, label, .stMarkdown, .stText {
    color: #2C1A0E !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: #2C1A0E !important;
}

/* Logo / Header Row */
.mend-logo-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
    padding: 8px 0;
}
.mend-logo-icon {
    background: linear-gradient(135deg, #5C7A4E, #7A9E6A);
    border-radius: 12px;
    width: 52px;
    height: 52px;
    min-width: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    flex-shrink: 0;
}
.mend-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 32px !important;
    font-weight: 700 !important;
    color: #2C1A0E !important;
    line-height: 1.1;
    white-space: nowrap;
}
.mend-subtitle {
    font-size: 11px !important;
    color: #7A6555 !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    white-space: nowrap;
}

/* Banners */
.emergency-banner {
    padding: 14px 18px;
    border-radius: 10px;
    background-color: #FFF0F0 !important;
    border: 1px solid #F0C0C0;
    border-left: 4px solid #D05050;
    color: #8B3030 !important;
    margin-bottom: 16px;
    font-size: 14px;
    line-height: 1.6;
}
.emergency-banner * { color: #8B3030 !important; }

.disclaimer-banner {
    padding: 14px 18px;
    border-radius: 10px;
    background-color: #FFFBF0 !important;
    border: 1px solid #E8D5A0;
    border-left: 4px solid #C4794A;
    color: #7A5533 !important;
    margin-bottom: 20px;
    font-size: 13px;
    line-height: 1.6;
}
.disclaimer-banner * { color: #7A5533 !important; }

.disclaimer-title {
    font-family: 'Playfair Display', serif !important;
    font-weight: 700;
    font-size: 14px !important;
    color: #C4794A !important;
    margin-bottom: 6px;
}

.input-label {
    font-family: 'Playfair Display', serif !important;
    font-size: 22px !important;
    font-weight: 600 !important;
    color: #2C1A0E !important;
    margin-bottom: 16px;
}

/* Buttons */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #5C7A4E, #7A9E6A) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}
.stButton > button {
    border-radius: 10px !important;
    font-family: 'Lato', sans-serif !important;
    border: 1px solid #E0D5C5 !important;
    color: #2C1A0E !important;
    background-color: #FFFFFF !important;
}

/* View on Amazon link buttons — cream/white text */
.stLinkButton a,
.stLinkButton > a,
[data-testid="stLinkButton"] a,
div[data-testid="stLinkButton"] a,
.stLinkButton a:link,
.stLinkButton a:visited {
    color: #FAF6EF !important;
    border-radius: 10px !important;
    font-family: 'Lato', sans-serif !important;
    text-decoration: none !important;
}
.stLinkButton a:hover,
[data-testid="stLinkButton"] a:hover {
    color: #FFFFFF !important;
}
.stLinkButton a *,
.stLinkButton a p,
.stLinkButton a span,
.stLinkButton a div,
.stLinkButton a label,
[data-testid="stLinkButton"] a *,
[data-testid="stLinkButton"] a p,
[data-testid="stLinkButton"] a span {
    color: #FAF6EF !important;
}

/* Inputs */
.stTextArea textarea, .stTextInput input {
    border-radius: 10px !important;
    border: 1px solid #E0D5C5 !important;
    background-color: #FFFFFF !important;
    font-family: 'Lato', sans-serif !important;
    font-size: 14px !important;
    color: #2C1A0E !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #5C7A4E !important;
    box-shadow: 0 0 0 3px rgba(92,122,78,0.15) !important;
}
.stTextArea textarea::placeholder, .stTextInput input::placeholder {
    color: #A09080 !important;
}

/* Cards */
.result-card {
    background: #FFFFFF !important;
    border: 1px solid #E0D5C5;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
}
.result-card-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #2C1A0E !important;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid #EAF0E6;
}
.recommendation-card {
    background: #FFFFFF !important;
    border: 1px solid #E0D5C5;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}
.recommendation-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #2C1A0E !important;
    margin-bottom: 8px;
}
.recommendation-text {
    font-size: 13px !important;
    color: #5A4A3A !important;
    line-height: 1.6;
}

hr { border-color: #E0D5C5 !important; }

/* Streamlit native alert/info boxes */
.stAlert {
    background-color: #FFF8EE !important;
    border: 1px solid #E0D5C5 !important;
    border-radius: 12px !important;
    color: #2C1A0E !important;
}
.stAlert p, .stAlert span, .stAlert div {
    color: #2C1A0E !important;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #FFFFFF !important;
    color: #2C1A0E !important;
    border: 1px solid #E0D5C5 !important;
    border-radius: 10px !important;
}
.streamlit-expanderContent {
    background-color: #FDFAF5 !important;
    color: #2C1A0E !important;
    border: 1px solid #E0D5C5 !important;
}

/* Caption */
.stCaption, small {
    color: #7A6555 !important;
}

/* Category headers */
.category-header {
    font-family: 'Playfair Display', serif !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    color: #5C7A4E !important;
    margin-top: 24px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #EAF0E6;
}

/* Footer */
.mend-footer {
    text-align: center;
    color: #7A6555 !important;
    font-size: 12px;
    font-style: italic;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #E0D5C5;
}

/* Spinner text */
.stSpinner > div {
    color: #5C7A4E !important;
}

/* Nuclear override: any anchor inside a Streamlit link button widget */
div.stLinkButton a,
div.stLinkButton a:link,
div.stLinkButton a:visited,
div.stLinkButton a:hover,
div.stLinkButton a:active,
div.stLinkButton a span,
div.stLinkButton a p {
    color: #FAF6EF !important;
    -webkit-text-fill-color: #FAF6EF !important;
}
</style>
""", unsafe_allow_html=True)

# ===========================
# HEADER / LOGO
# ===========================
st.markdown("""
<div class="mend-logo-row">
    <div class="mend-logo-icon">🌱</div>
    <div style="overflow: visible;">
        <div class="mend-title">Mend</div>
        <div class="mend-subtitle">Natural Relief Guide</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===========================
# BANNERS
# ===========================
st.markdown("""
<div class="emergency-banner">
    🚨 <strong>Emergency:</strong> If you have chest pain, trouble breathing, confusion, or feel you are in danger — call <strong>911</strong> or campus security immediately. This app is not for emergencies.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-banner">
    <div class="disclaimer-title">⚠️ Medical Disclaimer</div>
    Mend is for general informational purposes only and is <strong>not a substitute</strong> for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider before starting any new remedy or supplement.
</div>
""", unsafe_allow_html=True)

with st.expander("📋 Full disclaimer — read me"):
    st.write("""
- I **cannot diagnose** any conditions.
- I provide general self-care and over-the-counter information only.
- If you have severe symptoms (chest pain, trouble breathing, fainting, confusion), seek urgent care immediately.
- Information is AI-generated and should be verified with healthcare professionals.
    """)

# ===========================
# INPUT FORM
# ===========================
st.markdown('<div class="input-label">🌿 How are you feeling today?</div>', unsafe_allow_html=True)

user_input = st.text_area(
    "Describe your symptoms",
    placeholder="Example: sore throat for 2 days, mild fever, low energy...",
    height=120,
    max_chars=500,
    label_visibility="collapsed"
)

# Character counter
if user_input:
    char_count = len(user_input)
    st.caption(f"{char_count}/500 characters")

# Buttons
col1, col2 = st.columns([3, 1])

with col1:
    submit_button = st.button("🌱 Get guidance", type="primary", use_container_width=True)

with col2:
    if st.button("Clear", use_container_width=True):
        st.session_state.history = []
        st.rerun()

st.markdown("---")

# ===========================
# SUBMIT LOGIC
# ===========================

if submit_button and user_input.strip():

    # Step 1: Validate input
    validation_result = validate_symptom_input(user_input)

    if not validation_result['valid']:
        st.error(f"{validation_result['error_message']}")
        st.stop()

    cleaned_symptom = validation_result['cleaned_input']

    # Step 2: Check emergencies
    if check_for_emergency(cleaned_symptom):
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #DC2626, #EF4444);
            color: white;
            padding: 24px;
            border-radius: 12px;
            border: 3px solid #DC2626;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        '>
            <h2 style='margin: 0; font-size: 28px; color: white !important; font-family: Playfair Display, serif;'>
                🚨 EMERGENCY DETECTED
            </h2>
            <p style='margin-top: 12px; font-size: 16px; color: white !important; line-height: 1.6;'>
                Your symptoms may require immediate medical attention.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.subheader("⚕️ What to do RIGHT NOW:")
        st.markdown("- ☎️ **Call 911 immediately** or have someone take you to the ER")
        st.markdown("- 🏥 **Go to the emergency room** - do NOT drive yourself")
        st.markdown("- 📱 **Call campus security** if on campus (they can help)")
        st.markdown("- 👥 **Stay with someone** - don't be alone")
        st.write("")

        st.warning("⚠️ **This app cannot help with emergency situations.** Please seek immediate medical care. If you're alone, call 911 and unlock your door for responders.")
        st.stop()

    # Step 3: Only call AI if NOT an emergency
    with st.spinner("🔍 Analyzing your symptom and generating recommendations..."):
        ai_response = get_ai_response(cleaned_symptom)
        parsed_result = parse_ai_response(ai_response)
        
        if parsed_result['error']:
            st.error(f"❌ Error: {parsed_result['message']}")
            st.info("Please try again or rephrase your symptom description.")
            st.stop()
        
        recommendations = parsed_result['recommendations']
        
        if not recommendations or not validate_recommendations_structure(recommendations):
            st.warning("⚠️ Received response in unexpected format")
            if 'raw_response' in parsed_result:
                st.write(parsed_result['raw_response'])
            st.info("Please update the AI prompt to return JSON format")
            st.stop()
        
        recommendations = add_amazon_links_to_recommendations(recommendations)
        
        st.session_state.history.append({
            'symptom': cleaned_symptom,
            'recommendations': recommendations
        })
    
    st.success("✅ Recommendations generated!")

# ===========================
# DISPLAY RESULTS
# ===========================
if st.session_state.history:
    
    for item in reversed(st.session_state.history):
        recommendations = item['recommendations']
        
        st.markdown(f'<h2 style="font-family: Playfair Display, serif; font-size: 22px; color: #2C1A0E !important;">Your Relief Guide for: {item["symptom"]}</h2>', unsafe_allow_html=True)
        
        if recommendations.get('medical_note') and recommendations['medical_note'].strip():
            st.warning(f"⚕️ **Medical Guidance:** {recommendations['medical_note']}")
            st.write("")
        
        # Herbal Teas
        if recommendations.get('teas'):
            st.markdown('<div class="category-header">🍵 Herbal Teas</div>', unsafe_allow_html=True)
            
            for i, tea in enumerate(recommendations['teas'], 1):
                st.markdown(f"""
                <div class="recommendation-card">
                    <div class="recommendation-title">{i}. {tea.get('name', 'Unknown Tea')}</div>
                    <div class="recommendation-text">{tea.get('benefits', 'No description available')}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if tea.get('amazon_link'):
                    st.link_button("🛒 View on Amazon", tea['amazon_link'], use_container_width=True)
                st.write("")
        
        # OTC Medications
        if recommendations.get('medications'):
            st.markdown('<div class="category-header">💊 Over-the-Counter Options</div>', unsafe_allow_html=True)
            
            for i, med in enumerate(recommendations['medications'], 1):
                st.markdown(f"""
                <div class="recommendation-card">
                    <div class="recommendation-title">{i}. {med.get('name', 'Unknown Medication')}</div>
                    <div class="recommendation-text">{med.get('usage', 'No usage information available')}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if med.get('amazon_link'):
                    st.link_button("🛒 View on Amazon", med['amazon_link'], use_container_width=True)
                st.write("")
        
        # Exercises/Remedies
        if recommendations.get('exercises'):
            st.markdown('<div class="category-header">🧘 Exercises & Home Remedies</div>', unsafe_allow_html=True)
            
            for i, exercise in enumerate(recommendations['exercises'], 1):
                st.markdown(f"""
                <div class="recommendation-card">
                    <div class="recommendation-title">{i}. {exercise.get('name', 'Unknown Exercise')}</div>
                    <div class="recommendation-text">{exercise.get('instructions', 'No instructions available')}</div>
                </div>
                """, unsafe_allow_html=True)
                st.write("")
        
        # Helpful Products
        if recommendations.get('products'):
            st.markdown('<div class="category-header">🛍️ Helpful Products</div>', unsafe_allow_html=True)
            
            for i, product in enumerate(recommendations['products'], 1):
                st.markdown(f"""
                <div class="recommendation-card">
                    <div class="recommendation-title">{i}. {product.get('name', 'Unknown Product')}</div>
                    <div class="recommendation-text">{product.get('purpose', 'No description available')}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if product.get('amazon_link'):
                    st.link_button("🛒 View on Amazon", product['amazon_link'], use_container_width=True)
                st.write("")
        
        st.info("💡 **Reminder:** These are general wellness suggestions. Consult a healthcare provider for personalized medical advice.")
        st.markdown("---")

# FOOTER
st.markdown("""
<div class="mend-footer">
    Mend · Natural Relief Guide · Not a substitute for medical advice
</div>
""", unsafe_allow_html=True)
