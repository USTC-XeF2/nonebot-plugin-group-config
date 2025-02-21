import json
import time
import inspect
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from nonebot import get_plugin_config, logger
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

def get_group_config_file(group_id: str):
    return group_config_dir / plugin_config.group_config_format.format(group_id)

class ConfigFileWatcher(FileSystemEventHandler):
    _debounce = 0.05
    _observer = Observer()
    _observer.start()
    config: dict[str, dict[str]]
    def __init__(self, group_id: str):
        self.config_file = get_group_config_file(group_id)
        if self.config_file.exists():
            with self.config_file.open() as rf:
                self.config = json.load(rf)
        else:
            self.config = {}
        self.last_modified = time.time()
        self._observer.schedule(self, path=group_config_dir)

    def on_modified(self, event):
        if event.is_directory or not self.config_file.samefile(event.src_path):
            return
        current = time.time()
        if current - self.last_modified < self._debounce:
            return
        self.last_modified = current
        logger.info(f"reload config from {self.config_file.name}")
        with self.config_file.open() as rf:
            self.config = json.load(rf)

    def save(self):
        self.last_modified = time.time()
        logger.info(f"save config to {self.config_file.name}")
        with self.config_file.open("w") as wf:
            json.dump(self.config, wf, indent=4)

def is_command_enabled():
    return plugin_config.group_config_enable_command is not False

GLOBAL = "GLOBAL"
