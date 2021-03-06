/* vim: set backspace=2 ts=4 softtabstop=4 sw=4 cinoptions=>4 expandtab autoindent smartindent: */
/* xkb-config.c
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

#include "xkb-config.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <libxklavier/xklavier.h>

#include <glib.h>
#include <gtk/gtk.h>
#include <gdk/gdkx.h>

/*LXDE GARBAGE: #include <lxpanel/plugin.h> */

#ifndef DEBUG
#define G_DISABLE_ASSERT
#endif

/* REFACTORED: XkbConfig *config; */

/* ---------------------- implementation ------------------------- */

/* USELESS: gui-related
void update_display( t_xkb_settings * settings )
{
    panel_draw_label_text(settings -> plugin -> panel,
                          settings -> tray_icon,
                          g_utf8_strup(settings->current,-1),
                          TRUE);
}
*/

gboolean
xkb_config_initialize (XkbConfig *config, t_xkb_settings *settings,
                       XkbCallback callback,
                       gpointer callback_data) 
{
	gint cur;

    g_assert (settings != NULL);

    /*config = g_new0 (XkbConfig, 1);*/

    config->settings = settings;
    config->callback = callback;
    config->callback_data = callback_data;

    config->engine = xkl_engine_get_instance (GDK_DISPLAY ());

    if (!config->engine)
    {
        return FALSE;
    }

    xkb_config_update_settings (config, settings);

    xkl_engine_set_group_per_toplevel_window (config->engine, FALSE);

    /*Current group*/

    cur = xkb_config_get_current_group(config);

    config->settings->current = g_strdup(config->group_names[cur]);


    xkl_engine_start_listen (config->engine, XKLL_TRACK_KEYBOARD_STATE | XKLL_MANAGE_WINDOW_STATES);

    g_signal_connect (config->engine, 
            "X-state-changed", 
            G_CALLBACK (xkb_config_state_changed), 
            config);
    g_signal_connect (config->engine,
            "X-config-changed",
            G_CALLBACK (xkb_config_xkl_config_changed),
            config);
    g_signal_connect (config->engine,
            "new-toplevel-window",
            G_CALLBACK (xkb_config_window_changed),
            config);

    gdk_window_add_filter (NULL, (GdkFilterFunc) handle_xevent, config);

    return TRUE;
}

static void
xkb_config_initialize_xkb_options (XkbConfig* config, t_xkb_settings *settings)
{
    XklConfigRegistry *registry;
    XklConfigItem *config_item;
    GHashTable *index_variants;
    gchar **group;
    gint val, i;
    gpointer pval;
    gboolean flag = FALSE;

    XklState *state = xkl_engine_get_current_state (config->engine);
    group = config->config_rec->layouts;
    config->group_count = 0;
    while (*group)
    {
        group++;
        config->group_count++;
    }


    xkb_config_free (config);
    
    config->window_map = g_hash_table_new (g_direct_hash, NULL);
    config->application_map = g_hash_table_new (g_direct_hash, NULL);

    registry = xkl_config_registry_get_instance (config->engine);
    xkl_config_registry_load (registry, FALSE);
    
    config_item = xkl_config_item_new ();

    config->group_names = (gchar **) g_new0 (typeof (gchar **), config->group_count);
    config->variants = (gchar **) g_new0 (typeof (gchar **), config->group_count);
    config->variant_index_by_group = g_hash_table_new (NULL, NULL);
    index_variants = g_hash_table_new (g_str_hash, g_str_equal);

    for (i = 0; i < config->group_count; i++)
    {
        g_stpcpy (config_item->name, config->config_rec->layouts[i]);
        config->group_names[i] = g_strdup (config->config_rec->layouts[i]);


        if (config->config_rec->variants[i] != NULL)
        {
        	strcpy(config_item->name,config->config_rec->variants[i]);
        }
        config->variants[i] = (config->config_rec->variants[i] == NULL)
            ? g_strdup ("") : g_strdup (config->config_rec->variants[i]);

        pval = g_hash_table_lookup (
                index_variants, 
                config->group_names[i]
        );
        val = (pval != NULL) ? GPOINTER_TO_INT (pval) : 0;
        val++;
        g_hash_table_insert (
                config->variant_index_by_group, 
                config->group_names[i], 
                GINT_TO_POINTER (val)
        );
        g_hash_table_insert (
                index_variants,
                config->group_names[i],
                GINT_TO_POINTER (val)
        );
    }
    g_hash_table_destroy (index_variants);
}

