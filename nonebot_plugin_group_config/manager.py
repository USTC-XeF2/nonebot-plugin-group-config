from .utils import plugin_config, get_caller_plugin_name, ConfigFileWatcher, GLOBAL

_enable_command = plugin_config.group_config_enable_command

class GroupConfig:
    def __init__(self, watcher: ConfigFileWatcher, scope: str):
        self._watcher = watcher
        self.scope = scope

    def get_all(self):
        return self._watcher.config[self.scope].copy()

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
        config = self._watcher.config[self.scope]
        if key not in config:
            raise KeyError(f"Key {key!r} not in config")
        super().__setitem__(key, value)
        if config[key] != value:
            config[key] = value
            self._watcher.save()

class GroupConfigManager:
    _watchers = dict[str, ConfigFileWatcher]()
    _managers = dict[str, 'GroupConfigManager']()
    default_config: dict[str]
    scope: str
    _configs: dict[str, GroupConfig]
    def __new__(cls, default_config: dict[str], scope: str = None):
        scope = scope or get_caller_plugin_name()
        if scope in cls._managers:
            raise ValueError(f"GroupConfigManager with scope {scope!r} already exists")
        instance = super().__new__(cls)
        instance.default_config = default_config.copy()
        instance.scope = scope
        instance._configs = {}
        cls._managers[scope] = instance
        return instance

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
        config = cls._watchers[group_id].config
        for manager in cls._managers.values():
            if manager.scope not in config:
                config[manager.scope] = manager.default_config
            else:
                config[manager.scope].update(manager.default_config)
        cls._watchers[group_id].save()

    @classmethod
    def generate_keys(cls) -> dict[str, tuple[str, str]]:
        """
        生成用于指令的配置项键值对
        """
        if _enable_command is False:
            return {}
        return {
            (i.scope + "." + j if i.scope != GLOBAL else j): (i.scope, j)
            for i in cls._managers.values()
            if _enable_command is True or i.scope in _enable_command
            for j in i.default_config.keys()
        }

    def get_group_config(self, group_id: str):
        """
        获取群聊配置对象
        """
        group_id = str(group_id)
        if group_id not in self._configs:
            cls = type(self)
            if group_id not in cls._watchers:
                cls._watchers[group_id] = ConfigFileWatcher(group_id)
                self.complete_config(group_id)
            self._configs[group_id] = GroupConfig(cls._watchers[group_id], self.scope)
        return self._configs[group_id]
