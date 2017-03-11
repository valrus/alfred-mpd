from __future__ import unicode_literals
from __future__ import print_function

import itertools
import json
import os
import sys

from mpd import MPDClient

MPC_HOST = 'localhost'
MPC_PORT = 6600


def make_item(album_name, artist_name):
    return dict(
        title=album_name,
        subtitle=artist_name,
        valid=True,
        arg=json.dumps({
            'album': album_name,
            'artist': artist_name,
        }),
        icon='icon.png',
        autocomplete=album_name,
        text={
            'copy': album_name,
            'largetype': album_name
        }
    )


def main():
    client = MPDClient()
    client.connect(os.getenv('MPD_HOST', 'localhost'), int(os.getenv('MPD_PORT', '6600')))
    artists = set(client.list('albumartist')) | set(client.list('artist'))
    print(json.dumps({
        'items': list(itertools.chain.from_iterable([
            make_item(album, artist)
            for album in client.list('album', 'artist', artist)
        ]
        for artist in client.list('albumartist'))
    )}))
    client.close()


if __name__ == '__main__':
    sys.exit(main())