static void
xkb_config_free (XkbConfig* config)
{
    g_assert (config != NULL);

    if (config->group_names) g_free (config->group_names);
    if (config->variants) g_free (config->variants);

    if (config->variant_index_by_group)
    	g_hash_table_destroy (config->variant_index_by_group);

    if (config->window_map)
    	g_hash_table_destroy (config->window_map);
    if (config->application_map)
    	g_hash_table_destroy (config->application_map);
}

void 
xkb_config_finalize (XkbConfig* config) 
{
    xkb_config_free (config);

    gdk_window_remove_filter (NULL, (GdkFilterFunc) handle_xevent, config);

    xkl_engine_stop_listen (config->engine, XKLL_TRACK_KEYBOARD_STATE | XKLL_MANAGE_WINDOW_STATES);
}

gint
xkb_config_get_current_group (XkbConfig *config)
{
    XklState* state = xkl_engine_get_current_state (config->engine);
    return state->group;
}

gboolean
xkb_config_set_group (XkbConfig *config, gint group)
{
    g_assert (config != NULL);

    if (G_UNLIKELY (group < 0 || group >= config->group_count))
    {
        return FALSE;
    }

    xkl_engine_lock_group (config->engine, group);

    return TRUE;
}

gboolean
xkb_config_next_group (XkbConfig* config)
{
    xkl_engine_lock_group (config->engine,
            xkl_engine_get_next_group (config->engine));

    return TRUE;
}

gboolean
xkb_config_update_settings (XkbConfig* config, t_xkb_settings *settings)
{
    gboolean activate_settings = FALSE;
    
    gchar **opt;
    gchar **prefix;

    g_assert (config != NULL);
    g_assert (settings != NULL);

    config->settings = settings;

    if (config->config_rec == NULL)
    {
        config->config_rec = xkl_config_rec_new ();
    }

    if (settings->kbd_config == NULL || settings->never_modify_config)
    {
        xkl_config_rec_get_from_server (config->config_rec, config->engine);

        settings->kbd_config = g_new (t_xkb_kbd_config, 1);
        settings->kbd_config->model = g_strdup (config->config_rec->model);
        settings->kbd_config->layouts = g_strjoinv (",", config->config_rec->layouts);
        settings->kbd_config->variants = g_strjoinv (",", config->config_rec->variants);
        settings->kbd_config->options = strdup("grp:alt_shift_toggle");

        if (strcmp ("", settings->kbd_config->options) == 0)
        {
            settings->kbd_config->options = NULL;
        }

    }
    else
    {
        activate_settings = TRUE;
        config->config_rec->model = g_strdup (settings->kbd_config->model);
        config->config_rec->layouts = g_strsplit(settings->kbd_config->layouts, ",", -1);
        config->config_rec->variants = g_strsplit_set (settings->kbd_config->variants, ",", 0);
        config->config_rec->options = g_strsplit_set (settings->kbd_config->options, ",", 0);

    }

    /* select the first "grp" option and use it (should be fixed to support more options) */
    opt = config->config_rec->options;
    while (opt && *opt)
    {
        prefix = g_strsplit(*opt, ":", 2);
        if (prefix && strcmp(*prefix, "grp") == 0)
        {
            settings->kbd_config->toggle_option = *opt;
            break;
        }
        opt++;
    }
    
    if (activate_settings && !settings->never_modify_config)
    {
        xkl_config_rec_activate (config->config_rec, config->engine);
    }

    xkb_config_initialize_xkb_options (config, settings);
    /* update_display(settings); */

    return TRUE;
}

