from pydantic import BaseModel, Field

class WanPortIpv4Config(BaseModel):
    ip: str
    ip2: str = Field(default=None)
    gateway: str
    gateway2: str
    priDns: str
    sndDns: str
    priDns2: str
    sndDns2: str
    mac: str = Field(default=None)
