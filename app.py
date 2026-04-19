import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from utils import detect_disaster, detect_intent
from prompts import generate_prompt

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="DisasterPrep AI", layout="wide", page_icon="🚨")

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# =========================
# NEXT-LEVEL CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=JetBrains+Mono:wght@300;400;500&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap');

/* ══════════════════════════════════════
   ROOT TOKENS
══════════════════════════════════════ */
:root {
    --bg-void:      #060608;
    --bg-deep:      #0b0b0f;
    --bg-surface:   #0f0f14;
    --bg-raised:    #141419;
    --bg-hover:     #1a1a21;

    --border-dim:   #1a1a22;
    --border-mid:   #252530;
    --border-lit:   #ff5500;

    --amber:        #ff8800;
    --fire:         #ff4400;
    --ember:        #ff2200;
    --gold:         #ffaa33;
    --ash:          #8a8578;
    --smoke:        #5a5650;
    --paper:        #e8e2d8;
    --white:        #f5f0e8;

    --mono: 'JetBrains Mono', monospace;
    --serif: 'Crimson Pro', Georgia, serif;
    --display: 'Bebas Neue', sans-serif;
}

/* ══════════════════════════════════════
   BASE
══════════════════════════════════════ */
html, body, [class*="css"] {
    font-family: var(--mono);
    background-color: var(--bg-void);
}

.stApp {
    background-color: var(--bg-void);
    /* Fine grid texture */
    background-image:
        linear-gradient(rgba(255,85,0,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,85,0,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    color: var(--paper);
}

.block-container {
    padding: 2.2rem 2.8rem 4rem;
    max-width: 1120px;
}

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background-color: var(--bg-deep);
    border-right: 1px solid var(--border-dim);
    /* Subtle vertical scan lines */
    background-image: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(255,85,0,0.015) 2px,
        rgba(255,85,0,0.015) 4px
    );
}

section[data-testid="stSidebar"] * {
    color: var(--paper);
}

/* Sidebar title — big display font */
section[data-testid="stSidebar"] h1 {
    font-family: var(--display) !important;
    font-size: 1.6rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.12em;
    color: var(--white) !important;
    text-transform: uppercase;
    padding-bottom: 0.8rem;
    margin-bottom: 0.8rem !important;
    border-bottom: 1px solid var(--border-dim);
    /* Glow on title */
    text-shadow: 0 0 30px rgba(255, 85, 0, 0.35);
}

section[data-testid="stSidebar"] label {
    font-family: var(--mono) !important;
    font-size: 9.5px !important;
    font-weight: 500 !important;
    color: var(--smoke) !important;
    text-transform: uppercase;
    letter-spacing: 0.14em;
}

section[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    font-family: var(--mono) !important;
    color: var(--ash) !important;
    font-size: 12.5px !important;
    text-transform: none;
    letter-spacing: 0.02em;
}

