from __future__ import unicode_literals
from __future__ import print_function

import itertools
import json
import os
import sys

from util import open_mpd_client, make_item


def make_artist_item(artist_name):
    return make_item(
        artist_name,
        artist_name,
        {
            'ALFRED_MPD_ARTIST': artist_name,
        }
    )


def main():
    with open_mpd_client() as client:
        print(json.dumps({
            'items': [
                make_artist_item(item['albumartist'])
                for item in client.list('albumartist')
            ]
        }))


if __name__ == '__main__':
    sys.exit(main())
