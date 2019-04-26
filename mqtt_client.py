#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


class PlantgrowerMQTTClient(mqtt.Client):
    def __init__(self, grow_id, **kwargs):
        self.grow_id = grow_id
        super().__init__(**kwargs)

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"Connection returned result: {rc}")
        self.subscribe(f"grow/{self.grow_id}/#", 0)

    def on_message(self, client, userdata, msg):
        logger.info(f"Unrecognized message received: {msg.topic} - {msg.payload}")

    def on_publish(self, client, userdata, mid):
        logger.info("mid: "+str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        logger.info("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, client, userdata, level, string):
        logger.info(string)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.info("Unexpected disconnection. Reconnecting.")
            self.reconnect()
        else:
            logger.info("Received disconnect signal.")

    def message_callback_add(self, sub_filter, callback):
        super().message_callback_add(
            f"grow/{self.grow_id}/{sub_filter}", callback
        )
