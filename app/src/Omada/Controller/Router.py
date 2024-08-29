import datetime
import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices


class Router:

    __router_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/gateways/{gatewayMac}"
    __switch_port_stats_path: str = "/api/v2/sites/{siteId}/stat/{gatewayMac}/5min?type=gateway"
    __router_port_info_path: str = "/api/v2/sites/{siteId}/gateways/{gatewayMac}"
    @staticmethod
    def get_info() -> list[Model.Router]:

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
        return result

    @staticmethod
    def get_port_info():
        router_port: list[Model.Ports.RouterPort] = []
        router_port_stats: list[Model.Ports.RouterPortStats] = []

        for router in Devices.gateways:
            router_port_response: dict = Connection.Request.get(
                Router.__router_port_info_path, {
                    "gatewayMac": router.mac
                }
            )
            for port in router_port_response.get("portStats"):
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
            router_port_stats = router_port_stats + Router.__get_port_stats(
                router.mac, router.name, len(router_port_response.get("portStats"))
            )
            
                
        return router_port, router_port_stats

    @staticmethod
    def __get_port_stats(router_mac: str, router_name: str, port_count: int):

        router_port_stats: list[Model.Ports.SwitchPortStats] = []

        current_time = int(datetime.datetime.now().timestamp())
        router_port_stats_response: dict = Connection.Request.post(
            Router.__switch_port_stats_path, {
                "gatewayMac": router_mac
            },
            {
                "attrs": [
                    "tx",
                    "rx",
                    "txPkts",
                    "rxPkts"
                ],
                "ports": list(range(1, port_count + 1)),
                "start": current_time - 301,
                "end":   current_time
            }
        )[-1]

        for stats in router_port_stats_response.get("ports"):
            router_port_stats.append(
                Model.Ports.RouterPortStats(
                    **(
                        {
                            **stats,
                            "mac": router_mac,
                            "gatewayName": router_name
                        }
                    )
                )
            )

        return router_port_stats