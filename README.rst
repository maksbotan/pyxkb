=======
 PyXKB
=======

Introduction
------------
PyXKB is X11 keyboard layout switcher that can remember layouts per window.
C backend is written by qnikst, mine is python daemon and dbus support.

Dependencies
------------
* swig
* python-dbus
* python-gobject
* libX11 =)

Downloading and compiling
-------------------------
Some simple steps:
::
    $ git clone git://github.com/maksbotan/pyxkb.git
    $ cd pyxkb
    $ git pull origin kbdd-int
    $ git submodule init
    $ git submodule update
    $ make

Running
-------
./pyxkb.py

Testing
-------
* Change keyboard layout and try to change activve window. Notice layout changing
* Launch 'qdbusviewer' or something like that and look at 'ru.gentoo.Kbdd'
