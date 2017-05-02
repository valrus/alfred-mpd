from __future__ import unicode_literals
from __future__ import print_function

import itertools
import json
import os
import sys

from util import open_mpd_client


def make_item(artist_name):
    return dict(
        title=artist_name,
        subtitle=artist_name,
        valid=True,
        arg=json.dumps({
            'alfredworkflow': {
                'arg': artist_name,
                'variables': {
                    'ALFRED_MPD_ARTIST': artist_name,
                }
            }
        }),
        icon='icon.png',
        autocomplete=artist_name,
        text={
            'copy': artist_name,
            'largetype': artist_name
        }
    )


def main():
    with open_mpd_client() as client:
        print(json.dumps({
            'items': [
                make_item(artist)
                for artist in client.list('albumartist')
            ]
        }))


if __name__ == '__main__':
    sys.exit(main())
