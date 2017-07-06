#!/usr/bin/python

# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT
import fileinput
import sys

BAR_HEIGHT=40
XMONAD_BAR_WIDTH=900

COLOR_ACTIVE_WORKSPACE="#FFFFFF"
COLOR_HAVINGWINDOW_WORKSPACE="#00DFFC"
COLOR_URGENT_WORKSPACE="#FF0000"
COLOR_INACTIVE_WORKSPACE="#4F4F4F"
COLOR_OTHERSCREEN="#FFFF00"

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

def getMonitorHeight():
    proc = Popen('/home/alex/myScripts/screenHeight', stdout=PIPE)
    tmp = proc.stdout.read()
    return int(tmp)

Y_POS = getMonitorHeight() - BAR_HEIGHT

cmd = [ 
    "/home/alex/workspace/electron-statusbar/build/Electron-Test-linux-x64/Electron-Test", 
    "--enable-transparent-visuals",
    "--disable-gpu",
    "--css=/home/alex/workspace/electron-statusbar/examples/custom.css",
]

proc = Popen(cmd, stdin=PIPE)

while 1:
    try:
        line = sys.stdin.readline()
    except KeyboardInterrupt:
        break
    if not line:
        break
    data = line

    pp = LogHookPP( data )
    formater = ppFormater( pp )
    output = formater.format() 
    proc.stdin.writelines( output + "\n" )
