from __future__ import unicode_literals
from __future__ import print_function

import json
import os

from util import open_mpd_client, alfred_json, play_state


def main():
    with open_mpd_client() as client:
        action = 'Queued'

        # state is play, pause or stop
        state = play_state(client)
        if (state == 'pause' or state == 'stop') and not os.environ.get('ALFRED_MPD_QUEUE'):
            action = 'Playing'
            client.clear()

        variables = {}
        album = os.environ['ALFRED_MPD_ALBUM']
        query_args = ['album', album]

        artist = os.environ.get('ALFRED_MPD_ARTIST')
        if artist:
            query_args += ['albumartist', artist]
            variables['artist'] = artist

        track = os.environ.get('ALFRED_MPD_TRACK')
        if track:
            query_args += ['title', track]
            variables['track'] = track

        client.findadd(*query_args)
        if os.environ.get('ALFRED_MPD_SHUFFLE'):
            client.shuffle()

        if not os.environ.get('ALFRED_MPD_QUEUE'):
            client.play()

        print(alfred_json(' '.join([action, track or album]), variables=variables))


if __name__ == '__main__':
    main()
