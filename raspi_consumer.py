#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from mqtt_client import PlantgrowerMQTTClient

GROW_ID = os.getenv("GROW_ID", "1")
MOSQUITTO_HOST = os.getenv("MOSQUITTO_HOST", "m2m.eclipse.org")
MOSQUITTO_PORT = os.getenv("MOSQUITTO_PORT", "1883")
MOSQUITTO_KEEPALIVE = os.getenv("MOSQUITTO_KEEPALIVE", "60")


def on_message_output(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # grow/id/output/#
    print(f"MESSAGE: {msg.topic} - {msg.payload}")


# TODO: Parametrise grow_id or use device serial?
mqttc = PlantgrowerMQTTClient(grow_id=GROW_ID)

mqttc.message_callback_add("output", on_message_output)
# TODO: Add callback for sensor reading

mqttc.connect(MOSQUITTO_HOST, MOSQUITTO_PORT, MOSQUITTO_KEEPALIVE)

mqttc.loop_forever()
