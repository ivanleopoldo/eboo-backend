from .load_plugins import *
from .create_default import *
from .plugin_handler import *
from .bookbinder import *
from ..assets import *
import os

if os.path.isdir(plugin_dir) == False:
    os.mkdir(plugin_dir)
    create_default_plugin(plugin_dir)

if os.path.isdir(results_dir) == False:
    os.mkdir(results_dir)