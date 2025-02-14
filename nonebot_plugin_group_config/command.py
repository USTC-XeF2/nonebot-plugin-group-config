from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot_plugin_uninfo import ADMIN, Uninfo

from .utils import is_command_enabled
from .manager import GroupConfigManager

config_handler = on_command(
    "config",
    rule=is_command_enabled,
    permission=SUPERUSER | ADMIN(),
    priority=0,
    block=True
)

@config_handler.handle()
async def _(session: Uninfo, args: Message = CommandArg()):
    if not session.scene.is_group:
        await config_handler.finish("管理员跨群聊配置功能暂未实现", reply_message=True)
    parsed_args = args.extract_plain_text().split()
    config_keys = GroupConfigManager.generate_keys()
    if len(parsed_args) == 0:
        all_config = "\n".join(config_keys)
        if all_config:
            await config_handler.finish(
                f"可用配置项：\n{all_config}\n\n使用'/config [key] [value]'以查看/更改配置",
                reply_message = True
            )
        else:
            await config_handler.finish("暂无配置项", reply_message=True)
    if not (key := config_keys.get(parsed_args[0])):
        await config_handler.finish("无效的配置项", reply_message=True)
    group_config = GroupConfigManager._managers[key[0]][session.scene.id]
    old_value = group_config[key[1]]
    if len(parsed_args) == 1:
        await config_handler.finish(str(old_value), reply_message=True)
    elif len(parsed_args) == 2:
        if parsed_args[1] == "--default":
            group_config.reset(key[1])
        else:
            group_config[key[1]] = type(old_value)(parsed_args[1])
        await config_handler.finish("配置设置成功", reply_message=True)
    else:
        await config_handler.finish("参数过多", reply_message=True)
