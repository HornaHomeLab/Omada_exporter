from prometheus_client import Gauge

import src.Omada as Omada
from src.Prometheus.BaseClient import BaseDeviceMetrics, labels

router_labels = [
    "name",
    "mac",
    "port",
    "portName",
    "portDesc",
    "mode",
    "ip",
    "poe",
    "linkStatus",
    "internetState",
    "online",
    "linkSpeed",
    "duplex",
    "protocol",
    "wanPortIpv6Config",
    "wanPortIpv4Config",
    "latency",
    "loss",
]


class Router(BaseDeviceMetrics):
    ports_rx: Gauge = Gauge(
        "router_port_rx", "Sum of received bytes", router_labels
    )
    ports_tx: Gauge = Gauge(
        "router_port_tx", "Sum of transmitted bytes", router_labels
    )

    @staticmethod
    def update_metrics(router_metrics: list[Omada.Model.Router], router_port_metrics: list[Omada.Model.Ports.RouterPort]):
        Router.update_base_metrics(router_metrics)
        Router.__update_port_status(router_port_metrics)

    @staticmethod
    def __update_port_status(port_metrics: list[Omada.Model.Ports.RouterPort]):
        for port in port_metrics:
            port_labels = Router.get_port_labels(port)
            (
                Router
                .ports_rx
                .labels(**port_labels)
                .set(port.rx)
            )
            (
                Router
                .ports_tx
                .labels(**port_labels)
                .set(port.tx)
            )
