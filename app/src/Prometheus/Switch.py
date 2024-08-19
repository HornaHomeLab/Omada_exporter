from prometheus_client import Gauge

import src.Omada as Omada
from src.Omada.Model.Ports import SwitchPort
from src.Prometheus.BaseClient import BaseDeviceMetrics, labels

switch_labels = [
    "name",
    "mac",
    "port",
    "portName",
    "disable",
    "profileName",
    "operation",
    "linkStatus",
    "linkSpeed",
    "duplex",
    "poe",
]


class Switch(BaseDeviceMetrics):
    ports_rx: Gauge = Gauge(
        "switch_port_rx", "Sum of received bytes", switch_labels
    )
    ports_tx: Gauge = Gauge(
        "switch_port_tx", "Sum of transmitted bytes", switch_labels
    )

    @staticmethod
    def update_metrics(switch_metrics: list[Omada.Model.Switch], switch_port_metrics: list[Omada.Model.Ports.SwitchPort]):
        Switch.update_base_metrics(switch_metrics)
        Switch.__update_port_status(switch_port_metrics)

    @staticmethod
    def __update_port_status(switch_port_metrics: list[Omada.Model.Ports.SwitchPort]):
        for port in switch_port_metrics:
            port_labels: dict[str, str] = Switch.__get_port_labels(port)
            (
                Switch
                .ports_rx
                .labels(**(port_labels))
                .set(port.rx)
            )
            (
                Switch
                .ports_tx
                .labels(**(port_labels))
                .set(port.tx)
            )

    @staticmethod
    def __get_port_labels(port: SwitchPort):
        return {
            k: v
            for k, v in port.model_dump().items()
            if k not in ["rx", "tx"]
        }
