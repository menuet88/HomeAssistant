import logging
from . import DOMAIN
from datetime import timedelta

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import DEVICE_DEFAULT_NAME

SCAN_INTERVAL = timedelta(seconds=0.5)
_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config,add_devices, discovery_info=None):
    if not 'inputs' in discovery_info[1]:
        _LOGGER.error("No valid config for binary_sensor")
        return
    chipInstance=hass.data[DOMAIN][discovery_info[0]]
    binary_sensors = []
    for pin_num, pin_name in discovery_info[1]['inputs'].items():
        binary_sensors.append(PCF8574(chipInstance,pin_num, pin_name or DEVICE_DEFAULT_NAME))
    add_devices(binary_sensors, True)
    
class PCF8574(BinarySensorEntity):
    def __init__(self,chip,pin,name):
        self._chip = chip
        self._pin=pin
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._chip.readInput(self._pin)

    def update(self):
        self._chip.updateInput()
