import time

from datapizza.tools import tool
from datapizza.tracing import ContextTracing
from estimates_ai.observability.tracing import set_attributes_and_status, set_exception, tracer
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

                set_attributes_and_status(span, result, latency, prompt_tokens, completion_tokens)

            except Exception as e:
                latency = time.perf_counter() - t0
                set_exception(span, e, latency)
                raise

            analisi = result.structured_data[0]
            try:
                import streamlit as st
                st.session_state["overall_risk"] = analisi.overall_risk_assessment
            except Exception:
                pass
            return analisi.model_dump_json(indent=2)
