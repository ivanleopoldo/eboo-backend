import sys

from bs4 import BeautifulSoup
sys.path.append(".\\")

from core.assets import Scraper, Base
from core.assets import results_dir
from core.utils import create_book, add_chapter
from concurrent.futures import ProcessPoolExecutor
from math import ceil
import os


class Novelfull(Base):
    def __init__(self, path=results_dir):
        self.hostname = "https://novelfull.com/"
        self.search_url = self.hostname + "search?keyword="
        self.scraper_obj = Scraper(self.hostname)
        self.path = path

    def make_book(self, url):
        soup = self.scraper_obj.cook_soup(url)
        last_num = self._get_last_page_number(soup)
        img = self._get_cover_img(soup)
        title = self.get_title(soup)
        authors = self.get_authors(soup)

        with ProcessPoolExecutor(max_workers=15) as executor:
            chapterLinks = list(executor.map(
                self._get_chapter_links, self._parse_url(url, last_num)))

            parsedList = []
            for i in range(0, len(chapterLinks)):
                parsedList += chapterLinks[i]

            results = []
            for i in parsedList:
                thread = executor.submit(self.get_chapter, i)
                result = thread.result()
                results.append(result)
                progress = ceil((len(results)/len(parsedList))*100)
                yield progress

            for j in results:
                add_chapter(j['title'], j['data'])

        epub_path = create_book(title, url, authors, img)

        return epub_path

    def search(self, keyword):
        soup = self.scraper_obj.cook_soup(self.search_url + keyword.lower().replace(" ", "+"))

        try: 
            search_results = soup.find("div", {"class": "list list-truyen col-xs-12"}).find_all("div", {"class": "row"})
            resultsList = []
            for i in search_results:
                parent_tag = i.find("div", {"class": "col-xs-7"}).find("h3", {"class": "truyen-title"})
                resultsList.append({
                    "title": parent_tag.a["title"],
                    "link": self.hostname[:-1] + parent_tag.a["href"]
                })
            return resultsList
        
        except AttributeError:
            return None

    def get_title(self, soup: BeautifulSoup):
        return soup.find("h3", {"class": "title"}).text

    def get_authors(self, soup: BeautifulSoup):
        return [author.text for author in soup.find("div", {"class": "info"}).find_all("div")[0].find_all("a")]

    def get_chapter(self, url: str):
        soup = self.scraper_obj.cook_soup(url)
        return dict({
            "title": soup.find("span", class_="chapter-text").text,
            "data": "".join(f"<p>{i.text}</p>" for i in soup.find("div", id="chapter-content").find_all('p'))
        })
    
    def _get_cover_img(self, soup: BeautifulSoup):
        img_path = f"{self.path}\\cover\\"
        if os.path.isdir(img_path) == False:
            os.mkdir(img_path)

        img_name = img_path + "cover-page.jpg"

        src = self.hostname[:-1] + str(soup.find("div", {"class": "book"}).img["src"])
        try:
            r = self.scraper_obj.scraper.get(src).content
            with open(img_name, "wb") as f:
                f.write(r)
            with open(img_name, "rb") as s:
                return s.read()
        except:
            return None

    def _get_last_page_number(self, soup: BeautifulSoup) -> int:
        try:
            return int(soup.find("li", class_="last").a["data-page"]) + 1
        except:
            return 1

    def _get_chapter_links(self, soup: BeautifulSoup):
        if len(soup.find_all("ul", class_="list-chapter")) > 1:
            links = [[self.hostname + k.find("a")["href"] for k in soup.find_all(
                "ul", class_="list-chapter")[i]] for i in range(0, 2)]
            return links[0] + links[1]
        else:
            return [self.hostname+k.find('a')["href"] for k in soup.find("ul", class_="list-chapter")]

    def _parse_url(url: str, last_page_number: int):
        return [url + f'?page={i}' for i in range(1, last_page_number+1)]

    def _create_folder(self, title):
        folder_path = f"{self.path}\\{title}\\"
        if os.path.isdir(folder_path) == False:  
            os.mkdir(folder_path)
        return folder_path

