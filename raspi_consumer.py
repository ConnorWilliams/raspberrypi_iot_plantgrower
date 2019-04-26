#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
from mqtt_client import PlantgrowerMQTTClient


logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

GROW_ID = os.getenv("GROW_ID", "1")
MOSQUITTO_HOST = os.getenv("MOSQUITTO_HOST", "m2m.eclipse.org")
MOSQUITTO_PORT = os.getenv("MOSQUITTO_PORT", "1883")
MOSQUITTO_KEEPALIVE = os.getenv("MOSQUITTO_KEEPALIVE", "60")


def on_message_output(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # grow/id/output/#
    logger.info(f"MESSAGE: {msg.topic} - {msg.payload}")


mqttc = PlantgrowerMQTTClient(grow_id=GROW_ID)

mqttc.message_callback_add("output", on_message_output)
# TODO: Add callback for sensor reading

logger.info(f"Connecting to {MOSQUITTO_HOST} on port {MOSQUITTO_PORT}")
mqttc.connect(MOSQUITTO_HOST, int(MOSQUITTO_PORT), int(MOSQUITTO_KEEPALIVE))

mqttc.loop_forever()
