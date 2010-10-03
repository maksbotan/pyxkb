/* vim: set backspace=2 ts=4 softtabstop=4 sw=4 cinoptions=>4 expandtab autoindent smartindent: */
/* xkb-config.h
 * Copyright (C) 2008 Alexander Iliev <sasoiliev@mamul.org>
 *
 * Parts of this program comes from the XfKC tool:
 * Copyright (C) 2006 Gauvain Pocentek <gauvainpocentek@gmail.com>
 * 
 * A part of this file comes from the gnome keyboard capplet (control-center):
 * Copyright (C) 2003 Sergey V. Oudaltsov <svu@users.sourceforge.net>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */

#ifndef _XKB_CONFIG_H_
#define _XKB_CONFIG_H_

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <glib.h>
#include <glib/gstdio.h>
#include <libxklavier/xklavier.h>

#include <gtk/gtk.h>

/* LXDE GARBAGE: #include <lxpanel/plugin.h> */

typedef enum
{
    GROUP_POLICY_GLOBAL     = 0,
    GROUP_POLICY_PER_WINDOW     = 1,
    GROUP_POLICY_PER_APPLICATION    = 2
} t_group_policy;

typedef struct
{
    gchar*          model;
    gchar*          layouts;
    gchar*          variants;
    gchar*          options;
    gchar*          toggle_option;
} t_xkb_kbd_config;

typedef struct
{
    /*LXDE GARBAGE:     Plugin    			* plugin; */
    GtkWidget 			* mainw,
						* tray_icon;
  	gchar 	  			* current;

    t_group_policy      group_policy;
    gint                default_group;
    gboolean            never_modify_config, config_changed;
    t_xkb_kbd_config*   kbd_config;
    gint 				next;
} t_xkb_settings;


typedef void        (*XkbCallback)                  (gint current_group,
                                                     gboolean groups_changed,
                                                     gpointer user_data);

typedef struct
{
    XklEngine			 *engine;

    gchar               **group_names;
    gchar               **variants;
    t_xkb_settings       *settings;
    GHashTable           *variant_index_by_group;


    GHashTable           *application_map;
    GHashTable           *window_map;

    guint                 current_window_id;
    guint                 current_application_id;

    gint                  group_count;

    XkbCallback           callback;
    gpointer              callback_data;


    XklConfigRec         *config_rec;
} XkbConfig;

/*t_xkb_settings * xkb_settings_new( *LXDE GARBAGE Plugin * p *);*/

gboolean   	xkb_config_initialize            	    (XkbConfig *config, t_xkb_settings *settings,
                                                     XkbCallback callback, 
                                                     gpointer data);
void        xkb_config_finalize                     ();
gboolean    xkb_config_update_settings              (XkbConfig* config, t_xkb_settings *settings);
gint        xkb_config_get_group_count              ();
gchar*      xkb_config_get_group_map               	(XkbConfig* config,
                                                     gint group);
gchar*      xkb_config_get_variant_map 				(XkbConfig* config,
                                                     gint group);
gboolean    xkb_config_set_group                    (XkbConfig* config, gint group);
gboolean    xkb_config_next_group                   (XkbConfig* config);
gint        xkb_config_variant_index_for_group      (XkbConfig* config, gint group);
gchar*		xkb_config_get_layout_desc				(XkbConfig* config, gchar *group, gchar *variant);

void 		xkb_config_add_layout					(XkbConfig* config, gchar *group, gchar *variant);
void 		xkb_config_remove_group					(XkbConfig* config, gint group);
void        xkb_config_window_changed               (XkbConfig* config,
                                                     guint new_window_id,
                                                     guint application_id);
void        xkb_config_application_closed           (XkbConfig* config,
                                                     guint application_id);
void        xkb_config_window_closed                (XkbConfig* config,
                                                     guint window_id);

void        xkb_config_state_changed                (XklEngine *engine,
                                                     XklEngineStateChange *change,
                                                     gint group, 
                                                     gboolean restore,
                                                     XkbConfig* config);

void        xkb_config_xkl_config_changed           (XklEngine *engine,
                                                     XkbConfig* config);

GdkFilterReturn handle_xevent                       (GdkXEvent * xev,
                                                     GdkEvent * event,
                                                     XkbConfig* config);

/* Probablt useless: void        xkb_config_update_configuration     (t_xkb_settings *settings); */
static void xkb_config_free                         (XkbConfig* config);
static void xkb_config_initialize_xkb_options       (XkbConfig* config, t_xkb_settings *settings);



/* USELSS: gui-related void update_display( t_xkb_settings * ); */

/* TODO: remove this function - xkl structures should not be used outside xkb-config */
/* TODO: ^^ */
XklConfigRegistry*
            xkb_config_get_xkl_registry             ();
gint        xkb_config_get_max_layout_number        ();

#ifdef DEBUG

#define XKB_DEBUG(...) \
    do { g_fprintf (stderr, "[[ XFCE XKB PLUGIN ]]: "__VA_ARGS__); g_fprintf (stderr, "\n"); } while (0)

#define XKB_DEBUG_KBD(kbd, msg) g_printf("DUMPING KEYBOARD SETTINGS [[[%s]]] {%d}: ", msg, kbd);\
    if (kbd) { \
        g_printf ("\n\
          model: %s [%d]\n\
          layouts: %s [%d]\n\
          variants: %s [%d]\n\
          options: %s [%d]\n", \
                kbd->model, kbd->model, \
                kbd->layouts, kbd->layouts, \
                kbd->variants, kbd->variants, \
                kbd->options, kbd->options); \
    } else { \
        g_printf("NULL\n"); \
    }

#define XKB_DEBUG_CONFIG_REC(crec, msg) g_printf("DUMPING CONFIG REC [[[%s]]] {%d}: ", msg, (int) crec);\
    if (crec) { \
        g_printf ("\n\
            model: %s [%d]\n\
            layouts: %s [%d]\n\
            variants: %s [%d]\n", \
                crec->model, (int) crec->model, \
                g_strjoinv (",", crec->layouts), (int) crec->layouts, \
                g_strjoinv (",", crec->variants), (int) crec->variants); \
    } else { \
        g_printf ("NULL\n"); \
    }

#define XKB_DEBUG_GROUP_NAMES(groupnames, i, count) \
    for (i = 0; i < count; i++) {\
        if (groupnames && groupnames[i]) { \
            XKB_DEBUG("group : %s", groupnames[i]); \
        } \
    }

#else

#define XKB_DEBUG(...) 
#define XKB_DEBUG_KBD(kbd, msg)
#define XKB_DEBUG_CONFIG_REC(crec, msg)
#define XKB_DEBUG_GROUP_NAMES(groupnames, i, count)

#endif

#endif

