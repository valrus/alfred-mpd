#!/usr/bin/python3

import argparse
import json
import os
import sys

from util import open_mpd_client, make_item, format_time


def make_song_item(track_title, track_length):
    return make_item(
        track_title,
        format_time(track_length),
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
