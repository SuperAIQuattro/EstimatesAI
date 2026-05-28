from datapizza.tools import tool
from datapizza.tracing import ContextTracing
from opentelemetry.trace import StatusCode
from estimates_ai.observability.tracing import set_attributes_and_status, set_exception, tracer
from estimates_ai.llm.client_factory import default_client as client

from estimates_ai.schemas.task_decomposition import Activity
from estimates_ai.schemas.team_allocation import Team

import time

@tool
def team_allocation(activity: Activity) -> Team:
    """
    Allocates a team for a given activity.

    Args:
        activity (Activity): The activity for which to allocate a team. The activity should include a name and a description.

    Returns:
        Team: The allocated team, including its name, members, and kind.
    """
    t0 = time.perf_counter()

    print(f"Allocating a team for the activity: {activity.name}")
    with ContextTracing().trace(tracer, "team_allocation"):
        with tracer.start_as_current_span("team_allocation") as span:
            try:
                result = client.structured_response(
                    input=f"""
                    Data la seguente attività, allocare un team adatto a svolgerla.
                    L'attività è descritta da un nome e una descrizione.
                    Il team allocato deve essere descritto da un nome, una lista di membri e un tipo (ad esempio, "sviluppo", "design", "marketing", "frontend", "backend", ecc.).

                    L'attività da allocare è la seguente:
                    - Nome: {activity.name}
                    - Descrizione: {activity.description}
                    """,
                    output_cls=Team,
                    system_prompt="""
                    Sei un assistente che aiuta a allocare team per attività specifiche.
                    Riceverai una descrizione dell'attività e dovrai rispondere con un team adatto a svolgerla.
                    """,
                    temperature=0.7
                )

                latency = time.perf_counter() - t0

                prompt_tokens = result.usage.prompt_tokens
                completion_tokens = result.usage.completion_tokens

                set_attributes_and_status(span, result, latency, prompt_tokens, completion_tokens)

            except Exception as e:
                latency = time.perf_counter() - t0
                set_exception(span, e, latency)
                raise

            team = result.structured_data[0]
            return team.model_dump_json(indent=2)
