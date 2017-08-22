#!/usr/bin/python

# -*- coding: utf-8 -*-

import dbus
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

class BatteryDBUS:

    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.SERVICE = 'org.freedesktop.UPower'
        self.bus = dbus.SystemBus()

    def getDevices(self):
        OBJECT =  '/org/freedesktop/UPower'
        INTERFACE =  'org.freedesktop.UPower'
        proxy = self.bus.get_object( self.SERVICE, OBJECT )
        return proxy.EnumerateDevices(dbus_interface=INTERFACE)

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
        self.bus.add_signal_receiver(callback,
                signal_name=None,
                dbus_interface=None,
                bus_name=None,
                path=obj)

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
        # r = []
        # r.append( "State : " + self.State )
        # r.append( "Interface : " + self.Interface )
        # r.append( "Device Type : " + str( self.DeviceType ) )
        # r.append( "Real : " + self.Real )
        # r.append( "Driver : " + self.Driver )
        # r.append( "Udi : " + self.Udi )

        # if self.ActiveConnection != None:
            # r.append( "Connected :" + self.ActiveConnection.State )
            # r.append( "VPN :" + self.ActiveConnection.Vpn )
            # r.append( "Connection type :" + self.ActiveConnection.Type )
            # r.append( "Connection id :" + self.ActiveConnection.Id )
        # return "\n".join( r )

        clss = ['network_interface']
        if 100 == self.State :
             clss.append( "active" )
        r = '<'
        if 1 == self.DeviceType:
            clss.append( "ethernet" )
        if 2 == self.DeviceType:
            clss.append( "wifi" )
        if 16 == self.DeviceType:
            clss.append( "vpn" )
        r = '<div class="' + ' '.join( clss ) + '">'
        r += self.ActiveConnection.Id
        r += '</div>'
        return r
