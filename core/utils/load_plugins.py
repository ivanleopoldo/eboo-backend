from importlib import util
from core.assets import plugin_dir
import os

# variables
filename_filter = tuple(("__", ".", "config."))

# methods
def load_module(plugin):
    spec = util.spec_from_file_location(plugin, os.path.join(plugin_dir, plugin))
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)

# main
def load_plugins():
    for plugin in os.listdir(plugin_dir):
        if plugin.endswith(".py") and \
            not plugin.startswith(filename_filter):
            load_module(plugin)