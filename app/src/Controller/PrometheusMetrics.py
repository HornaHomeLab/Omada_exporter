import src.Prometheus as Prometheus
import src.Omada as Omada

class PrometheusMetrics:
    
    
    @staticmethod
    def update_switch_metrics():
        devices = Omada.Controller.Switch.get_info()
        ports = Omada.Controller.Switch.get_port_info()
        
        Prometheus.Switch.update_metrics(devices, ports)
        
        
    @staticmethod
    def update_router_metrics():
        devices = Omada.Controller.Router.get_info()
        ports = Omada.Controller.Router.get_port_info()
        Prometheus.Router.update_metrics(devices, ports)
        
    @staticmethod
    def update_access_point_metrics():
        devices = Omada.Controller.AccessPoint.get_info()
        Prometheus.AccessPoint.update_metrics(devices)