"""Hue remotes."""
from datetime import timedelta
import logging

from aiohue.sensors import TYPE_ZGP_SWITCH, TYPE_ZLL_SWITCH
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.components.remote import PLATFORM_SCHEMA  # noqa: F401
from homeassistant.helpers.event import async_track_time_interval

from .implemented_remotes import (
    HueRemoteZGPSwitch,
    HueRemoteZLLRelativeRotary,
    HueRemoteZLLSwitch,
)
from homeassistant.components.hue import DOMAIN as HUE_DOMAIN
from homeassistant.components.hue.sensor_base import SENSOR_CONFIG_MAP
from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

# TODO add ZLLRelativeRotary definitions to aiohue
TYPE_ZLL_ROTARY = "ZLLRelativeRotary"

# Filter by aiohue.sensor data using "type" attribute
_IMPLEMENTED_REMOTE_TYPES = (TYPE_ZGP_SWITCH, TYPE_ZLL_SWITCH, TYPE_ZLL_ROTARY)

REMOTE_NAME_FORMAT = "{}"  # just the given one in Hue app

# Scan interval for remotes and binary sensors is set to < 1s
# just to ~ensure that an update is called for each HA tick,
# as using an exact 1s misses some of the ticks
DEFAULT_SCAN_INTERVAL = timedelta(seconds=0.5)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up remote platform by registering it on each Hue Bridge."""
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

                existing = bridge.sensor_manager.current.get(sensor.uniqueid)
                if existing is not None:
                    continue

                sensor_config = SENSOR_CONFIG_MAP.get(sensor.type)
                base_name = sensor.name
                name = sensor_config["name_format"].format(base_name)

                new_remote = sensor_config["class"](sensor, name, bridge)
                bridge.sensor_manager.current[sensor.uniqueid] = new_remote
                new_remotes.append(new_remote)

                _LOGGER.debug(
                    "Setup remote %s: %s", sensor.type, sensor.uniqueid,
                )
            if new_remotes:
                async_add_entities(new_remotes)

        # Add listener to add discovered remotes
        bridge.sensor_manager.coordinator.async_add_listener(_add_remotes)
        _add_remotes()

        # Set up updates at scan_interval
        async def _update_remotes(now=None):
            """Request a bridge data refresh so remote states are updated."""
            await bridge.sensor_manager.coordinator.async_refresh()
            _LOGGER.debug("Update requested at %s", now)

        remote_sc = max(
            DEFAULT_SCAN_INTERVAL, config.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )
        if remote_sc < bridge.sensor_manager.coordinator.update_interval:
            # Add listener to update remotes at high rate
            # TODO change sm.coordinator.update_interval instead.
            #  It can be done right here, but any bridge.reset event
            #  would re-write it, so we maintain our own scheduler meanwhile
            async_track_time_interval(
                hass, _update_remotes, remote_sc,
            )


SENSOR_CONFIG_MAP.update(
    {
        TYPE_ZLL_SWITCH: {
            "platform": "remote",
            "name_format": REMOTE_NAME_FORMAT,
            "class": HueRemoteZLLSwitch,
        },
        TYPE_ZGP_SWITCH: {
            "platform": "remote",
            "name_format": REMOTE_NAME_FORMAT,
            "class": HueRemoteZGPSwitch,
        },
        TYPE_ZLL_ROTARY: {
            "platform": "remote",
            "name_format": REMOTE_NAME_FORMAT,
            "class": HueRemoteZLLRelativeRotary,
        },
    }
)
