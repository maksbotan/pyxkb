#!/usr/bin/env python

import threading
import dbus, dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import gobject

import kbdd

DBusGMainLoop(set_as_default=True)

class KbddDbus(dbus.service.Object):
    def __init__(self, bus, object_path):
        dbus.service.Object.__init__(self, bus, object_path)
        
        self.kbdd = None

    @dbus.service.signal(dbus_interface='ru.gentoo.Kbdd',
                         signature="")
    def GroupChanged(self):
        pass

    @dbus.service.method(dbus_interface='ru.gentoo.Kbdd',
                         in_signature='', out_signature='',
                         sender_keyword='sender')
    def NextGroup(self, sender=None):
        self.kbdd.next_group()
    
    @dbus.service.method(dbus_interface='ru.gentoo.Kbdd',
                         in_signature='i', out_signature='',
                         sender_keyword='sender')
    def SetPolicy(self, policy, sender=None):
        self.kbdd.set_policy(policy)

    def emitGroupChanged(self, group, dbus_object):
        dbus_object.GroupChanged()

if __name__ == '__main__':
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName('ru.gentoo.Kbdd', session_bus)
    
    dbus_object = KbddDbus(session_bus, '/ru/gentoo/Kbdd')
    kbd_daemon = kbdd.Kbdd(dbus_object.emitGroupChanged, None)

    dbus_object.kbdd = kbd_daemon
    
    threading.Thread(target=kbd_daemon.start).start()
    
    loop = gobject.MainLoop()
    loop.run()
