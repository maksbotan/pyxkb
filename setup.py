#!/usr/bin/env python

import sys
import subprocess, commands
from distutils.core import setup, Extension

if subprocess.call(["make", "-C", "kbdd/"]):
    print "make failed!"
    sys.exit(1)

GLIB_LIBS = [ i for i in commands.getoutput('pkg-config --libs glib-2.0').replace('-l', '').split(' ') if i]
GLIB_CFLAGS = [ i for i in commands.getoutput('pkg-config --cflags glib-2.0').replace('-I', '').split(' ') if i]

setup(name="PyXKB",
      version="0.1",
      py_modules = ["kbdd"],
      scripts = ["pyxkbd.py"],
      ext_modules=[Extension(
        '_kbdd',
        ['xkb-config.i'],
        swig_opts=['-shadow'],
        extra_objects=["kbdd/storage.o", "kbdd/libkbdd.o"],
        include_dirs=["kbdd/src"] + GLIB_CFLAGS,
        libraries=GLIB_LIBS + ["X11"],
      )]
)
