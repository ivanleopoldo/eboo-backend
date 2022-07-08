from core import Base, Scraper

hostname = "https://novelfull.com/"
search_url = hostname + "search?keyword="

class Novelfull(Base):
    def __init__(self):
        self.scraper = Scraper(hostname)

    def search(self, keyword):
        soup = self.scraper.cook_soup(search_url + keyword.lower().replace(" ", "+"))

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

obj = Novelfull()

print(obj.search("otherworldly"))