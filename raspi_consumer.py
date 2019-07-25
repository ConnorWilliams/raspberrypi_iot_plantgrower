#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import re
import gpiozero
from gpiozero.pins.mock import MockFactory
from mqtt_client import PlantgrowerMQTTClient
from sensors import BME280


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
    message_string = validate_message(
        msg.payload,
        r"^[(](1[1-9]|2[0-7]){1}, (True|False){1}[)]$",  # ([11-27], True|False)
        "(pin_number, boolean)"
    ).replace(" ", "")

    pin_number, status = tuple(message_string[1:-1].split(","))
    set_output_pin(pin_number, status)


def on_message_read(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # grow/id/read/#
    logger.info(f"Message on {msg.topic} on grow {GROW_ID}: {msg.payload}")
    message_string = validate_message(
        msg.payload,
        r"^[(](1[1-9]|2[0-7]){1}, (.*)[)]$",  # ([11-27], sensor_type)
        "(pin_number, sensor_type)"
    ).replace(" ", "")

    pin_number, sensor_type = tuple(message_string[1:-1].split(","))
    sensor_type = sensor_type.replace("'", "")
    reading = read_sensor(pin_number, sensor_type)
    logger.info(reading)


def validate_message(message, regex_string, proper_form):
    regex = re.compile(regex_string)
    decoded_message = message.decode("utf-8")
    if regex.match(decoded_message):
        return decoded_message
    else:
        logger.error(f"Message {message} not valid. Should be in form {proper_form}")
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


def read_sensor(pin_number, sensor_type):
    sensor_type = sensor_type.lower()
    SUPPORTED_SENSORS = {
        'bme280': BME280
    }
    try:
        sensor = SUPPORTED_SENSORS[sensor_type]()
        return sensor.read()
    except KeyError:
        raise (
            f"Unsupported sensor {sensor_type}."
            f"Should be one of {list(SUPPORTED_SENSORS.keys())}"
        )


if __name__ == "__main__":
    mqttc = PlantgrowerMQTTClient(grow_id=GROW_ID)

    mqttc.message_callback_add("output", on_message_output)
    mqttc.message_callback_add("read", on_message_read)

    mqttc.connect(
        MOSQUITTO_HOST,
        int(MOSQUITTO_PORT),
        int(MOSQUITTO_KEEPALIVE)
    )
    mqttc.loop_forever()
