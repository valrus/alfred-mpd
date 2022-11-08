import argparse
import json
import sys
from datetime import datetime, timedelta
from itertools import islice
from random import sample

from util import open_mpd_client, make_item, format_time, list_wrap


TIME_FORMATS = [
    "%H:%M",
    "%Hh%Mm",
    "%Mm",
    "%M",
]

MIN_ALBUMS_TO_SHOW = 50
# Don't show albums more than 10 minutes shorter than the requested time,
# even if that means we don't get up to MIN_ALBUMS_TO_SHOW
MAX_TIME_DELTA = 600

class AlbumInfo:
    def __init__(self, album_name, album_playtime, *, album_artists):
        self.title = album_name
        self.length_in_seconds = album_playtime

        # Look up the artist for each album.
        # Handle the edge case where two albums have the same name,
        # by grouping the albums with that name by artist and then
        # matching up the playtimes.
        # If two albums have the same name *and* the same playtime,
        # you're out of luck.
        for artist, playtime in zip(
            list_wrap(album_artists['albumartist']),
            list_wrap(album_artists['playtime'])
        ):
            if album_playtime == int(playtime):
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


def albums_to_show(album_counts, seconds_limit):
    count = 0
    for album_name, album_playtime in sorted(
        (
            (album_name, album_playtime)
            for album_name, album_playtime in
            zip(
                album_counts['album'],
                (int(playtime) for playtime in album_counts['playtime'])
            )
            if album_playtime < seconds_limit
        ),
        key=lambda album_details: seconds_limit - album_details[1]
    ):
        time_delta = seconds_limit - album_playtime
        # take all albums less than a minute shorter than the given time,
        # and then up to MIN_ALBUMS_TO_SHOW if necessary
        if time_delta < 60 or (count < MIN_ALBUMS_TO_SHOW and time_delta <= MAX_TIME_DELTA):
            count += 1
            yield album_name, album_playtime
        else:
            return


def albums_shorter_than(seconds_limit):
    with open_mpd_client() as client:
        album_counts = client.count('group', 'album')
        album_list = list(albums_to_show(album_counts, seconds_limit))

        return [
            AlbumInfo(
                album_name,
                album_playtime,
                album_artists=client.count('album', album_name, 'group', 'albumartist')
            )
            for (album_name, album_playtime) in
            # randomize the list order
            sample(album_list, k=len(album_list))
        ]


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
