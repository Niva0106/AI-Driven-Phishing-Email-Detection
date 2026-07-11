import streamlit as st
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Load saved model and vectorizer
model = joblib.load("phishing_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]

    return " ".join(words)

st.title("🛡️ PhishShield AI")

st.subheader("AI-Driven Phishing Email Detection")

st.write(
    "Paste an email below and let the model predict whether it is "
    "a legitimate email or a phishing attempt."
)

email = st.text_area(
    "Email",
    height=250,
    placeholder="Paste email here..."
)

if st.button("🔍 Analyze Email"):

    cleaned = clean_text(email)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)

    if prediction[0] == 1:
        st.error("⚠️ This email is likely PHISHING.")
    else:
        st.success("✅ This email appears LEGITIMATE.")