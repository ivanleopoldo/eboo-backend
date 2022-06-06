from core.assets import default_plugin_contents
import os

def create_default_plugin(plugin_dir):
    with open(f"{plugin_dir}\\default.scraper.py", "w+", encoding="utf-8") as default_file:
        default_file.write(default_plugin_contents)