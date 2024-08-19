import src.Omada as Omada

class WanConnection:

    __wan_status_path = "/openapi/v1/{omadacId}/sites/{siteId}/gateways/{gatewayMac}/wan-status"

    @staticmethod
    def get_status() -> list[Omada.Model.WanConnection]:

        result = []

        for router in Devices.get_router_mac():
            result += [
                Omada.Model.WanConnection(**port)
                for port in Omada.Request.get(
                    WanConnection.__wan_status_path, {
                        "gatewayMac": router
                    }
                )
            ]

        return result