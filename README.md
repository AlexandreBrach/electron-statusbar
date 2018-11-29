# ELECTRON Status bar

A web-based desktop status bar written in Electron, written to be used with tiled window managers (may be used with other kind of WM ?)

It allow to build and configure your desktop toolbar using HTML, javascript and CSS.

## Features

* prevent window overlapping using WINDOW_STRUT properties
* transparent visuals

# 2 Modes

the bar can be used in two different modes

## STDIN Mode

You can echo some html directly to the bar and it render it

## DBUS Mode

The bar is splitted into sections (HTML `div`). Each section listen to its dedicated dbus service. It wait for a specific service event, then retrieve data from the service and update its view using the data.


In dbus mode, data can be :
* raw html to render in the bar
* JSON data that will be injected in an EJS template that will be rendered

# Installation

Download a release and unpack it into a folder of your choice, like `/opt/statusbar` for exemple.
Use the weebar executable inside the folder.

# BUILD

    npm run-script build

# Sample DBUS services

Some dbus services are provided  into the `services` folder,

It can be installed with the following command :

    ./services/install.sh

The system must follow these prerequisites :

* python 3
* dbus lib for python

    apt install python-dbus-dev libglib2.0-dev

All of these provide JSON data to be injected in a (provided) EJS template, so it's quite easy for HTML developpers to customize the rendering.

Each of these services can push the folowing informations on your statusbar :

* battery status
* calendar
* network status
* realtime CPU/RAM usage
* time
* xmonad workspace and active application

The battery status need the following package :

    # Debian/Ubuntu
    apt-get install upower

    # Archlinux
    pacman -S upower

