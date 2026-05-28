import time

from datapizza.tools import tool
from datapizza.tracing import ContextTracing
from estimates_ai.observability.tracing import set_attributes_and_status, set_exception, tracer
from estimates_ai.llm.client_factory import default_client as client
from estimates_ai.schemas.team_allocation import Team


TEAM_ALLOCATION_SYSTEM_PROMPT = """Sei un assistente che aiuta ad allocare team per attività specifiche.

Riceverai l'input nel seguente formato:
Totale ore stimate: <ore>
Range: <min> - <max> ore
Confidenza: <score>
Livello di rischio: <livello>
Complessità tecnica: <complessità>
Ruoli suggeriti: <lista>
Possibili colli di bottiglia: <lista>
Note: <note>

Rispondi con un team adatto a svolgere l'attività, includendo nome del team, membri e tipo di team."""


@tool
def team_allocation(query: str) -> str:
    """Allocates a team for a given estimated task."""
    t0 = time.perf_counter()
    print("Allocating a team for the task...")
    with ContextTracing().trace("team_allocation"):
        with tracer.start_as_current_span("team_allocation") as span:
            try:
                result = client.structured_response(
                    input=query,
                    output_cls=Team,
                    system_prompt=TEAM_ALLOCATION_SYSTEM_PROMPT,
                    temperature=0.7,
                )
                latency = time.perf_counter() - t0
                prompt_tokens = result.usage.prompt_tokens
                completion_tokens = result.usage.completion_tokens
                set_attributes_and_status(span, result, latency, prompt_tokens, completion_tokens)
            except Exception as e:
                latency = time.perf_counter() - t0
                set_exception(span, e, latency)
                raise
            analisi = result.structured_data[0]
            try:
                import streamlit as st
                st.session_state["team_name"] = analisi.name
            except Exception:
                pass
            return analisi.model_dump_json(indent=2)
