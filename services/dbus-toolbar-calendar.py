#!/usr/bin/python

# -*- coding: utf-8 -*-

import dbus
import dbus.service
from datetime import date,datetime,timedelta
import time

from dbus.mainloop.glib import DBusGMainLoop
from multiprocessing import Process

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
        self.monthName=('janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre')
        self.data = self._serializeResult(self._getDays())
        self.month=None

    def _getDays(self):
        """
        Return informations about the 8 next days
        """
        week = [datetime.now()]
        dayDelta = timedelta(1)

        d_of_w = week[0].isoweekday()%7
        days = [(week[0].day,d_of_w+1)]
        self.month=self.monthName[week[0].month-1]

        for i in range(1,8):
            week.append(week[i-1]+dayDelta)
            days.append((week[i].day,((d_of_w+i)%7+1)))

        return days

    def _serializeResult(self, days):
        table_result = []
        for d in days:
            table_result.append( '{"n":'+str(d[0])+',"dayOfWeek":'+str(d[1])+'}')
        return "["+",".join(table_result)+"]"


    @dbus.service.signal(dbus_interface=DBUS_INTERFACE, signature='')
    def changes(self, *data):
        days = self._getDays()
        self.data = '{"month":"'+self.month+'","days":'+self._serializeResult(days)+'}'
        print(self.data)
        return True

    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='', out_signature='s')
    def getState(self):
        return self.data

e = Emitter( BUS_NAME, OBJECT_PATH )

def run():
    e.changes()
    return True

while True:
    action_process = Process(target=run)
    action_process.start()
    action_process.join()
    action_process.terminate()
    time.sleep(10)

# gobject.timeout_add( 60000, run )
# loop = gobject.MainLoop()
# e.changes()
# loop.run()
