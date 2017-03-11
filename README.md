# alfred-mpd

alfred-mpd is an [Alfred](http://www.alfredapp.com/) workflow designed to make
playing music using [mpd](https://www.musicpd.org) extremely quick and convenient.

This workflow uses the [python-mpd2](https://github.com/Mic92/python-mpd2) library
to control mpd from Python. (The library is included; you don't need to install
it yourself. This is just to give credit.)

Current functionality is designed around the way I myself play music, which is to
say, a whole album at a time. In the future I may be willing to implement other
use cases if people ask, but I get the impression that use of mpd on a Mac is
at best an extremely niche proposition.

Trigger this workflow using the `mpdalbum` keyword. Alfred will scan your mpd
database, and you can use Alfred's fuzzy matching to search for an album and
play it. The workflow also comes with a hotkey (default ⌃⇧↑) to save you
from having to type the keyword. You may of course change or disable it.

*Copyright 2016 Ian McCowan*  
