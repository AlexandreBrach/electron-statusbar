#!/usr/bin/python

# -*- coding: utf-8 -*-

import sys
import dbus
import dbus.service
import gobject
import os

from subprocess import Popen, PIPE, STDOUT
import fileinput

sys.path.append( '.' )

from DBusProvider.NetworkManager import NetworkManagerService,NetworkInterface

BAR_HEIGHT=40
XMONAD_BAR_WIDTH=900

COLOR_ACTIVE_WORKSPACE="#FFFFFF"
COLOR_HAVINGWINDOW_WORKSPACE="#00DFFC"
COLOR_URGENT_WORKSPACE="#FF0000"
COLOR_INACTIVE_WORKSPACE="#4F4F4F"
COLOR_OTHERSCREEN="#FFFF00"


BUS_NAME = 'org.alexandrebrach.toolbar.xmonad'
OBJECT_PATH = '/org/alexandrebrach/toolbar/xmonad'
DBUS_INTERFACE = 'org.alexandrebrach.toolbar'
# OBJECT_PATH = '/org/alexandrebrach/toolbar/network'
# DBUS_INTERFACE = 'org.alexandrebrach.toolbar.network'

class ppFormater:

    def __init__( self, pp ):
        self.pp = pp
        self.currentColor = "#C8FF00"
        self.hiddenColor = "#666666"
        self.hiddenWithWindowsColor = "#CCCCCC"

    def setCurrentColor( self, color ):
        self.currentColor = color

    def layoutIcon( self, layout ):

        if( 'Mirror' in layout ):
            return 'vertical'
        else:
            if( 'Full' in layout ):
                return 'full'
            else:
                if( 'ResizableTall' in layout ):
                    return 'horizontal'
        return '?'

    def formatLayout( self, layout ):
        icon = self.layoutIcon( layout )
        result = '&nbsp;<span class="layout ' + icon + '"></span>'
        return result

    def formatWorkspace( self ):
        result = ''
        result = '<div class="workspaces">'
        for i in range(0,self.pp.getWorkspacesNumber()):
            workspace = self.pp.getWorkspacePropertiesById( i )
            name = workspace[0]
            status = workspace[1]
            x = i%3
            y = i//3
            result += "<div class='workspace " + status + " w" + str(x) + str(y) +  "'></div>"
        result += '</div>'
        return result

    def formatCurrentWorkspace( self ):
        result = '<span class="workspaceName"> ' + self.pp.current + ' </span>'
        return result

    def formatWindowName(self, name):
        result = '<span class="windowName">' + name + '</span>'
        return result


    def format( self ):
        result = ''
        result += self.formatWorkspace()
        result += self.formatLayout( self.pp.layout )
        result += self.formatCurrentWorkspace()
        if( self.pp.windowName != '' ):
            result += self.formatWindowName( self.pp.windowName )

        return result

class LogHookPP():

    def __init__(self, message):

        self.parse(message)

    def parse( self, message):

        self.message = message
        self.sections = self.message.split( '|' )
        workspaces = self.sections[0].split( '$' )
        self.workspaces = []
        for w in workspaces:
            token = w[:1]
            name = w[1:]
            status = "inactive"
            if token == '{' :
                status = "havingWindow"
            if token == '^' :
                status = "urgent"
            # Le status current prevaut
            if token == '[' :
                status = "active"
            if token == '<' :
                status = "otherScreen"
            self.workspaces.append( [name,status] )
            if status == "active":
                self.current = name

        self.layout = self.sections[1]
        if( len(self.sections) == 4 ):
            # There is an active window in the current workspace
            self.windowName = self.sections[2]
        else:
            self.windowName = ''

    def getWorkspacePropertiesById( self, n ):
        return self.workspaces[n]

    def raw( self ):
        return self.message

    def getWorkspacesNumber( self ):
        return len( self.workspaces )

class Debogger:

    def __init__(self, filename, actif ):
        self.fd = open( filename, 'a' )
        self.actif = actif

    def debug( self, data ):
        if self.actif:
            self.fd.write( data + "\n")
            self.fd.flush()

class Emitter(dbus.service.Object):
    def __init__(self, bus_name, object_path):
        bus = dbus.SessionBus()
        bus.request_name( bus_name )
        busName = dbus.service.BusName(bus_name, bus=bus)
        dbus.service.Object.__init__(self, busName, object_path)
        self.data = ""

    @dbus.service.signal(dbus_interface=DBUS_INTERFACE, signature='')
    def changes(self, data):
        self.data = "<div class='xmonad'>"
        self.data += data
        self.data += "</div>"
        debogger.debug( "---------------------" )
        debogger.debug( self.data )
        return True

    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='', out_signature='s')
    def getState(self):
        return self.data

debogger = Debogger( "/home/alex/dbus_out", False )
emitter = Emitter( BUS_NAME, OBJECT_PATH )

def job( data, stri ):
    d = data.readline()
    debogger.debug( "========================" )
    debogger.debug( d )
    try:
        # output = d
        pp = LogHookPP( d )
        formater = ppFormater( pp )
        output = formater.format()
    except Exception as e:
        debogger.debug( type(e).__name__ + ':' )
        debogger.debug( d )
        return True
    else:
        emitter.changes( output )
        return True

def end( data, stri):
    sys.exit( "Terminated.")

def error( data, stri):
    debogger.debug( data )
    return True

loop = gobject.MainLoop()
gobject.io_add_watch(sys.stdin, gobject.IO_IN | gobject.IO_PRI, job)
gobject.io_add_watch(sys.stdin, gobject.IO_HUP, end)
gobject.io_add_watch(sys.stdin, gobject.IO_ERR, error)
gobject.io_add_watch(sys.stdin, gobject.IO_NVAL, job)
loop.run()
