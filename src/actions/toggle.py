#!/usr/bin/python3

from util import open_mpd_client, play_state, alfred_json


def main():
    with open_mpd_client() as client:
        state = play_state(client)
        if state == 'play':
            client.pause()
            print(alfred_json('pause'))
        elif state == 'pause':
            client.play()
            print(alfred_json('play'))
        else:
            print(alfred_json('stop'))


if __name__ == '__main__':
    main()
