#!/usr/bin/python

# -*- coding: utf-8 -*-

import dbus
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

"""
NM_DEVICE_TYPE_UNKNOWN = 0
The device type is unknown.
NM_DEVICE_TYPE_ETHERNET = 1
The device is wired Ethernet device.
NM_DEVICE_TYPE_WIFI = 2
The device is an 802.11 WiFi device.
NM_DEVICE_TYPE_UNUSED1 = 3
Unused
NM_DEVICE_TYPE_UNUSED2 = 4
Unused
NM_DEVICE_TYPE_BT = 5
The device is Bluetooth device that provides PAN or DUN capabilities.
NM_DEVICE_TYPE_OLPC_MESH = 6
The device is an OLPC mesh networking device.
NM_DEVICE_TYPE_WIMAX = 7
The device is an 802.16e Mobile WiMAX device.
NM_DEVICE_TYPE_MODEM = 8
The device is a modem supporting one or more of analog telephone, CDMA/EVDO, GSM/UMTS/HSPA, or LTE standards to access a cellular or wireline data network.
NM_DEVICE_TYPE_INFINIBAND = 9
The device is an IP-capable InfiniBand interface.
NM_DEVICE_TYPE_BOND = 10
The device is a bond master interface.
NM_DEVICE_TYPE_VLAN = 11
The device is a VLAN interface.
NM_DEVICE_TYPE_ADSL = 12
The device is an ADSL device supporting PPPoE and PPPoATM protocols.
NM_DEVICE_TYPE_BRIDGE = 13
The device is a bridge interface.
"""

class NetWorkManagerDBUS:

    def __init__(self):
        # self.loop = DBusGMainLoop()
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        self.SERVICE =   'org.freedesktop.NetworkManager'
        # dbus.set_default_main_loop( self.loop )
        self.bus = dbus.SystemBus()
        # self.bus = dbus.SystemBus(mainloop=self.loop)

    def getDevices(self):
        OBJECT =    '/org/freedesktop/NetworkManager'
        INTERFACE =  'org.freedesktop.NetworkManager'
        proxy = self.bus.get_object( self.SERVICE, OBJECT )
        # proxy = dbus.SystemBus().get_object( self.SERVICE, OBJECT )
        return proxy.GetAllDevices(dbus_interface=INTERFACE)

    def getDevicesProperties( self, deviceName ):
        proxy = self.bus.get_object( self.SERVICE, deviceName )
        o = dbus.Interface( proxy , 'org.freedesktop.DBus.Properties' )
        return o.GetAll( 'org.freedesktop.NetworkManager.Device' )

    def getActiveConnectionProperties( self, objectPath ):
        proxy = self.bus.get_object( self.SERVICE, objectPath )
        o = dbus.Interface( proxy , 'org.freedesktop.DBus.Properties' )
        return o.GetAll( 'org.freedesktop.NetworkManager.Connection.Active')

    def attachNetworkInterfaceChanges( self, callback ):
        print 'attach to signal'
        obj='/org/freedesktop/NetworkManager/Settings'
        # proxy = self.bus.get_object( self.SERVICE, '/org/freedesktop/NetworkManager/Settings' )
        # proxy.connect_to_signal( "Test", callback, dbus_interface="org.freedesktop.NetworkManager.Settings" )
        self.bus.add_signal_receiver(callback,
                signal_name=None,
                dbus_interface=None,
                bus_name=None,
                path=obj)
        # self.bus.add_signal_receiver(callback,
                                # interface_keyword='org.freedesktop.NetworkManager.Settings',
                                # member_keyword='/org/freedesktop/NetworkManager/Settings')

