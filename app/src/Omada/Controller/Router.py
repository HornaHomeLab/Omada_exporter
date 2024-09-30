import datetime
import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry import trace
from src.Observability.Log.logger import logger


tracer = trace.get_tracer("Router-tracer")


class Router:

    __router_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/gateways/{gatewayMac}"
    __router_port_stats_path: str = "/api/v2/sites/{siteId}/stat/{gatewayMac}/5min?type=gateway"
    __router_port_info_path: str = "/api/v2/sites/{siteId}/gateways/{gatewayMac}"

    @staticmethod
    @tracer.start_as_current_span("Router.get_info")
    def get_info() -> list[Model.Router]:
        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))
        logger.info("Getting Router info", extra={
            "devices": [item.mac for item in Devices.gateways]
        })
        result = [
            Model.Router(
                **{
                    "name": item.name,
                    **Connection.Request.get(
                        Router.__router_info_path, {
                            "gatewayMac": item.mac
                        }
                    )
                }
            )
            for item in Devices.gateways
        ]
        current_span.set_status(status=trace.StatusCode(1))
        return result

    @staticmethod
    @tracer.start_as_current_span("Router.get_port_info")
    def get_port_info() -> list[Model.Ports.RouterPort]:

        router_port: list[Model.Ports.RouterPort] = []
        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))

        logger.info(
            "Getting Router port info for {num} Routers".format(
                num=len(Devices.gateways),

            ),
            extra={
                "devices": [item.mac for item in Devices.switches]
            }
        )
        for router in Devices.gateways:
            router_port_response: dict = Connection.Request.get(
                Router.__router_port_info_path, {
                    "gatewayMac": router.mac
                }
            )
            for port in router_port_response.get("portStats"):
                try:
                    router_port.append(
                        Model.Ports.RouterPort(
                            **(
                                {
                                    "gatewayName": router.name,
                                    "mac": router.mac,
                                    **port,
                                }
                            )
                        )
                    )
                except Exception as e:
                    logger.warning(e, exc_info=True)
            # Needed to fix Omada bug, that it records traffic on port with disconnected cable
            port_status = {}
            for port in router_port:
                port_status[port.port] = port.linkSpeed

        logger.info(
            "Found {num} router ports".format(
                num=len(router_port)
            ),
            extra={
                "devices": [item.mac for item in Devices.switches]
            }
        )
        current_span.set_status(status=trace.StatusCode(1))
        return router_port