section[data-testid="stSidebar"] strong {
    font-family: var(--mono) !important;
    font-weight: 400 !important;
    font-size: 11px !important;
    color: var(--smoke) !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* ══════════════════════════════════════
   DIVIDERS
══════════════════════════════════════ */
hr {
    border: none !important;
    border-top: 1px solid var(--border-dim) !important;
    margin: 1rem 0 !important;
    position: relative;
}

/* ══════════════════════════════════════
   HEADINGS
══════════════════════════════════════ */
h1 {
    font-family: var(--display) !important;
    font-size: 2.6rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.1em;
    color: var(--white) !important;
    text-transform: uppercase;
    margin-bottom: 0 !important;
    line-height: 1 !important;
    /* Heat glow */
    text-shadow:
        0 0 40px rgba(255, 100, 0, 0.4),
        0 0 80px rgba(255, 60, 0, 0.15);
}

h2, h3 {
    font-family: var(--display) !important;
    font-weight: 400 !important;
    letter-spacing: 0.08em;
    color: var(--white) !important;
    text-transform: uppercase;
}

/* ══════════════════════════════════════
   CAPTION
══════════════════════════════════════ */
[data-testid="stCaptionContainer"] p {
    font-family: var(--mono) !important;
    color: var(--smoke) !important;
    font-size: 11px !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.2rem !important;
}

/* ══════════════════════════════════════
   FORM LABELS
══════════════════════════════════════ */
.stTextInput label,
.stSelectbox label,
.stMultiSelect label,
.stSlider label {
    font-family: var(--mono) !important;
    font-size: 9.5px !important;
    font-weight: 500 !important;
    color: var(--smoke) !important;
    text-transform: uppercase;
    letter-spacing: 0.14em;
}

/* ══════════════════════════════════════
   TEXT INPUT
══════════════════════════════════════ */
.stTextInput input {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: 4px !important;
    color: var(--paper) !important;
    font-family: var(--mono) !important;
    font-size: 13px !important;
    padding: 0.6rem 0.9rem !important;
    letter-spacing: 0.03em;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.stTextInput input:focus {
    border-color: var(--fire) !important;
    box-shadow:
        0 0 0 1px rgba(255, 68, 0, 0.3),
        0 0 16px rgba(255, 68, 0, 0.12) !important;
    outline: none !important;
}

.stTextInput input::placeholder {
    color: var(--smoke) !important;
    font-style: italic;
}

/* ══════════════════════════════════════
   SELECTBOX / MULTISELECT
══════════════════════════════════════ */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: 4px !important;
    color: var(--paper) !important;
    font-family: var(--mono) !important;
    font-size: 12.5px !important;
    letter-spacing: 0.02em;
}

/* Multiselect tags */
.stMultiSelect span[data-baseweb="tag"] {
    background-color: rgba(255, 85, 0, 0.15) !important;
    border: 1px solid rgba(255, 85, 0, 0.35) !important;
    color: var(--amber) !important;
    border-radius: 3px !important;
    font-family: var(--mono) !important;
    font-size: 11px !important;
    letter-spacing: 0.05em;
}

/* ══════════════════════════════════════
   RADIO BUTTONS
══════════════════════════════════════ */
.stRadio [data-baseweb="radio"] span:first-child {
    border-color: var(--border-mid) !important;
    background-color: var(--bg-surface) !important;
}

.stRadio [data-baseweb="radio"][aria-checked="true"] span:first-child {
    border-color: var(--fire) !important;
    background-color: var(--fire) !important;
    box-shadow: 0 0 8px rgba(255,68,0,0.5) !important;
}

/* ══════════════════════════════════════
   SLIDERS
══════════════════════════════════════ */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: var(--fire) !important;
    border-color: var(--fire) !important;
    box-shadow: 0 0 0 3px rgba(255, 68, 0, 0.2), 0 0 12px rgba(255, 68, 0, 0.4) !important;
    width: 14px !important;
    height: 14px !important;
}

.stSlider [data-baseweb="slider"] [data-testid="stTickBarMin"],
.stSlider [data-baseweb="slider"] [data-testid="stTickBarMax"] {
    font-family: var(--mono) !important;
    font-size: 10px !important;
    color: var(--smoke) !important;
}

/* ══════════════════════════════════════
   BUTTONS — PRIMARY (Generate)
══════════════════════════════════════ */
.stButton > button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #ff5500 0%, #cc2200 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: var(--display) !important;
    font-size: 18px !important;
    letter-spacing: 0.14em;
    padding: 0.6rem 1.6rem !important;
    text-transform: uppercase;
    box-shadow:
        0 0 0 1px rgba(255,85,0,0.4),
        0 4px 20px rgba(255, 68, 0, 0.35) !important;
    transition: box-shadow 0.2s ease, transform 0.1s ease !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow:
        0 0 0 1px rgba(255,85,0,0.6),
        0 6px 30px rgba(255, 68, 0, 0.55) !important;
    transform: translateY(-2px) !important;
}

.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

