#!/usr/bin/python

import dbus
import sys

bus = dbus.SessionBus()

proxy = bus.get_object('com.Skype.API', '/com/Skype')

proxy.Invoke('NAME skype_status.py')
proxy.Invoke('PROTOCOL 2')

if len(sys.argv) >= 2:
    command = 'SET USERSTATUS %s' % sys.argv[1]
else:
    command = 'GET USERSTATUS' 

print proxy.Invoke(command)