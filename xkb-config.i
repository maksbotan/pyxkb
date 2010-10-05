%module kbdd
%{
#include "libkbdd.h"
#include <X11/Xlib.h>
#include <glib.h>
typedef struct
{
   PyObject *func, *data;
} CallBack;

typedef void (*KbddCallback)(unsigned int, void*);

typedef struct
{
    CallBack* __swig_callback;
    Display*  __display;
} Kbdd;

void kbdd_callback_marshal(unsigned int group,
                          void* user_data)
{
        CallBack* callback;
        callback = (CallBack*) user_data;
        PyGILState_STATE state;
        int retval;

        state = PyGILState_Ensure();
                        
        if (callback->data != NULL)
            PyObject_CallFunction(callback->func, "iO", group, callback->data);
        else
            Py_INCREF(Py_None);
            PyObject_CallFunction(callback->func, "iO", group, Py_None);
                                                                
        PyGILState_Release(state);

        /*free (callback);*/

        return;
}

typedef enum
{
        GROUP_POLICY_GLOBAL     = 0,
        GROUP_POLICY_PER_WINDOW     = 1,
        GROUP_POLICY_PER_APPLICATION    = 2
} t_group_policy;

%}

typedef struct
{
    CallBack* __swig_callback;
    Display*  __display;
} Kbdd;

%extend Kbdd {
    Kbdd(PyObject* callback, PyObject* userdata){
        Kbdd* kbdd;

        kbdd = g_new0(Kbdd, 1);

        Kbdd_init();
        Display* display;
        display = Kbdd_initialize_display();
        Kbdd_initialize_listeners(display);
        
        kbdd->__swig_callback = malloc(sizeof(CallBack));
        kbdd->__swig_callback->func = callback;
        kbdd->__swig_callback->data = userdata;

        kbdd->__display = display;

        Py_INCREF(callback);
        Py_XINCREF(userdata);

        Kbdd_setupUpdateCallback(kbdd_callback_marshal,kbdd->__swig_callback);

        return kbdd;
    }

    ~Kbdd(){
        if (self != NULL)
            Kbdd_clean();
            free (self->__swig_callback);
            g_free(self);
    }

    void start(){
        Kbdd_default_loop(self->__display);
    }
    
    void next_group(){
        /*TODO: when implemented in libkbdd.c*/
        return;
    }
    
    void set_policy(t_group_policy policy){
        /*TODO: when implemented in libkbdd.c*/
        return;
    }

    char* get_current_layout(){
        /*TODO: when implemented in libkbdd.c*/
        return "us";
    }
}
