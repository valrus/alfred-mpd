from pathlib import Path
import os

from util import open_mpd_client, alfred_json

import lyricsgenius
import eyed3


def main():
    with open_mpd_client() as client:
        music_dir = Path(client.config())
        data = client.currentsong()

    audiofile = eyed3.load(music_dir / Path(data['file']))
    tag_lyrics = audiofile.tag.lyrics

    if tag_lyrics:
        print(alfred_json('\n'.join([frame.text for frame in tag_lyrics])))
    elif os.environ.get('GENIUS_ACCESS_TOKEN', '').strip():
        genius = lyricsgenius.Genius(os.environ['GENIUS_ACCESS_TOKEN'], verbose=False)
        song = genius.search_song(
            data['title'],
            data['albumartist'] or data['artist']
        )
        if song:
            audiofile.tag.lyrics.set(song.lyrics)
            audiofile.tag.save()
            print(
                alfred_json(song.lyrics, variables={'error': False})
            )
        else:
            print(
                alfred_json(
                    f'''Couldn't find lyrics for
                    "{data['title']}"
                    by {data['albumartist']}''',
                    variables={'error': True}
                ),
            )
    else:
        print(
            alfred_json(
                f"No lyrics in song file or Genius access token",
                variables={'error': True}
            ),
        )


if __name__ == '__main__':
    main()
