from __future__ import unicode_literals
from __future__ import print_function

import itertools
import json
import os
import sys

from util import open_mpd_client


def make_item(album_name, artist_name):
    return dict(
        title=album_name,
        subtitle=artist_name,
        valid=True,
        arg=json.dumps({
            'alfredworkflow': {
                'arg': album_name,
                'variables': {
                    'ALFRED_MPD_ALBUM': album_name,
                    'ALFRED_MPD_ARTIST': artist_name,
                }
            }
        }),
        icon='icon.png',
        autocomplete=album_name,
        text={
            'copy': album_name,
            'largetype': album_name
        }
    )


def main():
    with open_mpd_client() as client:
        print(json.dumps({
            'items': list(itertools.chain.from_iterable(
                [
                    make_item(album, artist)
                    for album in client.list('album', 'artist', artist)
                ]
                for artist in client.list('albumartist')
            ))
        }))


if __name__ == '__main__':
    sys.exit(main())
