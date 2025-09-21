import streamlit as st
from services.ollama_service import get_ollama_models

def render_sidebar():
    st.sidebar.markdown(
        "<div style='margin-top:-40px;font-size:28px;font-weight:bold;'>My Agentic-AI Playground</div>",
        unsafe_allow_html=True
    )
    st.sidebar.divider()

    with st.sidebar.expander("Change Model", expanded=False):
        try:
            models = get_ollama_models()
        except Exception as e:
            models = ["default"]
            st.warning(f"Ollama not reachable: {e}")

        model = st.selectbox("Model", models, index=0)
        st.write(f"Selected model: {model}")

    with st.sidebar.expander("Change Option", expanded=False):
        option = st.selectbox("Option", ["Chat", "Data Agent"], index=0)
        st.write(f"Selected option: {option}")

    st.sidebar.divider()
    st.sidebar.markdown(f"> ### You have selected **{option}** with **{model}**")
    return model, option
