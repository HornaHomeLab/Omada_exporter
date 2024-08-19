import src.Omada as Omada
from prometheus_client import Gauge
import src.Omada.Model.Ports as Ports

labels = ["deviceType", "name", "mac", "ip", "model", "firmwareVersion"]


class BaseDeviceMetrics:
    cpu_usage: Gauge = Gauge("cpu_usage", "CPU usage in %", labels)
    memory_usage: Gauge = Gauge("memory_usage", "Memory usage in %", labels)

    @staticmethod
    def update_base_metrics(
            metrics: list[
                Omada.Model.Switch |
                Omada.Model.AccessPoint |
                Omada.Model.Router
            ]
    ):
        for device in metrics:
            device_labels = BaseDeviceMetrics.__get_values_for_labels(device)
            (
                BaseDeviceMetrics
                .cpu_usage
                .labels(**device_labels)
                .set(device.cpuUtil)
            )
            (
                BaseDeviceMetrics
                .memory_usage
                .labels(**device_labels)
                .set(device.memUtil)
            )

    @staticmethod
    def __get_values_for_labels(model: Omada.Model.Switch | Omada.Model.AccessPoint | Omada.Model.Router):
        result = {}
        model_dump: dict[str, any] = model.model_dump()
        for label in labels:
            result[label] = model_dump.get(label)

        return result
    
    @staticmethod
    def get_port_labels(port: Ports.RouterPort | Ports.SwitchPort):
        return {
            k: v
            for k, v in port.model_dump().items()
            if k not in ["rx", "tx"]
        }
