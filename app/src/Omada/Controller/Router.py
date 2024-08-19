import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices

class Router:

    __router_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/gateways/{gatewayMac}"

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
