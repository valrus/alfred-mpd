from __future__ import unicode_literals
from __future__ import print_function

from util import open_mpd_client


def main():
    with open_mpd_client() as client:
        state = client.status()['state']
        if (state == 'play'):
            client.pause()
        else:
            client.play()


if __name__ == '__main__':
    main()
