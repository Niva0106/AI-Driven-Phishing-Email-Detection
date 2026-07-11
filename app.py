import streamlit as st
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Load Model and Vectorizer
model = joblib.load("phishing_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

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

# Page Configuration
st.set_page_config(
    page_title="Gone Phishing",
    page_icon="🎣",
    layout="centered"
)

# Custom CSS
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

    st.write("""
### About

This application uses **Machine Learning**
to detect whether an email is likely to be:

- ✅ Legitimate
- ⚠️ Phishing

### Technologies

- Random Forest
- TF-IDF Vectorizer
- Streamlit
- Scikit-learn
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

        vector = vectorizer.transform([cleaned])

        prediction = model.predict(vector)

        probabilities = model.predict_proba(vector)

        confidence = max(probabilities[0]) * 100

        st.divider()

        if prediction[0] == 1:

            st.error("🦈 Suspicious Catch!")

            st.write("""
The model believes this email is likely to be a **phishing attempt**.

Be cautious before clicking links or downloading attachments.
""")

        else:

            st.success("🐟 Safe Catch!")

            st.write("""
The model believes this email appears to be **legitimate**.
""")

        st.subheader("Prediction Confidence")

        st.progress(confidence / 100)

        st.write(f"**Confidence:** {confidence:.2f}%")

# Footer
st.divider()

st.caption(
    "⚠️ This application is intended for educational purposes. "
    "Machine learning predictions are not always perfect and should "
    "be used alongside good cybersecurity practices."
)