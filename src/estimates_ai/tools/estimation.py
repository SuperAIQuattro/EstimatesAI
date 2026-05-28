from datapizza.tools import tool
from datapizza.tracing import ContextTracing
from opentelemetry.trace import StatusCode
from estimates_ai.observability.tracing import tracer
from estimates_ai.llm.client_factory import default_client as client
from estimates_ai.schemas.estimation import EstimationResult
from estimates_ai.schemas.task_decomposition import Activity

import time


# ── Tool ─────────────────────────────────────────────────────────────────────

@tool
def estimate_activity(activity: Activity) -> str:
    """Stima il carico di lavoro umano (in ore) per una User Story / attività software.

    Riceve un'attività ad alto livello (User Story in ottica Scrum) e produce una stima
    strutturata che include:
    - ore totali stimate con range min/max
    - confidence score e livello di rischio
    - complessità tecnica
    - scomposizione in sottotask implementativi
    - ruoli del team necessari
    - possibili bottleneck

    Il risultato viene poi utilizzato da team_allocation per assegnare i subtask al team.

    Args:
        activity: L'attività da stimare, con nome, descrizione e tipo.

    Returns:
        JSON con la stima completa in formato EstimationResult.
    """
    t0 = time.perf_counter()

    print(f"Estimating activity: {activity.name}")
    with ContextTracing().trace(tracer, "estimate_activity"):
        with tracer.start_as_current_span("estimate_activity") as span:
            try:
                prompt = (
                    f"User Story da stimare:\n"
                    f"Nome: {activity.name}\n"
                    f"Tipo: {activity.activity_type}\n"
                    f"Descrizione: {activity.description}"
                )

                result = client.structured_response(
                    input=prompt,
                    output_cls=EstimationResult,
                    system_prompt=(
                        "Sei un senior engineering manager con 15+ anni di esperienza nella stima di progetti software. "
                        "Ricevi una User Story in formato Scrum e devi produrre una stima realistica. "
                        "Scomponi la User Story in sottotask implementativi concreti (es. design API, implementazione BE, test unitari, deploy). "
                        "Stima le ore per ogni sottotask e calcola il totale con un range min/max. "
                        "Considera overhead per code review, testing, fix e deploy. "
                        "Indica i ruoli necessari e i possibili colli di bottiglia. "
                        "Se le informazioni sono insufficienti, abbassa il confidence_score e spiega nelle note."
                    ),
                    temperature=0,
                )

                latency = time.perf_counter() - t0

                prompt_tokens = result.usage.prompt_tokens
                completion_tokens = result.usage.completion_tokens

                span.set_attribute("llm.prompt_tokens", prompt_tokens)
                span.set_attribute("llm.completion_tokens", completion_tokens)
                span.set_attribute("llm.latency_ms", round(latency * 1000, 1))
                span.set_attribute("result", result.text)
                span.set_status(StatusCode.OK)

            except Exception as e:
                print(f"❌ ERROR: {e}")
                latency = time.perf_counter() - t0
                span.record_exception(e)
                span.set_status(StatusCode.ERROR, str(e))
                raise

            estimate: EstimationResult = result.structured_data[0]
            return estimate.model_dump_json(indent=2)
