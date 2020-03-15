"""Examples of raw and parsed data for known remotes."""

# Known remotes
MOCK_ZGP = {
    "state": {"buttonevent": 17, "lastupdated": "2019-06-22T14:43:50"},
    "swupdate": {"state": "notupdatable", "lastinstall": None},
    "config": {"on": True},
    "name": "Hue Tap",
    "type": "ZGPSwitch",
    "modelid": "ZGPSWITCH",
    "manufacturername": "Philips",
    "productname": "Hue tap switch",
    "diversityid": "d8cde5d5-0eef-4b95-b0f0-71ddd2952af4",
    "uniqueid": "00:00:00:00:00:44:23:08-f2",
    "capabilities": {"certified": True, "primary": True, "inputs": []},
}
MOCK_FOH = {
    "state": {"buttonevent": 21, "lastupdated": "2019-04-22T07:48:56"},
    "swupdate": {"state": "notupdatable", "lastinstall": None},
    "config": {"on": True},
    "name": "Bed Switch",
    "type": "ZGPSwitch",
    "modelid": "FOHSWITCH",
    "manufacturername": "PhilipsFoH",
    "productname": "Friends of Hue Switch",
    "diversityid": "ded6468f-6b26-4a75-9582-f2b52d36a5a3",
    "uniqueid": "00:00:00:00:01:70:xx:xx-xx",
    "capabilities": {
        "certified": True,
        "inputs": [
            {
                "repeatintervals": [],
                "events": [
                    {"buttonevent": 16, "eventtype": "initial_press"},
                    {"buttonevent": 20, "eventtype": "short_release"},
                ],
            },
            {
                "repeatintervals": [],
                "events": [
                    {"buttonevent": 17, "eventtype": "initial_press"},
                    {"buttonevent": 21, "eventtype": "short_release"},
                ],
            },
            {
                "repeatintervals": [],
                "events": [
                    {"buttonevent": 19, "eventtype": "initial_press"},
                    {"buttonevent": 23, "eventtype": "short_release"},
                ],
            },
            {
                "repeatintervals": [],
                "events": [
                    {"buttonevent": 18, "eventtype": "initial_press"},
                    {"buttonevent": 22, "eventtype": "short_release"},
                ],
            },
        ],
    },
}
MOCK_ROM = {
    "state": {"buttonevent": 1002, "lastupdated": "2019-11-16T11:48:24"},
    "swupdate": {"state": "noupdates", "lastinstall": "2019-11-16T10:54:58"},
    "config": {"on": True, "battery": 100, "reachable": True, "pending": []},
    "name": "Hue Smart button 2",
    "type": "ZLLSwitch",
    "modelid": "ROM001",
    "manufacturername": "Philips",
    "productname": "Hue Smart button",
    "diversityid": "8b18a40c-eb6a-40d7-a0af-eb0906613d41",
    "swversion": "2.21.0_r29784",
    "uniqueid": "00:17:88:01:06:06:81:5c-01-fc00",
    "capabilities": {
        "certified": True,
        "primary": True,
        "inputs": [
            {
                "repeatintervals": [800],
                "events": [
                    {"buttonevent": 1000, "eventtype": "initial_press"},
                    {"buttonevent": 1001, "eventtype": "repeat"},
                    {"buttonevent": 1002, "eventtype": "short_release"},
                    {"buttonevent": 1003, "eventtype": "long_release"},
                ],
            }
        ],
    },
}
MOCK_RWL = {
    "state": {"buttonevent": 4002, "lastupdated": "2019-12-28T21:58:02"},
    "swupdate": {"state": "noupdates", "lastinstall": "2019-10-13T13:16:15"},
    "config": {"on": True, "battery": 100, "reachable": True, "pending": []},
    "name": "Hue dimmer switch 1",
    "type": "ZLLSwitch",
    "modelid": "RWL021",
    "manufacturername": "Philips",
    "productname": "Hue dimmer switch",
    "diversityid": "73bbabea-3420-499a-9856-46bf437e119b",
    "swversion": "6.1.1.28573",
    "uniqueid": "00:17:88:01:10:3e:3a:dc-02-fc00",
    "capabilities": {"certified": True, "primary": True, "inputs": []},
}
MOCK_Z3_ROTARY = {
    "state": {
        "rotaryevent": 2,
        "expectedrotation": 208,
        "expectedeventduration": 400,
        "lastupdated": "2020-01-31T15:56:19",
    },
    "swupdate": {"state": "noupdates", "lastinstall": "2019-11-26T03:35:21"},
    "config": {"on": True, "battery": 100, "reachable": True, "pending": []},
    "name": "Lutron Aurora 1",
    "type": "ZLLRelativeRotary",
    "modelid": "Z3-1BRL",
    "manufacturername": "Lutron",
    "productname": "Lutron Aurora",
    "diversityid": "2c3a75ff-55c4-4e4d-8c44-82d330b8eb9b",
    "swversion": "3.4",
    "uniqueid": "ff:ff:00:0f:e7:fd:ba:b7-01-fc00-0014",
    "capabilities": {
        "certified": True,
        "primary": True,
        "inputs": [
            {
                "repeatintervals": [400],
                "events": [
                    {"rotaryevent": 1, "eventtype": "start"},
                    {"rotaryevent": 2, "eventtype": "repeat"},
                ],
            }
        ],
    },
}
MOCK_Z3_SWITCH = {
    "state": {"buttonevent": 1002, "lastupdated": "2019-09-01T17:45:47"},
    "swupdate": {"state": "noupdates", "lastinstall": "2019-09-01T15:26:15"},
    "config": {"on": True, "battery": 100, "reachable": True, "pending": []},
    "name": "Lutron Aurora 2",
    "type": "ZLLSwitch",
    "modelid": "Z3-1BRL",
    "manufacturername": "Lutron",
    "productname": "Lutron Aurora",
    "diversityid": "2c3a75ff-55c4-4e4d-8c44-82d330b8eb9b",
    "swversion": "3.1",
    "uniqueid": "ff:ff:00:0f:e7:fe:95:cd-01-fc00",
    "capabilities": {
        "certified": True,
        "primary": False,
        "inputs": [
            {
                "repeatintervals": [800],
                "events": [
                    {"buttonevent": 1000, "eventtype": "initial_press"},
                    {"buttonevent": 1001, "eventtype": "repeat"},
                    {"buttonevent": 1002, "eventtype": "short_release"},
                    {"buttonevent": 1003, "eventtype": "long_release"},
                ],
            }
        ],
    },
}
