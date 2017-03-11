from __future__ import unicode_literals
from __future__ import print_function

import argparse
import json
import os
import sys

from mpd import MPDClient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data')
    args = parser.parse_args()

    data = json.loads(args.data)
    album, artist = data['album'], data.get('artist', '')

    client = MPDClient()
    client.connect(os.getenv('MPD_HOST', 'localhost'), int(os.getenv('MPD_PORT', '6600')))
    client.clear()
    vars = {}
    if artist:
        client.findadd('album', album, 'artist', artist)
        vars['artist'] = artist
    else:
        client.findadd('album', album)
    print(json.dumps({
        "alfredworkflow": {
            "arg": album,
            "variables": vars
        }
    }))
    client.play()
    client.close()


if __name__ == '__main__':
    main()