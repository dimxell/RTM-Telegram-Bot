from configparser import ConfigParser
import requests
from bs4 import BeautifulSoup


class DiscogsAPI:
    def __init__(self):
        cfg = ConfigParser()
        cfg.read("config.conf")
        self.__api_token = cfg.get("Discogs", "api_token")
        self.base_url = "https://api.discogs.com"

        self.db_url = self.base_url + "/database"

    def __request(self, url: str, method: str, params: dict):
        url_params = "".join(f"{k}={v}&" for k, v in params.items())
        request = f"{url}/{method}?{url_params}token={self.__api_token}"

        r = requests.get(request)

        return r.json()

    def search_release(self, query: str, results_count: int = 5, page: int = 1):
        result = self.__request(self.db_url, "search", {
            "query": query,
            "type": "release",
            "per_page": results_count,
            "page": page
        })

        return result


if __name__ == "__main__":
    parser = DiscogsAPI()
    print(parser.search_release("risk of rain 2"))
