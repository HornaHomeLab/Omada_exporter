import logging
from loki_logger_handler.loki_logger_handler import LokiLoggerHandler
from src.Observability.Log.SpanFormatter import SpanFormatter
import src.Config as Config



logger = logging.getLogger("uvicorn")
logger.setLevel(Config.LOG_LEVEL)

if Config.USE_LOKI:
    loki_handler = LokiLoggerHandler(
        url=f"http://{Config.LOKI_IP}:{Config.LOKI_PORT}/loki/api/v1/push",
        labels={
            "service_name": Config.SERVICE_NAME,
            "Environment": Config.ENVIRONMENT
            },
        defaultFormatter=SpanFormatter()
    )
    logger.addHandler(loki_handler)