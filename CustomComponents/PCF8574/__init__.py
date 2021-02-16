
import logging
import time

from smbus import SMBus

from homeassistant.const import DEVICE_DEFAULT_NAME
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'pcf8574'

DEFAULT_INVERT_LOGIC = False
DEFAULT_I2C_ADDRESS = 0x38
DEFAULT_I2C_BUS = 5


def setup(hass, config):
    module_config = config[DOMAIN]
  
    i2cBus=SMBus(module_config['bus'] or DEFAULT_I2C_BUS)
    invertLogic = module_config['invert'] or DEFAULT_INVERT_LOGIC
    chipsConfig = module_config['chips']
    #create global list of PCF instances
    chipsList = []
    for singleChip in chipsConfig:
        chipsList.append(pcf8574_chip(i2cBus,singleChip['i2c_address'],invertLogic))
        
    hass.data[DOMAIN]=chipsList
    
    chipIdInList=0
    
    for singleChip in chipsConfig:
        platformConfig=[chipIdInList,singleChip]
        if 'inputs' in singleChip:
            hass.helpers.discovery.load_platform('binary_sensor', DOMAIN, platformConfig, config)
        if 'outputs' in singleChip:
            hass.helpers.discovery.load_platform('switch', DOMAIN, platformConfig, config)
        chipIdInList = chipIdInList + 1
       
    return True


class pcf8574_chip():
    def __init__(self,i2c,address,invert):
        self._bus=i2c
        self._addr = address
        self._ic_state=self._bus.read_byte(self._addr)#get the current state of device
        self._ic_outputPinsMask=0x00#none is output
        self._ic_outputState = 0xFF#all outputs are high state
        self._invert = invert
        self._bus.write_byte(self._addr,self._ic_outputState)
        self._ic_lastRead = time.time()
        
    
    def updateInput(self):
        #update only when 0.5 seconds elapsed from last read
        if ((time.time() - self._ic_lastRead)>0.4):
            self._ic_state = self._bus.read_byte(self._addr)
            self._ic_lastRead = time.time()
            
        return self._ic_state
    
    def setOutput(self, pin_num, state):        
        ic_pinMask = pow(2,pin_num)
        if(state == self._invert):
            self._ic_outputState = self._ic_outputState & (~ic_pinMask)#set low state    
        else:
            self._ic_outputState = self._ic_outputState | ic_pinMask#set High state
        self._bus.write_byte(self._addr,self._ic_outputState)
        
    def readOutput(self, pin_num):
        if (self._ic_outputState & pow(2,pin_num) ):
            return not self._invert
        else:
            return self._invert
    
    def readInput(self, pin_num):
        if (self._ic_state & pow(2,pin_num) ):
            return not self._invert
        else:
            return self._invert
