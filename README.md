# ELECTRON Status bar

A web-based desktop status bar created with Electron.

# PREREQUIS

Dbus lib for python

    apt install python-dbus-dev libglib2.0-dev python-gobject

# BUILD

    npm rebuild --runtime=electron --target=1.7.8 --disturl=https://atom.io/download/atom-shel

# Install the related DBUS service

Some services need the following package (Debian) :

    upower (battery)


run :

    ./services/install.sh
