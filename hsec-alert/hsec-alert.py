#!/usr/bin/env python3.4
"""
Receive events and state changes. Alert interested parties.
"""
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import requests             # for webhooks
import configparser         # for reading config
import time                 # for sleeping
import comms.comms as comms # for getting a channel to the sensor
from pyicloud import PyiCloudService # for sending "find my iPhone alerts"


def iCloud_alert(account, device_name):

    api=PyiCloudService(account) # password already saved via icloud cmdline

    # look through the list of devices associated with this account
    for k, v in api.devices.items():

	# find the device that matches what you have configured to receive the alerts
        if api.devices[k].data['name'] == device_name:

            # send an alert
            api.devices[k].play_sound("Door opened")


def main():
    """ main method """

    # get key for ifttt maker recipe
    config = configparser.ConfigParser()
    config.read('hsec-alert.cfg')
    key=config['maker.ifttt.com']['Key']
    appleAlertAccount = config['Apple.alert.devices']['Account']
    appleAlertDevice  = config['Apple.alert.devices']['Device']

    # create object for communication to state system
    state_channel = comms.SubChannel("tcp://localhost:5564", ['state'])

    try:
        while True:
            # Read envelope and address from queue
            rv = state_channel.get()
            if rv is not None:
                [address, contents] = rv
                print("State: [%s] %s" % (address, contents))
                post = "https://maker.ifttt.com/trigger/front_door_opened/with/key/" + key
                print("not really..." + post)
                iCloud_alert( appleAlertAccount, appleAlertDevice)
                #print(requests.post(post))
            else:
                time.sleep(0.1)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
