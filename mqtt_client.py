#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt


class PlantgrowerMQTTClient(mqtt.Client):
    def __init__(self, grow_id, **kwargs):
        self.grow_id = grow_id
        super().__init__(**kwargs)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connection returned result: {rc}")
        self.subscribe("grow/{self.grow_id}/#", 0)

    def on_message(self, client, userdata, msg):
        print(f"Unrecognized message received: {msg.topic} - {msg.payload}")

    def on_publish(self, client, userdata, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, client, userdata, level, string):
        print(string)

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")
        else:
            print("Received disconnect signal.")

    def message_callback_add(self, sub_filter, callback):
        super().message_callback_add(
            f"grow/{self.grow_id}/{sub_filter}", callback
        )
