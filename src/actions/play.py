from __future__ import unicode_literals
from __future__ import print_function

import json
import os

from util import open_mpd_client


def main():
    with open_mpd_client() as client:
        client.clear()
        variables = {}
        album = os.environ['ALFRED_MPD_ALBUM']
        query_args = ['album', album]

        artist = os.environ.get('ALFRED_MPD_ARTIST')
        if artist:
            query_args += ['artist', artist]
            variables['artist'] = artist

        track = os.environ.get('ALFRED_MPD_TRACK')
        if track:
            query_args += ['title', track]
            variables['track'] = track

        client.findadd(*query_args)
        if os.environ.get('ALFRED_MPD_SHUFFLE'):
            client.shuffle()
        print(json.dumps({
            "alfredworkflow": {
                "arg": track or album,
                "variables": variables
            }
        }))
        client.play()


if __name__ == '__main__':
    main()
