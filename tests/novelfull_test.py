from ast import keyword
from core import Scraper

hostname = "https://novelfull.com/"
url = hostname + "search?keyword="

keyword = "dou"

soup = Scraper(hostname).cookSoup(url + keyword.lower().replace(" ", "+"))

for i in soup.find("div", {"class": "list list-truyen col-xs-12"}).find_all("div", {"class": "row"}):
    parent_tag = i.find("div", {"class": "col-xs-7"}).find("h3", {"class": "truyen-title"})
    print({
        "title": parent_tag.a["title"],
        "link": hostname[:-1] + parent_tag.a["href"]
    })