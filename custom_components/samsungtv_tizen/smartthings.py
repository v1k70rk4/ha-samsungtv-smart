#Smartthings TV integration#
import asyncio
from datetime import timedelta
from async_timeout import timeout
import logging
from typing import Any, Dict, List, Optional
from aiohttp import ClientSession
import json
import os

from homeassistant.util import Throttle
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
COMMAND_VOLUME_UP = "{'commands':[{'component': 'main','capability': 'audioVolume','command': 'volumeUp'}]}"
COMMAND_VOLUME_DOWN = "{'commands':[{'component': 'main','capability': 'audioVolume','command': 'volumeDown'}]}"
COMMAND_PLAY = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'play'}]}"
COMMAND_STOP = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'stop'}]}"
COMMAND_REWIND = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'rewind'}]}"
COMMAND_FAST_FORWARD = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'fastForward'}]}"
COMMAND_CHANNEL_UP = "{'commands':[{'component': 'main','capability': 'tvChannel','command': 'channelUp'}]}"
COMMAND_CHANNEL_DOWN = "{'commands':[{'component': 'main','capability': 'tvChannel','command': 'channelDown'}]}"

COMMAND_SET_VOLUME = "{'commands':[{'component': 'main','capability': 'audioVolume','command': 'setVolume','arguments': "
ARGS_SET_VOLUME  = "[{}]}}]}}"
COMMAND_SET_SOURCE =  "{'commands':[{'component': 'main','capability': 'mediaInputSource','command': 'setInputSource', 'arguments': "
ARGS_SET_SOURCE  = "['{}']}}]}}"
COMMAND_SET_CHANNEL =  "{'commands':[{'component': 'main','capability': 'tvChannel','command': 'setTvChannel', 'arguments': "
ARGS_SET_CHANNEL  = "['{}']}}]}}"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)
_LOGGER = logging.getLogger(__name__)

def _headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": "Bearer " + api_key,
    }

class SmartThingsTV:

    def __init__(
            self,
            api_key: str,
            device_id: str,
            refresh_status: bool = True,
            session: Optional[ClientSession] = None,
    ):
   
        """Initialize SmartThingsTV."""
        self._api_key = api_key
        self._device_id = device_id
        self._refresh_status = refresh_status
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
        self._prev_source = self._source = None
        self._prev_channel = self._channel = ""
        self._prev_channel_name = self._channel_name = ""

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

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def _device_refresh(self, **kwargs):

        API_DEVICE = API_DEVICES + self._device_id
        API_COMMAND = API_DEVICE + "/commands"

        if self._refresh_status:
            with timeout(5):
                await self._session.post(
                    API_COMMAND,
                    headers=_headers(self._api_key),
                    data=COMMAND_REFRESH,
                    raise_for_status=True,
                )

    def set_application(self, appid):
        if self._refresh_status:
            self._channel = ""
            self._channel_name = appid

    async def async_device_update(self):

        API_DEVICE = API_DEVICES + self._device_id
        API_DEVICE_HEALT = API_DEVICE + "/health"
        API_DEVICE_STATUS = API_DEVICE + "/states"
        API_DEVICE_MAIN_STATUS = API_DEVICE + "/components/main/status" #not used, just for reference

        # this get the real status of the device
        async with self._session.get(
            API_DEVICE_HEALT,
            headers=_headers(self._api_key),
            raise_for_status=True,
        ) as resp:
            health = await resp.json()

        _LOGGER.debug(health)

        if health['state'] == "ONLINE":
            self._state = STATE_ON
        else:
            self._state = STATE_OFF
            return

        await self._device_refresh()

        async with self._session.get(
            API_DEVICE_STATUS,
            headers=_headers(self._api_key),
            raise_for_status=True,
        ) as resp:
            data = await resp.json()

        _LOGGER.debug(data)

        device_state = data['main']['switch']['value']
        device_volume = data['main']['volume']['value']
        device_volume = int(device_volume) / 100
        device_muted = data['main']['mute']['value'] 
        device_all_sources = json.loads(data['main']['supportedInputSources']['value'])
        device_source = data['main']['inputSource']['value']
        device_tv_chan = data['main']['tvChannel']['value']
        device_tv_chan_name = data['main']['tvChannelName']['value']

        self._volume = device_volume
        self._source_list = device_all_sources
        if device_muted == "mute":
            self._muted = True
        else:
            self._muted = False
            
        if (self._prev_source != device_source or self._prev_channel != device_tv_chan or self._prev_channel_name != device_tv_chan_name):
            self._source = self._prev_source = device_source
            # if the status is not refreshed this info may become not reliable
            if self._refresh_status:
                self._channel = self._prev_channel = device_tv_chan
                self._channel_name = self._prev_channel_name = device_tv_chan_name

    async def async_send_command(self, command, cmdtype):

        API_DEVICE = API_DEVICES + self._device_id
        API_COMMAND = API_DEVICE + "/commands"
        datacmd = None

        if cmdtype == "setvolume": # sets volume
           cmdargs = ARGS_SET_VOLUME.format(command)
           datacmd = COMMAND_SET_VOLUME + cmdargs
        elif cmdtype == "stepvolume": # steps volume up or down
           if command == "up":
              datacmd = COMMAND_VOLUME_UP
           else:
              datacmd = COMMAND_VOLUME_DPWN
        elif cmdtype == "audiomute": # mutes audio
           if self._muted == False:
              datacmd = COMMAND_MUTE
           else:
              datacmd = COMMAND_UNMUTE
        elif cmdtype == "turn_off": # turns off
           datacmd = COMMAND_POWER_OFF
        elif cmdtype == "turn_on": # turns on
           datacmd = COMMAND_POWER_ON
        elif cmdtype == "selectsource": #changes source
           cmdargs = ARGS_SET_SOURCE.format(command)
           datacmd = COMMAND_SET_SOURCE + cmdargs
           # set property to reflect new changes
           self._source = command
           self._channel = ""
           self._channel_name = ""
        elif cmdtype == "selectchannel": #changes channel
           cmdargs = ARGS_SET_CHANNEL.format(command)
           datacmd = COMMAND_SET_CHANNEL + cmdargs
        elif cmdtype == "stepchannel": # steps channel up or down
           if command == "up":
              datacmd = COMMAND_CHANNEL_UP
           else:
              datacmd = COMMAND_CHANNEL_DOWN
            
        if datacmd:
           await self._session.post(
               API_COMMAND,
               headers=_headers(self._api_key),
               data=datacmd,
               raise_for_status=True,
           )
           
           await self._device_refresh()

