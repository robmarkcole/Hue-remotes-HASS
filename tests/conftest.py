"""Pytest fixtures for huesensors tests."""
from copy import deepcopy
from unittest.mock import MagicMock, patch

from aiohue import Bridge
from aiohue.sensors import (
    GenericSensor,
    TYPE_ZGP_SWITCH,
    TYPE_ZLL_ROTARY,
    TYPE_ZLL_SWITCH,
    ZLLRotarySensor,
    ZLLSwitchSensor,
    ZGPSwitchSensor,
)
from homeassistant.core import HomeAssistant
from homeassistant.components.hue import DOMAIN as HUE_DOMAIN, HueBridge
from homeassistant.components.hue.sensor_base import SensorManager
import pytest

from .api_samples import (
    MOCK_FOH,
    MOCK_RWL,
    MOCK_ZGP,
    MOCK_Z3_ROTARY,
    MOCK_Z3_SWITCH,
)

DEV_ID_REMOTE_1 = "00:00:00:00:00:44:23:08-f2"


class MockAsyncCounter:
    """
    Call counter for the hue data coordinator.

    Used to mock and count bridge updates done with
    `await bridge.sensor_manager.coordinator.async_request_refresh()`.
    """

    _counter: int = 0

    def __await__(self):
        """Dumb await."""
        yield

    def __call__(self, *args, **kwargs):
        """Call just returns self, increasing counter."""
        self._counter += 1
        return self

    @property
    def call_count(self) -> int:
        """Return call counter."""
        return self._counter


def add_sensor_data_to_bridge(bridge, raw_data):
    """Append a sensor raw data packed to the mocked bridge."""
    sensor_type = raw_data["type"]
    if sensor_type == TYPE_ZGP_SWITCH:
        aio_sensor_cls = ZGPSwitchSensor
    elif sensor_type == TYPE_ZLL_ROTARY:
        aio_sensor_cls = ZLLRotarySensor
    elif sensor_type in (TYPE_ZLL_SWITCH, TYPE_ZLL_SWITCH):
        aio_sensor_cls = ZLLSwitchSensor
    else:
        aio_sensor_cls = GenericSensor
    sensor_key = raw_data["uniqueid"]
    aio_sensor = aio_sensor_cls(sensor_key, deepcopy(raw_data), None)
    bridge.sensors[sensor_key] = aio_sensor


def _mock_hue_bridge(*sensors):
    # mocking HueBridge at homeassistant.components.hue level
    bridge = MagicMock(spec=Bridge)
    bridge.sensors = {}
    for i, raw_data in enumerate(sensors):
        add_sensor_data_to_bridge(bridge, raw_data)

    hue_bridge = MagicMock(spec=HueBridge)
    hue_bridge.hass = MagicMock(spec=HomeAssistant)
    hue_bridge.hass.bus = MagicMock()
    hue_bridge.api = bridge
    hue_bridge.reset_jobs = MagicMock()

    with patch("homeassistant.components.hue.sensor_base.debounce"):
        sensor_manager = SensorManager(hue_bridge)
        sensor_manager.coordinator.update_method = MockAsyncCounter()

    hue_bridge.sensor_manager = sensor_manager

    return hue_bridge


@pytest.fixture
def mock_hass():
    """Mock HA object for tests, including some sensors in hue integration."""
    hass = MagicMock(spec=HomeAssistant)
    hass.data = {
        HUE_DOMAIN: {
            0: _mock_hue_bridge(MOCK_Z3_ROTARY),
            1: _mock_hue_bridge(MOCK_ZGP, MOCK_RWL, MOCK_FOH, MOCK_Z3_SWITCH),
        }
    }
    hass.config = MagicMock()
    hass.states = MagicMock()

    return hass
