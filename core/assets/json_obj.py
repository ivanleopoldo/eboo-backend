import json
import os

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