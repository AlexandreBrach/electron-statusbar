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
        return o.GetAll( 'org.freedesktop.UPower.Device' )

    def attachDeviceChanges( self, callback ):
        print 'attach to device changes'
        OBJECT =  '/org/freedesktop/UPower'
        self.bus.add_signal_receiver(callback,
                signal_name=None,
                dbus_interface=None,
                bus_name=None,
                path=OBJECT)

class BatteryDevice:

    def __init__( self, device ):
        s = BatteryDBUS()
        deviceProperties = s.getDevicesProperties( device )

        # The capacity of the power source expressed as a percentage between 0 and 100.
        # The capacity of the battery will reduce with age.
        self.Capacity = str(deviceProperties['Capacity'])
        # If the power device is used to supply the system.
        # This would be set TRUE for laptop batteries and UPS devices,
        # but set FALSE for wireless mice or PDAs.
        self.PowerSupply = str(deviceProperties['PowerSupply'])
        # If the power source is rechargeable.
        self.IsRechargeable = str(deviceProperties['IsRechargeable'])
        # The battery power state.
        self.State = self.getPowerState( str(deviceProperties['State']) )
        # Whether power is currently being provided through line power.
        # This property is only valid if the property type has the value "line-power".
        self.Online = str(deviceProperties['Online'])
        # The amount of energy left in the power source expressed as a percentage between 0 and 100.
        # Typically this is the same as (energy - energy-empty) / (energy-full - energy-empty).
        # However, some primitive power sources are capable of only reporting percentages
        # and in this case the energy-* properties will be unset while this property is set.
        self.Percentage = str(deviceProperties['Percentage'])
# Type of power source
        self.Type = self.getDeviceType( str( deviceProperties['Type'] ) )
# The point in time (seconds since the Epoch Jan 1, 1970 0:00 UTC) that data was read from the power source.)
        self.UpdateTime = str(deviceProperties['UpdateTime'])
        # Name of the vendor of the battery.
        self.Vendor = str( deviceProperties['Vendor'])
        # Number of seconds until the power source is considered full. Is set to 0 if unknown.
        # This property is only valid if the property type has the value "battery".
        self.TimeToFull = str(deviceProperties['TimeToFull'])
        # If the power source is present in the bay.
        # This field is required as some batteries are hot-removable,
        # for example expensive UPS and most laptop batteries.
        self.IsPresent = str(deviceProperties['IsPresent'])
        # Amount of energy being drained from the source, measured in W.
        # If positive, the source is being discharged, if negative it's being charged.
        # This property is only valid if the property type has the value "battery".
        self.EnergyRate = str(deviceProperties['EnergyRate'])
        # Number of seconds until the power source is considered empty. Is set to 0 if unknown.
        # This property is only valid if the property type has the value "battery".
        self.TimeToEmpty = str(deviceProperties['TimeToEmpty'])
# Name of the model of this battery.
        self.Model = str(deviceProperties['Model'])
        # Amount of energy (measured in Wh) the power source is designed
        #to hold when it's considered full.
        # This property is only valid if the property type has the value "battery".
        self.EnergyFullDesign = str(deviceProperties['EnergyFullDesign'])
        # Voltage in the Cell or being recorded by the meter.
        self.Voltage = str(deviceProperties['Voltage'])
        # Amount of energy (measured in Wh) in the power source when it's considered full.
        # This property is only valid if the property type has the value "battery".
        self.EnergyFull = str(deviceProperties['EnergyFull'])
