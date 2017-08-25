#!/usr/bin/python

# -*- coding: utf-8 -*-

import dbus
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

class NetWorkManagerDBUS:

    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.SERVICE =   'org.freedesktop.NetworkManager'
        self.bus = dbus.SystemBus()

    def getDevices(self):
        OBJECT =    '/org/freedesktop/NetworkManager'
        INTERFACE =  'org.freedesktop.NetworkManager'
        proxy = self.bus.get_object( self.SERVICE, OBJECT )
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

    def serializeDevices( self ):
        d = []
        for device in self.getAllDevices():
             d.append( str( device ) )
        return '[' + ','.join( d ) + ']'

    # def filterHardDevice( self, devices ):
        # result = []
        # for device in devices:
            # if device.DeviceType in [1,2,16]:
                # result.append( device )
        # return result

    # def getAllHardDevices( self ):
        # devices = self.getAllDevices()
        # return self.filterHardDevice( devices )

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
        self.Ip6Config=str(prop['Ip6Config'])
        self.Uuid=str(prop['Uuid'])
        self.Ip4Config=str(prop['Ip4Config'])
        self.Default=str(prop['Default'])
        self.SpecificObject=str(prop['SpecificObject'])
        self.State= str(prop['State'])
        # self.Devices=str(prop['Devices'])
        self.Connection=str(prop['Connection'])
        self.Default6=str(prop['Default6'])
        self.Master=str(prop['Master'])
        self.Vpn=str(prop['Vpn'])
        self.Type=str(prop['Type'])
        self.Id=str(prop['Id'])

    def __str__(self):
        r = []
        r.append( '"ip6Config":"' + self.Ip6Config + '"' )
        r.append( '"uuid":"' + self.Uuid + '"' )
        r.append( '"ip4Config":"' + self.Ip4Config+ '"'  )
        r.append( '"default":' + self.Default )
        r.append( '"specificObject":"' + self.SpecificObject + '"' )
        r.append( '"state":' + self.State )
        # r.append( '"devices":' + self.Devices )
        r.append( '"connection":"' + self.Connection + '"' )
        r.append( '"default6":' + self.Default6 )
        r.append( '"master":"' + self.Master + '"' )
        r.append( '"vpn":' + self.Vpn )
        r.append( '"type":"' + self.Type + '"' )
        r.append( '"id":"' + self.Id + '"' )
        return "{" + ",".join( r ) + "}"

