#!/bin/bash

# Network toolbar
ln -s $(pwd)/dbus-toolbar-network.py /usr/bin/dbus-toolbar-network.py
ln -s $(pwd)/org.alexandrebrach.toolbar.network.service /usr/share/dbus-1/services/org.alexandrebrach.toolbar.network.service

# Battery toolbar
ln -s $(pwd)/dbus-toolbar-battery.py /usr/bin/dbus-toolbar-battery.py
ln -s $(pwd)/org.alexandrebrach.toolbar.battery.service /usr/share/dbus-1/services/org.alexandrebrach.toolbar.battery.service
