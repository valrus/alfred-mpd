#!/usr/bin/python3

import itertools
import json
import sys

from util import open_mpd_client, make_item


def make_album_items(album_or_albums, artist_name):
    if isinstance(album_or_albums, list):
        album_names = album_or_albums
    else:
        album_names = [album_or_albums]
    return (
        make_item(
            album_name, subtitle=artist_name,
            variables={
                'ALFRED_MPD_ALBUM': album_name,
                'ALFRED_MPD_ARTIST': artist_name,
            }
        )
        for album_name in album_names
    )


def all_albums(client):
    """Return a list of all available albums.

    Return a list instead of a generator because by the time
    the generator is used, the client might no longer be usable."""
    return list(
        itertools.chain.from_iterable(
            [
                make_album_items(item['album'], item['albumartist'])
                for item in client.list('album', 'group', 'albumartist')
            ]
        )
    )


def main():
    with open_mpd_client() as client:
        print(json.dumps({'items': all_albums(client)}))


if __name__ == '__main__':
    sys.exit(main())
