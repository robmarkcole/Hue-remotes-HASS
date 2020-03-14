"""Hue API data parsing for sensors."""
import logging
from typing import Any, Callable, Iterable, Dict, Optional, Tuple

from homeassistant.const import STATE_OFF, STATE_ON

REMOTE_MODELS = ("RWL", "ROM", "FOH", "ZGP", "Z3-")
ENTITY_ATTRS = {
    "RWL": ["last_updated", "last_button_event", "battery", "on", "reachable"],
    "ROM": ["last_updated", "last_button_event", "battery", "on", "reachable"],
    "ZGP": ["last_updated", "last_button_event"],
    "FOH": ["last_updated", "last_button_event"],
    "Z3-": [
        "last_updated",
        "last_button_event",
        "battery",
        "on",
        "reachable",
        "dial_state",
        "dial_position",
        "software_update",
    ],
    "SML": [
        "light_level",
        "battery",
        "last_updated",
        "lx",
        "dark",
        "daylight",
        "temperature",
        "on",
        "reachable",
        "sensitivity",
        "threshold_dark",
        "threshold_offset",
    ],
}
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
RWL_RESPONSE_CODES = {
    "0": "_click",
    "1": "_hold",
    "2": "_click_up",
    "3": "_hold_up",
}
TAP_BUTTONS = {34: "1_click", 16: "2_click", 17: "3_click", 18: "4_click"}
Z3_BUTTON = {
    1000: "initial_press",
    1001: "repeat",
    1002: "short_release",
    1003: "long_release",
}
Z3_DIAL = {1: "begin", 2: "end"}


def parse_zgp(response: Dict[str, Any]) -> Dict[str, Any]:
    """Parse the json response for a ZGPSWITCH Hue Tap."""
    press = response["state"]["buttonevent"]
    if press is None or press not in TAP_BUTTONS:
        button = "No data"
    else:
        button = TAP_BUTTONS[press]

    data = {
        "model": "ZGP",
        "name": response["name"],
        "state": button,
        "last_button_event": button,
        "last_updated": response["state"]["lastupdated"].split("T"),
    }
    return data


def parse_rwl(response: Dict[str, Any]) -> Dict[str, Any]:
    """Parse the json response for a RWL Hue remote."""
    button = None
    if response["state"]["buttonevent"]:
        press = str(response["state"]["buttonevent"])
        button = str(press)[0] + RWL_RESPONSE_CODES[press[-1]]

    data = {
        "model": "RWL",
        "name": response["name"],
        "state": button,
        "battery": response["config"]["battery"],
        "on": response["config"]["on"],
        "reachable": response["config"]["reachable"],
        "last_button_event": button,
        "last_updated": response["state"]["lastupdated"].split("T"),
    }
    return data


def parse_foh(response: Dict[str, Any]) -> Dict[str, Any]:
    """Parse the JSON response for a FOHSWITCH (type still = ZGPSwitch)."""
    press = response["state"]["buttonevent"]
    if press is None or press not in FOH_BUTTONS:
        button = "No data"
    else:
        button = FOH_BUTTONS[press]

    data = {
        "model": "FOH",
        "name": response["name"],
        "state": button,
        "last_button_event": button,
        "last_updated": response["state"]["lastupdated"].split("T"),
    }
    return data


def parse_z3_rotary(response: Dict[str, Any]) -> Dict[str, Any]:
    """Parse the json response for a Lutron Aurora Rotary Event."""
    turn = response["state"]["rotaryevent"]
    dial_position = response["state"]["expectedrotation"]
    if turn is None or turn not in Z3_DIAL:
        dial = "No data"
    else:
        dial = Z3_DIAL[turn]

    data = {
        "model": "Z3-",
        "name": response["name"],
        "dial_state": dial,
        "dial_position": dial_position,
        "software_update": response["swupdate"]["state"],
        "battery": response["config"]["battery"],
        "on": response["config"]["on"],
        "reachable": response["config"]["reachable"],
        "last_updated": response["state"]["lastupdated"].split("T"),
    }
    return data


def parse_z3_switch(response: Dict[str, Any]) -> Dict[str, Any]:
    """Parse the json response for a Lutron Aurora."""
    press = response["state"]["buttonevent"]
    logging.warning(press)
    if press is None or press not in Z3_BUTTON:
        button = "No data"
    else:
        button = Z3_BUTTON[press]

    data = {
        "last_button_event": button,
        "state": button,
        "last_updated": response["state"]["lastupdated"].split("T"),
    }
    return data


def _ident_raw_sensor(
    raw_sensor_data: Dict[str, Any]
) -> Tuple[Optional[str], Callable]:
    """Identify sensor types and return unique identifier and parser."""

    def _default_parser(*x):
        return x

    model_id = raw_sensor_data["modelid"][0:3]
    unique_sensor_id = raw_sensor_data["uniqueid"]

    if model_id == "SML":
        sensor_key = model_id + "_" + unique_sensor_id[:-5]
        return sensor_key, parse_sml

    elif model_id in ("RWL", "ROM"):
        sensor_key = model_id + "_" + unique_sensor_id[:-5]
        return sensor_key, parse_rwl

    elif model_id in ("FOH", "ZGP"):
        # **** New Model ID ****
        # needed for uniqueness
        sensor_key = model_id + "_" + unique_sensor_id[-14:-3]
        if model_id == "FOH":
            return sensor_key, parse_foh

        return sensor_key, parse_zgp

    elif model_id == "Z3-":
        # Newest Model ID / Lutron Aurora / Hue Bridge
        # treats it as two sensors, I wanted them combined
        if raw_sensor_data["type"] == "ZLLRelativeRotary":  # Rotary Dial
            # Rotary key is substring of button
            sensor_key = model_id + "_" + unique_sensor_id[:-5]
            return sensor_key, parse_z3_rotary
        else:
            sensor_key = model_id + "_" + unique_sensor_id
            return sensor_key, parse_z3_switch

    return None, _default_parser


def parse_hue_api_response(sensors: Iterable[Dict[str, Any]]):
    """Take in the Hue API json response."""
    data_dict = {}  # The list of sensors, referenced by their hue_id.

    # Loop over all keys (1,2 etc) to identify sensors and get data.
    for sensor in sensors:
        _key, _raw_parser = _ident_raw_sensor(sensor)
        if _key is None:
            continue

        parsed_sensor = _raw_parser(sensor)
        if _key not in data_dict:
            data_dict[_key] = parsed_sensor
        else:
            data_dict[_key].update(parsed_sensor)

    return data_dict
