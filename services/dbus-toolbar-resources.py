#!/usr/bin/python

# -*- coding: utf-8 -*-

import json
import shlex
from subprocess import Popen,PIPE
from gi.repository import GLib

from interval_command import IntervalCommand

BUS_NAME = 'org.alexandrebrach.toolbar.resources'
OBJECT_PATH = '/org/alexandrebrach/toolbar/resources'

class Emitter(IntervalCommand):

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

    def _refresh_data(self):

        result = {}
        self._add_mem_stat(result)
        self._add_cpu_stat(result)

        return json.dumps(result)


e = Emitter( BUS_NAME, OBJECT_PATH, 3000 )

def run():
    e.changes()
    return True

GLib.timeout_add( e.interval, run )
e.debug = True
e.changes()
e.loop.run()
