import streamlit as st

from datapizza.memory import Memory


# style constants
CARD_STYLE = """
  background-color:#1e1e1e;
  padding:14px;
  border-radius:14px;
  border:1px solid rgba(255,255,255,0.08);
  text-align:center;
  margin-bottom:10px;
"""
LABEL_STYLE = """
  font-size:0.8rem;
  color:#9ca3af;
  margin-bottom:6px;
"""
VALUE_STYLE = """
  font-size:1.15rem;
  font-weight:700;
  color:white;
"""


def _render_card(label: str, value: str) -> None:
  st.markdown(
    f"""
    <div style="{CARD_STYLE}">
        <div style="{LABEL_STYLE}">
            {label}
        </div>
        <div style="{VALUE_STYLE}">
            {value}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
  )


def render_sidebar() -> tuple[str, float]:
  """Render the sidebar and return (selected_model, temperature)."""
  with st.sidebar:
    if st.button("🗑️ Nuovo task", use_container_width=True):
      st.session_state["history"] = []
      st.session_state["token_total"] = 0
      st.session_state["token_input"] = 0
      st.session_state["token_output"] = 0
      st.session_state["memory"] = Memory()
      st.session_state["cost"] = 0.0
      st.session_state["activity_type"] = ""

      st.rerun()

    history_text = "\n".join(
      f"[{m['role']}] {m['content']}" for m in st.session_state["history"]
    )
    st.download_button(
      "⬇️ Scarica cronologia",
      data=history_text,
      file_name="history_chat.txt",
      mime="text/plain",
      use_container_width=True,
      disabled=len(st.session_state["history"]) == 0,
    )

    st.markdown(
      """
      <div style="text-align: center;">
          <a href="http://localhost:3000" target="_blank">
              Apri Grafana
          </a>
      </div>
      """,
      unsafe_allow_html=True,
    )

    st.divider()

    # Tool results
    for label, key in [
      ("Tipo di attività", "activity_type"),
    ]:
      valore = st.session_state[key] if st.session_state[key] != "" else "-"
      _render_card(label, valore)

    st.divider()

    n_turni = len(st.session_state["history"]) // 2

    # ROW METRICS
    col1, col2 = st.columns(2)
    with col1:
      _render_card("Turni", str(n_turni))
    with col2:
      _render_card("Token", str(st.session_state["token_total"]))

    _render_card(
      "Costo Token Utilizzati",
      f"€ {st.session_state['cost']:.2f}",
    )

    st.divider()

    st.header("Impostazioni")

    system_prompt = st.text_area(
      "System prompt",
      value=st.session_state["system"],
      height=200,
      key="system",
    )
    if system_prompt != st.session_state["system"]:
      st.session_state["system"] = system_prompt

    st.divider()

    selected_model = st.selectbox(
      "Seleziona modello",
      ["gpt-5.4-nano", "gpt-5.4"],
      key="selected_model",
      help="Scegli il modello OpenAI da usare per questa sessione",
    )

    temperature = st.slider(
      "Temperatura",
      min_value=0.0,
      max_value=1.0,
      value=0.7,
      step=0.05,
      key="temperature",
      help="Valori più alti rendono le risposte più creative ma meno deterministiche",
    )

  return selected_model, temperature
