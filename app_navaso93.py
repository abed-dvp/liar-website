"""
What is this file?
This file defines the Streamlit frontend for the LIAR prediction project.

What is its responsibility?
It collects user input, lets the user optionally provide metadata, sends the request to the FastAPI backend, and displays the prediction, similar statements, and explanation.
"""

import requests
import streamlit as st
import pandas as pd

# =====================================================
# DEFINING API PARAMETERS AND VARIABLES
# =====================================================

API_URL = "https://liar-api-1091606282523.europe-west1.run.app/predict"

MODEL_OPTIONS = ["naive", "naive_xboost", "roberta"]
# I would name thos eoptions differently, somehting more customer focused:
#   - Basic
#   - Pro
#   - Premium
# Something less technical and more relatable

CONTEXT_OPTIONS = [
    "unknown",
    "ad",
    "interview",
    "press release",
    "news conference",
    "debate",
    "social media",
    "statement",
    "email",
    "tv appearance",
    "other",
]

# =====================================================
# DEFINING MAIN FUNCTIONS FOR LAYOUT
# =====================================================

def render_prediction_label(prediction: str) -> None:
    label_styles = {
        "trustworthy": {"background": "#2ecc71", "text": "Trustworthy"},
        "questionable": {"background": "#ffd93b", "text": "Questionable"},
        "unreliable": {"background": "#ff4b4b", "text": "Unreliable"},
    }

    style = label_styles.get(
        prediction,
        {"background": "#cccccc", "text": prediction},
    )

    st.markdown(
        f"""
        <div style="
            border-radius: 1px;
            padding: 18px;
            background-color: {style["background"]};
            color: #000000;
            font-weight: 700;
            text-align: center;
            font-size: 22px;
            margin-top: 12px;
            margin-bottom: 12px;
        ">
            Prediction: {style["text"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_probabilities(class_probabilities: dict) -> None:
    st.subheader("Class probabilities")

    for label, probability in class_probabilities.items():
        st.write(f"{label}: {probability:.2%}")
        st.progress(float(probability))

def render_similar_statements(similar_statements: list[dict]) -> None:
    st.subheader("Similar statements")

    if not similar_statements:
        st.info("No similar statements were returned.")
        return

    for index, item in enumerate(similar_statements, start=1):
        with st.expander(f"Similar statement {index}: {item.get('label', 'unknown')}"):
            st.write(f"Speaker: {item.get('speaker', 'unknown')}")
            st.write(f"Label: {item.get('label', 'unknown')}")
            st.write(f"Context: {item.get('context', 'unknown')}")
            st.write(item.get("statement", ""))


def render_explanation(explanation: str) -> None:
    st.subheader("Explanation")

    if explanation:
        st.write(explanation)
    else:
        st.info("No explanation was returned.")

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="LIAR - Trustworthiness Predictor",
    page_icon="⚖️",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

.stApp {
    background: radial-gradient(
        circle at center,
        #91dcff 0%,
        #c7b8ff 45%,
        #f5bdff 80%,
        #a228ad 95%
    );
}

.block-container {
    padding-top: 5rem;
    padding-bottom: 4rem;
    max-width: 1200px;
}

.hero-title {
    text-align: center;
    font-size: 4rem;
    font-weight: 800;
    color: #1E1B4B;     /* Darkest */
}

.hero-subtitle {
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.3rem;
    color: #5B21B6;     /* Secondary purple */
    margin-bottom: 2rem;
}

.section-title {
    font-family: 'Orbitron', sans-serif;
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    color: #312E81;     /* Main section color */
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.metric-card {
    background-color: rgba(255,255,255,0.8);
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid #c4b5fd;
}

.custom-subheader {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #4338CA;     /* Accent indigo */
}

/* Metric card */
[data-testid="stMetric"] {
    width: 100%;
    background-color: rgba(255,255,255,0.0.85);
    border: 2px solid #7c3aed;
    padding: 15px;
    border-radius: 15px;
    box-shadow:0 4px 12px rgba(0,0,0,0.08);
}

/* Metric value */
[data-testid="stMetricValue"] {
    color: #4c1d95;
    font-size: 2rem;
}

/* Metric label */
[data-testid="stMetricLabel"] {
    color: #312e81;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HERO SECTION
# =====================================================

# Optional banner image
# st.image("assets/banner.png", use_container_width=True)

col1, col2, col3 = st.columns([1,3,1])

with col1:
    st.markdown("""
    <div style='text-align:center; font-family: Orbitron, sans-serif;'>
        <div style='font-size:1rem;'>Trained on</div>
        <div style='font-size:2rem; font-weight:700;'>35k+</div>
        <div style='font-size:1rem;'>Real Political Statements</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style='text-align:center; font-family: Orbitron, sans-serif;'>
        <div style='font-size:1rem;'>Made by</div>
        <div style="font-size:2rem; font-weight:700;">1000+</div>
        <div style='font-size:1rem;'>Different Speakers</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='text-align:center; font-family: Orbitron, sans-serif;'>
        <div style='font-size:1rem;'>Predictions of</div>
        <div style='font-size:2rem; font-weight:700;'>3</div>
        <div style='font-size:1rem;'>Different Trust Levels</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style='text-align:center; font-family: Orbitron, sans-serif;'>
        <div style='font-size:1rem;'>Made by</div>
        <div style='font-size:2rem; font-weight:700;'>3</div>
        <div style='font-size:1rem;'>Different Models</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image(
        "images/logo_liar.png",
        use_container_width=True,
    )

    st.markdown(
        '<div class="hero-subtitle">Detect Trustworthy, Questionable and Unreliable Political Claims</div>',
        unsafe_allow_html=True
    )


st.divider()

# =====================================================
# ABOUT SECTION
# =====================================================

st.markdown(
    '<div class="section-title">About LIAR</div>',
    unsafe_allow_html=True
)

st.markdown("""
    <div style='text-align:center; font-family: Exo 2, sans-serif; font-weight:bold'>
        LIAR is an AI-powered fact-checking tool that evaluates political statements as
        Trustworthy, Questionable, or Unreliable. Combining Machine Learning, RAG, and LLMs,
        it not only predicts a label but also retrieves similar historical claims and explains
        the reasoning behind each assessment.
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================================
# DATASET INSIGHTS
# =====================================================

st.markdown(
    '<div class="section-title">Dataset Insights</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        '<div class="custom-subheader">Top Unreliable Speakers</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        pd.DataFrame({
            "Speaker": ["Speaker A", "Speaker B", "Speaker C"],
            "Statements": [120, 105, 99],
            "% Unreliable": [72, 69, 65]
        }),
        use_container_width=True
    )

with col2:

    st.markdown(
        '<div class="custom-subheader">Top Trustworthy Speakers</div>',
        unsafe_allow_html=True
    )

    # Here we input a dataframe from the backend with top5 trustworthy speakers (True Statements / Total Statements)
    st.dataframe(
        pd.DataFrame({
            "Speaker": ["Speaker X", "Speaker Y", "Speaker Z"],
            "Statements": [85, 79, 70],
            "% Trustworthy": [82, 80, 78]
        }),
        use_container_width=True
    )

st.markdown(
        '<div class="custom-subheader">Context Statistics</div>',
        unsafe_allow_html=True
    )

st.dataframe(
    pd.DataFrame({
        "Context": [
            "Campaign Rally",
            "TV Interview",
            "Debate"
        ],
        "Statements": [
            400,
            320,
            290
        ]
    }),
    use_container_width=True
)

st.divider()

# =====================================================
# INPUT SECTION
# =====================================================

st.markdown(
    "<div class='section-title'>Predict a Statement's Trustworthiness</div>",
    unsafe_allow_html=True
)

statement = st.text_area(
    'Statement',
    height=150,
    placeholder="Enter a statement made by a political figure..."
)

col1, col2 = st.columns(2)

with col1:
    speaker = st.text_input(
        'Speaker',
        placeholder="Enter the speaker full first and last name"
    )

with col2:
    context = st.text_input(
        'Context',
        placeholder="Enter the context (press, speech, social media...)"
    )

model_name = st.selectbox(
    'Prediction Model',
    MODEL_OPTIONS
)

analyze_button = st.button(
    "Predict statement trustworthiness",
    use_container_width=True
)

status_placeholder = st.empty()

# ================= MANAGING API CALL ==================

if analyze_button:
    if not statement.strip():
        status_placeholder.error("Please enter a statement first")
    else:
        payload = {
            'model_name': model_name,
            'statement': statement,
            'speaker': speaker,
            'context': context
        }

        try:
            status_placeholder.info('Sending request to FastAPI backend...')

            response = requests.post(
                API_URL,
                json=payload,
                timeout=270
            )

            if response.status_code == 200:
                st.session_state["results"] = response.json()
                status_placeholder.success("Prediction and explanation completed.")

            else:
                status_placeholder.error(
                    f"API error: HTTP {response.status_code}"
                )
                with st.expander("API response"):
                    st.write(response.text)

        except requests.exceptions.ConnectionError:
            status_placeholder.error(
                "Could not connect to the FastAPI backend. Make sure the API is running and the API URL is correct."
            )
        except requests.exceptions.Timeout:
            status_placeholder.error(
                "The API request timed out. RoBERTa, Chroma, or Gemini may need more time."
            )
        except Exception as error:
            status_placeholder.error(f"Unexpected error: {error}")



st.divider()

# =====================================================
# PREDICTION RESULTS
# =====================================================

st.markdown(
    '<div class="section-title">Prediction Results</div>',
    unsafe_allow_html=True
)

# only show after prediction
if 'results' in st.session_state:
    data = st.session_state["results"]

    render_prediction_label(data["prediction"])

    st.metric(
        "Confidence",
        f"{data['confidence']:.2%}"
    )

    render_probabilities(
        data["class_probabilities"]
    )

st.divider()

# =====================================================
# RAG RESULTS
# =====================================================

st.markdown(
    '<div class="section-title">Similar Verified Statements (RAG)</div>',
    unsafe_allow_html=True
)

if 'results' in st.session_state:
    data = st.session_state["results"]

    render_similar_statements(
        data.get("similar_statements", [])
    )

st.divider()

# =====================================================
# LLM ANALYSIS
# =====================================================

st.markdown(
    '<div class="section-title">AI Analysis</div>',
    unsafe_allow_html=True
)

if 'results' in st.session_state:
    data = st.session_state["results"]

    render_explanation(
        data.get("gemini_explanation", "")
    )

st.divider()

# =====================================================
# OPTIONAL IMAGE PLACEHOLDERS
# =====================================================

# st.image("assets/model_pipeline.png")
# st.image("assets/rag_diagram.png")
# st.image("assets/confusion_matrix.png")
