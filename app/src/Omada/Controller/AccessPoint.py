import datetime
import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices
from src.Observability import *

tracer = trace.get_tracer("AccessPoint-tracer")


class AccessPoint:
    __access_point_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}"
    __access_point_port_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}/wired-uplink"
    __access_point_radio_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}/radios"
    __access_point_radio_stats_path: str = "/api/v2/sites/{siteId}/stat/{apMac}/5min?type=ap"

    @staticmethod
    @tracer.start_as_current_span("AccessPoint.get_info")
    def get_info() -> list[Model.AccessPoint]:

        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))
        logger.info("Getting AccessPoint info", extra={
            "devices": [item.mac for item in Devices.access_points]
        })
        result = [
            Model.AccessPoint(
                **Connection.Request.get(
                    AccessPoint.__access_point_info_path, {
                        "apMac": item.mac
                    }
                )
            )
            for item in Devices.access_points
        ]
        current_span.set_status(status=trace.StatusCode(1))
        return result

    @staticmethod
    @tracer.start_as_current_span("AccessPoint.get_port_info")
    def get_port_info() -> list[Model.Ports.AccessPointPort]:

        access_point_port: list[Model.Ports.AccessPointPort] = []
        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))

        logger.info(
            "Getting AccessPoint port info for {num} APs".format(
                num=len(Devices.access_points)
            ),
            extra={
                "devices": [item.mac for item in Devices.access_points]
            }
        )
        for ap in Devices.access_points:
            ap_port_response: dict = Connection.Request.get(
                AccessPoint.__access_point_port_info_path, {
                    "apMac": ap.mac
                }
            )
            try:
                access_point_port.append(
                    Model.Ports.AccessPointPort(
                        **(
                            {
                                "accessPointName": ap.name,
                                "accessPointMac": ap.mac,
                                **ap_port_response.get("wiredUplink"),
                            }
                        )
                    )
                )
            except Exception as e:
                logger.warning(e, exc_info=True)

        logger.info(
            "Found {num} AccessPoint ports".format(
                num=len(access_point_port)
            ),
            extra={
                "devices": [item.mac for item in Devices.access_points]
            }
        )
        current_span.set_status(status=trace.StatusCode(1))
        return access_point_port

    @staticmethod
    @tracer.start_as_current_span("AccessPoint.get_radio_info")
    def get_radio_info() -> list[Model.Ports.AccessPointRadio]:

        access_point_radio: list[Model.Ports.AccessPointRadio] = []
        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))
        logger.info(
            "Getting AccessPoint radio info for {num} APs".format(
                num=len(Devices.access_points)
            ),
            extra={
                "devices": [item.mac for item in Devices.access_points]
            }
        )

        for ap in Devices.access_points:
            ap_radio_response: dict = Connection.Request.get(
                AccessPoint.__access_point_radio_info_path, {
                    "apMac": ap.mac
                }
            )

            access_point_radio.append(
                Model.Ports.AccessPointRadio(
                    **(
                        {
                            "accessPointName": ap.name,
                            "accessPointMac": ap.mac,
                            **ap_radio_response,
                        }
                    )
                )
            )
        logger.info(
            "Found {num} AccessPoint radios".format(
                num=len(access_point_radio)
            ),
            extra={
                "devices": [item.mac for item in Devices.access_points]
            }
        )
        current_span.set_status(status=trace.StatusCode(1))
        return access_point_radio
