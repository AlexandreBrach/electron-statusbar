#!/usr/bin/python

# -*- coding: utf-8 -*-

import dbus
import dbus.service
import gobject
import time

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

BUS_NAME = 'org.alexandrebrach.toolbar.calendar'
OBJECT_PATH = '/org/alexandrebrach/toolbar/calendar'
DBUS_INTERFACE = 'org.alexandrebrach.toolbar'

class Emitter(dbus.service.Object):
    def __init__(self, bus_name, object_path):
        bus = dbus.SessionBus()
        bus.request_name( bus_name )
        busName = dbus.service.BusName(bus_name, bus=bus)
        dbus.service.Object.__init__(self, busName, object_path)
        self.data = self._get_time()

    def _get_time(self):
        t=time.localtime()
        return '{"time":"' + str(t.tm_hour) + ':' + str(t.tm_min) + '"}'

    @dbus.service.signal(dbus_interface=DBUS_INTERFACE, signature='')
    def changes(self, *data):
        self.data = self._get_time()
        return True

    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='', out_signature='s')
    def getState(self):
        return self.data

e = Emitter( BUS_NAME, OBJECT_PATH )

def run():
    e.changes()
    return True

gobject.timeout_add( 30000, run )
loop = gobject.MainLoop()
e.changes()
loop.run()
