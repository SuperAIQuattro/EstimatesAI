from opentelemetry import trace
from opentelemetry.trace import StatusCode

tracer = trace.get_tracer("estimates-ai")


def _resolve_value(source, *path, default=None):
    value = source
    for element in path:
        if value is None:
            return default

        if isinstance(value, dict):
            value = value.get(element, default)
        else:
            value = getattr(value, element, default)

    return value


def set_attributes_and_status(
        span: trace.Span,
        ai_result,
        latency: float,
        prompt_tokens: int = None,
        completion_tokens: int = None
    ):
    """
    Helper function to set common attributes and status for a span based on the LLM result and latency.

    Args:
        span: The OpenTelemetry span to set attributes on.
        ai_result: The result object returned by the LLM client, which includes usage information and the generated text.
        latency: The latency of the LLM call in seconds.
    """
    if prompt_tokens is None:
        prompt_tokens = _resolve_value(ai_result, "usage", "prompt_tokens")

    if completion_tokens is None:
        completion_tokens = _resolve_value(ai_result, "usage", "completion_tokens")

    text = _resolve_value(ai_result, "text")

    span.set_attribute("llm.prompt_tokens", prompt_tokens)
    span.set_attribute("llm.completion_tokens", completion_tokens)
    span.set_attribute("llm.latency_ms", round(latency * 1000, 1))
    span.set_attribute("result", text)
    span.set_status(StatusCode.OK)

def set_exception(span: trace.Span, exception: Exception, latency: float):
    """
    Helper function to record an exception and set the span status to ERROR.

    Args:
        span: The OpenTelemetry span to record the exception on.
        exception: The exception that was raised.
        latency: The latency of the operation in seconds before the exception was raised.
    """
    print(f"❌ ERROR: {exception}")
    span.record_exception(exception)
    span.set_status(StatusCode.ERROR, str(exception))
