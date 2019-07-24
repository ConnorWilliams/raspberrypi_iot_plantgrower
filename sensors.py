import smbus2
import bme280


class Sensor:
    def read(self):
        pass


class BME280(Sensor):
    def __init__(self, i2c_port=1, i2c_address=0x76):
        self.i2c_port = i2c_port
        self.i2c_address = i2c_address

    def read(self):
        bus = smbus2.SMBus(self.i2c_port)
        calibration_params = bme280.load_calibration_params(
            bus, self.i2c_address
        )
        reading = bme280.sample(bus, self.i2c_address, calibration_params)
        return {
            'id': reading.id,
            'timestamp': reading.timestamp,
            'values': {
                'temperature': reading.temperature,
                'humidity': reading.humidity,
                'pressure': reading.pressure
            }
        }
