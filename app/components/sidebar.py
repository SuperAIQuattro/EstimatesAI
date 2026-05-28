import streamlit as st

from datapizza.memory import Memory

CARD_STYLE = "background-color:#1e1e1e;padding:14px;border-radius:14px;border:1px solid rgba(255,255,255,0.08);text-align:center;margin-bottom:10px;"
LABEL_STYLE = "font-size:0.8rem;color:#9ca3af;margin-bottom:6px;"
VALUE_STYLE = "font-size:1.15rem;font-weight:700;color:white;"
VALUE_STYLE_SM = "font-size:0.82rem;font-weight:600;color:white;word-break:break-word;white-space:normal;line-height:1.5;text-align:left;"


def _render_card(label: str, value: str, small: bool = False) -> None:
    vs = VALUE_STYLE_SM if small else VALUE_STYLE
    st.markdown(
        f'<div style="{CARD_STYLE}"><div style="{LABEL_STYLE}">{label}</div><div style="{vs}">{value}</div></div>',
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
            st.session_state["n_activities"] = ""
            st.session_state["total_hours"] = 0.0
            st.session_state["risk_level"] = ""
            st.session_state["team_name"] = ""
            st.session_state["overall_risk"] = ""
            st.session_state["tech_summary"] = ""
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

        n_act = st.session_state["n_activities"]
        tot_h = st.session_state["total_hours"]
        risk = st.session_state["risk_level"]
        team = st.session_state["team_name"]
        overall = st.session_state["overall_risk"]
        tech = st.session_state["tech_summary"]

        col_a, col_b = st.columns(2)
        with col_a:
            _render_card("Attività", str(n_act) if n_act != "" else "-")
        with col_b:
            _render_card("Ore stimate", f"{tot_h:.1f}h" if tot_h else "-")

        col_c, col_d = st.columns(2)
        with col_c:
            _render_card("Risk Level", risk or "-")
        with col_d:
            _render_card("Team", team or "-")

        _render_card("Rischio", overall or "-", small=True)
        _render_card("Stack", tech or "-", small=True)

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            _render_card("Turni", str(len(st.session_state["history"]) // 2))
        with col2:
            _render_card("Token", str(st.session_state["token_total"]))

        _render_card("Costo Token Utilizzati", f"€ {st.session_state['cost']:.6f}")

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
