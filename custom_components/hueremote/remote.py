"""Hue remotes."""
from datetime import timedelta
import logging

from aiohue.sensors import TYPE_ZGP_SWITCH, TYPE_ZLL_ROTARY, TYPE_ZLL_SWITCH
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.components.hue import DOMAIN as HUE_DOMAIN
from homeassistant.components.remote import PLATFORM_SCHEMA  # noqa: F401
from homeassistant.core import callback
from .implemented_remotes import (
    HueRemoteZGPSwitch,
    HueRemoteZLLRelativeRotary,
    HueRemoteZLLSwitch,
)

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

_MINIMUM_SCAN_INTERVAL = timedelta(seconds=1)
_PLATFORM = "remote"
_REMOTE_NAME_FORMAT = "{}"  # just the given one in Hue app

# Implemented remotes: gilter by aiohue.sensor data using "type" attribute
_REMOTE_CONFIG_MAP = {
    TYPE_ZLL_SWITCH: {
        "platform": _PLATFORM,
        "name_format": _REMOTE_NAME_FORMAT,
        "class": HueRemoteZLLSwitch,
    },
    TYPE_ZGP_SWITCH: {
        "platform": _PLATFORM,
        "name_format": _REMOTE_NAME_FORMAT,
        "class": HueRemoteZGPSwitch,
    },
    TYPE_ZLL_ROTARY: {
        "platform": _PLATFORM,
        "name_format": _REMOTE_NAME_FORMAT,
        "class": HueRemoteZLLRelativeRotary,
    },
}
_IMPLEMENTED_REMOTE_TYPES = tuple(_REMOTE_CONFIG_MAP.keys())


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up remote platform by adding an update listener on each Hue Bridge."""
    remote_sc = max(
        _MINIMUM_SCAN_INTERVAL,
        config.get(CONF_SCAN_INTERVAL, 2 * _MINIMUM_SCAN_INTERVAL),
    )

    # Store the created remote entities in the domain data
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    for bridge_entry_id, bridge in hass.data[HUE_DOMAIN].items():

        @callback
        def _add_remotes():
            """Check for new devices to be added to HA."""
            new_remotes = []
            api = bridge.api.sensors
            for item_id in api:
                sensor = api[item_id]
                if sensor.type not in _IMPLEMENTED_REMOTE_TYPES:
                    continue  # pragma: no cover

                existing = hass.data[DOMAIN].get(sensor.uniqueid)
                if existing is not None:
                    continue

                sensor_config = _REMOTE_CONFIG_MAP.get(sensor.type)
                base_name = sensor.name
                name = sensor_config["name_format"].format(base_name)
                new_remote = sensor_config["class"](sensor, name, bridge)
                hass.data[DOMAIN][sensor.uniqueid] = new_remote
                new_remotes.append(new_remote)

                _LOGGER.debug(
                    "Setup remote %s: %s", sensor.type, sensor.uniqueid,
                )
            if new_remotes:
                async_add_entities(new_remotes)

            # Check update_interval
            if remote_sc < bridge.sensor_manager.coordinator.update_interval:
                # Update refresh rate for sensors and remotes
                _LOGGER.debug(
                    "Modified hue update interval: from %s to %s",
                    bridge.sensor_manager.coordinator.update_interval,
                    remote_sc,
                )
                bridge.sensor_manager.coordinator.update_interval = remote_sc

        # Add listener to add discovered remotes
        bridge.sensor_manager.coordinator.async_add_listener(_add_remotes)
        _add_remotes()
