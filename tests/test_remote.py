"""Tests for remote.py."""
import logging
from datetime import timedelta

from homeassistant.components.hue import DOMAIN as HUE_DOMAIN

from custom_components.hueremote import DOMAIN
from custom_components.hueremote.remote import async_setup_platform

from .api_samples import MOCK_ROM
from .conftest import DEV_ID_REMOTE_1, add_sensor_data_to_bridge


async def test_platform_remote_setup(mock_hass, caplog):
    """Test platform setup for remotes."""
    entity_counter = []
    config_remote = {"platform": DOMAIN, "scan_interval": timedelta(seconds=3)}

    sm_b1 = mock_hass.data[HUE_DOMAIN][0].sensor_manager
    sm_b2 = mock_hass.data[HUE_DOMAIN][1].sensor_manager
    data_coord_b1 = sm_b1.coordinator
    data_coord_b2 = sm_b2.coordinator
    assert DOMAIN not in mock_hass.data

    def _add_entity_counter(*_args):
        entity_counter.append(1)

    with caplog.at_level(logging.DEBUG):
        # setup remotes
        await async_setup_platform(mock_hass, config_remote, _add_entity_counter)
        assert sum(entity_counter) == 2

        remote_container = mock_hass.data[DOMAIN]
        assert len(remote_container) == 5

        # Check bridge updates
        assert data_coord_b1.update_method.call_count == 0
        assert data_coord_b2.update_method.call_count == 0

        assert DEV_ID_REMOTE_1 in remote_container
        remote = remote_container[DEV_ID_REMOTE_1]
        assert remote.state == "3_click"
        assert len(caplog.messages) == 7
        assert remote.icon == "mdi:remote"
        for rem_i in remote_container.values():
            assert rem_i.state
            assert not rem_i.force_update
            assert rem_i.icon
            assert rem_i.device_state_attributes

        # Change the state on bridge and call update
        hue_bridge = mock_hass.data[HUE_DOMAIN][1].api
        r1_data_st = hue_bridge.sensors[DEV_ID_REMOTE_1].raw["state"]
        r1_data_st["buttonevent"] = 16
        r1_data_st["lastupdated"] = "2019-06-22T14:43:55"
        hue_bridge.sensors[DEV_ID_REMOTE_1].raw["state"] = r1_data_st
        assert len(caplog.messages) == 7

        await data_coord_b1.async_refresh()
        await data_coord_b2.async_refresh()
        assert data_coord_b1.update_method.call_count == 1
        assert data_coord_b2.update_method.call_count == 1
        assert remote.state == "2_click"

        assert len(caplog.messages) == 9

        # add a new item to bridge
        add_sensor_data_to_bridge(hue_bridge, MOCK_ROM)
        await data_coord_b2.async_refresh()
        assert data_coord_b2.update_method.call_count == 2
        assert sum(entity_counter) == 3
        assert len(remote_container) == 6
        assert len(caplog.messages) == 11
