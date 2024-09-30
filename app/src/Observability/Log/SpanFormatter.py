from opentelemetry import trace
from loki_logger_handler.loki_logger_handler import LoggerFormatter


class SpanFormatter(LoggerFormatter):
    def format(self, record):
        current_span = trace.get_current_span()
        trace_id = current_span.get_span_context().trace_id
        span_id = current_span.get_span_context().span_id

        if trace_id == 0:
            record.trace_id = None
        else:
            record.trace_id = "{trace:032x}".format(trace=trace_id)

        if span_id == 0:
            record.span_id = None
        else:
            record.span_id = "{span:016x}".format(span=span_id)

        return super().format(record)
