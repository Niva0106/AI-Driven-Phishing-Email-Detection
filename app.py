import streamlit as st
import joblib
import re

model = joblib.load("phishing_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    return text

st.set_page_config(
    page_title="PhishShield AI",
    page_icon="🛡️",
    layout="centered"
)

st.title("Catch the Phish")
st.subheader("AI-Driven Phishing Email Detection")

st.write(
    "Paste an email below to check whether it is **Legitimate** or **Phishing**."
)

email = st.text_area(
    "Paste Email Here",
    height=250,
    placeholder="Paste the email content..."
)

if st.button("🔍 Analyze Email"):

    if email.strip() == "":
        st.warning("Please enter an email first.")
    else:

        cleaned = clean_text(email)

        vector = vectorizer.transform([cleaned])

        prediction = model.predict(vector)

        if prediction[0] == 1:
            st.error("⚠️ This email is likely a PHISHING email.")
        else:
            st.success("✅ This email appears to be LEGITIMATE.")