import streamlit as st
import requests
import langcodes

# Load GROQ API key securely from secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"  # or llama3-70b if you have access

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Supported languages
language_options = {
    "English (US)": "en",
    "Spanish (Spain)": "es",
    "French (France)": "fr",
    "German (Germany)": "de",
    "Hindi (India)": "hi",
    "Chinese (Simplified)": "zh",
    "Arabic": "ar",
}

def get_translation_prompt(source_lang, target_lang, text):
    return f"Translate this from {source_lang} to {target_lang}:\n\n{text}"

# Send prompt to Groq + LLaMA
def get_llama_response(prompt):
    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 512,
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Streamlit UI
st.title("🌐 Bilingual Chat: Agent ↔ Customer Translator")

st.sidebar.header("User Role")
user_role = st.sidebar.radio("Select Interface", ["Customer", "Agent"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Language selection
st.sidebar.header("Language Settings")
user_language = st.sidebar.selectbox("Your Language", list(language_options.keys()))
user_lang_code = language_options[user_language]

if user_role == "Agent":
    peer_lang_code = st.sidebar.selectbox("Customer Language", list(language_options.values()), index=1)
else:
    peer_lang_code = st.sidebar.selectbox("Agent Language", list(language_options.values()), index=0)

# Chat input
user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    translation_prompt = get_translation_prompt(user_lang_code, peer_lang_code, user_input)
    translated_text = get_llama_response(translation_prompt)

    st.session_state.chat_history.append({
        "role": user_role,
        "original": user_input,
        "translated": translated_text,
        "lang": user_lang_code
    })

# Display chat history
st.markdown("### 💬 Conversation")
for msg in st.session_state.chat_history:
    label = "🧑 Agent" if msg["role"] == "Agent" else "👤 Customer"
    st.markdown(f"**{label} ({msg['lang']}):** {msg['original']}")
    st.markdown(f"> Translated: _{msg['translated']}_")
