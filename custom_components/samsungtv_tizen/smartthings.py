#Smartthings TV integration#
import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
from typing import Any, Dict, List, Optional
from aiohttp import ClientSession
import json
import os
from homeassistant.const import (
    STATE_OFF,
    STATE_ON,
)
API_BASEURL = "https://api.smartthings.com/v1"
API_DEVICES = API_BASEURL + "/devices/"
COMMAND_POWER_OFF = "{'commands': [{'component': 'main','capability': 'switch','command': 'off'}]}"
COMMAND_POWER_ON = "{'commands': [{'component': 'main','capability': 'switch','command': 'on'}]}"
COMMAND_REFRESH = "{'commands':[{'component': 'main','capability': 'refresh','command': 'refresh'}]}"
COMMAND_PAUSE = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'pause'}]}"
COMMAND_MUTE = "{'commands':[{'component': 'main','capability': 'audioMute','command': 'mute'}]}"
COMMAND_UNMUTE = "{'commands':[{'component': 'main','capability': 'audioMute','command': 'unmute'}]}"
COMMAND_PLAY = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'play'}]}"
COMMAND_STOP = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'stop'}]}"
COMMAND_REWIND = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'rewind'}]}"
COMMAND_FAST_FORWARD = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'fastForward'}]}"
COMMAND_CHANNEL_UP = "{'commands':[{'component': 'main','capability': 'tvChannel','command': 'channelUp'}]}"
COMMAND_CHANNEL_DOWN = "{'commands':[{'component': 'main','capability': 'tvChannel','command': 'channelDown'}]}"

def _headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": "Bearer " + api_key,
    }

class SmartThingsTV:

    def __init__(
            self,
            api_key: str,
            device_id: str,
            session: Optional[ClientSession] = None,
    ):
   
        """Initialize SmartThingsTV."""
        self._api_key = api_key
        self._device_id = device_id
        if session:
            self._session = session
            self._managed_session = False
        else:
            self._session = ClientSession()
            self._managed_session = True
            
        self._state = STATE_OFF
        self._muted = False
        self._volume = 10
        self._source_list = None
        self._source = None
        self._channel = None
        self._channel_name = None

    @property
    def api_key(self) -> str:
        """Return currently api_key."""
        return self._api_key

    @property
    def device_id(self) -> str:
        """Return currently device_id."""
        return self._device_id

    @property
    def state(self) -> str:
        """Return currently state."""
        return self._state

    @property
    def muted(self) -> bool:
        """Return currently muted state."""
        return self._muted

    @property
    def volume(self) -> int:
        """Return currently volume."""
        return self._volume

    @property
    def source(self) -> str:
        """Return currently source."""
        return self._source

    @property
    def channel(self) -> str:
        """Return currently channel."""
        return self._channel

    @property
    def channel_name(self) -> str:
        """Return currently channel_name."""
        return self._channel_name

    async def async_device_update(self):

        API_DEVICE = API_DEVICES + self._device_id
        API_COMMAND = API_DEVICE + "/commands"
        API_DEVICE_STATUS = API_DEVICE + "/states"

        async with self._session.post(
            API_COMMAND,
            headers=_headers(self._api_key),
            data=COMMAND_REFRESH,
            raise_for_status=True,
        ) as resp:
            cmdurl = await resp.json()

        async with self._session.get(
            API_DEVICE_STATUS,
            headers=_headers(self._api_key),
            raise_for_status=True,
        ) as resp:
            data = await resp.json()

        device_volume = data['main']['volume']['value']
        device_volume = int(device_volume) / 100
        device_state = data['main']['switch']['value']
        device_source = data['main']['inputSource']['value']
        device_all_sources = json.loads(data['main']['supportedInputSources']['value'])
        device_tv_chan = data['main']['tvChannel']['value']
        device_tv_chan_name = data['main']['tvChannelName']['value']
        device_muted = data['main']['mute']['value'] 

        if device_state == "off":
            self._state = STATE_OFF
        else:
            self._state = STATE_ON
        self._volume = device_volume
        self._source_list = device_all_sources
        if device_muted == "mute":
            self._muted = True
        else:
            self._muted = False
        self._source = device_source
        self._channel = device_tv_chan
        self._channel_name = device_tv_chan_name

    async def async_send_command(self, command, cmdtype):

        API_DEVICE = API_DEVICES + self._device_id
        API_COMMAND = API_DEVICE + "/commands"
        datacmd = None

        if cmdtype == "setvolume": # sets volume
           API_COMMAND_DATA = "{'commands':[{'component': 'main','capability': 'audioVolume','command': 'setVolume','arguments': "
           API_COMMAND_ARG  = "[{}]}}]}}".format(command)
           API_FULL = API_COMMAND_DATA + API_COMMAND_ARG
           datacmd = API_FULL
        elif cmdtype == "stepvolume": # steps volume up or down
           if command == "up":
              API_COMMAND_DATA = "{'commands':[{'component': 'main','capability': 'audioVolume','command': 'volumeUp'}]}"
              datacmd = API_COMMAND_DATA
           else:
              API_COMMAND_DATA = "{'commands':[{'component': 'main','capability': 'audioVolume','command': 'volumeDown'}]}"
              datacmd = API_COMMAND_DATA
        elif cmdtype == "audiomute": # mutes audio
           if self._cloud_muted == False:
              datacmd = COMMAND_MUTE
           else:
              datacmd = COMMAND_UNMUTE
        elif cmdtype == "turn_off": # turns off
           datacmd = COMMAND_POWER_OFF
        elif cmdtype == "turn_on": # turns on
           datacmd = COMMAND_POWER_ON
        elif cmdtype == "selectsource": #changes source
           API_COMMAND_DATA =  "{'commands':[{'component': 'main','capability': 'mediaInputSource','command': 'setInputSource', 'arguments': "
           API_COMMAND_ARG  = "['{}']}}]}}".format(command)
           API_FULL = API_COMMAND_DATA + API_COMMAND_ARG
           datacmd = API_FULL
        elif cmdtype == "selectchannel": #changes channel
           API_COMMAND_DATA =  "{'commands':[{'component': 'main','capability': 'tvChannel','command': 'setTvChannel', 'arguments': "
           API_COMMAND_ARG  = "['{}']}}]}}".format(command)
           API_FULL = API_COMMAND_DATA + API_COMMAND_ARG
           datacmd = API_FULL
        elif cmdtype == "stepchannel": # steps channel up or down
           if command == "up":
              datacmd = COMMAND_CHANNEL_UP
           else:
              datacmd = COMMAND_CHANNEL_DOWN
            
        if datacmd:
           async with self._session.post(
               API_COMMAND,
               headers=_headers(self._api_key),
               data=datacmd,
               raise_for_status=True,
           ) as resp:
               cmdurl = await resp.json()
