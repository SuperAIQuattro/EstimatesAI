import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import streamlit as st
from datapizza.memory import Memory
from components.chat import render_chat
from components.sidebar import render_sidebar
from estimates_ai.observability.metrics import initialize_observability


st.set_page_config(page_title="ESTIMATES AI", page_icon="🗃️", layout="centered")

if "history" not in st.session_state:
    st.session_state["history"] = []

if "memory" not in st.session_state:
    st.session_state["memory"] = Memory()

if "token_total" not in st.session_state:
    st.session_state["token_total"] = 0

if "token_input" not in st.session_state:
    st.session_state["token_input"] = 0

if "token_output" not in st.session_state:
    st.session_state["token_output"] = 0

if "cost" not in st.session_state:
    st.session_state["cost"] = 0.0

if "n_activities" not in st.session_state:
    st.session_state["n_activities"] = ""

if "total_hours" not in st.session_state:
    st.session_state["total_hours"] = 0.0

if "risk_level" not in st.session_state:
    st.session_state["risk_level"] = ""

if "team_name" not in st.session_state:
    st.session_state["team_name"] = ""

if "overall_risk" not in st.session_state:
    st.session_state["overall_risk"] = ""

if "tech_summary" not in st.session_state:
    st.session_state["tech_summary"] = ""

if "system" not in st.session_state:
    st.session_state["system"] = (
        "Sei il team leader di un team di sviluppo software. "
        "Quando ricevi la descrizione di un task, usa i tool disponibili per: "
        "scomporre il progetto in attività, stimare il carico di lavoro, allocare il team, "
        "analizzare i rischi e valutare lo stack tecnologico."
    )

if "observability_initialized" not in st.session_state:
    metrics = initialize_observability()
    st.session_state.update(metrics)
    st.session_state["observability_initialized"] = True
    print("✅ OpenTelemetry e Prometheus inizializzati")


selected_model, temperature = render_sidebar()

st.title("💬 ESTIMATES AI")
st.caption(f"Modello: `{selected_model}` · Temperatura: `{temperature}`")
st.divider()

render_chat(selected_model, temperature)
