# -*- coding: utf-8 -*-
import os
import sys
import click
import inquirer
import jinxed.terminfo.vtwin10  # Hidden import for compilation

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import parolesnet.tools as tools
from parolesnet.paroles import ArtistSearch
import parolesnet.default_values as default_values


@click.command()
@click.argument("artist_url", required=False)
@click.option("--download-folder", help="Download folder.", default=default_values.DOWNLOAD_FOLDER)
def main(artist_url, download_folder) -> None:
    interactive = False
    if not artist_url:
        artist_url = tools.override_parameters()
        interactive = True

    artist_search = ArtistSearch(artist_url=artist_url)
    print("Songs found:", len(artist_search.songs))
    if len(artist_search.songs) == 0:
        sys.exit()
    if interactive:
        conti = tools.inquir(
            inquirer.List(
                "continue",
                message=f'Continue, download and save all to "{download_folder}"',
                choices=[("Yes", "yes"), ("No", "no"), ("Yes, but change folder", "change")],
            )
        )
        if conti == "no":
            sys.exit()
        if conti == "change":
            download_folder = tools.inquir(
                inquirer.Text(
                    "download_folder",
                    message="Save folder",
                )
            )
    artist_search.get_infos()
    for song in artist_search.songs:
        song.save(folder=download_folder)
    print(len(artist_search.songs), "files saved.")


if __name__ == "__main__":
    main()
