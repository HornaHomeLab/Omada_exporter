from opentelemetry import trace
from loki_logger_handler.loki_logger_handler import LoggerFormatter
from src.Observability.Trace.OpenTelemetry import get_trace_id, get_span_id

class SpanFormatter(LoggerFormatter):
    def format(self, record):
        
        record.trace_id = get_trace_id()
        record.span_id = get_span_id()

        return super().format(record)
