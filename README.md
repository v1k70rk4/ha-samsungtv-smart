[![](https://img.shields.io/github/release/ollo69/ha-samsungtv-smart/all.svg?style=for-the-badge)](https://github.com/ollo69/ha-samsungtv-smart/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![](https://img.shields.io/github/license/ollo69/ha-samsungtv-smart?style=for-the-badge)](LICENSE)
[![](https://img.shields.io/badge/MAINTAINER-%40ollo69-red?style=for-the-badge)](https://github.com/ollo69)
[![](https://img.shields.io/badge/COMMUNITY-FORUM-success?style=for-the-badge)](https://community.home-assistant.io)

# HomeAssistant - SamsungTV Smart Component

This is a custom component to allow control of SamsungTV devices in [HomeAssistant](https://home-assistant.io). 
Is a modified version of the built-in [samsungtv](https://www.home-assistant.io/integrations/samsungtv/) with some extra
 features.<br/>
**This plugin is only for 2016+ TVs model!** (maybe all tizen family)

This project is a fork of the component [SamsungTV Tizen](https://github.com/jaruba/ha-samsungtv-tizen). I added some 
feature like the possibility to configure it using the HA user interface, simplifing the configuration process. 
I also added some code optimizition in the comunication layer using async aiohttp instead of request.
**Part of the code and documentation available here come from the original project.**<br/>

### Important note 
Starting from version 0.2.x the websocket protocol has been completely rewritten in order to keep communication with the
TV always open (as it should be). In addition, all REST-type messages, that create problems in communications and 
management of the access token, have been eliminated.<br/>
The new protocol should make communication with the TV much more efficient, however, being this the first version, I ask 
everyone to open any [issues](https://github.com/ollo69/ha-samsungtv-smart/issues) with the greatest number of details 
so that I can identify and resolve any anomalies in the best way. For those who cannot use the new version, they can 
eventually install the latest version 0.1.x waiting new fixes.

# Additional Features:

* Ability to send keys using a native Home Assistant service
* Ability to send chained key commands using a native Home Assistant service
* Supports Assistant commands (Google Home, should work with Alexa too, but untested)
* Extended volume control
* Ability to customize source list at media player dropdown list
* Cast video URLs to Samsung TV
* Connect to SmartThings Cloud API for additional features: see TV channel names, see which HDMI source is selected, more key codes to change input source

![N|Solid](https://i.imgur.com/8mCGZoO.png)
![N|Solid](https://i.imgur.com/t3e4bJB.png)

# Installation

### 1. Easy Mode

Install via HACS.

### 2. Manual

Install it as you would do with any homeassistant custom component:

1. Download `custom_components` folder.
1. Copy the `samsungtv_smart` directory within the `custom_components` directory of your homeassistant installation. The `custom_components` directory resides within your homeassistant configuration directory.
**Note**: if the custom_components directory does not exist, you need to create it.
After a correct installation, your configuration directory should look like the following.
    ```
    └── ...
    └── configuration.yaml
    └── custom_components
        └── samsungtv_smart
            └── __init__.py
            └── media_player.py
            └── websockets.py
            └── shortcuts.py
            └── smartthings.py
            └── upnp.py
            └── exceptions.py
            └── ...
    ```

# Configuration

Once the component has been installed, you need to configure it in order to make it work.
There are two ways of doing so:
- Using the web interface (Lovelace) [**recommended**]
- Manually editing the `configuration.yaml` file

**Important**: To complete the configuration procedure properly, you must be sure that your **TV is turned on and 
connected to the LAN (wired or wireless)**. Stay near to your TV during configuration because probably you will need 
to accept the access request that will prompt on your TV screen.

**Note**: To configure the component for using **SmartThings (strongly suggested)** you need to generate an access 
token as explained in [this guide](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/Smartthings.md). 
Also make sure your **TV is logged into your SmartThings account** and **registered in SmartThings phone app** before 
starting configuration.

### Option A: Configuration using the web UI [**recommended**]

1. From the Home Assistant front-end, navigate to 'Configuration' then 'Integrations'. Click `+` button in botton right corner,
search '**SamsungTV Smart**' and click 'Configure'.
2. In the configuration mask, enter the IP address of the TV, the name for the Entity and the SmartThings personal 
access token (if created) and then click 'Submit'
3. **Important**: look for your TV screen and confirm **immediatly** with OK if a popup appear.
4. Congrats! You're all set!

### Option B: Configuration via editing `configuration.yaml`

1. Enable the component by editing the configuration.yaml file (within the config directory as well). Edit it by adding 
the following lines:
    ```
    samsungtv_smart:
      - host: <YOUR TV IP ADDRES>
        name: My TV name
        api_key: <YOUR SMARTTHINGS TOKEN> #omit if not generated
        ...
    ```
2. Restart Home Assistant.
3. **Important**: look for your TV screen and confirm **immediatly** with OK if a popup appear.
4. Congrats! You're all set!

## Configuration options

From the Home Assistant front-end, navigate to 'Configuration' then 'Integrations'. Identify the '**SamsungTV Smart**'
integration configured for your TV and click the `OPTIONS` button.<br/>
Here you chan change the following options:  

- **Use SmartThings TV Status information**<br/>
(default = True)
When enabled and SmartThings is configured, the component will try to retrieve from SmartThings the information
about the TV Status. This information is always used in conjunction with local ping result.<br/>

- **Use SmartThings TV Channels information**<br/>
(default = False)
When enabled and SmartThings is configured, the component will try to retrieve from SmartThings the information
about the TV Channel and TV Channel Name or Running App<br/>
**Note: in many case this information is not properly updated, so this option is disabled by default.**<br/>

- **Seconds to delay power ON status**<br/>
(default = 30, range from 0 to 60)<br/>
This option allow to configure a delay to wait before setting the TV status to ON. This is used to avoid false
ON status for TV that enable the network interface on regular interval also when the TV status is OFF.<br/>

## Custom configuration parameters

You can configure additional option for the component using configuration variable in `configuration.yaml` section.<br/>
Some of this option are available only during component configuration because are stored in the registry during 
setup phase, other can be changed in `configuration.yaml` at any moment.<br/>

Section in `configuration.yaml` file can also not be present if you configure the componet using web interface. If you 
want configure any parameters, you must create one section that start with `- host` as shown in the example below:<br/>
```
samsungtv_smart:
  - host: <YOUR TV IP ADDRES>
    ...
```
Then you can add any of the following parameters:<br/>

- **api_key:**<br/>
(string)(Optional)<br/>
API Key for the SmartThings Cloud API, this is optional but adds better state handling on, off, channel name, hdmi source, 
and a few new keys: `ST_TV`, `ST_HDMI1`, `ST_HDMI2`, `ST_HDMI3`, etc. (see more at [SmartThings Keys](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/Smartthings.md#smartthings-keys))<br/>
Read [How to get an API Key for SmartThings](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/Smartthings.md)<br/>
This parameter can also be provided during the component configuration using the user interface.<br/>
**Note: this parameter is used only during initial configuration and then stored in the registry. It's not possible to change the value after that the component is configured. To change the value you must delete the integration from UI.**<br/>

- **device_id:**<br/>
(string)(Optional)<br/>
Device ID for the SmartThings Cloud API. This is optional, to be used only if component fails to automatically determinate it.
Read [SmartThings Device ID](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/Smartthings.md#smartthings-device-id)
to understand how identify the correct value to use.<br/>
This parameter will be requested during component configuration from user interface when required.<br/>
**Note: this parameter is used only during initial configuration and then stored in the registry. It's not possible to 
change the value after that the component is configured. To change the value you must delete the integration from UI.**<br/>

- **device_name:**<br/>
(string)(Optional)<br/>
This is an optional value, used only to identify the TV in SmartThings during initial configuration if you have more TV 
registered. You should  configure this parameter only if the setup fails in the detection.<br/>
The device_name to use can be read using the SmartThings app<br/>
**Note: this parameter is used only during initial configuration.**<br/>

- **mac:**<br/>
(string)(Optional)<br/>
This is an optional value, normally is automatically detected during setup phase and so is not required to specify it. 
You should try to configure this parameter only if the setup fail in the detection.<br/>
The mac-address is used to turn on the TV. If you set it manually, you must find the right value from the TV Menu or 
from your network router.<br/>

- **source_list:**<br/>
(json)(Optional)<br/>
This contains the KEYS visible sources in the dropdown list in media player UI.<br/>
Default value: '{"TV": "KEY_TV", "HDMI": "KEY_HDMI"}'<br/>
If SmartThings is [configured](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/Smartthings.md) and the 
source_list not, the component will try to identify and configure automatically the sources configured on the TV with 
the relative associated names (new feature, tested on QLed TV). The created list is available in the HA log file.<br/>
You can also chain KEYS, example: '{"TV": "KEY_SOURCES+KEY_ENTER"}'<br/>
And even add delays (in milliseconds) between sending KEYS, example:<br/>
    '{"TV": "KEY_SOURCES+500+KEY_ENTER"}'<br/>
Resources: [key codes](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/Key_codes.md) / [key patterns](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/Key_chaining.md)<br/>
**Warning: changing input source with voice commands only works if you set the device name in `source_list` as one of 
the whitelisted words that can be seen on [this page](https://web.archive.org/web/20181218120801/https://developers.google.com/actions/reference/smarthome/traits/modes#mode-settings) 
(under "Mode Settings")**<br/>
    
- **app_list:**<br/>
(json)(Optional)<br/>
This contains the APPS visible sources in the dropdown list in media player UI.<br/>
Default value: AUTOGENERATED<br/>
If the `app_list` is not manually configured, during startup is generated a file in the custom component folder with the 
list of all available applications. This list can be used to create a manual list following [app_list guide](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/App_list.md)<br/>
Example value: '{"Netflix": "11101200001", "YouTube": "111299001912", "Spotify": "3201606009684"}'<br/>
Known lists of App IDs: [List 1](https://github.com/tavicu/homebridge-samsung-tizen/issues/26#issuecomment-447424879), 
[List 2](https://github.com/Ape/samsungctl/issues/75#issuecomment-404941201)<br/>

- **load_all_apps:**<br/>
(boolean)(Optional)<br/>
This option is `True` by default.</br>
Setting this parameter to false, if a custom `app_list` is not defined, the automatic app_list will be generated  
limited to few application (the most common).<br/>

- **show_channel_number:**<br/>
(boolean)(Optional)<br/>
If the SmartThings API is enabled (by settings "api_key" and "device_id"), then the TV Channel Names will show as media 
titles, by setting this to True the TV Channel Number will also be attached to the end of the media title (when applicable).<br/>
**Note: not always SmartThings provide the information for channel_name and channel_number.**<br/>
    
- **broadcast_address:**<br/>
(string)(Optional)<br/>
**Do not set this option if you do not know what it does, it can break turning your TV on.**<br/>
The ip address of the host to send the magic packet (for wakeonlan) to if the "mac" property is also set.<br/>
Default value: "255.255.255.255"<br/>
Example value: "192.168.1.255"<br/>

- **update_method:** (obsolete/not used from v0.3.3)<br/>
(string)(Optional)<br/>
This change the ping method used for state update. Values: "ping", "websockets" and "smartthings"<br/>
Default value: "ping" if SmartThings is not enabled, else "smartthings"<br/>
Example update_method: "websockets"<br/>

- **update_custom_ping_url:** (obsolete/not used from v0.2.x)<br/>
(string)(Optional)<br/>
Use custom endpoint to ping.<br/>
Default value: PING TO 8001 ENDPOINT<br/>
Example update_custom_ping_url: "http://192.168.1.77:9197/dmr"<br/>

- **scan_app_http:** (obsolete/not used from v0.2.x)<br/>
(boolean)(Optional)<br/>
This option is `True` by default. In some cases (if numerical IDs are used when setting `app_list`) HTTP polling will 
be used (1 request per app) to get the running app.<br/>
This is a lengthy task that some may want to disable, you can do so by setting this option to `False`.<br/>
For more information about how we get the running app, read the [app_list guide](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/App_list.md).<br/>

# Usage

### Known Supported Voice Commands

* Turn on `SAMSUNG-TV-NAME-HERE` (for some older TVs this only works if the TV is connected by LAN cable to the Network)
* Turn off `SAMSUNG-TV-NAME-HERE`
* Volume up on `SAMSUNG-TV-NAME-HERE` (increases volume by 1)
* Volume down on `SAMSUNG-TV-NAME-HERE` (decreases volume by 1)
* Set volume to 50 on `SAMSUNG-TV-NAME-HERE` (sets volume to 50 out of 100)
* Mute `SAMSUNG-TV-NAME-HERE` (sets volume to 0)
* Change input source to `DEVICE-NAME-HERE` on `SAMSUNG-TV-NAME-HERE` (only works if `DEVICE-NAME-HERE` is a whitelisted word from [this page](https://web.archive.org/web/20181218120801/https://developers.google.com/actions/reference/smarthome/traits/modes) under "Mode Settings")

(if you find more supported voice commands, please create an issue so I can add them here)

### Cast to TV

`service: media_player.play_media`

```
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "url",
  "media_content_id": "FILE_URL",
}
```
_Replace FILE_URL with the url of your file._

### Send Keys
```
service: media_player.play_media
```

```json
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "send_key",
  "media_content_id": "KEY_CODE"
}
```
**Note**: Change "KEY_CODE" by desired [key_code](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/Key_codes.md). (also works with key chaining and SmartThings keys: ST_TV, ST_HDMI1, ST_HDMI2, ST_HDMI3, etc. / see more at [SmartThings Keys](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/Smartthings.md#smartthings-keys))

Script example:
```
tv_channel_down:
  alias: Channel down
  sequence:
  - service: media_player.play_media
    data:
      entity_id: media_player.samsung_tv55
      media_content_type: "send_key"
      media_content_id: KEY_CHDOWN
```

### Hold Keys
```
service: media_player.play_media
```

```json
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "send_key",
  "media_content_id": "KEY_CODE, <hold_time>"
}
```

**Note**: Change "KEY_CODE" by desired [key_code](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/Key_codes.md) and <hold_time> with a valid numeric value in milliseconds (this also works with key chaining but not with SmartThings keys).

***Key Chaining Patterns***
---------------
Key chaining is also supported, which means a pattern of keys can be set by delimiting the keys with the "+" symbol, delays can also be set in milliseconds between the "+" symbols.

[See the list of known Key Chaining Patterns](https://github.com/ollo69/ha-samsungtv-smart/blob/master/docs/Key_chaining.md)


***Open Browser Page***
---------------

```
service: media_player.play_media
```

```json
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "browser",
  "media_content_id": "https://www.google.com"
}
```

# Be nice!
If you like the component, why don't you support me by buying me a coffe?
It would certainly motivate me to further improve this work.

[![Buy me a coffe!](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/ollo69)
