#!/usr/bin/env python3.4
"""
Receive events and state changes. Alert interested parties.
"""
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import requests             # for webhooks
#import configparser         # for reading config
import time                 # for sleeping
import comms.comms as comms # for getting a channel to the sensor
from pyicloud import PyiCloudService # for sending "find my iPhone alerts"
import os                   # for reading OS ENV vars


def old_iCloud_alert(account, device_name):

    api=PyiCloudService(account) # password already saved via icloud cmdline

    # look through the list of devices associated with this account
    for k, v in api.devices.items():

	# find the device that matches what you have configured to receive the alerts
        if api.devices[k].data['name'] == device_name:

            # send an alert
            api.devices[k].play_sound("Door opened")

def iCloud_alert(account,device_id_list):
 print("starting iCloud_alert(%s,%s)" % (account,device_id_list))
 api=PyiCloudService(account)
 for k,v in api.devices.items():
  print(" loop iteration")
  if k in device_id_list:
   print("  match on %s" % k)
   api.devices[k].play_sound("test message")

def main():
    """ main method """

    # get key for ifttt maker recipe
    #config = configparser.ConfigParser()
    #config.read('hsec-alert.cfg')
    #key=config['maker.ifttt.com']['Key']
    #appleAlertAccount = config['Apple.alert.devices']['Account']
    #appleAlertDevice  = config['Apple.alert.devices']['Device']

    # create object for communication to state system
    state_channel = comms.SubChannel("tcp://localhost:5564", ['alarm'])

    try:
        while True:
            # Read envelope and address from queue
            rv = state_channel.get()
            if rv is not None:
                [address, contents] = rv
                print("message: [%s, %s]" % (address, contents))
                iCloud_alert( \
                    os.environ["ICLOUD_ALERT_ACCOUNT"], \
                    os.environ["ICLOUD_ALERT_DEVICE_ID_LIST"])
                #post = "https://maker.ifttt.com/trigger/front_door_opened/with/key/" + key
                #print("not really..." + post)
                #print(requests.post(post))
            else:
                time.sleep(0.1)

    except KeyboardInterrupt:
        # call cleanup actions
        state_channel.close()


if __name__ == "__main__":
    main()
