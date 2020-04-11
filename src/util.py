from contextlib import contextmanager
import json
import os

from mpd import MPDClient


def make_item(title, subtitle, variables):
    return dict(
        title=title,
        subtitle=subtitle,
        valid=True,
        arg=json.dumps({
            'alfredworkflow': {
                'arg': title,
                'variables': variables,
            }
        }),
        icon='icon.png',
        autocomplete=title,
        text={
            'copy': title,
            'largetype': title
        }
    )


@contextmanager
def open_mpd_client(host=None, port=None):
    client = MPDClient()
    client.connect(host or os.getenv('MPD_HOST', 'localhost'),
                   port or int(os.getenv('MPD_PORT', '6600')))
    yield client
    client.close()
    client.disconnect()
