import streamlit as st
from time import perf_counter

from datapizza.type import ROLE, TextBlock
from estimates_ai.agent.orchestrator import build_estimates_agent
from estimates_ai.observability.tracing import set_attributes_and_status, set_exception
from opentelemetry import trace

MODEL_COSTS = {
    "gpt-4o-mini": {"cost_input": 0.15, "cost_output": 0.60},
    "gpt-4o": {"cost_input": 2.50, "cost_output": 10.00},
}

tracer = trace.get_tracer("stime-llm-monitor")


def total_cost(model: str, token_input: int, token_output: int) -> float:
    costs = MODEL_COSTS.get(model, {"cost_input": 0, "cost_output": 0})
    return (token_input * costs["cost_input"] + token_output * costs["cost_output"]) / 10**6


def render_chat(selected_model: str, temperature: float) -> None:
    if len(st.session_state["history"]) == 0:
        with st.chat_message("assistant"):
            st.write("Benvenuto")

    for messaggio in st.session_state["history"]:
        with st.chat_message(messaggio["role"]):
            st.write(messaggio["content"])

    prompt_utente = st.chat_input("Scrivi un messaggio...")

    if not prompt_utente:
        return

    with st.chat_message("user"):
        st.write(prompt_utente)

    st.session_state["history"].append({"role": "user", "content": prompt_utente})

    with st.chat_message("assistant"):
        with st.spinner("Sto pensando..."):
            start_time = perf_counter()
            with tracer.start_as_current_span("llm.request") as span:
                try:
                    agent = build_estimates_agent(
                        model=selected_model,
                        temperature=temperature,
                        system_prompt=st.session_state["system"],
                    )

                    response = agent.run(
                        task_input=prompt_utente,
                        memory=st.session_state["memory"],
                    )

                    latency = perf_counter() - start_time
                    response_text = response.text

                    st.session_state["memory"].add_turn(blocks=[TextBlock(content=prompt_utente)], role=ROLE.USER)
                    st.session_state["memory"].add_turn(blocks=response.content, role=ROLE.ASSISTANT)

                    st.session_state["token_input"] += response.usage.prompt_tokens
                    st.session_state["token_output"] += response.usage.completion_tokens
                    st.session_state["token_total"] += response.usage.prompt_tokens + response.usage.completion_tokens
                    st.session_state["cost"] = total_cost(selected_model, st.session_state["token_input"], st.session_state["token_output"])

                    st.session_state["llm_requests"].labels(model=selected_model, status="ok").inc()
                    st.session_state["llm_prompt_tokens"].labels(model=selected_model).inc(response.usage.prompt_tokens)
                    st.session_state["llm_completion_tokens"].labels(model=selected_model).inc(response.usage.completion_tokens)
                    st.session_state["llm_latency"].labels(model=selected_model).observe(latency)

                    set_attributes_and_status(span, response, latency)

                except Exception as e:
                    latency = perf_counter() - start_time
                    st.session_state["llm_requests"].labels(model=selected_model, status="error").inc()
                    st.session_state["llm_errors"].labels(model=selected_model, error_type=type(e).__name__).inc()
                    set_exception(span, e, latency)
                    response_text = f"Errore: {e}"
                    st.error(response_text)

        st.write(response_text)

    st.session_state["history"].append({"role": "assistant", "content": response_text})
    st.rerun()
