all: xkb-config

GLIB_LIBS = `pkg-config glib-2.0 --libs`
GLIB_CFLAGS = `pkg-config glib-2.0 --cflags`
GTK_LIBS = `pkg-config gtk+-2.0 --libs`
GTK_CFLAGS = `pkg-config gtk+-2.0 --cflags`

xkb-config:
	$(CC) xkb-config.c -c -o xkb-config.o ${GLIB_LIBS} ${GLIB_CFLAGS} ${GTK_LIBS} ${GTK_CFLAGS}
