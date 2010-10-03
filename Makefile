all: xkb-config

GLIB_LIBS = `pkg-config glib-2.0 --libs`
GLIB_CFLAGS = `pkg-config glib-2.0 --cflags`
GTK_LIBS = `pkg-config gtk+-2.0 --libs`
GTK_CFLAGS = `pkg-config gtk+-2.0 --cflags`

xkb-config:
	swig -python -shadow xkb-config.i
	$(CC) -c xkb-config.c xkb-config_wrap.c -I/usr/include/python2.6/ ${GLIB_LIBS} ${GLIB_CFLAGS} ${GTK_LIBS} ${GTK_CFLAGS} -g -ggdb
	$(CC} -shared xkb-config.o xkb-config_wrap.o -o _xkb_config.so ${GTK_LIBS} ${XKL_LIBS}
