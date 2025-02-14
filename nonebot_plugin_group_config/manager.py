from nonebot_plugin_localstore import _try_get_caller_plugin

from .utils import get_group_config_file, get_group_config, set_group_config, GLOBAL

class GroupConfig:
    def __init__(self, group_id: str, manager: 'GroupConfigManager'):
        self.group_id = group_id
        self._m = manager

    def get_all(self) -> dict[str]:
        return get_group_config(self.group_id).get(self._m.scope, self._m.default_config)

    def __getitem__(self, key: str):
        return self.get_all()[key]

    def __contains__(self, key: str):
        return key in self.get_all()

    def get(self, key: str, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key: str, value):
        full_config = get_group_config(self.group_id)
        if self._m.scope not in full_config:
            full_config[self._m.scope] = self._m.default_config.copy()
        if key not in full_config[self._m.scope]:
            raise KeyError(f"Key {key!r} not in config")
        if full_config[self._m.scope][key] != value:
            full_config[self._m.scope][key] = value
            set_group_config(self.group_id, full_config)

    def reset(self, key: str):
        """
        将配置项重置为默认值
        """
        self[key] = self._m.default_config[key]

class GroupConfigManager:
    _managers = dict[str, 'GroupConfigManager']()
    default_config: dict[str]
    scope: str
    _configs: dict[str, GroupConfig]
    def __new__(cls, default_config: dict[str], scope: str = None):
        scope = scope or _try_get_caller_plugin().name
        if scope not in cls._managers:
            instance = super().__new__(cls)
            instance.default_config = default_config
            instance.scope = scope
            instance._configs = {}
            cls._managers[scope] = instance
        return cls._managers[scope]

    @classmethod
    def get_manager(cls, scope: str):
        """
        获取指定作用域的配置管理器
        """
        return cls._managers[scope]

    @classmethod
    def complete_config(cls, group_id: str):
        """
        创建/补全配置文件
        """
        config = get_group_config(group_id)
        for manager in cls._managers.values():
            if manager.scope not in config:
                config[manager.scope] = manager.default_config
            else:
                config[manager.scope].update(manager.default_config)
        set_group_config(group_id, config)

    def __getitem__(self, group_id: str):
        if group_id not in self._configs:
            self._configs[group_id] = GroupConfig(group_id, self)
            if not get_group_config_file(group_id).exists():
                self.complete_config(group_id)
        return self._configs[group_id]

    @classmethod
    def generate_keys(cls):
        """
        生成用于指令的配置项键值对
        """
        return {
            (i.scope + "." + j if i.scope != GLOBAL else j): (i.scope, j)
            for i in cls._managers.values()
            for j in i.default_config.keys()
        }
