from pydantic import BaseModel, Field, field_serializer
import datetime
import src.Omada.helpers.timeFunctions as timeHelpers


status_def = {
    0: "Disconnected",
    1: "Connected",
    2: "Pending",
    3: "Heartbeat Missed",
    4: "Isolated",
}

class Device(BaseModel):

    mac: str
    name: str
    type: str
    model: str
    ip: str
    uptime: datetime.timedelta
    status: str
    lastSeen: datetime.datetime
    cpuUtil: int
    memUtil: int
    tagName: str = Field(default=None)

    def __init__(self, **data):
        
        data["lastSeen"] = timeHelpers.get_last_seen(data["lastSeen"])
        data["status"] = status_def.get(data["status"])
        data["uptime"] = timeHelpers.get_uptime(data["uptime"])
        
        super().__init__(**data)
        
    
    @field_serializer('lastSeen')
    def serialize_lastSeen(self, lastSeen: datetime.datetime, _info) -> str:
        return timeHelpers.datetime_to_string(lastSeen)

    @field_serializer('uptime')
    def serialize_uptime(self, uptime: datetime.timedelta, _info) -> str:
        return timeHelpers.timedelta_to_string(uptime)
