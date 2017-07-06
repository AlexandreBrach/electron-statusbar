#!/usr/bin/python

# -*- coding: utf-8 -*-

import sys
import dbus

sys.path.append( '.' )

from DBusProvider.NetworkManager import NetworkManagerService,NetworkInterface
import gobject

provider = NetworkManagerService()
devices = provider.getAllHardDevices()
# devices = []
# for device in watchedDevices:
    # devices.append( NetworkInterface( device ))

for device in devices:
    print "Auto-connect : " + device.Autoconnect
    print "State : " + device.State
    print "Interface : " + device.Interface
    print "Device Type : " + device.DeviceType
    print "VPN :" + device.ActiveConnection.Vpn

