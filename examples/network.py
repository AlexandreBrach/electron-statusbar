#!/usr/bin/python

# -*- coding: utf-8 -*-

import sys
import dbus
import gobject

sys.path.append( '.' )

from DBusProvider.NetworkManager import NetworkManagerService,NetworkInterface

provider = NetworkManagerService()

def printHardDevices( *args ):
    devices = provider.getAllHardDevices()

    for device in devices:
        print "============================="
        print device

provider.onInterfacesChange( printHardDevices )

printHardDevices()
loop = gobject.MainLoop()
loop.run()
