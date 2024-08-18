from prometheus_client import Info

import src.Omada as Omada
from src.Omada.Model.subModels.RouterPort import RouterPort
from src.Prometheus.BaseClient import BaseDeviceMetrics, labels

router_labels = labels + [
    "port",
    "duplex",
    "mirrorEnable",
    "mirroredPorts",
    "mirrorMode",
    "pvid",
]


class Router(BaseDeviceMetrics):
    ports: Info = Info("router_port_status", "Status of the router port",
                       router_labels)

    @staticmethod
    def update_metrics(metrics: list[Omada.Model.Router]):
        Router.update_base_metrics(metrics)
        Router.__update_port_status(metrics)

    @staticmethod
    def __update_port_status(metrics: list[Omada.Model.Router]):
        for device in metrics:
            for port in device.portConfigs:
                port_labels = Router.__get_port_labels(port, device)
                Router.ports.labels(
                    **port_labels
                ).info({"linkSpeed": port.linkSpeed})

    @staticmethod
    def __get_port_labels(port: RouterPort, device: Omada.Model.Switch):
        result = {}
        port_model_dump: dict[str, any] = port.model_dump()
        device_model_dump: dict[str, any] = device.model_dump()
        
        for label in router_labels:
            result[label] = port_model_dump.get(label,device_model_dump.get(label))
            
        return result
