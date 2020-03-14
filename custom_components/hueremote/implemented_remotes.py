"""Hue API data parsing for sensors."""
from aiohue.sensors import (
    ZGP_SWITCH_BUTTON_1,
    ZGP_SWITCH_BUTTON_2,
    ZGP_SWITCH_BUTTON_3,
    ZGP_SWITCH_BUTTON_4,
    ZLL_SWITCH_BUTTON_1_HOLD,
    ZLL_SWITCH_BUTTON_1_INITIAL_PRESS,
    ZLL_SWITCH_BUTTON_1_LONG_RELEASED,
    ZLL_SWITCH_BUTTON_1_SHORT_RELEASED,
    ZLL_SWITCH_BUTTON_2_HOLD,
    ZLL_SWITCH_BUTTON_2_INITIAL_PRESS,
    ZLL_SWITCH_BUTTON_2_LONG_RELEASED,
    ZLL_SWITCH_BUTTON_2_SHORT_RELEASED,
    ZLL_SWITCH_BUTTON_3_HOLD,
    ZLL_SWITCH_BUTTON_3_INITIAL_PRESS,
    ZLL_SWITCH_BUTTON_3_LONG_RELEASED,
    ZLL_SWITCH_BUTTON_3_SHORT_RELEASED,
    ZLL_SWITCH_BUTTON_4_HOLD,
    ZLL_SWITCH_BUTTON_4_INITIAL_PRESS,
    ZLL_SWITCH_BUTTON_4_LONG_RELEASED,
    ZLL_SWITCH_BUTTON_4_SHORT_RELEASED,
)
from homeassistant.components.hue.sensor_base import GenericHueSensor
from homeassistant.components.remote import RemoteDevice

REMOTE_ICONS = {
    "RWL": "mdi:remote",
    "ROM": "mdi:remote",
    "ZGP": "mdi:remote",
    "FOH": "mdi:light-switch",
    "Z3-": "mdi:light-switch",
}

# HA state mapping for switch presses
FOH_BUTTONS = {
    16: "left_upper_press",
    20: "left_upper_release",
    17: "left_lower_press",
    21: "left_lower_release",
    18: "right_lower_press",
    22: "right_lower_release",
    19: "right_upper_press",
    23: "right_upper_release",
    100: "double_upper_press",
    101: "double_upper_release",
    98: "double_lower_press",
    99: "double_lower_release",
}
RWL_BUTTONS = {
    ZLL_SWITCH_BUTTON_1_INITIAL_PRESS: "1_click",
    ZLL_SWITCH_BUTTON_2_INITIAL_PRESS: "2_click",
    ZLL_SWITCH_BUTTON_3_INITIAL_PRESS: "3_click",
    ZLL_SWITCH_BUTTON_4_INITIAL_PRESS: "4_click",
    ZLL_SWITCH_BUTTON_1_HOLD: "1_hold",
    ZLL_SWITCH_BUTTON_2_HOLD: "2_hold",
    ZLL_SWITCH_BUTTON_3_HOLD: "3_hold",
    ZLL_SWITCH_BUTTON_4_HOLD: "4_hold",
    ZLL_SWITCH_BUTTON_1_SHORT_RELEASED: "1_click_up",
    ZLL_SWITCH_BUTTON_2_SHORT_RELEASED: "2_click_up",
    ZLL_SWITCH_BUTTON_3_SHORT_RELEASED: "3_click_up",
    ZLL_SWITCH_BUTTON_4_SHORT_RELEASED: "4_click_up",
    ZLL_SWITCH_BUTTON_1_LONG_RELEASED: "1_hold_up",
    ZLL_SWITCH_BUTTON_2_LONG_RELEASED: "2_hold_up",
    ZLL_SWITCH_BUTTON_3_LONG_RELEASED: "3_hold_up",
    ZLL_SWITCH_BUTTON_4_LONG_RELEASED: "4_hold_up",
}
TAP_BUTTONS = {
    ZGP_SWITCH_BUTTON_1: "1_click",
    ZGP_SWITCH_BUTTON_2: "2_click",
    ZGP_SWITCH_BUTTON_3: "3_click",
    ZGP_SWITCH_BUTTON_4: "4_click",
}
Z3_BUTTON = {
    1000: "initial_press",
    1001: "repeat",
    1002: "short_release",
    1003: "long_release",
}
Z3_DIAL = {1: "begin", 2: "end"}


class HueGenericRemote(GenericHueSensor, RemoteDevice):
    """Parent class to hold Hue Remote entity info."""

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return REMOTE_ICONS.get(self.sensor.modelid[0:3])

    @property
    def force_update(self):
        """Force update."""
        return True

    def turn_on(self, **kwargs):
        """Do nothing."""

    def turn_off(self, **kwargs):
        """Do nothing."""

    @property
    def device_state_attributes(self):
        """Return the device state attributes."""
        # TODO review attributes and device_info in UI
        attributes = {
            "model": self.sensor.type,
            "last_button_event": self.state or "No data",
            "last_updated": self.sensor.lastupdated.split("T"),
            "name": self.sensor.name,
        }
        if hasattr(self.sensor, "battery"):
            attributes.update(
                {
                    "on": self.sensor.on,
                    "reachable": self.sensor.reachable,
                    "battery_level": self.sensor.battery,
                }
            )
        return attributes


class HueRemoteZLLSwitch(HueGenericRemote):
    """
    Class to hold ZLLSwitch remote entity info.

    Models:
    * RWL021, Hue Dimmer Switch
    * ROM001, Hue Smart button
    * Z3-1BRL, Lutron Aurora
    """

    @property
    def state(self):
        """Return the last button press of the remote."""
        if self.sensor.modelid.startswith("RWL"):
            return RWL_BUTTONS.get(self.sensor.state["buttonevent"])
        return Z3_BUTTON.get(self.sensor.state["buttonevent"])


class HueRemoteZGPSwitch(HueGenericRemote):
    """
    Class to hold ZGPSwitch remote entity info.

    Models:
    * ZGPSWITCH, Hue tap switch
    * FOHSWITCH, Friends of Hue Switch
    """

    @property
    def state(self):
        """Return the last button press of the remote."""
        if self.sensor.modelid.startswith("FOH"):
            return FOH_BUTTONS.get(self.sensor.state["buttonevent"])
        return TAP_BUTTONS.get(self.sensor.state["buttonevent"])


class HueRemoteZLLRelativeRotary(HueGenericRemote):
    """
    Class to hold ZLLRelativeRotary remote entity info.

    Models:
    * Z3-1BRL, Lutron Aurora Rotary
    """

    @property
    def state(self):
        """Return the last button press of the remote."""
        return Z3_DIAL.get(self.sensor.state["rotaryevent"])

    @property
    def device_state_attributes(self):
        """Return the device state attributes."""
        # TODO implement ZLLRotarySensor in aiohue
        # attributes = super().device_state_attributes
        # attributes["dial_state"] = self.state or "No data"
        # attributes["dial_position"] = self.sensor.state["expectedrotation"]
        # attributes["software_update"] = self.sensor.raw["swupdate"]["state"]

        return {
            "model": self.sensor.type,
            "dial_state": self.state or "No data",
            "dial_position": self.sensor.state["expectedrotation"],
            "last_button_event": self.state or "No data",
            "last_updated": self.sensor.state["lastupdated"].split("T"),
            "name": self.sensor.name,
            "on": self.sensor.raw["config"]["on"],
            "reachable": self.sensor.raw["config"]["reachable"],
            "battery_level": self.sensor.raw["config"].get("battery"),
            "software_update": self.sensor.raw["swupdate"]["state"],
        }
