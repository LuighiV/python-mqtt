# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2018 Digi International Inc. All Rights Reserved.

# Publishes a predefined message over MQTT to an MQTT broker

import time
import sys
import json
import random
import paho.mqtt.client as mqtt

# Global constants to generate data for temperature and humidity
TEMP_BASE = 25.
HUM_BASE = 70.
VAR_RANGE_TEMP = 2.
VAR_RANGE_HUM = 4.

# Constants for devices
CLIENT_NAME = "example"
RESERVOIR_1_INFO = { 'username' : "MY_TEST_DEVICE", 'password' : None }
RESERVOIR_2_INFO = { 'username' : "MY_TEST_DEVICE_2", 'password' : None }
VALVE_INFO = { 'username' : "MY_TEST_VALVE", 'password' : None }

# Replace by your local server (or cloud server)
CONNECT_URL = "localhost"
PORT = 1883
TIMEOUT = 600

# define function to run whenever a message is published
def on_publish(client, userdata, mid):
    print("publish successful")
    # after publishing disconnect, breaks out of loop_forever()
    client.disconnect()

def fixed_round(number,precision):
    """
    TODO: improve method to delete trailing digits when converting to float.
    Perhaps via Decimal library
    :number: float number to be rounded
    :returns: float number rounded

    """
    numberf = "%." +str(precision) + "f"
    return float(numberf % (number,))

def generate_random_values(base_value,range_value,precision):
    """l: Docstring for generate_random_values.

    :base_value: base value for the generated value
    :range_value: range value for the variation
    :precision: precision for the value
    :returns: random value generated

    """
    return base_value + fixed_round(range_value*random.random(),precision)

def set_payload_reservoir(temperature,humidity,volume):
    """ set_payload_reservoir.
    :temperature: temperature value to be sent
    :humidity: humidity value to be sent
    :volume: volume value to be sent
    :returns: object data with payload

    """
    return {
        'temperature':temperature,
        'humidity':humidity,
        'volume':volume,
    }

def set_payload_valve(isactive):
    """Set payload for valve device

    :isactive: Value for the is active value
    :returns: Payload to be sent to the device

    """
    return {
        'isActive':isactive,
    }

def send_device_data(client,client_info,payload):
    """Send only a message to specified device

    :client: client object to connect with
    :client_info: Dictionary holds username and password for client
        it has the follwing structure: {username: username, password: password}
    :payload: Payload to be sent in the message
    :returns: None

    """
    print(client_info)
    # set your username/password
    client.username_pw_set(username=client_info['username'],
                           password=client_info['password'],)
    # connect to your desired url:port with specified timeout
    print("connecting...")
    check = client.connect(CONNECT_URL, PORT, TIMEOUT)
    # This time is required to connect
    # https://github.com/thingsboard/thingsboard/issues/2092#issuecomment-630843871
    time.sleep(1)
    if(check == mqtt.MQTT_ERR_SUCCESS):
        print("connection succeded")
    else:
        print("connect failed")
        sys.exit(1)

    print(payload)
    message = json.dumps(payload)

    print("Publishing message:" + str(message))
    client.publish(TOPIC, message, QOS)

    # start the client, blocks
    # This is required as it doesn't have
    # non-blocking capabities
    client.loop_write()
    client.disconnect()
    return

def send_reservoir_data_controlled_volume(client,reservoir_info,volume):
    """ Send variable data in temperature and humidity and controlled in volume

    :client: client object to connect with
    :reservoir_info: Dictionary holds username and password for client
        it has the following structure: {username: username, password: password}
    :volume: volume value to be sent
    :returns: TODO

    """
    payload={}
    payload["temperature"] = generate_random_values(TEMP_BASE,VAR_RANGE_TEMP,1)
    payload["humidity"] = generate_random_values(HUM_BASE,VAR_RANGE_HUM,1)
    payload["volume"] = volume
    send_device_data(client,reservoir_info,payload)
    return

def send_valve_data(client,valve_info,isactive):
    """Send data to valve device

    :client: client object to connect with
    :valve_info: Dictionary holds username and password for client
        it has the following structure: {username: username, password: password}
    :isactive: Value of state of valve. Valid values, strings "true" and
    "false"
    :returns: None

    """
    payload = {
        "isActive" : isactive,
    }
    send_device_data(client,valve_info,payload)
    return



if __name__ =="__main__":


    TOPIC = "v1/telemetry"
    payload = {}
    QOS = 1
    # name your client whatever you want
    client = mqtt.Client(CLIENT_NAME)

    TIME_DELAY = 10


    # assign function to be run whenever a message is published
    client.on_publish = on_publish

    MAX_VOLUME = 1000
    #Defining methos for the state machine
    def init_state(volume):
        """Init values for the devices
        :returns: TODO

        """
        send_reservoir_data_controlled_volume(client,RESERVOIR_1_INFO,MAX_VOLUME)
        send_reservoir_data_controlled_volume(client,RESERVOIR_2_INFO,0)
        send_valve_data(client,VALVE_INFO,"false")

        return "up_state", volume

    def up_state(volume):
        """State with up value
        :returns: TODO

        """
        send_reservoir_data_controlled_volume(client,RESERVOIR_1_INFO,MAX_VOLUME-volume)
        send_reservoir_data_controlled_volume(client,RESERVOIR_2_INFO,volume)
        send_valve_data(client,VALVE_INFO,"true")

        if(volume>=MAX_VOLUME):
            return "wait_state_1",volume
        else:
            volume+=100
            return "up_state",volume

    def down_state(volume):
        """State with up value
        :returns: TODO

        """
        send_reservoir_data_controlled_volume(client,RESERVOIR_2_INFO,volume)
        send_reservoir_data_controlled_volume(client,RESERVOIR_1_INFO,MAX_VOLUME-volume)
        send_valve_data(client,VALVE_INFO,"true")

        if(volume<=0):
            return "wait_state_2", volume
        else:
            volume -=100
            return "down_state", volume

    def wait_state_1(volume):
        """State with up value
        :returns: TODO

        """
        send_reservoir_data_controlled_volume(client,RESERVOIR_1_INFO,0)
        send_reservoir_data_controlled_volume(client,RESERVOIR_2_INFO,MAX_VOLUME)
        send_valve_data(client,VALVE_INFO,"false")
        return "down_state", volume

    def wait_state_2(volume):
        """State with up value
        :returns: TODO

        """
        send_reservoir_data_controlled_volume(client,RESERVOIR_1_INFO,MAX_VOLUME)
        send_reservoir_data_controlled_volume(client,RESERVOIR_2_INFO,0)
        send_valve_data(client,VALVE_INFO,"false")
        return "up_state", volume

    states = {
        "init_state": init_state,
        "up_state":up_state,
        "wait_state_1":wait_state_1,
        "down_state":down_state,
        "wait_state_2":wait_state_2,
    }

    current_state = "init_state"
    volume = 0
    while  True:

        next_state, volume= states.get(current_state,"Not a valid state")(volume)

        print("Starting delay")
        time.sleep(TIME_DELAY)
        current_state = next_state

    sys.exit(0)
