from pydantic import BaseModel

class Config(BaseModel):
    group_config_format: str = "group-{}.json"
    group_config_enable_command: bool = True
