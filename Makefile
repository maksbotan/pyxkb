all: kbdd

GLIB_LIBS = `pkg-config glib-2.0 --libs`
GLIB_CFLAGS = `pkg-config glib-2.0 --cflags`
#GTK_LIBS = `pkg-config gtk+-2.0 --libs`
#GTK_CFLAGS = `pkg-config gtk+-2.0 --cflags`
#XKL_LIBS = `pkg-config libxklavier --libs`

KBDD_CFLAGS="-Ikbdd/src/"

SOURCES=xkb-config_wrap.c
OBJECTS=${SOURCES:.c=.o}
INTERFACES=xkb-config.i

libkbdd:
	$(MAKE) -C kbdd/ src/libkbdd.o CFLAGS="-g -ggdb"

$(SOURCES): $(INTERFACES)
	swig -python -shadow $<

$(OBJECTS): $(SOURCES)
	$(CC) $(GLIB_CFLAGS) $(KBDD_CFLAGS) -I/usr/include/python2.6/ $< -c -o $@ -g -ggdb

kbdd: libkbdd $(BINDINGS) $(OBJECTS)
	$(CC) -shared kbdd/libkbdd.o kbdd/storage.o xkb-config_wrap.o -o _kbdd.so ${GLIB_LIBS} -lpython2.6 -lX11
