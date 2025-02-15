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
| GROUP_CONFIG_ENABLE_COMMAND | 否 | true | 启用对话中的/config指令 |

本插件使用 localstore 插件进行存储，若需要修改群聊配置文件的存储路径，请参考 localstore 插件的说明更改 `LOCALSTORE_PLUGIN_CONFIG_DIR` 配置项。

## 🎉 使用
### 插件调用

每个群聊有单独的配置文件，配置文件为二级字典，一级字段为作用域，二级字段为该作用域下的配置项。配置文件存储于 `localstore` 配置文件夹的 `group_config` 文件夹下。

在使用其他插件时，可以通过 `GroupConfigManager` 类来管理配置信息。创建 `GroupConfigManager` 对象时，需要传入默认配置信息。

```python
from nonebot_plugin_group_config import GroupConfigManager, GLOBAL

# 默认使用去除 nonebot_plugin_ 前缀的插件名称作为作用域
config_manager1 = GroupConfigManager({
  "key1": "value1",
  "key2": 2
})

# 使用自定义作用域
config_manager2 = GroupConfigManager({
  "key1": "value1",
  "key2": 2
}, "my_scope")

# 使用全局作用域（配置文件中以 GLOBAL 为一级字段）
global_config_manager = GroupConfigManager({
  "key1": "value1",
  "key2": 2
}, GLOBAL)
```

声明配置管理器后，若重复声明则会返回已存在的配置管理器而不进行修改。可以通过 `GroupConfigManager.get_manager` 方法获取已注册的配置管理器，若不存在则返回 `None`。

上文获取的配置管理器可以通过以群 ID 为键获取指定群聊的 `GroupConfig` 对象，其中包含该作用域下的全部配置项。

```python
group_config = config_manager1[group_id] # 此处的 group_id 为 str 类型

print(group_config["key1"]) # 输出：value1
group_config["key2"] = -1 # 只能修改已存在的配置项
```

注：获取 `GroupConfig` 对象时若对应的群聊配置信息文件不存在，会根据已注册的所有管理器的默认配置信息创建新的配置文件，对 `GroupConfig` 对象的操作会直接修改配置文件。

### 指令调用

管理员与超级用户可以在群聊中通过指令对群聊配置进行管理。

使用 `/config` 指令查看当前群聊的所有可用配置项，这些配置项会以 `<作用域>.<配置项>` 的形式显示，但全局作用域不会显示其作用域名称。

使用 `/config <作用域>.<配置项> <值>` 指令可以设置指定的配置项，但不能创建不存在的配置项，配置后的值与旧值类型相同。

## TODO

- [ ] 超级管理员私聊指令
- [ ] 多级配置项支持
