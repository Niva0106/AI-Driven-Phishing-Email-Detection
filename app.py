import streamlit as st
import joblib
import pandas as pd
import re
import nltk
from scipy.sparse import csr_matrix, hstack
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

@st.cache_resource
def load_model():
    model = joblib.load("phishing_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_model()

# Text Cleaning Function
nltk.download('stopwords')

try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))

stemmer = PorterStemmer()
def clean_text(text):
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

SUSPICIOUS_KEYWORDS = [
    "verify",
    "account",
    "password",
    "login",
    "click",
    "urgent",
    "bank",
    "security",
    "confirm",
    "update"
]


def url_count(text):
    return len(re.findall(r"(https?://\S+|www\.\S+)", text))
def email_count(text):
    return len(re.findall(r"\S+@\S+", text))
def digit_count(text):
    return sum(c.isdigit() for c in text)
def capital_count(text):
    return sum(c.isupper() for c in text)
def exclamation_count(text):
    return text.count("!")
def email_length(text):
    return len(text)
def word_count(text):
    return len(text.split())
def suspicious_keyword_count(text):
    text = text.lower()
    return sum(
        len(re.findall(rf"\b{word}\b", text))
        for word in SUSPICIOUS_KEYWORDS
    )

st.set_page_config(
    page_title="Gone Phishing",
    page_icon="🎣",
    layout="centered"
)

st.markdown("""
<style>

.main {
    background-color: #f5f9fc;
}

h1 {
    color: #0d3b66;
    text-align: center;
}

h3 {
    text-align: center;
    color: #444;
}

.stButton>button {
    width:100%;
    background-color:#0077b6;
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background-color:#023e8a;
    color:white;
}

.result-box{
    padding:18px;
    border-radius:12px;
    background:#eef6ff;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:

    st.title("🎣 Gone Phishing")

    st.caption("AI-powered phishing email detection using Machine Learning")

    st.write("""
### About

This application uses **Machine Learning**
to detect whether an email is likely to be:

- ✅ Legitimate
- ⚠️ Phishing

### Model Pipeline
• Text Cleaning
• Porter Stemming
• TF-IDF (7000 Features)
• Engineered Email Features
• Random Forest Classifier
""")

    st.divider()

    st.write("👩‍💻 Developed by **Niveditha**")

# Header
st.title("🎣 Gone Phishing")

st.subheader("Catch phishing emails before they catch you.")

st.write("""
Welcome aboard!

Paste an email below and let our AI cast its net to determine whether the message is **Legitimate** or a **Phishing Attempt**.
""")

# Email Input
email = st.text_area(
    "📧 Paste Email Here",
    height=250,
    placeholder="Paste the email content..."
)

# Prediction
if st.button("🎣 Cast the Net"):

    if email.strip() == "":
        st.warning("⚠️ Please paste an email first.")

    else:

        cleaned = clean_text(email)

        # TF-IDF
        tfidf_features = vectorizer.transform([cleaned])

        # Engineered Features
        extra = pd.DataFrame([{
            "url_count": url_count(email),
            "email_count": email_count(email),
            "digit_count": digit_count(email),
            "capital_count": capital_count(email),
            "exclamation_count": exclamation_count(email),
            "email_length": email_length(email),
            "word_count": word_count(email),
            "keyword_count": suspicious_keyword_count(email)
        }])

        extra_sparse = csr_matrix(extra.values)

        final_features = hstack([tfidf_features, extra_sparse])

        prediction = model.predict(final_features)

        probabilities = model.predict_proba(final_features)

        confidence = probabilities.max() * 100

        st.divider()

        if prediction[0] == 1:

            st.error("🦈 Suspicious Catch!")

            st.write("""
        Our AI net believes this email is **likely to be a phishing attempt**.

        🎣 **Stay alert!**
        - Avoid clicking unknown links.
        - Do not download unexpected attachments.
        - Verify the sender before taking any action.
        """)

        else:

            st.success("🐟 Clean Catch!")

            st.write("""
        Our AI net believes this email appears to be **legitimate**.

        🎣 **Still remember:**
        Even legitimate-looking emails should be treated carefully if they request sensitive information.
        """)

        st.subheader("🎯 Prediction Confidence")

        st.progress(float(confidence) / 100)

        st.write(f"**Confidence:** {confidence:.2f}%")

        with st.expander("🔍 What did the model analyse?"):
            st.dataframe(extra, use_container_width=True)

# Footer
st.divider()

st.caption(
"""
Educational project developed using Random Forest and TF-IDF.

Predictions should be used as guidance and not as a replacement for cybersecurity best practices.
"""
)