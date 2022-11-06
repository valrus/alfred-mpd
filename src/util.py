#!/usr/bin/python3
# -*- coding: utf-8 -*-

from contextlib import contextmanager
import json
import os
import sys

# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
lib_dir = os.path.join(parent_dir, 'lib')

sys.path.append(lib_dir)

from mpd import MPDClient


ALBUM_ITEM_MODS = {
    'shift': {
        'variables': {
            'ALBUM_MOD': 'queue',
        },
        'subtitle': 'Queue this album',
    },
    'alt': {
        'variables': {
            'ALBUM_MOD': 'shuffle',
        },
        'subtitle': 'Shuffle this album',
    },
    'ctrl': {
        'variables': {
            'ALBUM_MOD': 'show',
        },
        'subtitle': 'Show album tracks',
    }
}

SPECIAL_CHAR_TRANSLATOR = {ord(x): ord(y) for x,y in zip( "‘’“”–-",  "''\"\"--")}


def make_item(title, *, subtitle, variables=None, mods=ALBUM_ITEM_MODS):
    return dict(
        title=title,
        subtitle=subtitle,
        valid=True,
        arg=alfred_json(title, variables=variables),
        icon='icon.png',
        match=title.translate(SPECIAL_CHAR_TRANSLATOR),
        autocomplete=title,
        text={
            'copy': title,
            'largetype': title
        },
        mods=mods,
    )


def alfred_json(arg, *, variables=None):
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


def play_state(client):
    return client.status()['state']


@contextmanager
def open_mpd_client(host=None, port=None):
    client = MPDClient()
    client.connect(
        host or os.path.expanduser(os.getenv('MPD_HOST', 'localhost')),
        port or int(os.getenv('MPD_PORT', '6600'))
    )
    yield client
    client.close()
    client.disconnect()


def list_wrap(obj):
    return obj if isinstance(obj, list) else [obj]