/* ══════════════════════════════════════
   BUTTONS — SECONDARY (all others)
══════════════════════════════════════ */
.stButton > button {
    background-color: var(--bg-surface) !important;
    color: var(--ash) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: 4px !important;
    font-family: var(--mono) !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    letter-spacing: 0.06em;
    padding: 0.5rem 1rem !important;
    transition: border-color 0.15s ease, color 0.15s ease,
                box-shadow 0.15s ease, transform 0.1s ease !important;
    text-transform: uppercase;
}

.stButton > button:hover {
    border-color: var(--fire) !important;
    color: var(--amber) !important;
    background-color: rgba(255, 68, 0, 0.06) !important;
    box-shadow: 0 0 14px rgba(255, 68, 0, 0.18) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ══════════════════════════════════════
   DOWNLOAD BUTTON
══════════════════════════════════════ */
.stDownloadButton > button {
    background-color: transparent !important;
    color: var(--amber) !important;
    border: 1px solid rgba(255, 136, 0, 0.45) !important;
    border-radius: 4px !important;
    font-family: var(--mono) !important;
    font-size: 11.5px !important;
    font-weight: 400 !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.5rem 1rem !important;
    margin-top: 0.75rem;
    transition: background 0.15s ease, box-shadow 0.15s ease !important;
}

.stDownloadButton > button:hover {
    background-color: rgba(255, 136, 0, 0.08) !important;
    box-shadow: 0 0 16px rgba(255, 136, 0, 0.2) !important;
}

/* ══════════════════════════════════════
   CHAT MESSAGES
══════════════════════════════════════ */
[data-testid="stChatMessage"] {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 4px !important;
    padding: 0.9rem 1.1rem !important;
    margin-bottom: 0.6rem !important;
    position: relative;
    transition: border-color 0.2s ease;
}

/* User message — left heat stripe */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-left: 2px solid var(--fire) !important;
    background-color: rgba(255, 60, 0, 0.04) !important;
    box-shadow: inset 3px 0 12px rgba(255, 60, 0, 0.06);
}

/* Assistant message — subtle gold stripe */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-left: 2px solid var(--border-mid) !important;
}

[data-testid="stChatMessage"] p {
    font-family: var(--mono) !important;
    color: var(--paper) !important;
    font-size: 13.5px !important;
    line-height: 1.8 !important;
    letter-spacing: 0.01em;
}

/* Avatar icons */
[data-testid="chatAvatarIcon-user"],
[data-testid="chatAvatarIcon-assistant"] {
    border-radius: 3px !important;
}

/* ══════════════════════════════════════
   CHAT INPUT
══════════════════════════════════════ */
[data-testid="stChatInput"] {
    border-top: 1px solid var(--border-dim) !important;
    padding-top: 0.75rem !important;
}

[data-testid="stChatInput"] textarea {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: 4px !important;
    color: var(--paper) !important;
    font-family: var(--mono) !important;
    font-size: 13px !important;
    letter-spacing: 0.02em;
    line-height: 1.6 !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: var(--fire) !important;
    box-shadow:
        0 0 0 1px rgba(255, 68, 0, 0.2),
        0 0 20px rgba(255, 68, 0, 0.1) !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--smoke) !important;
    font-style: italic;
}

/* ══════════════════════════════════════
   EXPANDERS (plan sections)
══════════════════════════════════════ */
.streamlit-expanderHeader {
    background-color: var(--bg-raised) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: 4px !important;
    color: var(--paper) !important;
    font-family: var(--display) !important;
    font-size: 17px !important;
    font-weight: 400 !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.8rem 1.1rem !important;
    transition: border-color 0.2s ease, background-color 0.2s ease;
}

.streamlit-expanderHeader:hover {
    border-color: var(--fire) !important;
    background-color: rgba(255, 68, 0, 0.05) !important;
    box-shadow: 0 0 18px rgba(255, 68, 0, 0.1);
}

.streamlit-expanderContent {
    background-color: var(--bg-deep) !important;
    border: 1px solid var(--border-dim) !important;
    border-top: none !important;
    border-radius: 0 0 4px 4px !important;
    padding: 1.1rem 1.3rem !important;
    line-height: 1.85 !important;
    font-family: var(--serif) !important;
    font-size: 15.5px !important;
    color: #c8c0b0 !important;
    letter-spacing: 0.01em;
}

