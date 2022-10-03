# -*- coding: utf-8 -*-
import inquirer
from parolesnet.paroles import ParolesSearch


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
