from pydantic import BaseModel, Field

class RouterPortStats(BaseModel):
    name: str = Field(alias="gatewayName")
    mac: str
    port: int
    txRate: int = Field(alias="tx", default=0)
    rxRate: int = Field(alias="rx", default=0)
    txPkts: int = Field(default=0)
    rxPkts: int = Field(default=0)
    dropPkts: int = Field(default=0)
    errPkts: int = Field(default=0)