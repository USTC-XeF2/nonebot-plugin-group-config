from nonebot import require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_localstore")
require("nonebot_plugin_uninfo")

from .config import Config
from .utils import group_config_dir, get_group_config_file, get_group_config, set_group_config, GLOBAL
from .manager import GroupConfig, GroupConfigManager
from .command import config_handler

__plugin_meta__ = PluginMetadata(
    name="群聊配置",
    description="群聊配置信息存储与管理插件",
    usage="使用GroupConfigManager类或使用config指令",
    type="library",
    homepage="https://github.com/USTC-XeF2/nonebot-plugin-group-config",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_uninfo"),
)
