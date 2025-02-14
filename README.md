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
| GROUP_CONFIG_PATH | 是 | 无 | 配置文件的存储文件夹 |
| GROUP_CONFIG_FORMAT | 否 | group-{}.json | 配置文件的名称格式化模板 |
| GROUP_CONFIG_ENABLE_COMMAND | 否 | true | 启用对话中的/config指令 |

## 🎉 使用
### 插件调用

每个群聊有单独的配置文件，配置文件为二级字典，一级字段默认为调用的插件名称，二级字段为配置项。

在使用其他插件时，可以通过`GroupConfigManager`类来管理配置信息。创建`GroupConfigManager`对象时，需要传入默认配置信息。

```python
from nonebot_plugin_group_config import GroupConfigManager, GLOBAL

# 在插件中调用，默认使用插件名称作为一级字段
config_manager1 = GroupConfigManager({
  "key1": "value1",
  "key2": 2
})

# 使用指定的一级字段
config_manager2 = GroupConfigManager({
  "key1": "value1",
  "key2": 2
}, "scope")

# 使用全局字段，在配置文件中以`GLOBAL`为一级字段
global_config_manager = GroupConfigManager({
  "key1": "value1",
  "key2": 2
}, GLOBAL)
```

上文获取的配置管理器可以通过以群ID为键获取指定群聊对应的二级字段信息，返回 `GroupConfig` 对象。修改字段时不能添加新字段，对 `GroupConfig` 对象的操作会直接修改配置文件。

```python
group_config = config_manager1[group_id] # 此处的 group_id 为 str 类型

print(group_config["key1"]) # value1
group_config["key2"] = -1
```

注：获取 `GroupConfig` 对象时若对应的群聊配置信息文件不存在，会根据已注册的所有管理器的默认配置信息创建新的配置文件。也可以通过 `GroupConfigManager.complete_config` 方法手动创建/补全配置文件。

### 指令调用

管理员与超级用户可以在群聊中通过指令对群聊配置进行管理。

使用 `/config` 指令查看当前群聊的所有可用配置字段，这些字段会以 `<一级字段>.<二级字段>` 的形式显示，但 `GLOBAL` 字段不会显示其一级字段。

使用 `/config <一级字段>.<二级字段> <值>` 指令可以设置指定的配置字段，但不能创建不存在的字段，配置后的值与旧值类型相同。

## TODO

- [ ] 获取所有群聊配置信息的接口
- [ ] 超级管理员私聊指令
- [ ] 多级字段支持
