# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from contextlib import contextmanager
import json
import os

from mpd import MPDClient


def make_item(title, subtitle, variables):
    return dict(
        title=title,
        subtitle=subtitle,
        valid=True,
        arg=alfred_json(title, variables=variables),
        icon='icon.png',
        autocomplete=title,
        text={
            'copy': title,
            'largetype': title
        }
    )


def alfred_json(arg, variables=None):
    variables = variables or {}
    return json.dumps({
        'alfredworkflow': {
            'arg': arg,
            'variables': variables
        }
    })


def increment_volume(delta):
    with open_mpd_client() as client:
        current_volume = int(client.status()['volume'])
        new_volume = max(0, min(100, current_volume + delta))
        client.setvol(new_volume)
    return new_volume


def volume_bar(volume):
    # █ ░
    return '{0:◯<10}'.format('⬤' * int(round(volume / 10.0)))


def format_time(total_seconds):
    return "{0:0.0f}:{1:02.0f}".format(*divmod(float(total_seconds), 60))


@contextmanager
def open_mpd_client(host=None, port=None):
    client = MPDClient()
    client.connect(host or os.getenv('MPD_HOST', 'localhost'),
                   port or int(os.getenv('MPD_PORT', '6600')))
    yield client
    client.close()
    client.disconnect()
