#!/usr/bin/python

# -*- coding: utf-8 -*-

import dbus
import json
import dbus.service
from gi.repository import GLib
import time
import shlex
from subprocess import Popen,PIPE

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

BUS_NAME = 'org.alexandrebrach.toolbar.resources'
OBJECT_PATH = '/org/alexandrebrach/toolbar/resources'
DBUS_INTERFACE = 'org.alexandrebrach.toolbar'

class Emitter(dbus.service.Object):
    def __init__(self, bus_name, object_path):
        bus = dbus.SessionBus()
        bus.request_name( bus_name )
        busName = dbus.service.BusName(bus_name, bus=bus)
        dbus.service.Object.__init__(self, busName, object_path)
        self.data = self._get_stats()

    def _add_mem_stat(self, dico):
        '''
        add memory stats to the dict
        '''
        free = str(Popen(["free"], stdout=PIPE).stdout.read())
        values = shlex.split(free.split("\\n")[1])
        data=["_","total","used","free","shared","buff_cache","available"]

        for i, key in enumerate(data):
            dico[key] = values[i]

    def _add_cpu_stat(self, dico):
        '''
        add memory stats to the dict
        '''
        free = str(Popen(["mpstat"], stdout=PIPE).stdout.read())
        values = shlex.split(free.split("\\n")[3])
        data=["_", "_", "_", "cpu_usr","cpu_nice","cpu_sys","cpu_iowait","cpu_irq","cpu_soft", "cpu_steal", "cpu_quest","cpu_gnice", "cpu_idle",]

        for i, key in enumerate(data):
            dico[key] = values[i]

    def _get_stats(self):

        result = {}
        self._add_mem_stat(result)
        self._add_cpu_stat(result)

        return json.dumps(result)

    @dbus.service.signal(dbus_interface=DBUS_INTERFACE, signature='')
    def changes(self, *data):
        self.data = self._get_stats()
        print( self.data )
        return True

    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='', out_signature='s')
    def getState(self):
        return self.data

e = Emitter( BUS_NAME, OBJECT_PATH )

def run():
    e.changes()
    return True

GLib.timeout_add( 3000, run )
loop = GLib.MainLoop()
e.changes()
loop.run()
