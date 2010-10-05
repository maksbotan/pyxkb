%module kbdd
%{
#include "libkbdd.h"
typedef struct
{
   PyObject *func, *data;
} CallBack;

typedef void (*KbddCallback)(unsigned int, void*);

typedef struct
{
    void* some;
} Kbdd;

void kbdd_callack_marshal(unsigned int group,
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
    void* some;
} Kbdd;

%extend Kbdd {
    Kbdd(PyObject* callback, PyObject* userdate){
        return;
    }
}
