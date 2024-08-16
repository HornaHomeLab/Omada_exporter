from pydantic import BaseModel, Field, field_serializer
import src.Omada.helpers.modelFields as modelFields

from src.Omada.Model.subModels.WanPortIpv4Config import WanPortIpv4Config
from src.Omada.Model.subModels.WanPortIpv6Config import WanPortIpv6Config


value_map: dict[str, dict] = {
    "status": {
        0: "disconnected",
        1: "connected",
    },
    "internetState": {
        0: "disconnected",
        1: "connected",
    },
    "onlineDetection": {
        0:"offline",
        1:"online",
    }
}

class WanConnection(BaseModel):
    port: int
    name: str
    portDesc: str
    status: str 
    internetState: str
    wanPortIpv6Config: WanPortIpv6Config = Field(default=None)
    wanPortIpv4Config: WanPortIpv4Config = Field(default=None)
    rxRate: int
    txRate: int
    latency: int
    loss: float
    onlineDetection: str
    
    def __init__(self, **data):
        data = modelFields.map_data_values(data, value_map)
        super().__init__(**data)