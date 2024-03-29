#!/bin/python3

'''
This script turns your screen including your touchscreen-device 
depending on the monitor-sensor.

You will need to configure your touchscreen pointer-device manually 
below.

List all input devices with the command 'xinput --list' and guess which 
one is your touchscreen.
For example 'xwayland-touch:12', mine are called 'SYNA7501:00 06CB:16C7' 
and 'Goodix Capacitive TouchScreen', it's not the 'Virtual...'-stuff.

(c) 2020-2024 by Dirk Winkel
Licensed unter GPL v3.0 or later.
'''

import os
import subprocess
from threading  import Thread
from time import sleep

# Insert your touchscreen device here.
# get it with `xinput --list`
# If you don't have a touchscreen uncomment the 'exit(0)' below.
touchdevices = ['xwayland-touch:12']
# Example for OneMix 1S (with the Stylus-Driver from Adya):
#touchdevices = ['Goodix Capacitive TouchScreen', 'Goodix Active Stylus Pen Pen (0)']

if touchdevices == ['']:
    print('Please execute "xinput --list" to find out the name of your touchscreen pointer-device and enter it in this script!')
    print('(Or uncomment this if you don\'t have a touchscreen device)')
    exit(0)

# maybe you need to change this to 90, 180 or 270 if your (touch)screen is not upside-down in normal mode
# default: 0
offset = 0

# set the following to 'x' if using x, 'wk' if using kde on wayland.
# other display-managers are not supported, pull-requests are appreciated!
dm = 'x'

# === no changes necessary below here ===

print('configured touchscreen devices:\n')
print(touchdevices)

def monitor(ms):
    ''' monitors changes in screen orientation and rotates it accordingly '''
    for line in iter(ms.stdout.readline, b''):
        lin = line.decode('utf-8')
        if 'orientation' in lin:
            if ': normal' in lin:
                print('new orientation: normal')
                rotate('n')
            elif ': left-up' in lin:
                print('new orientation: left-up')
                rotate('l')
            elif ': right-up' in lin:
                print('new orientation: right-up')
                rotate('r')
            elif ': bottom-up' in lin:
                print('new orientation: bottom-up')
                rotate('b')
            else:
                print('WARNING: new unknown orientation, rotating to normal mode!')
                rotate('n')

def rotate(d):
    ''' rotates the screen and the touchscreen device, including the offset '''
    if (d=='n' and offset==0) or (d=='l' and offset==90) or (d=='b' and offset==180) or (d== 'r'and offset==270):
        if dm=='x':
            os.system('xrandr -o normal')
            for device in touchdevices:
                os.system('xinput set-prop "pointer:%s" --type=float "Coordinate Transformation Matrix" 0 0 0 0 0 0 0 0 0'
                    % device)
        elif dm=='wk':
            os.system('kscreen-doctor output.1.rotation.normal')
    elif (d=='r' and offset==0) or (d=='b'and offset==90) or (d=='l'and offset==180) or (d=='n'and offset==270):
        if dm=='x':
            os.system('xrandr -o right')
            for device in touchdevices:
                os.system('xinput set-prop "pointer:%s" --type=float "Coordinate Transformation Matrix" 0 1 0 -1 0 1 0 0 1'
                    % device)
        elif dm=='wk':
            os.system('kscreen-doctor output.1.rotation.right')
    elif (d=='b' and offset==0) or (d=='r'and offset==90) or (d=='n'and offset==180) or (d=='l'and offset==270):
        if dm=='x':
            os.system('xrandr -o inverted')
            for device in touchdevices:
                os.system('xinput set-prop "pointer:%s" --type=float "Coordinate Transformation Matrix" -1 0 1 0 -1 1 0  0 1'
                    % device)
        elif dm=='wk':
            os.system('kscreen-doctor output.1.rotation.inverted')
    elif (d=='l' and offset==0) or (d=='n'and offset==90) or (d=='r'and offset==180) or (d=='b'and offset==270):
        if dm=='x':
            os.system('xrandr -o left')
            for device in touchdevices:
                os.system('xinput set-prop "pointer:%s" --type=float "Coordinate Transformation Matrix" 0 -1 1 1 0 0 0 0 1'
                    % device)
        elif dm=='wk':
            os.system('kscreen-doctor output.1.rotation.left')
    else:
        print('ERROR: Unknown rotation, please check if your configured offset is 0, 90, 180 or 270!')
        print('Bye.')
        exit(1)

ms = subprocess.Popen(['monitor-sensor'], stdout = subprocess.PIPE)

t = Thread(target=monitor, args=(ms,))
t.start()
t.join()
