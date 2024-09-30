import datetime
import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry import trace
from src.Observability.Log.logger import logger

tracer = trace.get_tracer("Switch-tracer")


class Switch:

    __switch_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/switches/{switchMac}"
    __switch_port_stats_path: str = "/api/v2/sites/{siteId}/stat/switches/{switchMac}/5min"
    __switch_port_info_path: str = "/api/v2/sites/{siteId}/switches/{switchMac}/ports"

    @staticmethod
    @tracer.start_as_current_span("Switch.get_info")
    def get_info() -> list[Model.Switch]:

        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))
        logger.info("Getting Switch info", extra={
            "devices": [item.mac for item in Devices.switches]
        })
        result = [
            Model.Switch(
                **{
                    "name": item.name,
                    **Connection.Request.get(
                        Switch.__switch_info_path, {
                            "switchMac": item.mac
                        }
                    )
                }
            )
            for item in Devices.switches
        ]
        current_span.set_status(status=trace.StatusCode(1))
        return result

    @staticmethod
    @tracer.start_as_current_span("Switch.get_port_info")
    def get_port_info() -> list[Model.Ports.SwitchPort]:

        switch_port: list[Model.Ports.SwitchPort] = []
        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))

        logger.info(
            "Getting Switch port info for {num} Switches".format(
                num=len(Devices.switches)
            ),
            extra={
                "devices": [item.mac for item in Devices.switches]
            }
        )

        for switch in Devices.switches:
            switch_port_response: dict = Connection.Request.get(
                Switch.__switch_port_info_path, {
                    "switchMac": switch.mac
                }
            )

            for port in switch_port_response:
                try:
                    switch_port.append(
                        Model.Ports.SwitchPort(
                            **(
                                {
                                    **Switch.__get_port_detail(port),
                                    "switchName": switch.name
                                }
                            )
                        )
                    )
                except Exception as e:
                    logger.warning(e, exc_info=True)

        logger.info(
            "Found {num} switch ports".format(
                num=len(switch_port)
            ),
            extra={
                "devices": [item.mac for item in Devices.switches]
            }
        )
        current_span.set_status(status=trace.StatusCode(1))
        return switch_port

    @staticmethod
    def __get_port_detail(port: dict):
        '''
        Put contents of port status to depth level 0 in JSON struct.
        Convert this:
            {
                "port": 1,
                "profileName": "All",
                "portStatus": {
                    "port": 1,
                    "linkStatus": 1,
                    "linkSpeed": 2,
                    "duplex": 2,
                    "poe": false,
                    "tx": 16826893482,
                    "rx": 488690848,
                    "stpDiscarding": false
                }
            }

        To this:
            {
                "port": 1,
                "profileName": "All",
                "linkStatus": 1,
                "linkSpeed": 2,
                "duplex": 2,
                "poe": false,
                "tx": 16826893482,
                "rx": 488690848,
                "stpDiscarding": false
            }
        '''
        port_status: dict = port["portStatus"]
        return {
            **port,
            **({k: v for k, v in port_status.items()})
        }
