import streamlit as st

from components.chat import render_chat
from components.sidebar import render_sidebar
from datapizza.memory import Memory


# PAGE CONFIGURATION
st.set_page_config(
  page_title="ESTIMATES AI",
  page_icon="🗃️",
  layout="centered",
)


# STATES
if "history" not in st.session_state:
  st.session_state["history"] = []  # role + content

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

if "competenze_tecniche" not in st.session_state:
  st.session_state["competenze_tecniche"] = ""

if "sezione" not in st.session_state:
  st.session_state["sezione"] = ""

if "numero_files" not in st.session_state:
  st.session_state["numero_files"] = ""

if "external" not in st.session_state:
  st.session_state["external"] = ""

if "system" not in st.session_state:
  st.session_state["system"] = """Sei il team leader del team SuperAIQuattro.
Quando uno sviluppatore ti segnala un task:
1. Classificalo con analizza_tipologia per capire il tipo di attività e le competenze tecniche necessarie
2. Quando ti chiedere la sezione coinvolta o quanti file bisogna modificare, usa analizza_sezione
3. Quando ti chiede se vengono usati servizi esterni, usa servizi_esterni

Mantieni il contesto della conversazione: ricorda la categoria, le competenze tecniche, la sezione coinvolta
o quanti file bisogna modificare e la risposta dai turni precedenti per produrre risposte coerenti.

Se il report è ambiguo, spiega il tuo ragionamento."""


# SIDEBAR
selected_model, temperature = render_sidebar()


# HEADER
st.title("💬 ESTIMATES AI")
st.caption(f"Modello scelto: `{selected_model}` · Temperatura: `{temperature}`")
st.divider()


# CHAT
render_chat(selected_model, temperature)
