# Raspberry Pi IoT Plantgrower
This service is a MQTT client which uses the paho library. It is the IoT part of the plantgrower application so it runs on the control box which is connected to the input (sensors) and output (lights, fans and pumps) devices which control a single grow.

## API?
This service is a MQTT client which accepts messages on the following message channels:

- [x] `output` Which takes a pin number and a boolean to switch a pin on or off `([11-27], True|False)`
- [x] `read` Which takes a list of sensors in the form `(pin, sensor_type)` and reads those sensors

## Arguments
```python
parser.add_argument('-g', '--growid', required=False, default=1)
parser.add_argument('-h', '--host', required=False, default="m2m.eclipse.org")
parser.add_argument('-p', '--port', required=False, type=int, default=None, help='Defaults to 8883 for TLS or 1883 for non-TLS')
parser.add_argument('-k', '--keepalive', required=False, type=int, default=60)
```

## Supported sensors
* BME280 which communicates over I2C