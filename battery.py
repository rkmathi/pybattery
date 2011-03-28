#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# newbattery.py

import os
import re
import time
import pynotify

INTERVAL_TIME = 600 # seconds

def main():
    while 1:
        state_err = info_err = 0

        # state -> remaining battery
        if os.path.exists('/proc/acpi/battery/BAT0/state') == False:
            state_err = 1
        else:
            state_f   = open('/proc/acpi/battery/BAT0/state')
            state_str = state_f.read()
            state_f.close()
            state_pat = re.compile('(remaining\D+)(\d+)(\sm[A|W]h)')
            state_res = state_pat.search(state_str)
            state_num = int(state_res.groups()[1])

        # info -> last full capacity
        if os.path.exists('/proc/acpi/battery/BAT0/info') == False:
            info_err  = 1
        else:
            info_f    = open('/proc/acpi/battery/BAT0/info', 'r')
            info_str  = info_f.read()
            info_f.close()
            info_pat  = re.compile('(last\D+)(\d+)(\sm[A|W]h)')
            info_res  = info_pat.search(info_str)
            info_num  = int(info_res.groups()[1])
        if   state_err == 1:
            message = "state not found"
        elif info_err  == 1:
            message = "info  not found"
        else:
            percent = state_num * 100 / info_num
            if (percent >= 80 or percent <= 20):
                message = str(percent)+" %"
                pynotify.init("Battery Status")
                notif   = pynotify.Notification("Battery Status", message, "dialog-information")
                notif.show()
                os.popen('aplay -q /home/rkmathi/opt/battery/mikutter.wav')
            time.sleep(INTERVAL_TIME)

if __name__ == "__main__":
    main()

