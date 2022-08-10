import argparse
import json
import sys
from datetime import datetime, timedelta
from itertools import islice

from util import open_mpd_client, make_item, format_time, list_wrap


TIME_FORMATS = [
    "%H:%M",
    "%Hh%Mm",
    "%Mm",
    "%M",
]

class AlbumInfo:
    def __init__(self, album_name, album_playtime, client):
        self.title = album_name
        self.length_in_seconds = int(album_playtime)

        # Look up the artist for each album.
        # Handle the edge case where two albums have the same name,
        # by grouping the albums with that name by artist and then
        # matching up the playtimes.
        # If two albums have the same name *and* the same playtime,
        # you're out of luck.
        album_artists = client.count('album', album_name, 'group', 'artist')
        for artist, playtime in zip(
                list_wrap(album_artists['artist']),
                list_wrap(album_artists['playtime'])
        ):
            if album_playtime == playtime:
                self.artist = artist
                break
        else:
            self.artist = "Unknown artist"

    def make_item(self):
        return make_item(
            self.title,
            subtitle=f'{self.artist} - {format_time(self.length_in_seconds)}',
            variables={
                'ALFRED_MPD_ALBUM': self.title,
                'ALFRED_MPD_ARTIST': self.artist,
            }
        )


def hours_and_minutes(time_string: str) -> int:
    # strptime expects hours to be zero-padded; do so appropriately
    if ':' in time_string:
        time_string = time_string.zfill(5)
    elif 'h' in time_string:
        time_string = time_string.zfill(6)

    for time_format in TIME_FORMATS:
        try:
            time = datetime.strptime(time_string, time_format)
            return timedelta(hours=time.hour, minutes=time.minute).seconds
        except ValueError:
            pass
    return timedelta(minutes=int(time_string)).seconds


def albums_shorter_than(seconds_limit):
    with open_mpd_client() as client:
        album_counts = client.count('group', 'album')

        return islice(
            sorted(
                (
                    AlbumInfo(album_name, album_playtime, client)
                    for album_name, album_playtime in
                    zip(album_counts['album'], album_counts['playtime'])
                    if int(album_playtime) < seconds_limit
                ),
                key=lambda album_info: seconds_limit - album_info.length_in_seconds
            ),
            50
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('time', type=hours_and_minutes)
    args = parser.parse_args()

    print(json.dumps({
        'items': [
            album.make_item()
            for album in albums_shorter_than(args.time)
        ]
    }))


if __name__ == '__main__':
    sys.exit(main())
