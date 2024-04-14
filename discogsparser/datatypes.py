from dataclasses import dataclass
from datetime import datetime


@dataclass
class DiscogsRelease:
    title: str
    country: str
    release_year: int
    genres: list[str]
    style: list[str]
    master_url: str
    release_url: str   # resource_url
