# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2018 Digi International Inc. All Rights Reserved.

# Publishes a predefined message over MQTT to an MQTT broker

import paho.mqtt.client as mqtt
import time
import json
import random
import math

client_name = "example"
username = "MY_DIGI_DEVICE"
password = None

# Replace by your local server (or cloud server)
connect_url = "172.17.0.1"
port = 1883
timeout = 600

topic = "v1/devices/me/telemetry"
payload = {}
qos = 1

# define function to run whenever a message is published
def on_publish(client, userdata, mid):
	print("publish successful")

	# after publishing disconnect, breaks out of loop_forever()
	client.disconnect()
	pass

def fixed_round(number,precision):
    """
    TODO: improve method to delete trailing digits when converting to float.  Perhaps via Decimal library
    :number: float number to be rounded
    :returns: float number rounded

    """
    f = "%." +str(precision) + "f"
    return float(f % (number,))

# name your client whatever you want
client = mqtt.Client(client_name)

# set your username/password
client.username_pw_set(username=username, password=password)

# assign function to be run whenever a message is published
client.on_publish = on_publish

print("connecting...")

counter = 0
TIME_DELAY = 10
# Emulates the variation in both variables
TEMP_BASE = 25.
HUM_BASE = 70.
VAR_RANGE_TEMP = 2.
VAR_RANGE_HUM = 4.

while  True:
    # connect to your desired url:port with specified timeout
    check = client.connect(connect_url, port, timeout)
    # This time is required to connect 
    # https://github.com/thingsboard/thingsboard/issues/2092#issuecomment-630843871
    time.sleep(1)
    if(check == mqtt.MQTT_ERR_SUCCESS):
            print("connection succeded")
    else:
            print("connect failed")
            exit(1)

    payload["temperature"] = TEMP_BASE + fixed_round(VAR_RANGE_TEMP*random.random(),2)
    payload["humidity"] = HUM_BASE + fixed_round(VAR_RANGE_HUM*random.random(),2)
    print(payload)

    message = json.dumps(payload)

    print("Publishing message:" + str(message))
    client.publish(topic, message, qos)

    # start the client, blocks
    # This is required as it doesn't have
    # non-blocking capabities
    client.loop_write()
    client.disconnect()
    counter += 1
    print("Starting delay")
    time.sleep(TIME_DELAY)

exit(0)
