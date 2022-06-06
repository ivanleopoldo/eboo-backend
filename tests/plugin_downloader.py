from __init__ import Scraper

class PluginHandler:
    def __init__(self):
        self.hostname = "https://raw.githubusercontent.com"
        self.scraper = Scraper(self.hostname).scraper
        self.plugin_json = "/ivanleopoldo/noveapi-plugins/main/plugins.json"
        self.plugin_url = "https://github.com/ivanleopoldo/noveapi-plugins/blob/main/plugins/"

    def get_plugin_list(self):
        plugin_list = self.scraper.get(self.hostname + self.plugin_json).json()["plugins"]
        return list(map(lambda plug: plug + self.plugin_url, plugin_list))

    def download_plugin(self, plugin):
        pass

    def delete_plugin(self, plugin):
        pass

    def _print_plugin_list(self):
        print(self.get_plugin_list())