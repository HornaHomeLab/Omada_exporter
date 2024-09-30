import src.Prometheus as Prometheus
import src.Omada as Omada
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry import trace
from src.Observability.Log.logger import logger

tracer = trace.get_tracer("PrometheusMetricsController-tracer")

class PrometheusMetrics:

    @staticmethod
    @tracer.start_as_current_span("PrometheusMetrics.update")
    def update():
        logger.info("PrometheusMetrics update invoked")
        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))
        
        PrometheusMetrics.__update_switch_metrics()
        PrometheusMetrics.__update_router_metrics()
        PrometheusMetrics.__update_access_point_metrics()
        
        current_span.set_status(status=trace.StatusCode(1))
        return None

    @staticmethod
    @tracer.start_as_current_span("PrometheusMetrics.__update_switch_metrics")
    def __update_switch_metrics():
        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))
        
        try:
            devices = Omada.Controller.Switch.get_info()
            logger.info("Switch data fetched successfully")
        except Exception as e:
            logger.exception(e,exc_info=True)
        
        try:
            ports = Omada.Controller.Switch.get_port_info()
            logger.info("Switch ports data fetched successfully")
        except Exception as e:
            logger.exception(e,exc_info=True)
            
        try:
            Prometheus.Switch.update_metrics(devices, ports)
            logger.info("Switch metrics updated successfully")
        except Exception as e:
            logger.exception(e,exc_info=True)
        
        current_span.set_status(status=trace.StatusCode(1))
        return None

    @staticmethod
    @tracer.start_as_current_span("PrometheusMetrics.__update_router_metrics")
    def __update_router_metrics():
        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))
        
        try:
            devices = Omada.Controller.Router.get_info()
            logger.info("Router data fetched successfully")
        except Exception as e:
            logger.exception(e,exc_info=True)
        
        try:
            ports = Omada.Controller.Router.get_port_info()
            logger.info("Router ports data fetched successfully")
        except Exception as e:
            logger.exception(e,exc_info=True)
        
        try:
            Prometheus.Router.update_metrics(devices, ports)
            logger.info("Router metrics updated successfully")
        except Exception as e:
            logger.exception(e,exc_info=True)
        
        current_span.set_status(status=trace.StatusCode(1))
        return None

    @staticmethod
    @tracer.start_as_current_span("PrometheusMetrics.__update_access_point_metrics")
    def __update_access_point_metrics():
        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))
        
        try:
            devices = Omada.Controller.AccessPoint.get_info()
            logger.info("AccessPoint data fetched successfully")
        except Exception as e:
            logger.exception(e,exc_info=True)
            
        try:
            ports = Omada.Controller.AccessPoint.get_port_info()
            logger.info("AccessPoint port data fetched successfully")
        except Exception as e:
            logger.exception(e,exc_info=True)
        
        try:
            radios = Omada.Controller.AccessPoint.get_radio_info()
            logger.info("AccessPoint radio data fetched successfully")
        except Exception as e:
            logger.exception(e,exc_info=True)
            
        try:
            Prometheus.AccessPoint.update_metrics(devices, ports, radios)
        except Exception as e:
            logger.exception(e,exc_info=True)
        
        current_span.set_status(status=trace.StatusCode(1))
        return None