.streamlit-expanderContent p,
.streamlit-expanderContent li {
    font-family: var(--serif) !important;
    color: #c8c0b0 !important;
    font-size: 15.5px !important;
    line-height: 1.85 !important;
}

.streamlit-expanderContent strong {
    color: var(--gold) !important;
    font-family: var(--serif) !important;
}

/* ══════════════════════════════════════
   SPINNER
══════════════════════════════════════ */
[data-testid="stSpinner"] p {
    font-family: var(--mono) !important;
    color: var(--smoke) !important;
    font-size: 11px !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

[data-testid="stSpinner"] svg {
    color: var(--fire) !important;
}

/* ══════════════════════════════════════
   WARNING / ALERT
══════════════════════════════════════ */
.stAlert {
    background-color: rgba(255, 136, 0, 0.06) !important;
    border: 1px solid rgba(255, 136, 0, 0.25) !important;
    border-left: 3px solid var(--amber) !important;
    border-radius: 4px !important;
    font-family: var(--mono) !important;
    font-size: 12px !important;
    color: var(--amber) !important;
    letter-spacing: 0.04em;
}

/* ══════════════════════════════════════
   INFO BOX (inside expanders)
══════════════════════════════════════ */
.stInfo {
    background-color: rgba(255, 85, 0, 0.05) !important;
    border: 1px solid rgba(255, 85, 0, 0.2) !important;
    border-radius: 4px !important;
    font-family: var(--mono) !important;
    font-size: 11.5px !important;
    color: var(--ash) !important;
}

/* ══════════════════════════════════════
   MARKDOWN BODY TEXT (plan content)
══════════════════════════════════════ */
.stMarkdown p {
    font-family: var(--mono);
    color: var(--paper);
    font-size: 13.5px;
    line-height: 1.75;
}

/* ══════════════════════════════════════
   METRIC / STATUS (sidebar)
══════════════════════════════════════ */
section[data-testid="stSidebar"] .stMarkdown p {
    font-family: var(--mono) !important;
    font-size: 11.5px !important;
    letter-spacing: 0.06em;
    color: var(--ash) !important;
}

/* ══════════════════════════════════════
   COLUMNS SPACING
══════════════════════════════════════ */
[data-testid="stHorizontalBlock"] {
    gap: 1rem;
}

/* ══════════════════════════════════════
   SCROLLBAR
══════════════════════════════════════ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-void); }
::-webkit-scrollbar-thumb {
    background: var(--border-mid);
    border-radius: 2px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--fire);
    box-shadow: 0 0 6px rgba(255,68,0,0.5);
}

/* ══════════════════════════════════════
   SELECTION
══════════════════════════════════════ */
::selection {
    background: rgba(255, 85, 0, 0.3);
    color: var(--white);
}

/* ══════════════════════════════════════
   FOCUS VISIBLE (accessibility)
══════════════════════════════════════ */
*:focus-visible {
    outline: 1px solid var(--fire) !important;
    outline-offset: 2px !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# MODEL
# =========================
@st.cache_resource
def get_model():
    return genai.GenerativeModel("models/gemini-2.5-flash")


def generate_response(prompt: str, temperature: float, top_p: float) -> str:
    model = get_model()
    response = model.generate_content(
        prompt,
        generation_config={"temperature": temperature, "top_p": top_p},
    )
    return response.text


def parse_plan_sections(plan_text: str) -> dict:
    """Split plan text into Before / During / After sections."""
    sections = {"Before": "", "During": "", "After": ""}
    current = None
    lines = []

    for line in plan_text.splitlines():
        lower = line.lower().strip()
        if "before" in lower and len(lower) < 30:
            if current and lines:
                sections[current] = "\n".join(lines).strip()
            current, lines = "Before", []
        elif "during" in lower and len(lower) < 30:
            if current and lines:
                sections[current] = "\n".join(lines).strip()
            current, lines = "During", []
        elif "after" in lower and len(lower) < 30:
            if current and lines:
                sections[current] = "\n".join(lines).strip()
            current, lines = "After", []
        elif current:
            lines.append(line)

    if current and lines:
        sections[current] = "\n".join(lines).strip()

    if not any(sections.values()):
        sections["Before"] = plan_text

    return sections


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("🚨 DisasterPrep AI")
    mode = st.radio("Mode", ["💬 Chatbot", "📋 Plan Generator"])
    st.divider()
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, step=0.05)
    top_p = st.slider("Top-p", 0.1, 1.0, 0.9, step=0.05)
    st.divider()
    st.markdown("**System status:** 🟢 Online")
    if st.button("🧹 Clear chat history"):
        st.session_state.messages = []
        st.rerun()


# =========================
# CHAT MODE
# =========================
if mode == "💬 Chatbot":
    st.title("💬 Emergency Chatbot")
    st.caption("Ask disaster-related safety questions.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    col1, col2, col3 = st.columns(3)
    quick_prompts = {
        "🌍 Earthquake": "What should I do during an earthquake?",
        "🌊 Flood": "What are the key flood safety steps?",
        "🔥 Fire": "What should I do in a fire emergency?",
    }
    for (label, prompt), col in zip(quick_prompts.items(), [col1, col2, col3]):
        if col.button(label, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Thinking…"):
                disaster = detect_disaster(prompt)
                intent = detect_intent(prompt)
                full_prompt = generate_prompt(prompt, disaster, intent)
                reply = generate_response(full_prompt, temperature, top_p)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Type your message…"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                disaster = detect_disaster(user_input)
                intent = detect_intent(user_input)
                full_prompt = generate_prompt(user_input, disaster, intent)
                reply = generate_response(full_prompt, temperature, top_p)
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})


# =========================
# PLAN GENERATOR
# =========================
else:
    st.title("📋 Disaster Plan Generator")
    st.caption("Generate a personalised preparedness plan.")

    col1, col2 = st.columns(2)

    with col1:
        location = st.text_input("📍 Location", placeholder="e.g. Mumbai, India")
        family = st.selectbox("👨‍👩‍👧 Family size", ["1–2 people", "3–4 people", "5+ people"])
        vulnerable = st.multiselect(
            "⚠️ Vulnerable members",
            ["Children", "Elderly", "People with disabilities", "Pets"],
            default=[],
        )

    with col2:
        dwelling = st.selectbox("🏠 Dwelling type", ["Apartment", "House", "Rural / farmhouse"])
        disaster = st.selectbox(
            "🌪 Disaster type",
            ["Earthquake", "Flood", "Fire", "Cyclone / Hurricane", "Heatwave", "Landslide"],
        )

    if st.button("🚀 Generate plan", type="primary", use_container_width=True):
        if not location.strip():
            st.warning("Please enter a location before generating a plan.")
        else:
            vulnerable_str = ", ".join(vulnerable) if vulnerable else "None"
            prompt = f"""
You are a disaster preparedness expert. Create a clear, actionable disaster preparedness plan.

Location: {location}
Family size: {family}
Vulnerable members: {vulnerable_str}
Dwelling type: {dwelling}
Disaster type: {disaster}

Structure your response with exactly three labelled sections:
## Before
(bullet points for preparation steps)

## During
(bullet points for actions during the event)

## After
(bullet points for recovery steps)

Be specific, practical, and concise. Tailor advice to the location and family profile.
"""
            with st.spinner("Generating your plan…"):
                plan_text = generate_response(prompt, temperature, top_p)

            sections = parse_plan_sections(plan_text)

            section_config = {
                "Before": ("🟢", "expanded"),
                "During": ("🔴", "expanded"),
                "After": ("🔵", "collapsed"),
            }

            for title, (icon, _) in section_config.items():
                with st.expander(f"{icon} {title}", expanded=(title != "After")):
                    content = sections.get(title, "")
                    if content:
                        st.markdown(content)
                    else:
                        st.info("No content generated for this section.")

            st.download_button(
                label="⬇️ Download plan as .txt",
                data=plan_text,
                file_name=f"disaster_plan_{disaster.lower().replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )