import time

from datapizza.tools import tool
from datapizza.tracing import ContextTracing
from estimates_ai.observability.tracing import set_attributes_and_status, set_exception, tracer
from estimates_ai.llm.client_factory import default_client as client
from estimates_ai.schemas.estimation import EstimationResult
from estimates_ai.schemas.task_decomposition import Activity


ESTIMATION_SYSTEM_PROMPT = (
    "Sei un senior engineering manager con 15+ anni di esperienza nella stima di progetti software. "
    "Ricevi una User Story in formato Scrum e devi produrre una stima realistica. "
    "Scomponi la User Story in sottotask implementativi concreti (es. design API, implementazione BE, test unitari, deploy). "
    "Stima le ore per ogni sottotask e calcola il totale con un range min/max. "
    "Considera overhead per code review, testing, fix e deploy. "
    "Indica i ruoli necessari e i possibili colli di bottiglia. "
    "Se le informazioni sono insufficienti, abbassa il confidence_score e spiega nelle note."
)


@tool
def estimate_activity(activity: Activity) -> str:
    """Stima il carico di lavoro in ore per una User Story / attività software."""
    t0 = time.perf_counter()

    print(f"Estimating activity: {activity.name}")
    with ContextTracing().trace(tracer, "estimate_activity"):
        with tracer.start_as_current_span("estimate_activity") as span:
            try:
                result = client.structured_response(
                    input=f"User Story da stimare:\nNome: {activity.name}\nTipo: {activity.activity_type}\nDescrizione: {activity.description}",
                    output_cls=EstimationResult,
                    system_prompt=ESTIMATION_SYSTEM_PROMPT,
                    temperature=0,
                )

                latency = time.perf_counter() - t0
                set_attributes_and_status(span, result, latency, result.usage.prompt_tokens, result.usage.completion_tokens)

            except Exception as e:
                latency = time.perf_counter() - t0
                set_exception(span, e, latency)
                raise

            return result.structured_data[0].model_dump_json(indent=2)
