from configparser import ConfigParser
import requests
from discogsparser.datatypes import DiscogsRelease


class DiscogsAPI:
    def __init__(self, api_token: str):
        self.__api_token = api_token
        self.base_url = "https://api.discogs.com"

        self.db_url = self.base_url + "/database"

    def __request(self, url: str, method: str, params: dict):
        url_params = "".join(f"{k}={v}&" for k, v in params.items())
        request = f"{url}/{method}?{url_params}token={self.__api_token}"

        r = requests.get(request)

        return r.json()

    def search_release(self, query: str, results_count: int = 5, page: int = 1) -> list[DiscogsRelease]:
        result = self.__request(self.db_url, "search", {
            "query": query,
            "type": "release",
            "per_page": results_count,
            "page": page
        })

        return [DiscogsRelease(
                title=r["title"],
                country=r["country"],
                release_year=int(r["year"]),
                genres=r["genre"],
                style=r["style"],
                master_url=r["master_url"],
                release_url=r["resource_url"],
                thumbnail_image_url=r["thumb"],
                cover_image_url=r["cover_image"],
            ) for r in result["results"]
        ]


if __name__ == "__main__":
    parser = DiscogsAPI()
    cfg = ConfigParser()
    cfg.read("config.conf")
    print(parser.search_release("risk of rain 2")[0])
