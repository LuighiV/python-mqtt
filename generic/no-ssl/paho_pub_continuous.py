# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2018 Digi International Inc. All Rights Reserved.

# Publishes a predefined message over MQTT to an MQTT broker

import paho.mqtt.client as mqtt
import time

client_name = "example"
username = "example"
password = None

connect_url = "test.mosquitto.org"
#connect_url = "172.17.0.1"
port = 1883
timeout = 600

topic = "example/test"
payload = "Counter: "
qos = 0

# define function to run whenever a message is published
def on_publish(client, userdata, mid):
	print("publish successful")

	# after publishing disconnect, breaks out of loop_forever()
	client.disconnect()
	pass


# name your client whatever you want
client = mqtt.Client(client_name)

# set your username/password
client.username_pw_set(username=username, password=password)

# assign function to be run whenever a message is published
client.on_publish = on_publish

print("connecting...")

counter = 0
TIME_DELAY = 10
while  True:
    # connect to your desired url:port with specified timeout
    check = client.connect(connect_url, port, timeout)

    if(check == mqtt.MQTT_ERR_SUCCESS):
            print("connection succeded")
    else:
            print("connect failed")
            exit(1)

    print("Start publishing process...")


    print("Publishing message:" + str(counter))
    message= payload + str(counter)
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
