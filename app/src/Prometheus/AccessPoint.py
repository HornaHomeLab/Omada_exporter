import src.Omada.Model as Model

from src.Prometheus.BaseClient import BaseDeviceMetrics


class AccessPoint(BaseDeviceMetrics):
    __device_type_name: str = "AccessPoint"

    @staticmethod
    def update_metrics(ap_metrics: list[Model.AccessPoint]):
        AccessPoint.update_base_metrics(ap_metrics)

    @staticmethod
    def __update_cpu(ap_metrics: list[Model.AccessPoint]):

        for access_point in ap_metrics:
            AccessPoint.cpu_usage.labels(
                device_type=AccessPoint.__device_type_name,
                name=access_point.name
            ).set(access_point.cpuUtil)
