import streamlit as st

from datapizza.memory import Memory

CARD_STYLE = "background-color:#1e1e1e;padding:14px;border-radius:14px;border:1px solid rgba(255,255,255,0.08);text-align:center;margin-bottom:10px;"
LABEL_STYLE = "font-size:0.8rem;color:#9ca3af;margin-bottom:6px;"
VALUE_STYLE = "font-size:1.15rem;font-weight:700;color:white;"


def _render_card(label: str, value: str) -> None:
    st.markdown(
        f'<div style="{CARD_STYLE}"><div style="{LABEL_STYLE}">{label}</div><div style="{VALUE_STYLE}">{value}</div></div>',
        unsafe_allow_html=True,
    )


def render_sidebar() -> tuple[str, float]:
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

        history_text = "\n".join(f"[{m['role']}] {m['content']}" for m in st.session_state["history"])
        st.download_button(
            "⬇️ Scarica cronologia",
            data=history_text,
            file_name="history_chat.txt",
            mime="text/plain",
            use_container_width=True,
            disabled=len(st.session_state["history"]) == 0,
        )

        st.markdown(
            '<div style="text-align:center;"><a href="http://localhost:3000" target="_blank">Apri Grafana</a></div>',
            unsafe_allow_html=True,
        )

        st.divider()

        valore = st.session_state["activity_type"] or "-"
        _render_card("Tipo di attività", valore)

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            _render_card("Turni", str(len(st.session_state["history"]) // 2))
        with col2:
            _render_card("Token", str(st.session_state["token_total"]))

        _render_card("Costo Token Utilizzati", f"€ {st.session_state['cost']:.2f}")

        st.divider()

        st.header("Impostazioni")
        st.text_area("System prompt", height=200, key="system")

        st.divider()

        selected_model = st.selectbox(
            "Seleziona modello",
            ["gpt-4o-mini", "gpt-4o"],
            key="selected_model",
        )

        temperature = st.slider(
            "Temperatura",
            min_value=0.0, max_value=1.0, value=0.7, step=0.05,
            key="temperature",
        )

    return selected_model, temperature
