[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![build status](http://img.shields.io/travis/robmarkcole/Hue-remotes-HASS/master.svg?style=flat)](https://travis-ci.org/robmarkcole/Hue-remotes-HASS)
[![Coverage](https://codecov.io/github/robmarkcole/Hue-remotes-HASS/coverage.svg?branch=master)](https://codecov.io/gh/robmarkcole/Hue-remotes-HASS)
[![Sponsor](https://img.shields.io/badge/sponsor-%F0%9F%92%96-green)](https://github.com/sponsors/robmarkcole)

[FOR COMMUNITY SUPPORT PLEASE USE THIS THREAD](https://community.home-assistant.io/t/hue-motion-sensors-remotes-custom-component)

For Hue motion sensors checkout [Hue-sensors-HASS](https://github.com/robmarkcole/Hue-sensors-HASS)

# Hue-remotes-HASS
Custom integration for Hue &amp; Lutron Aurora [Friends of Hue](https://www2.meethue.com/en-us/works-with) (FOH) remotes with Home Assistant.

## Overview

This custom integration provides the missing support for `remote` devices in the [official Hue integration of HA Core](https://www.home-assistant.io/integrations/hue), by registering the platform in the main integration and sharing the sensor data with it.

As this new platform imposes a lower `scan_interval` for all hue sensors (of 1Hz), sensors from the main hue integration will also increase their refresh rate to 1 Hz.

Be advised that the increased update of this custom integration may cause connectivity problems which can result in errors in the official hue integration, please do not create any issue for this. If you can't live with these errors, do not use this custom integration.

## Installation

Place the `custom_components` folder in your configuration directory (or add its contents to an existing `custom_components` folder). You need to set up your [Hue bridge](https://www.home-assistant.io/integrations/hue) first. TODO Alternatively install via [HACS](https://hacs.xyz/).

## Configuration

Once installed add to your configuration:

```
remote:
  - platform: hueremote
```

## Supported remotes
* [Hue dimmer switch](https://www2.meethue.com/en-us/p/hue-dimmer-switch/046677473372) - can be used for a click and long press (hold button for 2 sec and see LED blink twice).
* [Hue tap switch](https://www2.meethue.com/en-us/p/hue-tap-switch/046677473365)
* [Hue smart button](https://www2.meethue.com/en-us/p/hue-smart-button/046677553715)
* [Lutron Aurora smart bulb dimmer](http://www.lutron.com/en-US/products/pages/standalonecontrols/dimmers-switches/smartbulbdimmer/overview.aspx)
* [Lutron Aurora rotary dimmer](http://www.lutron.com/en-US/Products/Pages/StandAloneControls/Dimmers-Switches/RotaryDimmer/Overview.aspx)
