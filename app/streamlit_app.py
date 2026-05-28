import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import streamlit as st
from datapizza.memory import Memory
from components.chat import render_chat
from components.sidebar import render_sidebar


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

if "activity_type" not in st.session_state:
    st.session_state["activity_type"] = ""

if "system" not in st.session_state:
    st.session_state["system"] = (
        "Sei il team leader di un team di sviluppo software. "
        "Quando ricevi la descrizione di un task, usa i tool disponibili per: "
        "scomporre il progetto in attività, stimare il carico di lavoro, allocare il team, "
        "analizzare i rischi e valutare lo stack tecnologico."
    )


selected_model, temperature = render_sidebar()

st.title("💬 ESTIMATES AI")
st.caption(f"Modello: `{selected_model}` · Temperatura: `{temperature}`")
st.divider()

render_chat(selected_model, temperature)
