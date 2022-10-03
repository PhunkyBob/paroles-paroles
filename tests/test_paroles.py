# -*- coding: utf-8 -*-
import pytest

import os
import sys
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parolesnet.paroles import ArtistSearch, Song, ParolesSearch

ROOT_URL = "https://www.paroles.net"


def test_artist_page():
    url = "https://www.paroles.net/angele"
    artist_page = ArtistSearch(artist_url=url)
    assert len(artist_page.pages) > 1
    assert len(artist_page.songs) > 30


def test_get_lyrics():
    url = "https://www.paroles.net/angele/paroles-balance-ton-quoi"
    song = Song(url=url)
    song.get_infos()
    assert song.title == "Balance Ton Quoi"
    assert song.artist == "Angèle"
    assert len(song.lyrics) > 0


def test_get_all_lyrics():
    url = "https://www.paroles.net/angele"
    artist_page = ArtistSearch(artist_url=url)
    # Override songs
    artist_page.songs = [
        Song(url="https://www.paroles.net/angele/paroles-libre"),
        Song(url="https://www.paroles.net/angele/paroles-balance-ton-quoi"),
    ]
    artist_page.get_infos()
    for song in artist_page.songs:
        assert len(song.title) > 0
        assert len(song.artist) > 0
        assert len(song.lyrics) > 0


def test_write_song():
    song = Song(url="/url")
    expected_file = "temp/Artist - Title _ with _specials chars_ _.txt"
    if os.path.exists(expected_file):
        os.remove(expected_file)
    song.artist = "Artist"
    song.title = "Title / with <specials chars> :     "
    song.lyrics = "Line 1\nLine 2"
    song.save(folder="temp")
    assert os.path.exists(expected_file)
    with open(expected_file, "r", encoding="utf-8") as f:
        content = f.read().split("\n")
        assert content[0].startswith("Artist - Title")
        assert content[1].startswith(f"{ROOT_URL}/url")


def test_search_artist():
    result = ParolesSearch.search_site("angele")
    assert len(result) >= 3
