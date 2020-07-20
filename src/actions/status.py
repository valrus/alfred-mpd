#!/usr/bin/python3

from util import open_mpd_client, alfred_json, format_time


def main():
    # volume, album, songid, repeat, consume, song, track, random, pos,
    # elapsed, playlistlength, date, single, albumartist, file, duration,
    # bitrate, nextsongid, nextsong, mixrampdb, playlist, artist, title, id,
    # state, disc, time, lastmodified, audio, genre
    with open_mpd_client() as client:
        data = client.currentsong()
        data.update(client.status())
    data.update({
        'duration': format_time(data['duration']) if data.get('duration') else 'N/A',
        'elapsed': format_time(data['elapsed']) if data.get('elapsed') else 'N/A',
        'lastmodified': data.get('last-modified', 'N/A'),
    })
    print(alfred_json(data.get('title', ''), variables=data))


if __name__ == '__main__':
    main()
