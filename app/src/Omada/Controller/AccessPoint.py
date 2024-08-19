import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices

class AccessPoint:
    __access_point_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}"

    @staticmethod
    def get_info() -> list[Model.AccessPoint]:

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
        return result
