import time

from datapizza.tools import tool
from datapizza.tracing import ContextTracing
from opentelemetry.trace import StatusCode
from estimates_ai.observability.tracing import tracer
from estimates_ai.llm.client_factory import default_client as client
from estimates_ai.schemas.risk_analysis import RiskFactorStructuredResponse



RISK_ANALYSIS_SYSTEM_PROMPT = """You are a project risk analyst.
Given a project description, identify the main risks, assess their likelihood and impact (low/medium/high), and propose a mitigation strategy for each.
Be concise and focus only on risks relevant to the project scope, team, and timeline."""


@tool
def risk_analysis(query: str) -> str:
    """Risk Analysis: Identifies and assesses project risks."""
    t0 = time.perf_counter()

    print("Analyzing project risks")
    with ContextTracing().trace("risk_analysis"):
        with tracer.start_as_current_span("risk_analysis") as span:
            try:
                result = client.structured_response(
                    input=query,
                    output_cls=RiskFactorStructuredResponse,
                    system_prompt=RISK_ANALYSIS_SYSTEM_PROMPT,
                    temperature=0.3,
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

            analisi = result.structured_data[0]
            return analisi.model_dump_json(indent=2)
