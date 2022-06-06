from core.assets import Scraper
import os
import json
import glob

class BackupHandler():
    def __init__(self, backup_path):
        self.backup_path = backup_path

    def create_backup(self):
        pass

    def delete_backup(self):
        pass

    def delete_all_backups(self):
        pass

class DownloadsHandler():
    def __init__(self, results_dir):
        self.results_dir = results_dir
    
    def make_book(self):
        pass

    def delete_book(self):
        pass

    def get_all_books(self):
        pass

    def delete_all_books(self):
        pass

    def _print_books(self):
        print(glob.glob(self.results_dir))

class JsonPluginHandler:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

        if os.path.isfile(self.json_file_path) == False:
            self.reset()
            
    def add_plugin_to_json(self, plugin_file_name, plugin_url):
        with open(self.json_file_path, "r+") as file:
            json_data = json.load(file)

            json_data["downloaded"].append({
                "plugin_name": plugin_file_name,
                "plugin_url": plugin_url
            })

            file.seek(0)

            json.dump(json_data, file, indent=4)

    def remove_plugin_from_json(self, plugin_file_name):
        with open(self.json_file_path, "r+") as file:
            json_data = json.load(file)
            data_list = [plug for plug in json_data["downloaded"] if plug["plugin_name"] != plugin_file_name]
            
            file.truncate(0)
            json_data["downloaded"] = data_list
            file.seek(0)

            json.dump(json_data, file, indent=4)

    def reset(self):
        with open(self.json_file_path, "w+") as file:
            json_data = json.loads("""{
                "downloaded": []
            }""")

            json.dump(json_data, file, indent=4)

    def _print_json(self):
        with open(self.json_file_path, "r") as file:
            print(json.load(file))

class PluginHandler:
    def __init__(self, plugin_dir, json_db_file):
        self.hostname = "https://raw.githubusercontent.com"
        self.plugin_json = "/ivanleopoldo/eboo-plugins/main/plugins.json"
        self.plugin_url = "/ivanleopoldo/eboo-plugins/main/plugins/"
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

    def delete_all_plugins(self):
        pass

    def _create_file(self, url):
        with open(f'{self.plugin_dir}\\{url.split("/")[-1]}', 'w') as file:
            file.write(self.scraper.get(url).text)
    
    def _delete_file(self, file_name):
        os.remove(f'{self.plugin_dir}\\{file_name}')

    def _print_plugin_list(self):
        print(self.get_plugin_list())