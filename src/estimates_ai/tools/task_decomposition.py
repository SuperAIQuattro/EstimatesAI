import time

from datapizza.tools import tool
from datapizza.tracing import ContextTracing
from estimates_ai.observability.tracing import set_attributes_and_status, set_exception, tracer
from estimates_ai.llm.client_factory import default_client as client
from estimates_ai.schemas.task_decomposition import ActivityList


TASK_DECOMPOSITION_SYSTEM_PROMPT = """Sei un assistente che aiuta a decomporre idee di progetto in attività specifiche.

Riceverai l'input nel seguente formato:
Progetto: <descrizione del progetto>

Rispondi con una lista di attività adatte a realizzarlo. Ogni attività deve includere nome, descrizione, tipo (feature/bug/refactor/documentation/testing) e criteri di accettazione."""


@tool
def task_decomposition(query: str) -> str:
    """Decomposes a project idea into smaller activities."""
    t0 = time.perf_counter()
    print("Decomposing the project idea...")
    with ContextTracing().trace("task_decomposition"):
        with tracer.start_as_current_span("task_decomposition") as span:
            try:
                result = client.structured_response(
                    input=query,
                    output_cls=ActivityList,
                    system_prompt=TASK_DECOMPOSITION_SYSTEM_PROMPT,
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
            return result.structured_data[0].model_dump_json(indent=2)
