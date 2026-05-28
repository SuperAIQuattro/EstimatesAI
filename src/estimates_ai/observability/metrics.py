from typing import Dict

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME as OTEL_SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from prometheus_client import Counter, Histogram, start_http_server

SERVICE_NAME = "aitho-llm-monitor"
SERVICE_VERSION = "1.0.0"
DEPLOYMENT_ENVIRONMENT = "stime-lab"
TEMPO_ENDPOINT = "http://localhost:4317"
METRICS_PORT = 8000


def _ensure_tracer_provider() -> None:
    resource = Resource.create({
        OTEL_SERVICE_NAME: SERVICE_NAME,
        "service.version": SERVICE_VERSION,
        "deployment.environment": DEPLOYMENT_ENVIRONMENT,
    })

    exporter = OTLPSpanExporter(endpoint=TEMPO_ENDPOINT, insecure=True)
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)


def _start_prometheus_server() -> None:
    try:
        start_http_server(METRICS_PORT, addr="0.0.0.0")
    except OSError:
        pass


def build_llm_metrics() -> Dict[str, object]:
    return {
        "llm_requests": Counter(
            "llm_requests_total",
            "Numero totale di chiamate LLM",
            ["model", "status"],
        ),
        "llm_prompt_tokens": Counter(
            "llm_prompt_tokens_total",
            "Token prompt consumati",
            ["model"],
        ),
        "llm_completion_tokens": Counter(
            "llm_completion_tokens_total",
            "Token completion generati",
            ["model"],
        ),
        "llm_latency": Histogram(
            "llm_latency_seconds",
            "Latenza delle chiamate LLM in secondi",
            ["model"],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
        ),
        "llm_errors": Counter(
            "llm_errors_total",
            "Errori nelle chiamate LLM",
            ["model", "error_type"],
        ),
    }


def initialize_observability() -> Dict[str, object]:
    _ensure_tracer_provider()
    _start_prometheus_server()
    return build_llm_metrics()
