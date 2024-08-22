from prometheus_client import Gauge

import src.Omada as Omada
from src.Prometheus.BaseClient import BaseDeviceMetrics, labels

access_point_port_labels = [
    "name",
    "mac",
    "uplinkMac",
    "uplinkDeviceType",
    "linkSpeed",
    "duplex",
]
access_point_radio_traffic_labels = [
    "name",
    "mac",
    "frequency",
]
access_point_radio_util_labels =[
    "name",
    "mac",
    "frequency",
    "actualChannel",
    "maxTxRate",
    "region",
    "bandWidth",
    "mode",
]

class AccessPoint(BaseDeviceMetrics):
    port_rx: Gauge = Gauge(
        "access_point_port_rx", "Sum of received bytes", access_point_port_labels
    )
    port_tx: Gauge = Gauge(
        "access_point_port_tx", "Sum of transmitted bytes", access_point_port_labels
    )
    radio_rx: Gauge = Gauge(
        "radio_rx", "Sum of received bytes", access_point_radio_traffic_labels
    )
    radio_tx: Gauge = Gauge(
        "radio_tx", "Sum of transmitted bytes", access_point_radio_traffic_labels
    )
    radio_rx_util: Gauge = Gauge(
        "radio_rx_util", "Percentage of receive channel bandwidth usage", access_point_radio_util_labels
    )
    radio_tx_util: Gauge = Gauge(
        "radio_tx_util", "Percentage of transmit channel bandwidth usage", access_point_radio_util_labels
    )
    radio_rx_pkts: Gauge = Gauge(
        "radio_rx_pkts", "Sum of received packets", access_point_radio_traffic_labels
    )
    radio_tx_pkts: Gauge = Gauge(
        "radio_tx_pkts", "Sum of transmitted packets", access_point_radio_traffic_labels
    )
    radio_rx_pkts_dropped: Gauge = Gauge(
        "radio_rx_pkts_dropped", "Sum of dropped rx packets", access_point_radio_traffic_labels
    )
    radio_tx_pkts_dropped: Gauge = Gauge(
        "radio_tx_pkts_dropped", "Sum of dropped tx packets", access_point_radio_traffic_labels
    )
    radio_rx_pkts_error: Gauge = Gauge(
        "radio_rx_pkts_error", "Sum of error rx packets", access_point_radio_traffic_labels
    )
    radio_tx_pkts_error: Gauge = Gauge(
        "radio_tx_pkts_error", "Sum of error tx packets", access_point_radio_traffic_labels
    )
    radio_rx_pkts_retry: Gauge = Gauge(
        "radio_rx_pkts_retry", "Sum of retry rx packets", access_point_radio_traffic_labels
    )
    radio_tx_pkts_retry: Gauge = Gauge(
        "radio_tx_pkts_retry", "Sum of retry tx packets", access_point_radio_traffic_labels
    )

    @staticmethod
    def update_metrics(
        access_point_metrics: list[Omada.Model.AccessPoint],
        access_point_port_metrics: list[Omada.Model.Ports.AccessPointPort],
        access_point_radio_metrics: list[Omada.Model.Ports.AccessPointRadio]
    ):
        AccessPoint.update_base_metrics(access_point_metrics)
        AccessPoint.__update_port_status(access_point_port_metrics)
        AccessPoint.__update_radio_traffic_stats(access_point_radio_metrics)

    @staticmethod
    def __update_port_status(port_metrics: list[Omada.Model.Ports.AccessPointPort]):
        for port in port_metrics:
            port_labels = AccessPoint.get_port_labels(port)
            (
                AccessPoint
                .port_rx
                .labels(**port_labels)
                .set(port.rx)
            )
            (
                AccessPoint
                .port_tx
                .labels(**port_labels)
                .set(port.tx)
            )

    @staticmethod
    def __update_radio_traffic_stats(radio_metrics: list[Omada.Model.Ports.AccessPointRadio]):
        for device in radio_metrics:
            for field_name, value in device:
                if field_name in ["radioConfig24GHz","radioConfig50GHz"]:
                    radio_config_labels = AccessPoint.__get_radio_labels(value)
                    (
                        AccessPoint
                        .radio_rx_util
                        .labels(**radio_config_labels)
                        .set(value.rxUtil)
                    )
                    (
                        AccessPoint
                        .radio_tx_util
                        .labels(**radio_config_labels)
                        .set(value.txUtil)
                    )
                
                if field_name in ["radioTraffic24GHz","radioTraffic50GHz"]:
                    radio_traffic_labels = AccessPoint.__get_radio_labels(value)
                    (
                        AccessPoint
                        .radio_rx
                        .labels(**radio_traffic_labels)
                        .set(value.rx)
                    )
                    (
                        AccessPoint
                        .radio_tx
                        .labels(**radio_traffic_labels)
                        .set(value.tx)
                    )
                    (
                        AccessPoint
                        .radio_rx_pkts
                        .labels(**radio_traffic_labels)
                        .set(value.rxPkts)
                    )
                    (
                        AccessPoint
                        .radio_tx_pkts
                        .labels(**radio_traffic_labels)
                        .set(value.txPkts)
                    )
                    (
                        AccessPoint
                        .radio_rx_pkts_dropped
                        .labels(**radio_traffic_labels)
                        .set(value.rxDropPkts)
                    )
                    (
                        AccessPoint
                        .radio_tx_pkts_dropped
                        .labels(**radio_traffic_labels)
                        .set(value.txDropPkts)
                    )
                    (
                        AccessPoint
                        .radio_rx_pkts_error
                        .labels(**radio_traffic_labels)
                        .set(value.rxErrPkts)
                    )
                    (
                        AccessPoint
                        .radio_tx_pkts_error
                        .labels(**radio_traffic_labels)
                        .set(value.txErrPkts)
                    )
                    (
                        AccessPoint
                        .radio_rx_pkts_retry
                        .labels(**radio_traffic_labels)
                        .set(value.rxRetryPkts)
                    )
                    (
                        AccessPoint
                        .radio_tx_pkts_retry
                        .labels(**radio_traffic_labels)
                        .set(value.txRetryPkts)
                    )
            
    @staticmethod
    def __get_radio_labels(radio: Omada.Model.Ports.AccessPointRadio):
        return {
            k: v
            for k, v in radio.model_dump().items()
            if ("rx" not in k) and ("tx" not in k) and k != "interUtil"
        }