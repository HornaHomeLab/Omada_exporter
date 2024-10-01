import src.Omada.Controller as Controller
import src.Model as Model
from src.Observability import *

tracer = trace.get_tracer("HealthCheckController-tracer")


class HealthCheck:

    @staticmethod
    @tracer.start_as_current_span("HealthCheck.get_status")
    def get_status() -> Model.HealthCheck:
        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))

        try:
            result = Controller.HealthCheck.get()
        except Exception as e:
            logger.exception(e, exc_info=True)

        current_span.set_status(status=trace.StatusCode(1))
        return Model.HealthCheck(
            **result
        )
