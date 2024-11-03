import os
import logging

from opentelemetry import trace

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter  # noqa

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_tracing():
    # Set up a tracer provider with a resource name for the service
    service_name = os.getenv("SERVICE_NAME", "default-service")
    resource = Resource.create({"service.name": service_name})

    trace.set_tracer_provider(TracerProvider(resource=resource))
    logger.info("Tracer provider set with resource: %s", service_name)

    otlp_exporter = OTLPSpanExporter(
        endpoint="http://tempo:4317", insecure=True)
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    logger.info("OTLP exporter configured to send traces to Tempo")

    DjangoInstrumentor().instrument()
    logger.info("Django instrumentation enabled")

    RequestsInstrumentor().instrument()
    logger.info("Requests instrumentation enabled")

    Psycopg2Instrumentor().instrument()
    logger.info("Psycopg2 instrumentation enabled")
