from contextlib import contextmanager
import os

from mpd import MPDClient


@contextmanager
def open_mpd_client(host=None, port=None):
    client = MPDClient()
    client.connect(host or os.getenv('MPD_HOST', 'localhost'),
                   port or int(os.getenv('MPD_PORT', '6600')))
    yield client
    client.close()
    client.disconnect()
