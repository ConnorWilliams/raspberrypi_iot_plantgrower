#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import re
import gpiozero
from gpiozero.pins.mock import MockFactory
from mqtt_client import PlantgrowerMQTTClient


logger = logging.getLogger(__name__)
LOG_FORMAT = '[%(asctime)s] [%(levelname)s] %(funcName)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

GROW_ID = os.getenv("GROW_ID", "1")
MOSQUITTO_HOST = os.getenv("MOSQUITTO_HOST", "m2m.eclipse.org")
MOSQUITTO_PORT = os.getenv("MOSQUITTO_PORT", "1883")
MOSQUITTO_KEEPALIVE = os.getenv("MOSQUITTO_KEEPALIVE", "60")
GPIOZERO_PIN_FACTORY = os.getenv("GPIOZERO_PIN_FACTORY", "native")

if GPIOZERO_PIN_FACTORY == 'mock':
    gpiozero.OutputDevice.pin_factory = MockFactory()

output_devices = {}


def on_message_output(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # grow/id/output/#
    logger.info(f"Message on {msg.topic} on grow {GROW_ID}: {msg.payload}")
    try:
        message_string = validate_message(
            msg.payload,
            "\((1[1-9]|2[0-7]){1}, (True|False){1}\)"  # ([11-27], True|False)
        ).replace(" ", "")
    except ValueError:
        logger.error(
            f"Message on {msg.topic} should be in form (pin_number, boolean)"
        )
        raise

    pin_number, status = tuple(message_string[1:-1].split(","))
    set_output_pin(pin_number, status)


def validate_message(message, regex_string):
    regex = re.compile(regex_string)
    decoded_message = message.decode("utf-8")
    if regex.match(decoded_message):
        return decoded_message
    else:
        logger.error(f"Message {message} not valid")
        raise ValueError


def set_output_pin(pin_number, status):
    if pin_number not in output_devices.keys():
        logger.info(f"Creating new gpio outputdevice on pin {pin_number}")
        output_devices[pin_number] = gpiozero.OutputDevice(
            pin_number,
            active_high=False,
            initial_value=status
        )

    output_device = output_devices[pin_number]
    output_device.on() if status == "True" \
        else output_device.off()
    logger.debug(output_device)


mqttc = PlantgrowerMQTTClient(grow_id=GROW_ID)

mqttc.message_callback_add("output", on_message_output)
# TODO: Add callback for sensor reading

logger.info(f"Connecting to {MOSQUITTO_HOST} on port {MOSQUITTO_PORT}")
mqttc.connect(MOSQUITTO_HOST, int(MOSQUITTO_PORT), int(MOSQUITTO_KEEPALIVE))

mqttc.loop_forever()