# Unique serial number of the battery.
        self.Serial = str(deviceProperties['Serial'])
        # Technology used in the battery
        self.Technology = self.getTechnology( str(deviceProperties['Technology']) )

    def getDeviceType( self, value ):

        if '0' == value :
            return 'Unknown'
        if '1' == value :
            return 'Line Power'
        if '2' == value :
            return 'Battery'
        if '3' == value :
            return 'Ups'
        if '4' == value :
            return 'Monitor'
        if '5' == value :
            return 'Mouse'
        if '6' == value :
            return 'Keyboard'
        if '7' == value :
            return 'Pda'
        if '8' == value :
            return 'Phone'
        return str( value )

    def getTechnology(self, value ):
        """ return the technology used by the battery based on an integer value """
        if '0' == value :
            return 'Unknown'
        if '1' == value :
            return 'Lithium ion'
        if '2' == value :
            return 'Lithium polymer'
        if '3' == value :
            return 'Lithium iron phosphate'
        if '4' == value :
            return 'Lead acid'
        if '5' == value :
            return 'Nickel cadmium'
        if '6' == value :
            return 'Nickel metal hydride'
        return str( value )

    def getPowerState(self, value):
        """ return the power state corresponding to the DBUS value """
        if '0' == value :
            return 'Unknown'
        if '1' == value :
            return 'Charging'
        if '2' == value :
            return 'Discharging'
        if '3' == value :
            return 'Empty'
        if '4' == value :
            return 'Fully charged'
        if '5' == value :
            return 'Pending charge'
        if '6' == value :
            return 'Pending discharge'
        return str( value )

    def serialize(self):
        r = []
        r.append( '"capacity":' + self.Capacity )
        r.append( '"powerSupply":' + self.PowerSupply )
        r.append( '"isRechargeable":' + self.IsRechargeable )
        r.append( '"state":"' + self.State + '"' )
        r.append( '"online":' + self.Online )
        r.append( '"percentage":' + self.Percentage )
        r.append( '"type":"' + self.Type + '"' )
        r.append( '"updateTime":' + self.UpdateTime )
        r.append( '"vendor":"' + self.Vendor + '"' )
        r.append( '"timeToFull":' + self.TimeToFull )
        r.append( '"isPresent":' + self.IsPresent )
        r.append( '"energyRate":' + self.EnergyRate )
        r.append( '"timeToEmpty":' + self.TimeToEmpty )
        r.append( '"model":"' + self.Model + '"')
        r.append( '"energyFullDesign":' + self.EnergyFullDesign )
        r.append( '"voltage":' + self.Voltage )
        r.append( '"energyFull":' + self.EnergyFull )
        r.append( '"serial":"' + self.Serial + '"' )
        r.append( '"technology":"' + self.Technology + '"' )

        return "{" + ",".join( r ) + "}"


    def __str__(self):
        r = []
        r.append( "Capacity : " + self.Capacity )
        r.append( "PowerSupply : " + self.PowerSupply )
        r.append( "IsRechargeable : " + self.IsRechargeable )
        r.append( "State : " + self.State )
        r.append( "Online : " + self.Online )
        r.append( "Percentage : " + self.Percentage )
        r.append( "Type : " + self.Type )
        r.append( "UpdateTime : " + self.UpdateTime )
        r.append( "Vendor : " + self.Vendor )
        r.append( "TimeToFull : " + self.TimeToFull )
        r.append( "IsPresent : " + self.IsPresent )
        r.append( "EnergyRate : " + self.EnergyRate )
        r.append( "TimeToEmpty : " + self.TimeToEmpty )
        r.append( "Model : " + self.Model )
        r.append( "EnergyFullDesign : " + self.EnergyFullDesign )
        r.append( "Voltage : " + self.Voltage )
        r.append( "EnergyFull : " + self.EnergyFull )
        r.append( "Serial : " + self.Serial )
        r.append( "Technology : " + self.Technology )

        return "\n".join( r )


class BatteryService:

    def __init__(self):
        self.dbus = BatteryDBUS()

    def getDevices(self):
        dbusResult = self.dbus.getDevices()
        devices = self.assembleResult( dbusResult )
        return devices

    def getLoop(self):
        return self.dbus.getLoop()

    def assembleResult( self, dbusResult ):
        devices = []
        for device in dbusResult:
            d = BatteryDevice( device )
            devices.append( d )
        return devices

    def serializeDevices( self ):
        d = []
        for device in self.getDevices():
             d.append( device.serialize() )
        return '[' + ','.join( d ) + ']'

    def onDeviceChange( self, callback ):
        self.dbus.attachDeviceChanges( callback )

if __name__ == "__main__":

    service = BatteryService()
    print service.serializeDevices()