class NetworkManagerService:

    def __init__(self):
        self.dbus = NetWorkManagerDBUS()

    def getLoop(self):
        return self.dbus.getLoop()

    def getAllDevices(self):
        dbusResult = self.dbus.getDevices()
        return self.assembleResult( dbusResult )

    def filterHardDevice( self, devices ):
        result = []
        for device in devices:
            if device.DeviceType in [1,2,16]:
                result.append( device )
        return result

    def getAllHardDevices( self ):
        devices = self.getAllDevices()
        return self.filterHardDevice( devices )
        # return self.assembleResult( dbusResult )

    def assembleResult( self, dbusResult ):
        devices = []
        for device in dbusResult:
            devices.append( NetworkInterface( device ))
        return devices

    def onInterfacesChange( self, callback ):
        self.dbus.attachNetworkInterfaceChanges( callback )

class ActiveConnection:

    def __init__( self, properties ):
        s = NetWorkManagerDBUS()
        prop = s.getActiveConnectionProperties( str( properties ) )
        self.Dhcp6Config=str(prop['Dhcp6Config'])
        self.Dhcp4Config=str(prop['Dhcp4Config'])
        self.Ip6Config=str(prop['Ip6Config'])
        self.Uuid=str(prop['Uuid'])
        self.Ip4Config=str(prop['Ip4Config'])
        self.Default=str(prop['Default'])
        self.SpecificObject=str(prop['SpecificObject'])
        self.State=str(prop['State'])
        self.Devices=str(prop['Devices'])
        self.Connection=str(prop['Connection'])
        self.Default6=str(prop['Default6'])
        self.Master=str(prop['Master'])
        self.Vpn=str(prop['Vpn'])
        self.Type=str(prop['Type'])
        self.Id=str(prop['Id'])
 
class NetworkInterface:

    def __init__( self, device ):
        s = NetWorkManagerDBUS()
        deviceProperties = s.getDevicesProperties( device )
        self.Ip6Config=str(deviceProperties['Ip6Config'])
        self.NmPluginMissing=str(deviceProperties['NmPluginMissing'])
        self.FirmwareMissing=str(deviceProperties['FirmwareMissing'])
        self.Autoconnect=str(deviceProperties['Autoconnect'])
        self.Capabilities=str(deviceProperties['Capabilities'])
        self.LldpNeighbors=str(deviceProperties['LldpNeighbors'])
        self.State=str(deviceProperties['State'])
        self.Ip4Address=str(deviceProperties['Ip4Address'])
        self.Real=str(deviceProperties['Real'])
        self.DriverVersion=str(deviceProperties['DriverVersion'])
        self.Driver=str(deviceProperties['Driver'])
        self.Metered=str(deviceProperties['Metered'])
        self.Interface=str(deviceProperties['Interface'])
        self.Udi=str(deviceProperties['Udi'])
        self.FirmwareVersion=str(deviceProperties['FirmwareVersion'])
        self.Dhcp6Config=str(deviceProperties['Dhcp6Config'])
        self.Dhcp4Config=str(deviceProperties['Dhcp4Config'])
        self.IpInterface=str(deviceProperties['IpInterface'])
        self.DeviceType=int(deviceProperties['DeviceType'])
        self.PhysicalPortId=str(deviceProperties['PhysicalPortId'])
        self.StateReason=str(deviceProperties['StateReason'])
        self.Mtu=str(deviceProperties['Mtu'])
        self.AvailableConnections=str(deviceProperties['AvailableConnections'])
        self.Managed=str(deviceProperties['Managed'])
        self.Ip4Config=str(deviceProperties['Ip4Config'])
        connection = deviceProperties['ActiveConnection']

        if connection != '/':
            self.ActiveConnection=ActiveConnection( connection ) 
        else:
            self.ActiveConnection=None

    def __str__(self):
        r = []
        r.append( "State : " + self.State )
        r.append( "Interface : " + self.Interface )
        r.append( "Device Type : " + str( self.DeviceType ) )
        r.append( "Real : " + self.Real )
        r.append( "Driver : " + self.Driver )
        r.append( "Udi : " + self.Udi )

        if self.ActiveConnection != None:
            r.append( "Connected :" + self.ActiveConnection.State )
            r.append( "VPN :" + self.ActiveConnection.Vpn )
            r.append( "Connection type :" + self.ActiveConnection.Type )
            r.append( "Connection id :" + self.ActiveConnection.Id )
        return "\n".join( r )
