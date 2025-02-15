import json
import inspect
from functools import lru_cache

from nonebot import get_plugin_config
from nonebot.plugin import get_plugin_by_module_name
from nonebot_plugin_localstore import get_plugin_config_dir

from .config import Config

plugin_config = get_plugin_config(Config)
group_config_dir = get_plugin_config_dir()

def get_caller_plugin_name():
    current_frame = inspect.currentframe()
    if current_frame is None:
        raise RuntimeError("Cannot get current frame")

    frame = current_frame
    while frame := frame.f_back:
        module_name = (module := inspect.getmodule(frame)) and module.__name__
        if module_name is None:
            raise RuntimeError("Cannot get module name")

        if module_name.split(".", maxsplit=1)[0] == "nonebot_plugin_group_config":
            continue

        plugin = get_plugin_by_module_name(module_name)
        if plugin and plugin.id_ != "nonebot_plugin_group_config":
            return plugin.name.removeprefix("nonebot_plugin_")

    raise RuntimeError("Cannot get caller plugin")

@lru_cache
def get_group_config_file(group_id: str):
    return group_config_dir / plugin_config.group_config_format.format(group_id)

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
