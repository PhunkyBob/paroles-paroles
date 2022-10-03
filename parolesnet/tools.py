# -*- coding: utf-8 -*-
import inquirer
from parolesnet.paroles import ParolesSearch
import requests
import asyncio


def inquir(query):
    questions = [query]
    answers = inquirer.prompt(questions)
    _, val = answers.popitem()
    return val


def override_parameters():
    search_artist = inquir(inquirer.Text("search_artist", message="Artist to search"))
    results = ParolesSearch.search_site(search_artist)
    choices = [(k, v) for k, v in sorted(results.items())]
    artist = inquir(inquirer.List("artist", message="Choose the desired artist", choices=choices))
    return artist


def http_get_sync(url: str, allow_redirects: bool = True):
    response = requests.get(url, allow_redirects=allow_redirects)
    return response


async def http_get(url: str, allow_redirects: bool = True):
    return await asyncio.to_thread(http_get_sync, url, allow_redirects)
