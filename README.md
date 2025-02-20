<div align="center">
  <a href="https://nonebot.dev/"><img src="https://nonebot.dev/logo.png" width="180" height="180" alt="NoneBotLogo"></a>
</div>

<div align="center">

# nonebot-plugin-group-config

_✨ Nonebot2 群聊配置信息存储与管理插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/USTC-XeF2/nonebot-plugin-group-config.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-group-config">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-group-config.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

本插件以插件调用与指令控制的方式管理不同群聊的配置信息，支持配置信息的持久化存储。

## 💿 安装

- 使用 nb-cli 安装

```shell
nb plugin install nonebot-plugin-group-config
```

- 使用包管理器安装

```shell
pip install nonebot-plugin-group-config
```

## ⚙️ 配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| GROUP_CONFIG_FORMAT | 否 | group-{}.json | 配置文件的名称格式化模板 |
| GROUP_CONFIG_ENABLE_COMMAND | 否 | true | 启用对话中的/config指令，如果该项为列表则指令只获取列表中的作用域 |

本插件使用 localstore 插件进行存储，若需要修改群聊配置文件的存储路径，请参考 localstore 插件的说明更改 `LOCALSTORE_PLUGIN_CONFIG_DIR` 配置项。

## 🎉 使用
### 插件调用

每个群聊有单独的配置文件，配置文件为二级字典，一级字段为作用域，二级字段为该作用域下的配置项。配置文件存储于 `localstore` 配置文件夹的 `group_config` 文件夹下。

在使用其他插件时，可以通过 `GroupConfigManager` 类来管理配置信息。创建 `GroupConfigManager` 对象时，需要传入默认配置信息。

```python
from nonebot_plugin_group_config import GroupConfigManager, GLOBAL

# 默认使用去除 nonebot_plugin_ 前缀的插件名称作为作用域
config_manager = GroupConfigManager({
  "key1": "value1",
  "key2": 2
})

# 使用自定义作用域
custom_config_manager = GroupConfigManager({
  "key1": "value1",
  "key2": 2
}, "my_scope")

# 使用全局作用域（配置文件中以 GLOBAL 为一级字段）
global_config_manager = GroupConfigManager({
  "key1": "value1",
  "key2": 2
}, GLOBAL)
```

同一作用域的配置管理器只能声明一次。可以通过 `GroupConfigManager.get_manager` 方法获取已注册的配置管理器，若不存在则返回 `None`。

配置管理器可以通过 `get_group_config` 方法获取指定群聊的 `GroupConfig` 对象，其中包含该作用域下的全部配置项。该对象的配置值与配置文件同步，对 `GroupConfig` 对象的操作会直接修改配置文件。

```python
group_config = config_manager.get_group_config(group_id)

print(group_config["key1"]) # 输出：value1
group_config["key2"] = -1 # 只能修改已存在的配置项
```

在事件处理中调用时，也可以通过依赖注入获取 `GroupConfig` 对象，若事件非群聊类型则不会触发。

```python
from nonebot_plugin_group_config import GroupConfig, GetGroupConfig

handler = on(...) # 事件处理器

@handler.handle()
async def _(group_config: GroupConfig = GetGroupConfig(config_manager)):
  ...
```

注：获取 `GroupConfig` 对象时若对应的群聊配置信息文件不存在，会根据已注册的所有管理器的默认配置信息创建新的配置文件。

### 指令调用

管理员与超级用户可以在群聊中通过指令对群聊配置进行管理。

使用 `/config` 指令查看当前群聊的所有可用配置项，这些配置项会以 `<作用域>.<配置项>` 的形式显示，但全局作用域不会显示其作用域名称。

使用 `/config <作用域>.<配置项> <值>` 指令可以设置指定的配置项，但不能创建不存在的配置项，配置后的值与旧值类型相同。

## TODO

- [ ] 提前获取配置管理器与更好的全局管理器支持
- [ ] 超级管理员私聊指令
- [ ] 多级配置项支持
