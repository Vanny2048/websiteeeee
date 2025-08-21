import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
}

class HttpClient:
    def get(self, url: str, timeout: int = 20):
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp

    @staticmethod
    def soup(html: str):
        return BeautifulSoup(html, "html5lib")

