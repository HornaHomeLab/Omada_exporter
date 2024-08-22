from pydantic import BaseModel, Field

class ApRadioConfig(BaseModel):
    name: str
    mac: str
    frequency: str
    actualChannel: str
    maxTxRate: int
    region: int
    bandWidth: str
    mode: str = Field(alias="rdMode")
    txUtil: int
    rxUtil: int
    interUtil: int