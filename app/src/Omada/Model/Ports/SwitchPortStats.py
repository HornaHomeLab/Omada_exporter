from pydantic import BaseModel, Field

class SwitchPortStats(BaseModel):
    name: str = Field(alias="switchName")
    mac: str = Field(alias="switchMac")
    port: int
    tx: int = Field(default=0)
    rx: int = Field(default=0)
    txRate: int = Field(default=0)
    rxRate: int = Field(default=0)
    txPkts: int = Field(default=0)
    rxPkts: int = Field(default=0)
    txBroadPkts: int = Field(default=0)
    rxBroadPkts: int = Field(default=0)
    txMultiPkts: int = Field(default=0)
    rxMultiPkts: int = Field(default=0)
    dropPkts: int = Field(default=0)
    txErrPkts: int = Field(default=0)
    rxErrPkts: int = Field(default=0)
    
    
    