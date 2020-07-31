from pathlib import Path
import os

from util import open_mpd_client, alfred_json

import lyricsgenius
import mutagen


class TaggedAudioFile:
    LYRICS_TAG_KEYS = {
        'MP4': '\xa9lyr',
        'MP3': "USLT"
    }

    def __init__(self, file_path):
        self.audiofile = mutagen.File(file_path)
        if self.audiofile:
            self.filetype = self.audiofile.__class__.__name__
            self._lyrics = self.audiofile.tags.get(self.lyrics_key())
        else:
            self.filetype, self._lyrics = None, None

    @property
    def lyrics(self):
        return self._lyrics

    @lyrics.setter
    def lyrics(self, lyrics):
        self._lyrics = lyrics
        self.audiofile.tags[self.lyrics_key()] = lyrics

    def lyrics_key(self):
        return self.LYRICS_TAG_KEYS[self.filetype]

    def save(self):
        self.audiofile.save()


def main():
    with open_mpd_client() as client:
        music_dir = Path(client.config())
        data = client.currentsong()

    audiofile = TaggedAudioFile(music_dir / Path(data['file']))
    tag_lyrics = audiofile.lyrics

    if tag_lyrics:
        print(alfred_json('\n'.join([frame for frame in tag_lyrics])))

    elif os.environ.get('GENIUS_ACCESS_TOKEN', '').strip():
        genius = lyricsgenius.Genius(os.environ['GENIUS_ACCESS_TOKEN'], verbose=False)
        song = genius.search_song(
            data['title'],
            data['albumartist'] or data['artist']
        )
        if song:
            audiofile.lyrics = song.lyrics
            audiofile.save()
            print(alfred_json(song.lyrics, variables={'error': False}))
        else:
            print(
                alfred_json(
                    f'''Couldn't find lyrics for
                    "{data['title']}" by {data['albumartist']}''',
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
