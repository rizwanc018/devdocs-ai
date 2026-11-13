import os

from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor


def setup_tracing():
    endpoint = os.getenv(
        "PHOENIX_COLLECTOR_ENDPOINT",
        "http://localhost:6006/v1/traces",
    )

    resource = Resource.create(
        {
            "service.name": "devdocs-ai",
        }
    )

    tracer_provider = TracerProvider(
        resource=resource,
    )

    exporter = OTLPSpanExporter(
        endpoint=endpoint,
    )

    span_processor = SimpleSpanProcessor(
        exporter,
    )

    tracer_provider.add_span_processor(
        span_processor,
    )

    trace.set_tracer_provider(
        tracer_provider,
    )

    OpenAIInstrumentor().instrument(
        tracer_provider=tracer_provider,
    )

    return tracer_provider
