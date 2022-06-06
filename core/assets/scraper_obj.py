from bs4 import BeautifulSoup
from core.assets import user_agents
from cloudscraper import create_scraper
import ssl
import random

class Scraper:
    """Scraper Class"""
    def __init__(self, referer):
        self.referer = referer

        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        self.headers = {
                "User-Agent": random.choice(user_agents),
                "Referer": self.referer,
                "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
            }

        self.scraper = create_scraper(
            ssl_context=self.ctx,
            browser = self.headers
        )

    def cook_soup(self, url: str):
        return BeautifulSoup(self.scraper.get(url).content, 'lxml')