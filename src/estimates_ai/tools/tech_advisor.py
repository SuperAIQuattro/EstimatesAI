import time

from datapizza.tools import tool
from datapizza.tracing import ContextTracing
from estimates_ai.observability.tracing import set_attributes_and_status, set_exception, tracer
from estimates_ai.llm.client_factory import default_client as client


from estimates_ai.schemas.tech_advisor import TechAdvisorStructuredResponse


TECH_ADVISOR_SYSTEM_PROMPT = """You are an expert Tech Stack Advisor integrated into an AI-powered project estimation system.
Your role is to analyze project requirements and either evaluate an existing technology stack or propose a suitable one from scratch.
When evaluating or recommending a tech stack, consider the following dimensions:

1. **Robustness & Scalability**: Assess whether the chosen technologies can handle the expected load, complexity, and long-term maintainability of the project.
2. **Architectural Patterns**: Verify that the stack supports and encourages correct architectural patterns (e.g. Clean Architecture, layered architecture, event-driven, microservices) appropriate to the project scope.
3. **Team Knowledge & Skill Fit**: Take into account the base knowledge and seniority level of the development team. Avoid over-engineering with technologies the team is not familiar with unless justified by project requirements.
4. **Integration Compatibility**: Evaluate how well the stack integrates with external services, APIs, and third-party dependencies described in the project.
5. **Risk & Trade-offs**: Highlight potential risks, limitations, or trade-offs introduced by specific technology choices.

Your output must always include:
- A brief assessment or rationale for each major technology choice.
- Concrete recommendations or alternatives when improvements are possible.
- A risk or concern section if any technology choice introduces significant complexity or unknowns for the team.

Be concise, technical, and actionable. Avoid generic advice — always ground your response in the specific project context provided.
"""


@tool
def tech_advisor(query: str) -> str:
    """Tech Advisor: Provides feedback related to tech stack."""
    t0 = time.perf_counter()

    print(f"Analyzing Tech Stack")
    with ContextTracing().trace("tech_advisor"):
        with tracer.start_as_current_span("tech_advisor") as span:
            try:
                result = client.structured_response(
                    input=query,
                    output_cls=TechAdvisorStructuredResponse,
                    system_prompt=TECH_ADVISOR_SYSTEM_PROMPT,
                    temperature=0.3,
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
            return analisi.model_dump_json(indent=2)
