#!/usr/bin/python

# -*- coding: utf-8 -*-

import dbus

class NetWorkManagerDBUS:

    def __init__(self):
        self.SERVICE =   'org.freedesktop.NetworkManager'

    def getDevices(self):
        OBJECT =    '/org/freedesktop/NetworkManager'
        INTERFACE =  'org.freedesktop.NetworkManager'
        proxy = dbus.SystemBus().get_object( self.SERVICE, OBJECT )
        return proxy.GetAllDevices(dbus_interface=INTERFACE)

    def getDevicesProperties( self, deviceName ):
        proxy = dbus.SystemBus().get_object( self.SERVICE, deviceName )
        o = dbus.Interface( proxy , 'org.freedesktop.DBus.Properties' )
        return o.GetAll( 'org.freedesktop.NetworkManager.Device' )

    def getActiveConnectionProperties( self, objectPath ):
        proxy = dbus.SystemBus().get_object( self.SERVICE, objectPath )
        o = dbus.Interface( proxy , 'org.freedesktop.DBus.Properties' )
        return o.GetAll( 'org.freedesktop.NetworkManager.Connection.Active')

class NetworkManagerService:

    def __init__(self):
        self.dbus = NetWorkManagerDBUS()

    def getAllDevices(self):
        dbusResult = self.dbus.getDevices()
        return self.assembleResult( dbusResult )

    def filterHardDevice( self, devices ):
        result = []
        for device in devices:
            try:
                properties =  self.dbus.getDevicesProperties( device )
            except Exception as err:
                print err
                firwareVersion = ''
            else:
                firwareVersion = properties['FirmwareVersion']
            if ( firwareVersion != '' and firwareVersion != 'N/A' ):
                result.append( device )
        return result

    def getAllHardDevices( self ):
        devices = self.getAllDevices()
        dbusResult = self.filterHardDevice( devices )
        return self.assembleResult( dbusResult )

    def assembleResult( self, dbusResult ):
        devices = []
        for device in dbusResult:
            devices.append( NetworkInterface( device ))
        return devices


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
        self.DeviceType=str(deviceProperties['DeviceType'])
        self.PhysicalPortId=str(deviceProperties['PhysicalPortId'])
        self.StateReason=str(deviceProperties['StateReason'])
        self.Mtu=str(deviceProperties['Mtu'])
        self.AvailableConnections=str(deviceProperties['AvailableConnections'])
        self.Managed=str(deviceProperties['Managed'])
        self.Ip4Config=str(deviceProperties['Ip4Config'])
        # self.ActiveConnection=ActiveConnection( deviceProperties['ActiveConnection']) 
