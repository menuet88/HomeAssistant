# PCF8574 unix addon

Simple addon to Home Assistant which is platform independent (should work on any hardware with I2C bus and unix operating system).

Because there is no connection to INT pin, the expander is asking in some period of time (in this configuration 500ms) about some changes on its pin when they are configured as inputs. These means than shorter changes cannot be reported to Home Assistant.

## Prerequisities
- Use kernel modules to access I2C bus from devices:
`modprobe i2c-dev`
After that I2C bus should be visible in /dev/i2c-x, you can check it through command: `ls /dev/i2c*`

- Install i2c-tool to check at which bus your device is connected:
`apt-get install i2c-tools`
check all buses till you find your chip. For example run this command:
`i2cdetect -y -r 5`
to scan bus number 5
- when you find the chip with address from range 0x20 - 0x27 for PCF8574 and 0x38 - 0x3F for PCF8574A please write it down for later configuration.

## Home Assistant prerequisites
It is necessary to install some additional Python modules to get access to I2C bus on your board. If you using docker Home Assistant installation then is necessary to install that module directly to docker modules:
`pip3 install smbus --target /usr/share/hassio/homeassistant/deps/`
This will install smbus module to Home Assistant location. Of course first you need to check if the path of Home Assistant deps folder is correct.

## PCF8574 module installation
To do this you need to copy all four files (or just clone the repository) to Home Assistant custom-components location, for example
`cd /usr/share/hassio/custom_components`
`git clone https://github.com/menuet88/HomeAssistant.git`

## Configuring Home Assistant
In the main configuration file you can add module pcf8574, for example:
```yaml
pcf8574:
    bus: 5
    invert: true
    chips:
    - i2c_address: 0x38
      inputs: 
        0: input1
        1: input2
      outputs:
        2: output1
        3: output2
```
The main module configuration need three parameters:
- bus - number of your I2C bus where expander is connected
- invert - true or false, define if the expander logic is inverted or not
- chips - list of connected chips with config
	- i2c_address - address of device on specified bus, with following configuration
		- inputs - list of configured inputs with number and name. Each number correspond to IO port of the expander, so possible number is 0-7.
		- outputs - list of configured outputs with number and name. Each number correspond to IO port of the expander, so possible number is 0-7.

Every pin can be configured as an input and output. Please remember that pins are open drain configuration, so the IC can only drive some device with low level.

That`s all, the new devices should be visible in Home Assistant.

[![IMAGE ALT TEXT](http://img.youtube.com/vi/xX8wVSlxL1g/0.jpg)](http://www.youtube.com/watch?v=xX8wVSlxL1g "Example")
