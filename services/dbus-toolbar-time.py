#!/usr/bin/python

# -*- coding: utf-8 -*-

from interval_command import IntervalCommand
import time
from gi.repository import GLib

BUS_NAME = 'org.alexandrebrach.toolbar.time'
OBJECT_PATH = '/org/alexandrebrach/toolbar/time'

class Emitter(IntervalCommand):

    def _refresh_data(self):
        t=time.localtime()
        return '{"time":"' + str(t.tm_hour).rjust(2,'0') + ':' + str(t.tm_min).rjust(2,'0') + '"}'


e = Emitter( BUS_NAME, OBJECT_PATH, 1000 )

def run():
    e.changes()
    return True

GLib.timeout_add( e.interval, run )
e.debug = True
e.changes()
e.loop.run()
