"""The samsungtv_smart integration."""

import socket
import asyncio
import logging
import os
from aiohttp import ClientConnectionError, ClientSession
from async_timeout import timeout
from .websockets import SamsungTVWS
from .exceptions import ConnectionFailure
from websocket import WebSocketException
from .smartthings import SmartThingsTV

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.components.media_player.const import DOMAIN as MP_DOMAIN
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_MAC,
    CONF_ID,
    CONF_PORT,
    CONF_DEVICE_ID,
    CONF_TIMEOUT,
    CONF_API_KEY,
    CONF_BROADCAST_ADDRESS,
)

from .const import (
    DOMAIN,
    BASE_URL,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_TIMEOUT,
    DEFAULT_UPDATE_METHOD,
    CONF_DEVICE_NAME,
    CONF_DEVICE_MODEL,
    CONF_UPDATE_METHOD,
    CONF_UPDATE_CUSTOM_PING_URL,
    CONF_SOURCE_LIST,
    CONF_APP_LIST,
    CONF_SHOW_CHANNEL_NR,
    CONF_SCAN_APP_HTTP,
    DEFAULT_SOURCE_LIST,
    UPDATE_METHODS,
    WS_PREFIX,
    RESULT_SUCCESS,
    RESULT_NOT_SUCCESSFUL,
    RESULT_NOT_SUPPORTED,
    RESULT_WRONG_APIKEY,
)

SAMSMART_SCHEMA = {
        vol.Optional(CONF_MAC): cv.string,
        vol.Optional(CONF_SOURCE_LIST, default=DEFAULT_SOURCE_LIST): cv.string,
        vol.Optional(CONF_APP_LIST): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
        vol.Optional(CONF_UPDATE_METHOD): vol.In(UPDATE_METHODS.values()),
        vol.Optional(CONF_UPDATE_CUSTOM_PING_URL): cv.string,
        vol.Optional(CONF_SHOW_CHANNEL_NR, default=False): cv.boolean,
        vol.Optional(CONF_BROADCAST_ADDRESS): cv.string,
        vol.Optional(CONF_SCAN_APP_HTTP, default=True): cv.boolean,
}

def ensure_unique_hosts(value):
    """Validate that all configs have a unique host."""
    vol.Schema(vol.Unique("duplicate host entries found"))(
        [socket.gethostbyname(entry[CONF_HOST]) for entry in value]
    )
    return value

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            cv.ensure_list,
            [
                cv.deprecated(CONF_PORT),
                vol.Schema ({
                        vol.Required(CONF_HOST): cv.string,
                        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
                        vol.Optional(CONF_API_KEY): cv.string,
                        vol.Optional(CONF_DEVICE_NAME): cv.string,
                        #vol.Optional(CONF_DEVICE_ID): cv.string,
                }).extend(SAMSMART_SCHEMA),
            ],
            ensure_unique_hosts,
        )
    },
    extra=vol.ALLOW_EXTRA,
)

_LOGGER = logging.getLogger(__name__)

class SamsungTVInfo:

    def __init__(self, hass, hostname, name = ""):
        self._hass = hass
        self._hostname = hostname
        self._name = name

        self._uuid = None
        self._macaddress = None
        self._device_name = None
        self._devive_model = None
        self._token_support = False
        self._port = 0

    def _gen_token_file(self, port):
        if port != 8002:
            return None
            
        token_file = os.path.dirname(os.path.realpath(__file__)) + '/token-' + self._hostname + '.txt'

        if os.path.isfile(token_file) is False:
            # For correct auth
            self._timeout = 45

            # Create token file for catch possible errors
            try:
                handle = open(token_file, "w+")
                handle.close()
            except:
                _LOGGER.error("Samsung TV - Error creating token file: %s", self._token_file)
                return None
        
        return token_file

    def _try_connect_ws(self):
        for port in (8001, 8002):

            try:
                _LOGGER.debug("Try config with port: %s", str(port))
                with SamsungTVWS(
                    name=WS_PREFIX + " " + self._name, # this is the name shown in the TV list of external device.
                    host=self._hostname,
                    port=port,
                    token_file=self._gen_token_file(port),
                    timeout=45, # We need this high timeout because waiting for auth popup is just an open socket
                ) as remote:
                    remote.open()
                _LOGGER.debug("Working config with port: %s", str(port))
                self._port = port
                return RESULT_SUCCESS
            except WebSocketException:
                _LOGGER.debug("Working but unsupported config on port: %s", str(port))
                #return RESULT_NOT_SUPPORTED
            except (OSError, ConnectionFailure) as err:
                _LOGGER.debug("Failing config with port: %s, error: %s", str(port), err)
    
        return RESULT_NOT_SUCCESSFUL

    async def get_st_devices(self, api_key, session: ClientSession, st_device_label=""):
        devices = {}
        try:
            with timeout(4):
                devices = await SmartThingsTV.get_devices_list(api_key, session, st_device_label)
        except (asyncio.TimeoutError, ClientConnectionError) as ex:
            pass

        return devices

    async def get_device_info(self, session: ClientSession):

        if session is None:
            return RESULT_NOT_SUCCESSFUL

        result = await self._hass.async_add_executor_job(self._try_connect_ws)
        if result != RESULT_SUCCESS:
            return result
        
        try:
            with timeout(2):
                async with session.get(
                    BASE_URL.format(host = self._hostname), 
                    raise_for_status=True
                ) as resp:
                    info = await resp.json()
        except (asyncio.TimeoutError, ClientConnectionError) as ex:
            _LOGGER.error("Error getting HTTP info for TV: " + self._hostname)
            return RESULT_NOT_SUCCESSFUL
            
        device = info.get("device", None)
        if not device:
            return RESULT_NOT_SUCCESSFUL
            
        device_id = device.get("id")
        if device_id and device_id.startswith("uuid:"):
            self._uuid = device_id[len("uuid:") :]
        else:
            self._uuid = device_id
        self._macaddress = device.get("wifiMac")
        self._device_name = device.get("name")
        if not self._name:
            self._name = self._device_name
        self._device_model = device.get("modelName")
        self._tokensupport = device.get("TokenAuthSupport")

        return result

async def async_setup(hass: HomeAssistantType, config: ConfigEntry):
    """Set up the Samsung TV integration."""
    if DOMAIN in config:
        hass.data[DOMAIN] = {}
        for entry_config in config[DOMAIN]:
            ip_address = await hass.async_add_executor_job(
                socket.gethostbyname, entry_config[CONF_HOST]
            )
            for key in SAMSMART_SCHEMA:
                hass.data[DOMAIN].setdefault(ip_address, {})[key] = entry_config.get(key)
            if not entry_config.get(CONF_NAME):
                entry_config[CONF_NAME] = DEFAULT_NAME
            entry_config[SOURCE_IMPORT] = True
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN, context={"source": SOURCE_IMPORT}, data=entry_config
                )
            )

    return True

async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Set up the Samsung TV platform."""
    hass.data.setdefault(DOMAIN, {}).setdefault(entry.unique_id, {})
    
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, MP_DOMAIN)
    )

    return True

async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    await asyncio.gather(
        *[
            hass.config_entries.async_forward_entry_unload(config_entry, MP_DOMAIN)
        ]
    )
    hass.data[DOMAIN].pop(config_entry.unique_id)
    if not hass.data[DOMAIN]:
        hass.data.pop(DOMAIN)
    return True
