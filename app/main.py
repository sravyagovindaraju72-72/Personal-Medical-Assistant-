import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import streamlit as st

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Now this is safe
if st.session_state.history:
    for msg in st.session_state.history:
        st.write(msg)

from core.intake import intake_questions

st.set_page_config(page_title="Your Personal Medical Assistant", page_icon="🩺", layout="centered")

st.title("🩺 Personal Medical Assistant (College Student MVP)")

# --- 1. MOVE THIS TO THE TOP (Right after st.title) ---
st.markdown("""
    <style>
    .safety-note {
        padding: 15px;
        border-radius: 10px;
        background-color: #fff5f5;
        border: 1px solid #ff4b4b;
        color: #b91c1c;
        margin-bottom: 20px;
    }
    </style>
    <div class="safety-note">
        <strong>Hey!</strong> Just a reminder: I'm an AI, not a doctor. 
        If things feel urgent, please call 911 or campus security.
    </div>
    """, unsafe_allow_html=True)

# --- 2. CLEAN UP THE LOOP AT THE BOTTOM ---
if st.session_state.history:
    st.divider()
    st.subheader("Conversation")
    for item in reversed(st.session_state.history):
        # Everything here must be indented by 4 spaces
        st.info(f"**Assessment for:** {item['user_input']} (Severity: {item['severity']}/10)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🛡️ Safety Status")
            st.write(item["assistant"]["safety_status"])
            
            st.markdown("### ❓ Follow-ups")
            for q in item["assistant"]["follow_ups"]:
                st.write(f"- {q}")

        with col2:
            st.markdown("### 🏠 Self-Care")
            for tip in item["assistant"]["self_care"]:
                st.write(f"- {tip}")
            
            st.markdown("### 🏥 Seek Care")
            for sf in item["assistant"]["seek_care"]:
                st.write(f"- {sf}")

        # This caption is indented to stay inside the loop
        st.caption(f"📚 **Sources:** {', '.join(item['assistant']['sources'])}")
        st.divider()

st.caption("I do not provide a diagnosis and I am not for emergencies. If you think you’re in danger, please call local emergency services.")

with st.expander("Safety disclaimer READ ME: "):
    st.write(
        """
- I cannot diagnose any conditions.
- I will provide general self-care and over-the-counter informatiom, but will not prescribe official treatment.
- If you have severe symptoms (e.g., chest pain, trouble breathing, fainting, confusion), seek urgent care immediately.
        """
    )

st.subheader("How are you feeling?")
user_text = st.text_area("Symptoms/Context", placeholder="Example: sore throat for 2 days, mild fever, low energy...", height=120)
col_sev, col_dur = st.columns(2)
with col_sev:
    severity = st.select_slider(
        "How much pain/discomft do you feel? (1-10)",
        options=list(range(1, 11)),
        value=5
    )
with col_dur:
    duration = st.text_input("How long has this been happening?", placeholder="e.g., 3 days, since last night")

if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns([1, 1])

with col1:
    submit = st.button("Get guidance", type="primary")
with col2:
    clear = st.button("Clear")

if clear:
    st.session_state.history = []
    st.rerun()

if submit and user_text.strip():
    # For now: no LLM. Just show a structured follow-up plan.
    questions = intake_questions(user_text)

 # Ensure every { has a matching } and every [ has a matching ]
    response = {
        "user_input": user_text,  
        "severity": severity,
        "duration": duration,
        "assistant": {
            "safety_status": "Your situation looks stable, but monitor your symptoms.",
            "follow_ups": questions,
            "self_care": [
                "Hydrate (water/warm liquids (e.g. herbal tea)).",
                "Rest and sleep. Aim for a full night (8-10 hours) if possible.",
                "If sore throat: warm tea/honey (if safe for you) and salt-water gargle."
            ],
            "seek_care": [
                "If severity hits 8+",
                "If you have trouble breathing",
                "Chest pain",
                "Severe dehydration (can’t keep fluids down)",
                "Confusion/fainting",
                "High fever that persists"
            ],
            "sources": ["University Health Services", "CDC Guidelines"]
        }
    } 
  
    st.session_state.history.append(response)

# Display conversation
if st.session_state.history:
    st.divider()
    st.subheader("Conversation")
for item in reversed(st.session_state.history):
    st.info(f"**Assessment for:** {item['user_input']} (Severity: {item['severity']}/10)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🛡️ Safety Status")
        st.write(item["assistant"]["safety_status"])
        
        st.markdown("### ❓ Follow-ups")
        for q in item["assistant"]["follow_ups"]:
            st.write(f"- {q}")

    with col2:
        st.markdown("### 🏠 Self-Care")
        for tip in item["assistant"]["self_care"]:
            st.write(f"- {tip}")
        
        st.markdown("### 🏥 Seek Care")
        for sf in item["assistant"]["seek_care"]:
            st.write(f"- {sf}")
    st.caption(f"📚 **Sources:** {', '.join(item['assistant']['sources'])}")
    st.divider()
   