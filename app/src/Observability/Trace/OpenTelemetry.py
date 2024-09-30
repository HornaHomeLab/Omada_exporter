from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import Compression
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import src.Config as Config


# OpenTelemetry
trace_resource = Resource.create(
    attributes={
        SERVICE_NAME: Config.SERVICE_NAME
    }
)
trace.set_tracer_provider(TracerProvider(resource=trace_resource))

# OTLP Exporter
if Config.USE_TEMPO:
    otlp_exporter: OTLPSpanExporter = OTLPSpanExporter(
        endpoint=f"http://{Config.TEMPO_IP}:{Config.TEMPO_PORT}",
        insecure="true"
    )
    span_processor: BatchSpanProcessor = BatchSpanProcessor(otlp_exporter)
    tracer_provider: TracerProvider = trace.get_tracer_provider()
    tracer_provider.add_span_processor(span_processor)
