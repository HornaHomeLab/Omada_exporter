from pydantic import BaseModel, Field
import src.Omada.helpers.modelFields as modelFields

value_map: dict[str, dict] = {
    "poeMode": {
        0: "off",
        1: "on(802.3at/af)",
    },
    "status": {
        0: "off",
        1: "on",
        None: None
    }
}


class SwitchPort(BaseModel):
    port: int
    name: str
    profileId: str
    profileName: str
    profileOverrideEnable: bool
    poeMode: str
    lagPort: bool
    status: str = Field(default=None)

    def __init__(self, **data):
        data = modelFields.map_data_values(
            data, ["poeMode", "status"], value_map
        )
        super().__init__(**data)
