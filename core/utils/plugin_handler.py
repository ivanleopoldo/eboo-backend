from core.assets import Scraper
from core.assets import JsonPluginHandler
import os

class PluginHandler:
    def __init__(self, plugin_dir, json_db_file):
        self.hostname = "https://raw.githubusercontent.com"
        self.plugin_json = "/ivanleopoldo/noveapi-plugins/main/plugins.json"
        self.plugin_url = "/ivanleopoldo/noveapi-plugins/main/plugins/"
        self.plugin_dir = plugin_dir

        self.json_file = json_db_file
        self.scraper = Scraper(self.hostname).scraper
        self.json_obj = JsonPluginHandler(self.json_file)

    def download_plugin(self, plugin):
        plugin_link = self.hostname + self.plugin_url + plugin
        self._create_file(plugin_link)
        self.json_obj.add_plugin_to_json(plugin, plugin_link)

    def delete_plugin(self, plugin):
        self._delete_file(plugin)
        self.json_obj.remove_plugin_from_json(plugin)

    def get_plugin_list(self):
        plugin_list = self.scraper.get(self.hostname + self.plugin_json).json()["plugins"]
        return list(map(lambda plug: plug, plugin_list))

    def _create_file(self, url):
        with open(f'{self.plugin_dir}\\{url.split("/")[-1]}', 'w') as file:
            file.write(self.scraper.get(url).text)
    
    def _delete_file(self, file_name):
        os.remove(f'{self.plugin_dir}\\{file_name}')

    def _print_plugin_list(self):
        print(self.get_plugin_list())