import streamlit as st

st.set_page_config(
    page_title="Vision",
    page_icon="🚀",
    layout="wide"
)

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
    color: #1E1B4B;
}

.hero-subtitle {
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.3rem;
    color: #5B21B6;
    margin-bottom: 2rem;
}

.section-title {
    font-family: 'Orbitron', sans-serif;
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    color: #312E81;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.workflow-container {
    display: flex;
    justify-content: center;
    align-items: stretch;
    gap: 0.8rem;
    margin: 2rem 0 3rem 0;
    flex-wrap: wrap;
}

.workflow-card {
    background: rgba(255, 255, 255, 0.55);
    border: 2px solid #7C3AED;
    border-radius: 18px;
    padding: 1rem;
    width: 145px;
    min-height: 120px;
    text-align: center;
    color: #1E1B4B;
    font-size: 1.8rem;
    box-shadow: 0 6px 18px rgba(49, 46, 129, 0.18);
    backdrop-filter: blur(8px);
}

.workflow-card span {
    font-size: 0.9rem;
    font-weight: 700;
    color: #312E81;
}

.workflow-arrow {
    display: flex;
    align-items: center;
    color: #5B21B6;
    font-size: 2rem;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# HEADER

st.markdown(
    '<div class="hero-title">Vision</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">Towards a continuously learning fact-checking ecosystem</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# INTRO

st.markdown(
    '<div class="section-title">Beyond Static Datasets</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    Current fact-checking datasets are valuable, but they are inherently limited:
    they contain only a finite number of previously reviewed statements.

    Our long-term vision is to transform LIAR from a prediction tool into a
    living platform where new political statements can continuously be added,
    reviewed, and incorporated into the dataset.
    """
)

# COMMUNITY VALIDATION

st.markdown(
    '<div class="section-title">Community Validation</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    Inspired by community-driven verification systems such as Community Notes,
    users would be able to submit and evaluate new statements.

    Once a statement reaches a sufficient number of independent votes
    (for example 10,000), the consensus label could become eligible for
    inclusion in the LIAR database.
    """
)

# ROADMAP DIAGRAM

st.markdown(
    '<div class="section-title">Proposed Workflow</div>',
    unsafe_allow_html=True
)

st.image(
    "images/workflow.png",
    use_container_width=True
)

# FACT FEATURE

st.markdown(
    '<div class="section-title">The "Fact" Layer</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    A future extension would introduce a dedicated **Fact** field.

    While the current model predicts the credibility of a statement,
    the Fact field would aim to capture the verified outcome once
    sufficient evidence becomes available.

    Example:

    **Statement**
    > "Country X will reduce emissions by 50% before 2030."

    **Prediction**
    > Questionable

    **Fact (future)**
    > Target not achieved. Emissions reduced by 18%.

    This would allow users not only to assess credibility,
    but also to understand what eventually happened in reality.
    """
)

# LONG TERM

st.markdown(
    '<div class="section-title">Long-Term Goal</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    The ultimate ambition is to create a transparent and self-improving
    political fact-checking ecosystem where machine learning, collective
    intelligence, and verified outcomes work together.

    Rather than relying solely on static historical datasets, the platform
    could continuously learn from new information and evolve alongside
    political discourse itself.
    """
)

st.markdown("---")

st.caption(
    """
    This roadmap represents a conceptual vision and is not part of the current implementation.
    """
)