void
xkb_config_window_changed (XklEngine* engine, guint new_window_id, guint application_id, XkbConfig* config)
{
    g_assert (config != NULL);

    gint group;
    gpointer key, value;
    GHashTable *hashtable;
    guint id;
    gint DEBUG_FOUND = 0;

    id = 0;
    hashtable = NULL;

    switch (config->settings->group_policy)
    {
        case GROUP_POLICY_GLOBAL:
            return;

        case GROUP_POLICY_PER_WINDOW:
            hashtable = config->window_map;
            id = new_window_id;
            config->current_window_id = id;
            break;

        case GROUP_POLICY_PER_APPLICATION:
            hashtable = config->application_map;
            id = application_id;
            config->current_application_id = id;
            break;
    }

    group = config->settings->default_group;

    if (g_hash_table_lookup_extended (hashtable, GINT_TO_POINTER (id), &key, &value))
    {
        group = GPOINTER_TO_INT (value);
        DEBUG_FOUND = 1;
    }

    g_hash_table_insert (
            hashtable,
            GINT_TO_POINTER (id),
            GINT_TO_POINTER (group)
    );

    xkb_config_set_group (config, group);
}

void
xkb_config_application_closed (XkbConfig* config, guint application_id)
{
    g_assert (config != NULL);

    switch (config->settings->group_policy)
    {
        case GROUP_POLICY_GLOBAL:
        case GROUP_POLICY_PER_WINDOW:;
            return;

        case GROUP_POLICY_PER_APPLICATION:
            g_hash_table_remove (
                    config->application_map,
                    GINT_TO_POINTER (application_id)
            );

            break;
    }
}

void
xkb_config_window_closed (XkbConfig* config, guint window_id)
{
    g_assert (config != NULL);

    switch (config->settings->group_policy)
    {
        case GROUP_POLICY_GLOBAL:
        case GROUP_POLICY_PER_APPLICATION:
            return;

        case GROUP_POLICY_PER_WINDOW:
            g_hash_table_remove (
                    config->window_map,
                    GINT_TO_POINTER (window_id)
            );

            break;
    }
}


gint 
xkb_config_get_group_count (XkbConfig* config) 
{ 
    g_assert (config != NULL);

    return config->group_count;
}

gchar*
xkb_config_get_group_map (XkbConfig* config, gint group)
{
    g_assert (config != NULL);

    if (G_UNLIKELY (group >= config->group_count))
        return NULL;

    if (group == -1)
        group = xkb_config_get_current_group (config);

    gchar *result = config->group_names[group];
    return result;
}

gchar*
xkb_config_get_variant_map (XkbConfig* config, gint group)
{
    g_assert (config != NULL);

    if (G_UNLIKELY (group >= config->group_count))
        return NULL;

    if (group == -1)
        group = xkb_config_get_current_group (config);

    return config->variants[group];
}

void
xkb_config_state_changed (XklEngine *engine,
                          XklEngineStateChange *change,
                          gint group, 
                          gboolean restore,
                          XkbConfig* config)
{
    if (change == GROUP_CHANGED)
    {
        switch (config->settings->group_policy)
        {
            case GROUP_POLICY_GLOBAL:
                break;

            case GROUP_POLICY_PER_WINDOW:
                g_hash_table_insert (
                        config->window_map,
                        GINT_TO_POINTER (config->current_window_id),
                        GINT_TO_POINTER (group)
                );
                break;

            case GROUP_POLICY_PER_APPLICATION:
                g_hash_table_insert (
                        config->application_map,
                        GINT_TO_POINTER (config->current_application_id),
                        GINT_TO_POINTER (group)
                );
            break;
        }

        if (config->callback != NULL)
        {
        	config->settings->current = config->group_names[group];
        	config->callback (group, FALSE, config->callback_data);
        }

    }
}

