#!/usr/bin/python

# -*- coding: utf-8 -*-

import sys
import dbus
import dbus.service
import time

from multiprocessing import Process

sys.path.append( '.' )

from DBusProvider.Battery import BatteryService

BUS_NAME = 'org.alexandrebrach.toolbar.battery'
OBJECT_PATH = '/org/alexandrebrach/toolbar/battery'
DBUS_INTERFACE = 'org.alexandrebrach.toolbar'

provider = BatteryService()

class Emitter(dbus.service.Object):
    def __init__(self, bus_name, object_path):
        bus = dbus.SessionBus()
        bus.request_name( bus_name )
        busName = dbus.service.BusName(bus_name, bus=bus)
        dbus.service.Object.__init__(self, busName, object_path)
        self.data = ""

    @dbus.service.signal(dbus_interface=DBUS_INTERFACE, signature='')
    def changes(self, *data):
        self.data = provider.serializeDevices()
        print(self.data)
        return True

    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='', out_signature='s')
    def getState(self):
        return self.data

e = Emitter( BUS_NAME, OBJECT_PATH )

provider.onDeviceChange( e.changes )

def run():
    e.changes()
    return True


while True:
    action_process = Process(target=run)
    action_process.start()
    action_process.join()
    action_process.terminate()
    time.sleep(10)

