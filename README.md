[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![build status](http://img.shields.io/travis/robmarkcole/Hue-remotes-HASS/master.svg?style=flat)](https://travis-ci.org/robmarkcole/Hue-remotes-HASS)
[![Coverage](https://codecov.io/github/robmarkcole/Hue-remotes-HASS/coverage.svg?branch=master)](https://codecov.io/gh/robmarkcole/Hue-remotes-HASS)
[![Sponsor](https://img.shields.io/badge/sponsor-%F0%9F%92%96-green)](https://github.com/sponsors/robmarkcole)

[FOR COMMUNITY SUPPORT PLEASE USE THIS THREAD](https://community.home-assistant.io/t/hue-motion-sensors-remotes-custom-component)

# Hue-remotes-HASS
Custom integration for Hue &amp; Lutron Aurora [Friends of Hue](https://www2.meethue.com/en-us/works-with) (FOH) remotes with Home Assistant.


## Installation

Place the `custom_components` folder in your configuration directory (or add its contents to an existing `custom_components` folder). You need to set up your [Hue bridge](https://www.home-assistant.io/integrations/hue) first. Alternatively install via [HACS](https://hacs.xyz/). TODO

## Configuration

Once installed add to your configuration:

```
remote:
  - platform: hueremote
```

Hue dimmer remotes can be used for a click and long press (hold button for 2 sec and see LED blink twice).

## Supported remotes
* [Hue dimmer switch](https://www2.meethue.com/en-us/p/hue-dimmer-switch/046677473372)
* [hue tap switch](https://www2.meethue.com/en-us/p/hue-tap-switch/046677473365)
* [Lutron Aurora smart bulb dimmer](http://www.lutron.com/en-US/products/pages/standalonecontrols/dimmers-switches/smartbulbdimmer/overview.aspx)