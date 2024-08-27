import src.Omada as Omada
from prometheus_client import Gauge, Info
import src.Omada.Model.Ports as Ports

device_identity_labels = [
    "deviceType", 
    "name", 
    "mac"
]
device_info = [
    "ip", 
    "model", 
    "firmwareVersion"
]


class BaseDeviceMetrics:
    cpu_usage: Gauge = Gauge("cpu_usage", "CPU usage in %", device_identity_labels)
    memory_usage: Gauge = Gauge("memory_usage", "Memory usage in %", device_identity_labels)
    
    info: Info = Info(
        "device", "Device information", device_identity_labels
    )

    @staticmethod
    def update_base_metrics(
            metrics: list[
                Omada.Model.Switch |
                Omada.Model.AccessPoint |
                Omada.Model.Router
            ]
    ):
        for device in metrics:
            device_labels = BaseDeviceMetrics.get_labels(device,device_identity_labels)
            
            BaseDeviceMetrics.cpu_usage.labels(**device_labels).set(device.cpuUtil)            
            BaseDeviceMetrics.memory_usage.labels(**device_labels).set(device.memUtil)
            BaseDeviceMetrics.info.labels(**device_labels).info(
                BaseDeviceMetrics.get_labels(device,device_info)
            )
            
            

    @staticmethod
    def __get_values_for_labels(model: Omada.Model.Switch | Omada.Model.AccessPoint | Omada.Model.Router):
        result = {}
        model_dump: dict[str, any] = model.model_dump()
        for label in labels:
            result[label] = model_dump.get(label)

        return result

    @staticmethod
    def get_labels(
            port: Ports.RouterPort | Ports.SwitchPort, label_names: list[str] = [], include_all: bool = False
    ):
        if include_all:
            return{
                k: v
                for k, v in port.model_dump().items()
                if k not in ["rx", "tx"]
            }
        return {
            k: v
            for k, v in port.model_dump().items()
            if k in label_names
        }
