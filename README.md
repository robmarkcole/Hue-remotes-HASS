[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![build status](http://img.shields.io/travis/robmarkcole/Hue-remotes-HASS/master.svg?style=flat)](https://travis-ci.org/robmarkcole/Hue-remotes-HASS)
[![Coverage](https://codecov.io/github/robmarkcole/Hue-remotes-HASS/coverage.svg?branch=master)](https://codecov.io/gh/robmarkcole/Hue-remotes-HASS)

[FOR COMMUNITY SUPPORT PLEASE USE THIS THREAD](https://community.home-assistant.io/t/hue-motion-sensors-remotes-custom-component)

For Hue motion sensors checkout [Hue-sensors-HASS](https://github.com/robmarkcole/Hue-sensors-HASS)

If using Home Assistant >= v0.108, **please read the [deprecation and suggested migration section](#suggested-migration)**

# Hue-remotes-HASS
Custom integration for Hue &amp; Lutron Aurora [Friends of Hue](https://www2.meethue.com/en-us/works-with) (FOH) remotes with Home Assistant.

## Overview

This custom integration provides the ~~missing support~~ for `remote` devices in the [official Hue integration of HA Core](https://www.home-assistant.io/integrations/hue), by registering the platform in the main integration and sharing the sensor data with it.

As this new platform imposes a lower `scan_interval` for all hue sensors (of 1Hz), sensors from the main hue integration will also increase their refresh rate to 1 Hz.

**Be advised that the increased update of this custom integration may cause connectivity problems which can result in errors in the official hue integration**, please do not create any issue for this. If you can't live with these errors, do not use this custom integration.

## Suggested migration

Since HA v0.108 **Hue switches are recognized in the `hue` integration**, 
making this CC not really necessary anymore, but there are some caveats, 
as it is not a perfect replacement for this CC.

Now the main `hue` registers the remotes as `devices`, and fires events with the detected button presses. 
For easier usage from UI, it also presents the button presses as `device triggers` for automations. 
In addition, for battery-powered remotes it generates battery sensor `entities`.

The features of this CC over what the main hue offers are to:

1. Expose the switches as entities (of kind `remote`, but they actually are `sensor`), showing the last button press as the state, using fixed state mappings (like code 3002 is "3_click_up", etc.)
2. Modify the hue update interval to a fixed, **much faster**, rate (1Hz by default, customizable with scan_interval: X), to have a faster polling than the 5 secs of the main integration

But as this CC is not using the Integrations menu, it needs manual yaml and a HA restart for any config change. 
It also has some problems derived of doing too many calls to the Hue bridge, 
and its **usage for automation triggers now presents [some flaws with false positives](https://github.com/robmarkcole/Hue-remotes-HASS/issues/14)**.

In this context, **this CC is being deprecated**, and these are some suggestions 
to migrate to other **HACS custom integrations** to achieve the best results, depending of your own specific needs:

* If you **need a faster polling interval** for the hue bridge than the 5s, use [Fast-Hue CC](https://github.com/azogue/fasthue) to:
  - Modify the main hue update interval to any value, different for each bridge
  - Monitor the current refresh rates with sensor entities
  - Enable a service to change the refresh rate anytime

* If you want to **expose the remotes as entities**, because you want to track their state or use it to trigger automations, use [EventSensor CC](https://github.com/azogue/eventsensor)
  - It is UI configurable (with no restart required) and has configuration wizards to help configure the Hue switches for this specific migration.
  - The mapping for the button presses is customizable, being the default maps the same ones used here
  - It will not generate false positives, as it listens to the events generated in the main hue (listening directly to those events, or using UI device triggers would also do the trick)  

You can use both new CCs, **or none of them**, if you are comfortable with the main hue polling and change your automations to use 'device triggers'.

Both are configurable via UI, so no restarts are needed to install and try them. **To do the smoothest migration, with just one HA restart, follow these steps**:

1. Remove the yaml config for this CC, and replace every `remote.entity_name` in your config (like in `automations.yaml`) to `sensor.entity_name`, as the new entities will be of `sensor` type.
2. Disable all automations using the remotes, as we don't want them triggering until migration is finished :)
3. Uninstall this CC from HACS.
4. Restart HA. Now the `remote.x` entities should be gone and this CC would not be loaded.
5. Install "Event sensor" from HACS. 
6. In Integrations, add and configure a new sensor for each old `remote`. Follow the wizard for Hue remotes, set the same name as before (so new entities will be `sensor.entity_name`), and, as the identifier, choose "id" and set the `entity_name`. 

At that point the migration is done, and you can check the new sensor entities by pressing buttons, and then re-enable the automations to check that everything works as before.

If the fast polling interval is required, install "Fast-Hue polling" from HACS and configure it for your needs, taking into account that, if polling too fast, some logging errors may appear in the main hue. 
In that case, feel free of playing with different values to optimize your specific system, as there is a new service `fasthue.set_update_interval` to do just that in any moment.

## Installation

**Install via [HACS](https://hacs.xyz/)**. You need to set up your [Hue bridge](https://www.home-assistant.io/integrations/hue) first.

#### Manual installation

Alternatively, place the `custom_components` folder in your configuration directory (or add its contents to an existing `custom_components` folder).

## Configuration

Once installed add to your configuration:

```
remote:
  - platform: hueremote
```

The scan interval can be modified optionally, by adding `scan_interval: 2`.

## Supported remotes
* [Hue dimmer switch](https://www2.meethue.com/en-us/p/hue-dimmer-switch/046677473372) - can be used for a click and long press (hold button for 2 sec and see LED blink twice).
* [Hue tap switch](https://www2.meethue.com/en-us/p/hue-tap-switch/046677473365)
* [Hue smart button](https://www2.meethue.com/en-us/p/hue-smart-button/046677553715)
* [Lutron Aurora smart bulb dimmer](http://www.lutron.com/en-US/products/pages/standalonecontrols/dimmers-switches/smartbulbdimmer/overview.aspx)
* [Lutron Aurora rotary dimmer](http://www.lutron.com/en-US/Products/Pages/StandAloneControls/Dimmers-Switches/RotaryDimmer/Overview.aspx)

## Developers
* Create venv -> `$ python3 -m venv venv`
* Use venv -> `$ source venv/bin/activate`
* Install requirements -> `$ pip install -r requirements.txt` & `$ pip install -r requirements-dev.txt`
* Run tests -> `$ venv/bin/py.test --cov=custom_components tests/ -vv -p no:warnings`
* Black format -> `$ venv/bin/black custom_components/*` (or setup VScode for format on save)

## Contributors
Please format code usign [Black](https://github.com/psf/black) before opening a pull request.

A big thanks to [Atsuko Ito](https://github.com/yottatsa) and [Eugenio Panadero](https://github.com/azogue) for their many contributions to this work!