"""
What is this file?
This file defines the Streamlit frontend for the LIAR prediction project.

What is its responsibility?
It collects user input, sends the request to the FastAPI /explain endpoint, and displays the prediction, similar statements, and explanation in a styled interface.
"""

import requests
import streamlit as st
import pandas as pd


API_URL = "http://0.0.0.0:8080/explain"


MODEL_OPTIONS = ["naive", "naive_xboost", "roberta"]


st.set_page_config(
    page_title="LIAR - Trustworthiness Predictor",
    page_icon="⚖️",
    layout="wide",
)


st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

.stApp {
    background: radial-gradient(
        circle at center,
        #91dcff 0%,
        #f5bdff 90%,
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
    color: #312e81;
}

.hero-subtitle {
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.3rem;
    color: #4c1d95;
    margin-bottom: 2rem;
}

.section-title {
    font-family: 'Orbitron', sans-serif;
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    color: #312e81;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.custom-subheader {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #5b5d5f;
}

[data-testid="stMetric"] {
    width: 100%;
    background-color: rgba(255,255,255,0.85);
    border: 2px solid #7c3aed;
    padding: 15px;
    border-radius: 15px;
    box-shadow:0 4px 12px rgba(0,0,0,0.08);
}

[data-testid="stMetricValue"] {
    color: #4c1d95;
    font-size: 2rem;
}

[data-testid="stMetricLabel"] {
    color: #312e81;
    font-weight: bold;
}

.prediction-card {
    padding: 1.5rem;
    border-radius: 16px;
    text-align: center;
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 1rem;
    margin-bottom: 1rem;
    border: 2px solid rgba(255,255,255,0.8);
}

</style>
""",
    unsafe_allow_html=True,
)


def get_prediction_style(prediction: str) -> tuple[str, str]:
    prediction_styles = {
        "trustworthy": ("#2ecc71", "Trustworthy"),
        "questionable": ("#ffd93b", "Questionable"),
        "unreliable": ("#ff4b4b", "Unreliable"),
    }

    return prediction_styles.get(
        prediction,
        ("#cccccc", prediction.title()),
    )


def render_prediction_card(prediction: str) -> None:
    background_color, label = get_prediction_style(prediction)

    st.markdown(
        f"""
        <div class="prediction-card" style="background-color:{background_color}; color:#000000;">
            Predicted Label: {label}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_model_result(data: dict) -> None:
    st.markdown(
        '<div class="section-title">Prediction Results</div>',
        unsafe_allow_html=True,
    )

    render_prediction_card(data["prediction"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Selected Model", data["model_name"])

    with col2:
        st.metric("Confidence", f"{data['confidence']:.2%}")

    with col3:
        st.metric("Predicted Label", data["prediction"].title())

    probabilities_df = pd.DataFrame(
        [
            {
                "Class": label,
                "Probability": probability,
                "Probability %": f"{probability:.2%}",
            }
            for label, probability in data["class_probabilities"].items()
        ]
    )

    st.dataframe(
        probabilities_df,
        use_container_width=True,
        hide_index=True,
    )


def render_similar_statements(similar_statements: list[dict]) -> None:
    st.markdown(
        '<div class="section-title">Similar Verified Statements (RAG)</div>',
        unsafe_allow_html=True,
    )

    if not similar_statements:
        st.info("No similar statements were returned.")
        return

    for index, item in enumerate(similar_statements, start=1):
        with st.container(border=True):
            st.markdown(f"### Similar Statement {index}")
            st.write(item.get("statement", ""))
            st.write(f"Speaker: {item.get('speaker', 'unknown')}")
            st.write(f"Context: {item.get('context', 'unknown')}")
            st.write(f"Label: {item.get('label', 'unknown')}")


def render_explanation(explanation: str) -> None:
    st.markdown(
        '<div class="section-title">AI Analysis</div>',
        unsafe_allow_html=True,
    )

    if explanation:
        st.write(explanation)
    else:
        st.info("No explanation was returned.")


# =====================================================
# HERO SECTION
# =====================================================

col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.markdown(
        """
        <div style='text-align:center; font-family: Orbitron, sans-serif;'>
            <div style='font-size:1rem;'>Trained on</div>
            <div style='font-size:2rem; font-weight:700;'>35k+</div>
            <div style='font-size:1rem;'>Real Political Statements</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        """
        <div style='text-align:center; font-family: Orbitron, sans-serif;'>
            <div style='font-size:1rem;'>Made by</div>
            <div style="font-size:2rem; font-weight:700;">1000+</div>
            <div style='font-size:1rem;'>Different Speakers</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div style='text-align:center; font-family: Orbitron, sans-serif;'>
            <div style='font-size:1rem;'>Predictions of</div>
            <div style='font-size:2rem; font-weight:700;'>3</div>
            <div style='font-size:1rem;'>Different Trust Levels</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        """
        <div style='text-align:center; font-family: Orbitron, sans-serif;'>
            <div style='font-size:1rem;'>Powered by</div>
            <div style='font-size:2rem; font-weight:700;'>3</div>
            <div style='font-size:1rem;'>Different Models</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.image(
        "images/logo_liar.png",
        use_container_width=True,
    )

    st.markdown(
        '<div class="hero-subtitle">Detect Trustworthy, Questionable and Unreliable Political Claims</div>',
        unsafe_allow_html=True,
    )


st.divider()


# =====================================================
# ABOUT SECTION
# =====================================================

st.markdown(
    '<div class="section-title">About LIAR</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style='text-align:center; font-family: Exo 2, sans-serif; font-weight:bold'>
        LIAR is an AI-powered fact-checking tool that evaluates political statements as
        Trustworthy, Questionable, or Unreliable. Combining Machine Learning, RAG, and LLMs,
        it predicts a label, retrieves similar historical claims, and explains the reasoning
        behind each assessment.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()


# =====================================================
# INPUT SECTION
# =====================================================

st.markdown(
    "<div class='section-title'>Predict a Statement's Trustworthiness</div>",
    unsafe_allow_html=True,
)

statement = st.text_area(
    "Statement",
    height=150,
    placeholder="Enter a statement made by a political figure...",
)

col1, col2 = st.columns(2)

with col1:
    model_name = st.selectbox(
        "Model",
        MODEL_OPTIONS,
    )

    speaker = st.text_input(
        "Speaker",
        value="unknown",
        placeholder="Enter the speaker name",
    )

with col2:
    context = st.text_input(
        "Context",
        value="statement",
        placeholder="Enter the context, for example debate, interview, social media...",
    )

analyze_button = st.button(
    "Predict statement trustworthiness",
    use_container_width=True,
)

st.divider()


# =====================================================
# API REQUEST + RESULTS
# =====================================================

if analyze_button:
    if not statement.strip():
        st.error("Please enter a statement first.")
    else:
        payload = {
            "model_name": model_name,
            "statement": statement,
            "speaker": speaker or "unknown",
            "context": context or "other",
            "subject": "unknown",
            "job_title": "other",
            "state": "unknown",
            "party": "unknown",
        }

        try:
            with st.spinner("Analyzing statement with the backend API..."):
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=270,
                )

            if response.status_code == 200:
                data = response.json()

                render_model_result(data)
                st.divider()

                render_similar_statements(
                    data.get("similar_statements", [])
                )
                st.divider()

                render_explanation(
                    data.get("gemini_explanation", "")
                )
                st.divider()

                with st.expander("Raw API response"):
                    st.json(data)

            else:
                st.error(f"API error: HTTP {response.status_code}")

                with st.expander("API response"):
                    st.write(response.text)

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the FastAPI backend. Make sure the API URL is correct and the Cloud Run service is available."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The API request timed out. RoBERTa, Chroma, or Gemini may need more time."
            )

        except Exception as error:
            st.error(f"Unexpected error: {error}")
