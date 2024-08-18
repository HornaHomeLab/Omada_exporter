from prometheus_client import Info

import src.Omada as Omada
from src.Omada.Model.subModels.SwitchPort import SwitchPort
from src.Prometheus.BaseClient import BaseDeviceMetrics, labels

switch_labels = labels + [
    "profileName",
    "port",
    "port_name",
    "lagPort",
]


class Switch(BaseDeviceMetrics):
    ports: Info = Info("switch_port_status", "Status of the switch port",
                       switch_labels)

    @staticmethod
    def update_metrics(metrics: list[Omada.Model.Switch]):
        Switch.update_base_metrics(metrics)
        Switch.__update_port_status(metrics)

    @staticmethod
    def __update_port_status(metrics: list[Omada.Model.Switch]):
        for device in metrics:
            for port in device.portList:
                port_labels = Switch.__get_port_labels(port, device)
                Switch.ports.labels(
                    **port_labels
                ).info({"state": port.status})

    @staticmethod
    def __get_port_labels(port: SwitchPort, device: Omada.Model.Switch):
        result = {}
        port_model_dump: dict[str, any] = port.model_dump()
        device_model_dump: dict[str, any] = device.model_dump()
        
        for label in switch_labels:
            result[label] = port_model_dump.get(label,device_model_dump.get(label))
            
        return result
