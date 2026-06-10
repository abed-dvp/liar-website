import streamlit as st

st.set_page_config(
    page_title="Why LIAR",
    page_icon="🧠",
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

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown(
    """
    <div class="hero-title">
        Why LIAR?
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-subtitle">
        Understanding the motivation behind the project
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------- INTRO ----------
st.markdown(
    """
    <div class="section-title">
        The Global Problem
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    The rise of social media and digital communication has transformed the way people
    consume political information. Every day, millions of political claims, opinions,
    and news stories are shared online, often reaching large audiences before their accuracy
    can be verified.

    While access to information has never been greater, the volume and speed of content distribution
    make it increasingly difficult for individuals to distinguish between reliable information
    and misinformation. As a result, misleading or false claims can spread widely, influencing
    public perception and political discourse before fact-checkers have the opportunity to
    intervene.
    """
)

# ---------- AI AS A SOLUTION ------------
st.markdown(
    """
    <div class="section-title">
        AI As Solution
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    Recent research suggests that AI-powered fact-checking tools can play an
    important role in addressing online misinformation. By automatically evaluating
    claims and providing credibility assessments, AI systems can help users identify
    potentially misleading content more quickly and at scale.

    Studies have shown that when users are presented with fact-checking labels or
    credibility information alongside political content, they are more likely to
    engage critically with the information they consume. Rather than replacing human
    judgment, AI can serve as a decision-support tool, helping people navigate an
    increasingly complex information landscape and encouraging more informed engagement
    with political content.
    """
)

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("images/label_pic.png", use_container_width=True)

    st.caption(
        "Figure 1. Impact of trustworthiness labels on user engagement with true and false posts."
    )

st.markdown(
    """
    In LIAR, we have clustered 6 original labels from the dataset into 3 different categories:
    """
)
col1, col2, col3 = st.columns(3)

with col1:
    st.info("✅ Trustworthy")

with col2:
    st.warning("⚠️ Questionable")

with col3:
    st.error("❌ Unreliable")

# ---------- DISCLAIMER ----------
st.markdown("---")

st.caption(
    """
    This project is an educational and research-oriented application.
    Predictions should be interpreted as model estimates rather than
    definitive factual judgments.
    """
)
