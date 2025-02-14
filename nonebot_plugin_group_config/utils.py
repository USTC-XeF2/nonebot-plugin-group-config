import json

from nonebot import get_plugin_config
from nonebot_plugin_localstore import get_config_dir

from .config import Config

plugin_config = get_plugin_config(Config)

def get_group_config_file(group_id: str):
    config_dir = get_config_dir("group_config")
    return config_dir / plugin_config.group_config_format.format(group_id)

def get_group_config(group_id: str) -> dict[str, dict[str]]:
    config_file = get_group_config_file(group_id)
    if not config_file.exists():
        return {}

    with config_file.open() as rf:
        return json.load(rf)

def set_group_config(group_id: str, config: dict[str, dict[str]]):
    with get_group_config_file(group_id).open("w") as wf:
        json.dump(config, wf, indent=4)

async def is_command_enabled() -> bool:
    return plugin_config.group_config_enable_command

GLOBAL = "GLOBAL"
