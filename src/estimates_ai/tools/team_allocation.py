from datapizza.tools import tool
from datapizza.tracing import ContextTracing
from estimates_ai.observability.tracing import set_attributes_and_status, set_exception, tracer
from estimates_ai.llm.client_factory import default_client as client

from estimates_ai.schemas.team_allocation import Team
from estimates_ai.schemas.estimation import EstimationResult

import time

@tool
def team_allocation(estimated_task: EstimationResult) -> Team:
    """
    Allocates a team for a given task.

    Args:
        estimated_task (EstimationResult): The task for which to allocate a team. The task should include a name and a description.

    Returns:
        Team: The allocated team, including its name, members, and kind.
    """
    t0 = time.perf_counter()

    print(f"Allocating a team for the task...")
    with ContextTracing().trace(tracer, "team_allocation"):
        with tracer.start_as_current_span("team_allocation") as span:
            try:
                result = client.structured_response(
                    input=f"""
                    Data la seguente attività, allocare un team adatto a svolgerla.

                    - Totale ore stimate: {estimated_task.total_estimated_hours}
                    - Minimo ore stimate: {estimated_task.minimum_hours}
                    - Massimo ore stimate: {estimated_task.maximum_hours}
                    - Confidenza nella stima: {estimated_task.confidence_score}
                    - Livello di rischio: {estimated_task.risk_level}
                    - Complessità tecnica: {estimated_task.technical_complexity}
                    - Sottotask: {', '.join([subtask.name for subtask in estimated_task.subtasks])}
                    - Ruoli suggeriti: {', '.join(estimated_task.suggested_roles)}
                    - Possibili colli di bottiglia: {', '.join(estimated_task.possible_bottlenecks)}
                    - Note dell'attività: {estimated_task.notes}
                    """,
                    output_cls=Team,
                    system_prompt="""
                    Sei un assistente che aiuta a allocare team per attività specifiche.
                    Riceverai una descrizione dettagliata dell'attività e dovrai rispondere con un team adatto a svolgerla, includendo il nome del team, i membri e il tipo di team.
                    """,
                    temperature=0.7
                )

                latency = time.perf_counter() - t0

                prompt_tokens = result.usage.prompt_tokens
                completion_tokens = result.usage.completion_tokens

                TOTAL_PROMPT_TOKENS += prompt_tokens
                TOTAL_COMPLETION_TOKENS += completion_tokens

                set_attributes_and_status(span, result, latency, prompt_tokens, completion_tokens)

            except Exception as e:
                latency = time.perf_counter() - t0
                set_exception(span, e, latency)
                raise

            team = result.structured_data[0]
            return team.model_dump_json(indent=2)
