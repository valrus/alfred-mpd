#!/usr/bin/python3

from util import open_mpd_client


def main():
    with open_mpd_client() as client:
        client.next()


if __name__ == '__main__':
    main()