class NetworkInterface:

    def __init__( self, device ):
        s = NetWorkManagerDBUS()
        deviceProperties = s.getDevicesProperties( device )
        self.NmPluginMissing=str(deviceProperties['NmPluginMissing'])
        self.FirmwareMissing=str(deviceProperties['FirmwareMissing'])
        self.Autoconnect=str(deviceProperties['Autoconnect'])
        self.Capabilities=str(deviceProperties['Capabilities'])
        # self.State=str(deviceProperties['State'])
        self.State=self.getState( str(deviceProperties['State']) )
        self.Ip4Address=str(deviceProperties['Ip4Address'])
        self.Real=str(deviceProperties['Real'])
        self.DriverVersion=str(deviceProperties['DriverVersion'])
        self.Driver=str(deviceProperties['Driver'])
        self.Metered=str(deviceProperties['Metered'])
        self.Interface=str(deviceProperties['Interface'])
        self.Udi=str(deviceProperties['Udi'])
        self.FirmwareVersion=str(deviceProperties['FirmwareVersion'])
        self.IpInterface=str(deviceProperties['IpInterface'])
        self.DeviceType= self.getDeviceType( str(deviceProperties['DeviceType']) )
        self.PhysicalPortId=str(deviceProperties['PhysicalPortId'])
        # Raison du changement d'etat (dbus.strut)
        # self.StateReason=str(deviceProperties['StateReason'])
        self.Mtu=str(deviceProperties['Mtu'])
        self.Managed=str(deviceProperties['Managed'])
        self.Ip4Config=str(deviceProperties['Ip4Config'])
        connection = deviceProperties['ActiveConnection']

        if connection != '/':
            self.ActiveConnection=ActiveConnection( connection )
        else:
            self.ActiveConnection=None

    def getState( self, value ):
        if '0' == value :
            """ The device is in an unknown state. """
            return 'NM_DEVICE_STATE_UNKNOWN'
        if '10' == value :
            """ The device is recognized but not managed by NetworkManager. """
            return 'NM_DEVICE_STATE_UNMANAGED'
        if '20' == value :
            """ The device cannot be used (carrier off, rfkill, etc). """
            return 'NM_DEVICE_STATE_UNAVAILABLE'
        if '30' == value :
            """ The device is not connected. """
            return 'NM_DEVICE_STATE_DISCONNECTED'
        if '40' == value :
            """ The device is preparing to connect. """
            return 'NM_DEVICE_STATE_PREPARE'
        if '50' == value :
            """ The device is being configured. """
            return 'NM_DEVICE_STATE_CONFIG'
        if '60' == value :
            """ The device is awaiting secrets necessary to continue connection. """
            return 'NM_DEVICE_STATE_NEED_AUTH'
        if '70' == value :
            """ The IP settings of the device are being requested and configured. """
            return 'NM_DEVICE_STATE_IP_CONFIG'
        if '80' == value :
            """ The device's IP connectivity ability is being determined. """
            return 'NM_DEVICE_STATE_IP_CHECK'
        if '90' == value :
            """ The device is waiting for secondary connections to be activated. """
            return 'NM_DEVICE_STATE_SECONDARIES'
        if '100' == value :
            """ The device is active. """
            return 'NM_DEVICE_STATE_ACTIVATED'
        if '110' == value :
            """ The device's network connection is being torn down. """
            return 'NM_DEVICE_STATE_DEACTIVATING'
        if '120' == value :
            """ The device is in a failure state following an attempt to activate it. """
            return 'NM_DEVICE_STATE_FAILED'
        return value

    def getDeviceType( self, value ):
        if '0' == value :
            """ The device type is unknown. """
            return 'NM_DEVICE_TYPE_UNKNOWN'
        if '1' == value :
            """ The device is wired Ethernet device. """
            return 'NM_DEVICE_TYPE_ETHERNET'
        if '2' == value :
            """ The device is an 802.11 WiFi device. """
            return 'NM_DEVICE_TYPE_WIFI'
        if '3' == value :
            """ Unused """
            return 'NM_DEVICE_TYPE_UNUSED1'
        if '4' == value :
            """ Unused """
            return 'NM_DEVICE_TYPE_UNUSED2'
        if '5' == value :
            """ The device is Bluetooth device that provides PAN or DUN capabilities. """
            return 'NM_DEVICE_TYPE_BT'
        if '6' == value :
            """ The device is an OLPC mesh networking device. """
            return 'NM_DEVICE_TYPE_OLPC_MESH'
        if '7' == value :
            """ The device is an 802.16e Mobile WiMAX device. """
            return 'NM_DEVICE_TYPE_WIMAX'
        if '8' == value :
            """ The device is a modem supporting one or more of analog telephone, CDMA/EVDO, GSM/UMTS/HSPA, or LTE standards to access a cellular or wireline data network. """
            return 'NM_DEVICE_TYPE_MODEM'
        if '9' == value :
            """ The device is an IP-capable InfiniBand interface. """
            return 'NM_DEVICE_TYPE_INFINIBAND'
        if '10' == value :
            """ The device is a bond master interface. """
            return 'NM_DEVICE_TYPE_BOND'
        if '11' == value :
            """ The device is a VLAN interface. """
            return 'NM_DEVICE_TYPE_VLAN'
        if '12' == value :
            """ The device is an ADSL device supporting PPPoE and PPPoATM protocols. """
            return 'NM_DEVICE_TYPE_ADSL'
        if '13' == value :
            """ The device is a bridge interface. """
            return 'NM_DEVICE_TYPE_BRIDGE'
        if '16' == value :
            """ The device is a VPN """
            "'"" (not referenced in the doc) """
            return 'NM_DEVICE_TYPE_VPN'
        return value

    def __str__(self):

        r = []
        r.append( '"nmPluginMissing":' + self.NmPluginMissing )
        r.append( '"firmwareMissing":' + self.FirmwareMissing )
        r.append( '"autoconnect":' + self.Autoconnect )
        r.append( '"capabilities":' + self.Capabilities )
        r.append( '"state":"' + self.State + '"' )
        r.append( '"ip4Address":' + self.Ip4Address )
        r.append( '"real":' + self.Real )
        r.append( '"driverVersion":"' + self.DriverVersion + '"' )
        r.append( '"driver":"' + self.Driver + '"' )
        r.append( '"metered":' + self.Metered )
        r.append( '"interface":"' + self.Interface + '"' )
        r.append( '"udi":"' + self.Udi + '"' )
        r.append( '"firmwareVersion":"' + self.FirmwareVersion + '"' )
        r.append( '"ipInterface":"' + self.IpInterface + '"' )
        r.append( '"deviceType":"' + self.DeviceType + '"' )
        r.append( '"physicalPortId":"' + self.PhysicalPortId + '"' )
        # r.append( '"stateReason":' + self.StateReason )
        r.append( '"mtu":' + self.Mtu )
        r.append( '"Managed":' + self.Managed )
        r.append( '"Ip4Config":"' + self.Ip4Config + '"')
        if self.ActiveConnection != None:
            r.append( '"activeConnection":' + str( self.ActiveConnection ) )

        return "{" + ",".join( r ) + "}"
