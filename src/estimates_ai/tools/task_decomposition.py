from datapizza.tools import tool
from datapizza.tracing import ContextTracing
from opentelemetry.trace import StatusCode
from estimates_ai.observability.tracing import set_attributes_and_status, set_exception
from estimates_ai.observability.tracing import tracer
from estimates_ai.llm.client_factory import default_client as client

from estimates_ai.schemas.task_decomposition import ProjectIdea, ActivityList

import time

@tool
def task_decomposition(idea: ProjectIdea) -> ActivityList:
    """
    Decomposes a project idea into smaller tasks.

    Args:
        idea (ProjectIdea): The project idea to decompose into activities.

    Returns:
        ActivityList: A list of decomposed activities, each including its name and description.
    """
    t0 = time.perf_counter()

    print(f"Decomposing the project idea...")
    with ContextTracing().trace(tracer, "task_decomposition"):
        with tracer.start_as_current_span("task_decomposition") as span:
            try:
                result = client.structured_response(
                    input=f"""
                    Data la seguente idea di progetto, decomporla in attività più piccole.
                    L'idea di progetto è descritta da una breve descrizione. Ogni attività deve essere descritta da un nome e una descrizione.

                    Di seguito l'idea di progetto da decomporre in attività:
                    {idea.description}
                    """,
                    output_cls=ActivityList,
                    system_prompt=f"""
                    Sei un assistente che aiuta a decomporre idee di progetto in attività specifiche.
                    Riceverai una descrizione dell'idea di progetto e dovrai rispondere con una lista di attività adatte a realizzarla.
                    Ogni attività deve essere descritta da un nome e una descrizione.
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

            activity_list = result.structured_data[0]
            return activity_list.model_dump_json(indent=2)