void
xkb_config_xkl_config_changed (XklEngine* engine, XkbConfig* config)
{
    g_free (config->settings->kbd_config);
    config->settings->kbd_config = NULL;
    xkb_config_update_settings (config, config->settings);

    if (config->callback != NULL) 
        config->callback (xkb_config_get_current_group (config), TRUE, config->callback_data);
}

gint
xkb_config_variant_index_for_group (XkbConfig* config, gint group)
{
    g_return_val_if_fail (config != NULL, 0);

    gpointer presult;
    gint result;
    gchar *key;

    if (group == -1) group = xkb_config_get_current_group (config);

    key = config->group_names[group];

    presult = g_hash_table_lookup (
            config->variant_index_by_group,
            key
    );
    if (presult == NULL) return 0;

    result = GPOINTER_TO_INT (presult);
    result = (result <= 0) ? 0 : result - 1; 
    return result;
}

GdkFilterReturn
handle_xevent (GdkXEvent * xev, GdkEvent * event, XkbConfig* config)
{
    /*printf ("Event: %d\n", ((XEvent*) xev)->type);*/

    XEvent *xevent = (XEvent *) xev;
    
    /*printf ("return: %d\n", */xkl_engine_filter_events (config->engine, xevent)/*)*/;
   
    return GDK_FILTER_CONTINUE;
}

XklConfigRegistry*
xkb_config_get_xkl_registry (XkbConfig* config)
{
    XklConfigRegistry *registry;

    if (!config) return NULL;

    registry = xkl_config_registry_get_instance (config->engine);
    xkl_config_registry_load (registry, FALSE);

    return registry;
}

gint
xkb_config_get_max_layout_number (XkbConfig* config)
{
    if (config == NULL) return 0;
    return xkl_engine_get_max_num_groups (config->engine);
}

void xkb_config_add_layout(XkbConfig* config, gchar *group, gchar *variant)
{

	config->settings->kbd_config->layouts =
			g_strconcat(config->settings->kbd_config->layouts, ",", group, NULL);

	config->settings->kbd_config->variants =
			g_strconcat(config->settings->kbd_config->variants, ",", variant, NULL);

	xkb_config_update_settings(config, config->settings);
}

void xkb_config_remove_group(XkbConfig* config, gint group)
{
	gchar 	**groups,
			**variants;

	gint g_count, i, begin = 0;

	if (group == 0)
		begin = 1;

	g_count= xkb_config_get_group_count(config);

	groups = g_strsplit(config->settings->kbd_config->layouts,",", -1);
	variants = g_strsplit(config->settings->kbd_config->variants,",", -1);

	config->settings->kbd_config->layouts = g_strdup(groups[begin]);
	config->settings->kbd_config->variants = g_strdup(variants[begin]);


	for (i = 1; i < g_count; i++)
	{
		if (i != group)
		{
			config->settings->kbd_config->layouts =
					g_strconcat(config->settings->kbd_config->layouts, ",", groups[i], NULL);

			config->settings->kbd_config->variants =
					g_strconcat(config->settings->kbd_config->variants, ",", variants[i], NULL);
		}
	}
	xkb_config_update_settings(config, config->settings);
}

gchar *xkb_config_get_layout_desc(XkbConfig* config, gchar *group, gchar *variant)
{
	gchar *description;
	XklConfigRegistry *reg;
    reg = xkl_config_registry_get_instance (config->engine);
    xkl_config_registry_load (reg, FALSE);

	XklConfigItem *item;
	item = xkl_config_item_new();

	g_stpcpy(item->name ,group);

	xkl_config_registry_find_layout(reg, item);

	description = g_strdup(item->description);

	if (variant && strlen(variant) > 0)
	{
		g_stpcpy(item->name ,variant);
		xkl_config_registry_find_variant(reg, group, item);

		description = g_strconcat(description, " (", item->description,")", NULL);
	}

	return description;
}
