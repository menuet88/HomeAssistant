import logging
from . import DOMAIN
from homeassistant.const import DEVICE_DEFAULT_NAME
from homeassistant.helpers.entity import ToggleEntity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    if not 'outputs' in discovery_info[1]:
        _LOGGER.error("No valid config for switch")
        return
    chipInstance=hass.data[DOMAIN][discovery_info[0]]
    switch = []
    for pin_num, pin_name in discovery_info[1]['outputs'].items():
        switch.append(PCF8574(chipInstance,pin_num, pin_name or DEVICE_DEFAULT_NAME))
    add_entities(switch)

class PCF8574(ToggleEntity):

    def __init__(self,chip,pin,name):
        self._chip = chip
        self._name = name
        self._pin = pin

    @property
    def name(self):
        return self._name

    @property
    def should_poll(self):
        return False

    @property
    def is_on(self):
        state = self._chip.readOutput(self._pin)
        return state

    @property
    def assumed_state(self):
        return True

    def toggle(self, **kwargs):
        self._chip.setOutput(self._pin,~self._chip.readOutput(self._pin))
        self.schedule_update_ha_state()


    def turn_on(self, **kwargs):
        self._chip.setOutput(self._pin,True)
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        self._chip.setOutput(self._pin,False)
        self.schedule_update_ha_state()
