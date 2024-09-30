from opentelemetry import trace
from loki_logger_handler.loki_logger_handler import LoggerFormatter


class SpanFormatter(LoggerFormatter):
    def format(self, record):
        trace_id = trace.get_current_span().get_span_context().trace_id
        if trace_id == 0:
            record.trace_id = None
        else:
            record.trace_id = "{trace:32x}".format(trace=trace_id)
        return super().format(record)
