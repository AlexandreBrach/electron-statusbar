#!/usr/bin/python

# -*- coding: utf-8 -*-

import sys
import dbus
import dbus.service
import gobject

sys.path.append( '.' )

from DBusProvider.NetworkManager import NetworkManagerService,NetworkInterface

BUS_NAME = 'org.alexandrebrach.toolbar.network'
OBJECT_PATH = '/org/alexandrebrach/toolbar/network'
DBUS_INTERFACE = 'org.alexandrebrach.toolbar'

provider = NetworkManagerService()

class Emitter(dbus.service.Object):
    def __init__(self, bus_name, object_path):
        bus = dbus.SessionBus()
        bus.request_name( bus_name )
        busName = dbus.service.BusName(bus_name, bus=bus)
        dbus.service.Object.__init__(self, busName, object_path)
        self.data = ""

    @dbus.service.signal(dbus_interface=DBUS_INTERFACE, signature='')
    def changes(self, *data):
        r = provider.serializeDevices()
        self.data = r
        print r
        return True

    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='', out_signature='s')
    def getState(self):
        return self.data

e = Emitter( BUS_NAME, OBJECT_PATH )

provider.onInterfacesChange( e.changes )

loop = gobject.MainLoop()
e.changes()
loop.run()
