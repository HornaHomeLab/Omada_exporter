from pydantic import BaseModel, Field, field_serializer


from src.Omada.Model.subModels.ApWirelessUpLink import ApWirelessUpLink

class AccessPoint(BaseModel):
    type: str
    mac: str
    name: str
    ip: str
    ipv6List: list[str] = Field(default=None)
    wlanId: str
    wireless_uplink_info: list[ApWirelessUpLink] = Field(default=None)
    model: str = Field(default=None)
    firmwareVersion: str
    cpuUtil: int
    memUtil: int
    uptimeLong: int