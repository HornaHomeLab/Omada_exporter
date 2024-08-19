from pydantic import BaseModel, Field

import src.Omada.Model.Labels.Port as Port
import src.Omada.helpers.modelFields as modelFields


class SwitchPort(BaseModel):
    name: str
    mac: str = Field(alias="switchMac")
    port: int
    portName: str = Field(alias="name")
    disable: bool
    profileName: str
    operation: str
    linkStatus: str
    linkSpeed: str
    duplex: str
    poe: bool
    tx: int
    rx: int

    def __init__(self, **data):
        if data["linkStatus"] == 0:
            data["linkSpeed"] = -1
            data["duplex"] = -1
        data = modelFields.map_data_values(data, Port.value_map)
        super().__init__(**data)
