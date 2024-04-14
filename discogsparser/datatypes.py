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
    thumbnail_image_url: str
    cover_image_url: str

    def __str__(self) -> str:
        return f"DiscogsRelease Dataclass: {self.title} ({self.release_year})"
