#!/bin/bash

# Network toolbar
rm /usr/bin/dbus-toolbar-network.py
rm /usr/share/dbus-1/services/org.alexandrebrach.toolbar.network.service
ln -s $(pwd)/dbus-toolbar-network.py /usr/bin/dbus-toolbar-network.py
ln -s $(pwd)/org.alexandrebrach.toolbar.network.service /usr/share/dbus-1/services/org.alexandrebrach.toolbar.network.service

# Battery toolbar
rm /usr/bin/dbus-toolbar-battery.py
rm /usr/share/dbus-1/services/org.alexandrebrach.toolbar.battery.service
ln -s $(pwd)/dbus-toolbar-battery.py /usr/bin/dbus-toolbar-battery.py
ln -s $(pwd)/org.alexandrebrach.toolbar.battery.service /usr/share/dbus-1/services/org.alexandrebrach.toolbar.battery.service

# Time toolbar
rm /usr/bin/dbus-toolbar-time.py
rm /usr/share/dbus-1/services/org.alexandrebrach.toolbar.time.service
ln -s $(pwd)/dbus-toolbar-time.py /usr/bin/dbus-toolbar-time.py
ln -s $(pwd)/org.alexandrebrach.toolbar.time.service /usr/share/dbus-1/services/org.alexandrebrach.toolbar.time.service

# Calendar toolbar
rm /usr/bin/dbus-toolbar-calendar.py
rm /usr/share/dbus-1/services/org.alexandrebrach.toolbar.calendar.service
ln -s $(pwd)/dbus-toolbar-calendar.py /usr/bin/dbus-toolbar-calendar.py
ln -s $(pwd)/org.alexandrebrach.toolbar.calendar.service /usr/share/dbus-1/services/org.alexandrebrach.toolbar.calendar.service
