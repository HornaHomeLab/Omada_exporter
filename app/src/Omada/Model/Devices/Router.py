from pydantic import BaseModel, Field, field_serializer
import datetime
import src.Omada.helpers.timeFunctions as timeHelpers

from src.Omada.Model.subModels.RouterPort import RouterPort

class Router(BaseModel):
    mac: str 
    showModel: str
    firmwareVersion: str
    ip: str
    uptime: datetime.timedelta
    temp: int
    cpuUtil: int
    memUtil: int
    ipv6List: list[str] = Field(default=None)
    lastSeen: datetime.datetime
    portConfigs: list[RouterPort]
    
    
    def __init__(self, **data):
        
        data["lastSeen"] = timeHelpers.get_last_seen(data["lastSeen"])
        data["uptime"] = timeHelpers.get_uptime(data["uptime"])
        
        super().__init__(**data)
    
    @field_serializer('lastSeen')
    def serialize_lastSeen(self, lastSeen: datetime.datetime, _info) -> str:
        return timeHelpers.datetime_to_string(lastSeen)

    @field_serializer('uptime')
    def serialize_uptime(self, uptime: datetime.timedelta, _info) -> str:
        return timeHelpers.timedelta_to_string(uptime)