import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import streamlit as st
from core.intake import intake_questions

st.set_page_config(page_title="Your Personal Medical Assistant", page_icon="🩺", layout="centered")

st.title("🩺 Personal Medical Assistant (College Student MVP)")
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

    response = {
        "user": user_text,
        "assistant": {
            "follow_ups": questions,
            "self_care": [
                "Hydrate (water/warm liquids (e.g. herbal tea)).",
                "Rest and sleep. Aim for a full night (8-10 hours) if possible.",
                "If sore throat: warm tea/honey (if safe for you) and salt-water gargle."
            ],
            "red_flags": [
                "Trouble breathing",
                "Chest pain",
                "Severe dehydration (can’t keep fluids down)",
                "Confusion/fainting",
                "High fever that persists"
            ],
            "next_step": "How long as this been happening and how severe are your symptoms (1–10). Include any red flags listed above."
        }
    }
    st.session_state.history.append(response)

# Display conversation
if st.session_state.history:
    st.divider()
    st.subheader("Conversation")
    for item in reversed(st.session_state.history):
        st.markdown("**You:**")
        st.write(item["user"])
        st.markdown("**Assistant:**")
        st.write("**Follow-up questions:**")
        for q in item["assistant"]["follow_ups"]:
            st.write(f"- {q}")
        st.write("**Self-care (general):**")
        for tip in item["assistant"]["self_care"]:
            st.write(f"- {tip}")
        st.write("**Red flags (seek care if present):**")
        for rf in item["assistant"]["red_flags"]:
            st.write(f"- {rf}")
        st.info(item["assistant"]["next_step"])
        st.divider()
