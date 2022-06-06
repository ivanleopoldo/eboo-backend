from .load_plugins import *
from .bookbinder import *
from .handlers import *
import os

default_plugin_contents = """from core import Base, Scraper

hostname = "https://novelfull.com/"
search_url = hostname + "search?keyword="

class Novelfull(Base):
    def __init__(self):
        self.scraper = Scraper(hostname)

    def search(self, keyword):
        soup = self.scraper.cookSoup(search_url + keyword.lower().replace(" ", "+"))

        try: 
            search_results = soup.find("div", {"class": "list list-truyen col-xs-12"}).find_all("div", {"class": "row"})
            resultsList = []
            for i in search_results:
                parent_tag = i.find("div", {"class": "col-xs-7"}).find("h3", {"class": "truyen-title"})
                resultsList.append({
                    "title": parent_tag.a["title"],
                    "link": hostname[:-1] + parent_tag.a["href"]
                })
            return resultsList
        
        except AttributeError:
            return None
"""

def create_default_plugin(plugin_dir):
    with open(f"{plugin_dir}\\default.scraper.py", "w+", encoding="utf-8") as default_file:
        default_file.write(default_plugin_contents)

if os.path.isdir(plugin_dir) == False:
    os.mkdir(plugin_dir)
    create_default_plugin(plugin_dir)

if os.path.isdir(results_dir) == False:
    os.mkdir(results_dir)