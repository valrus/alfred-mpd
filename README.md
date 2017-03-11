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
it installed and configured:

Trigger this workflow using the `mpdalbum` keyword. Alfred will scan your mpd
database, and you can use Alfred's fuzzy matching to search for an album and
play it. The workflow also comes with a hotkey (default ⌃⇧↑) to save you
from having to type the keyword. You may of course change or disable it.

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
