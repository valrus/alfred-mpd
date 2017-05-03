from __future__ import unicode_literals
from __future__ import print_function

import argparse
import json
import os
import sys

from util import open_mpd_client


def make_item(track_title, track_length, album_name, artist_name):
    playtime = '{:01}:{:02}'.format(*divmod(track_length, 60))
    return dict(
        title=track_title,
        subtitle=playtime,
        valid=True,
        arg=json.dumps({
            'alfredworkflow': {
                'arg': track_title,
                'variables': {
                    'ALFRED_MPD_TRACK': track_title,
                }
            }
        }),
        icon='icon.png',
        autocomplete=track_title,
        text={
            'copy': track_title,
            'largetype': track_title
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
                make_item(item['title'], int(item['time']), item.get('album'), item.get('artist'))
                for item in client.find(*query_args)
            ]
        }))


if __name__ == '__main__':
    sys.exit(main())
