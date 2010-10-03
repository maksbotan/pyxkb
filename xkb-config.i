%module xkb_config
%{
#include "xkb-config.h"
typedef struct
{
   PyObject *func, *data;
} CallBack;

void xkbconfig_callack_marshal(gint current_group,
                              gboolean groups_changed,
                              gpointer user_data)
{
        CallBack* callback;
        callback = (CallBack*) user_data;
        PyGILState_STATE state;
        PyObject *ret;
        int retval;

        state = PyGILState_Ensure();
                        
        if (callback->data != NULL)
            ret = PyObject_CallFunction(callback->func, "OO", callback->data);                                          
        else
            Py_INCREF(Py_None);
            ret = PyObject_CallFunction(callback->func, "O", Py_None);
                                                                
        PyGILState_Release(state);

        free (callback);

        return;
}
%}

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
    /*LXDE GARBAGE:     Plugin              * plugin; */
    GtkWidget           * mainw,
                        * tray_icon;
    gchar               * current;
    t_group_policy      group_policy;
    gint                default_group;
    gboolean            never_modify_config, config_changed;
    t_xkb_kbd_config*   kbd_config;
    gint                next;
} t_xkb_settings;



typedef struct
{
    XklEngine            *engine;
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

%extend XkbConfig {
    XkbConfig(t_xkb_settings* settings, PyObject* callback, PyObject* data){
        XkbConfig* config;
        CallBack* c_callback;

        c_callback = g_new0(CallBack, 1);
        c_callback->func = callback;
        c_callback->data = data;
        Py_INCREF(c_callback->func);
        Py_XINCREF(c_callback->data);

        config = g_new0(XkbConfig, 1);

        xkb_config_initialize(config, settings, (XkbCallback) xkbconfig_callack_marshal, c_callback);

        return config;
    }
}
