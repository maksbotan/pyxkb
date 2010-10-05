all: xkb-config

GLIB_LIBS = `pkg-config glib-2.0 --libs`
GLIB_CFLAGS = `pkg-config glib-2.0 --cflags`
#GTK_LIBS = `pkg-config gtk+-2.0 --libs`
#GTK_CFLAGS = `pkg-config gtk+-2.0 --cflags`
#XKL_LIBS = `pkg-config libxklavier --libs`

KBDD_CFLAGS="-Ikbdd/src/"

xkb-config:
	$(MAKE) -C kbdd/
	swig -python -shadow xkb-config.i
	$(CC) -c xkb-config_wrap.c -I/usr/include/python2.6/ ${GLIB_LIBS} ${GLIB_CFLAGS} ${KBDD_CFLAGS} -g -ggdb 
	$(CC) -shared kbdd/libkbdd.o kbdd/storage.o xkb-config_wrap.o -o _kbdd.so ${GLIB_LIBS} -lpython2.6 -lX11
