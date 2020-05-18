# alfred-mpd

alfred-mpd is an [Alfred](http://www.alfredapp.com/) workflow designed to make
playing music using [mpd](https://www.musicpd.org) extremely quick and convenient.

This workflow uses the [python-mpd2](https://github.com/Mic92/python-mpd2) library
to control mpd from Python. (The library is included; you don't need to install
it yourself. This is just to give credit.)

Current functionality is designed around the way I myself play music, which is to
say, a whole album at a time. In the future I may be willing to implement other
use cases if people ask, but I get the impression that use of mpd on a Mac is
at best an extremely niche proposition. The following instructions assume you have
it installed and configured.

## Usage

Trigger this workflow using the `mpdalbum` keyword. Alfred will scan your mpd
database, and you can use Alfred's fuzzy matching to search for an album.
When you select the album, if mpd is already playing, the selected album will
be queued at the end of the playlist. Otherwise it will start playing immediately.

The workflow also comes with a **Play/Queue** hotkey (default ⌃⇧↑) to save you
from having to type the keyword. You may of course change or disable it.
The ⌃⇧↓ hotkey will show the currently playing (or paused) song, artist and
album as well as the time elapsed and duration of the current song.

The workflow also makes F7, F8 and F9 do for mpd what they do as media keys
for iTunes (previous track / toggle play / next track respectively).
As well, it makes F11 and F12 decrease and increase the volume in increments of 10
(MPD's volume range is 0–100).

### Modifier Keys for Playing / Queueing Albums

You can modify the behavior of the workflow when you select an album.

**Shift** will cause the album to be queued instead of played, regardless of
whether mpd is currently playing.

**Option** will shuffle the playlist after adding the album. Note that this means that
if you want to queue several albums with shuffle on, each additional album will re-shuffle
the playlist.

**Control** will show the album's tracks in Alfred instead of playing the album.
Selecting a track will behave as the **Play/Queue** hotkey above, but for the track.
Control-selecting the track will play or queue the whole album. This lets you preview
the tracks on an album before deciding to play it. Shift or Option-selecting a single track
works as for albums, above.

### What's With The Large Text

Aside from playing or queueing an album or song, most actions will show large text.
The problem with large text is that it's always _as large as possible_, which is sometimes
_very_ large indeed. In particular, the play/pause/stop emoji shown when you toggle play
are colossal if shown alone and typically extremely pixelated. I padded them out to force them
smaller; it's not a great solution but it's the best I could come up with.

## If You Don't Have mpd Installed Already

You should be aware that using mpd instead of iTunes to play music means
circumventing the "(usually) just works" nature of Apple's default music player
in the interest of maybe saving some memory and using some software that is
in principle more narrowly focused on a single purpose. As a result, you'll
probably be setting yourself up for a certain amount of frustration as you're
forced to tinker with your non-standard setup. This route is not for everyone!
On the other hand, this setup certainly allows for more tinkering than iTunes.

Here's a nice blog post that explains why you might be interested in going
this route, with instructions for setting things up:
http://ssrubin.com/posts/music-library-with-mpd-ncmpcpp-beets.html

Personally, I don't use beets or ncmpcpp, which is why I wrote my own
Alfred workflow rather than using the one linked in that post. I let iTunes
manage my music because trying to cut it out of my life entirely is too much
for me. But you can certainly just use the setup in that post if you prefer!

If you use Apple Lossless files, you might need to follow these instructions
when you install mpd to make sure it works with them:
http://onethingwell.org/post/16355956926/mpd-apple-lossless-os-x

*Copyright 2016 Ian McCowan*  
