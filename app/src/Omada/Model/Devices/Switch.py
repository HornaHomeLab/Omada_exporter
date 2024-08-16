from pydantic import BaseModel, Field, field_serializer
import datetime
import src.Omada.helpers.timeFunctions as timeHelpers

from src.Omada.Model.subModels.SwitchPort import SwitchPort

class Switch(BaseModel):
    mac: str
    ip: str
    ipv6List: list[str]
    model: str
    firmwareVersion: str
    version: str
    hwVersion: str
    cpuUtil: int
    memUtil: int
    uptime: datetime.timedelta
    portList: list[SwitchPort]
    
    def __init__(self, **data):
        
        data["uptime"] = timeHelpers.get_uptime(data["uptime"])
        
        super().__init__(**data)

    @field_serializer('uptime')
    def serialize_uptime(self, uptime: datetime.timedelta, _info) -> str:
        return timeHelpers.timedelta_to_string(uptime)