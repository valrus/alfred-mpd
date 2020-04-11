from __future__ import unicode_literals
from __future__ import print_function

import argparse
import json
import os
import sys

from util import open_mpd_client, make_item


def make_song_item(track_title, track_length):
    playtime = '{:01}:{:02}'.format(*divmod(track_length, 60))
    return make_item(
        track_title,
        playtime,
        {
            'ALFRED_MPD_TRACK': track_title,
        }
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='+')
    args = parser.parse_args()

    query_args = args.query

    with open_mpd_client() as client:
        client.clear()
        album = os.environ.get('ALFRED_MPD_ALBUM')
        if album:
            query_args = ['album', album]

        artist = os.environ.get('ALFRED_MPD_ARTIST')
        if artist:
            query_args += ['albumartist', artist]

        print(json.dumps({
            'items': [
                make_song_item(item['title'], int(item['time']))
                for item in client.find(*query_args)
            ]
        }))


if __name__ == '__main__':
    sys.exit(main())
