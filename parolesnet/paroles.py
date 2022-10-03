# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
from pydantic import BaseModel
import os
from typing import Optional, List
import sys
import asyncio
import re
from parolesnet import default_values

ROOT_URL = "https://www.paroles.net"


class Song(BaseModel):
    url: str
    title: Optional[str] = ""
    artist: Optional[str] = ""
    lyrics: Optional[str] = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.url.lower().startswith(ROOT_URL):
            self.url = ROOT_URL + self.url

    def get_infos(self) -> None:
        asyncio.run(self.get_infos_async())

    async def get_infos_async(self) -> None:
        url = self.url
        if not self.url.lower().startswith(ROOT_URL):
            url = ROOT_URL + self.url
        res = requests.get(url)
        soup = BeautifulSoup(res.text, features="html.parser")
        meta = soup.find("script", attrs={"type": "application/ld+json"})
        meta_data = json.loads(meta.text.strip())
        song_title = meta_data["name"]
        artist_name = meta_data["byArtist"]["name"]

        song_text = soup.find("div", attrs={"class": "song-text"})
        song_lyrics = "".join(div.text for div in song_text.find_all("div"))
        song_lyrics = Song.clean_lyrics(song_lyrics)
        self.artist = artist_name
        self.title = song_title
        self.lyrics = song_lyrics

    def save(self, folder: str = default_values.DOWNLOAD_FOLDER, filename: str = ""):
        if not filename:
            filename = f"{self.artist} - {self.title}".strip()
            filename += ".txt"

        filename = Song.clean_name(filename)
        if folder and folder[-1] not in ["/", "\\"]:
            folder += "/"
            os.makedirs(folder, exist_ok=True)
        filename = folder + filename
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{self.artist} - {self.title}")
            f.write("\n")
            f.write(self.url)
            f.write("\n")
            f.write("\n")
            f.write(self.lyrics)

    @staticmethod
    def clean_lyrics(lyrics):
        lyrics = re.sub("\r", "", lyrics)
        lyrics = re.sub("\n(\n+)", "\n\n", lyrics)
        return lyrics

    @staticmethod
    def clean_name(name):
        forbidden_chars = '\\/:*<>?"|'
        name = "".join([c if c not in forbidden_chars else "_" for c in name])
        name = re.sub(r"\s+", " ", name)
        name = re.sub(r"\.+$", "", name)
        name = name.strip()
        return name


class ArtistSearch(BaseModel):
    artist_url: str
    pages: Optional[List[str]] = []
    songs: Optional[List[Song]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_result_pages()
        links = asyncio.run(self.get_all_links_async())
        self.songs = [Song(url=url, title=title) for title, url in links.items()]

    def get_result_pages(self):
        res = requests.get(self.artist_url)
        soup = BeautifulSoup(res.text, features="html.parser")
        self.pages = [self.artist_url]
        for elem in soup.find_all("a", attrs={"class": "pager-letter"}):
            link = elem.attrs["href"]
            if link != "#":
                self.pages.append(link)

    async def get_all_links_async(self):
        results = await asyncio.gather(*[ArtistSearch.get_links(url) for url in self.pages])
        songs_url = {}
        for res in results:
            songs_url.update(res)
        return songs_url

    def get_infos(self):
        asyncio.run(self.get_infos_all_songs())

    async def get_infos_all_songs(self):
        await asyncio.gather(*[song.get_infos_async() for song in self.songs])

    @staticmethod
    async def get_links(url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, features="html.parser")
        all_urls = {}
        for elem in soup.find_all("p", attrs={"itemprop": "name"}):
            link = elem.find("a")
            if not link:
                continue
            all_urls[link.text.strip()] = link.attrs["href"]
        return all_urls


class ParolesSearch(BaseModel):
    @staticmethod
    def search_site(search) -> dict:
        data = {
            "search": search,
        }
        res = requests.post(f"{ROOT_URL}/search", data=data)
        if res.status_code not in [200]:
            print(f"Error: {res.reason}")
            sys.exit()
        soup = BeautifulSoup(res.text, features="html.parser")
        results = {}
        for td in soup.find_all("td", attrs={"class", "song-name"}):
            a = td.find("a")
            href = a.attrs["href"]
            if re.match(f"{ROOT_URL}/[^/]+$", href):
                results[a.text] = href
        return results
