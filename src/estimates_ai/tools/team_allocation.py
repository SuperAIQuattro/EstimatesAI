from datapizza.tools import tool
from datapizza.tracing import ContextTracing
from opentelemetry.trace import StatusCode
from main import tracer
from estimates_ai.llm.client_factory import default_client as client

import time

from estimates_ai.schemas.models import Activity, Team

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
                    input="""Data la seguente attività, allocare un team adatto a svolgerla. L'attività è descritta da un nome e una descrizione. Il team allocato deve essere descritto da un nome, una lista di membri e un tipo (ad esempio, "sviluppo", "design", "marketing", "frontend", "backend", ecc.).""",
                    output_cls=Team,
                    system_prompt="""Sei un assistente che aiuta a allocare team per attività specifiche. Riceverai una descrizione dell'attività e dovrai rispondere con un team adatto a svolgerla.""",
                    temperature=0.7
                )

                latency = time.perf_counter() - t0

                prompt_tokens = result.usage.prompt_tokens
                completion_tokens = result.usage.completion_tokens

                TOTAL_PROMPT_TOKENS += prompt_tokens
                TOTAL_COMPLETION_TOKENS += completion_tokens

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

            team = result.structured_data[0]
            return team.model_dump_json(indent=2)
