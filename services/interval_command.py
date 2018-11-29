
import sys
import dbus
import dbus.service
from gi.repository import GLib
import time

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

class IntervalCommand(dbus.service.Object):

    DBUS_INTERFACE = 'org.alexandrebrach.toolbar'

    def __init__(self, bus_name, object_path, interval):
        bus = dbus.SessionBus()
        bus.request_name( bus_name )
        busName = dbus.service.BusName(bus_name, bus=bus)
        dbus.service.Object.__init__(self, busName, object_path)
        self.data = self._refresh_data()
        self.interval = interval
        self.debug = False
        self.loop = GLib.MainLoop()

    @dbus.service.signal(dbus_interface=DBUS_INTERFACE, signature='')
    def changes(self, *data):
        self.data = self._refresh_data()
        self.print(self.data)
        return True

    def print(self,data):
        if self.debug:
            print(data)
            sys.stdout.flush()


    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='', out_signature='s')
    def getState(self):
        return self.data

