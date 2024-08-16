import src.Omada as Omada


class Devices:
    gateways: list[Omada.Model.Device]
    switches: list[Omada.Model.Device]
    access_points: list[Omada.Model.Device]

    __device_list_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/devices"

    @staticmethod
    def init() -> None:
        Devices.get_list()

    @staticmethod
    def get_list() -> Omada.Model.Device:
        response: dict = Omada.Request.get(Devices.__device_list_path)
        devices: list[Omada.Model.Device] = [
            Omada.Model.Device(**item)
            for item in response
        ]
        Devices.__update_device_cache(devices)

        return devices

    @staticmethod
    def __update_device_cache(devices: list[Omada.Model.Device]):
        Devices.gateways = [item for item in devices if item.type == "gateway"]
        Devices.switches = [item for item in devices if item.type == "switch"]
        Devices.access_points = [item for item in devices if item.type == "ap"]

    class Router:

        __router_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/gateways/{gatewayMac}"

        @staticmethod
        def get_info() -> list[Omada.Model.Router]:

            return [
                Omada.Model.Router(
                    **Omada.Request.get(
                        Devices.Router.__router_info_path, {
                            "gatewayMac": item.mac
                        }
                    )
                )
                for item in Devices.gateways
            ]

    class Switch:

        __switch_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/switches/{switchMac}"

        @staticmethod
        def get_info() -> list[Omada.Model.Router]:

            return [
                Omada.Model.Switch(
                    **Omada.Request.get(
                        Devices.Switch.__switch_info_path, {
                            "switchMac": item.mac
                        }
                    )
                )
                for item in Devices.switches
            ]

    class AccessPoint:
        __access_point_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}"
        
        @staticmethod
        def get_info() -> list[Omada.Model.AccessPoint]:

            return [
                Omada.Model.AccessPoint(
                    **Omada.Request.get(
                        Devices.AccessPoint.__access_point_info_path, {
                            "apMac": item.mac
                        }
                    )
                )
                for item in Devices.access_points
            ]


Devices.init()
