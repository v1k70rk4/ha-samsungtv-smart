
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

**From v0.3.16 initial configuration from yaml is not allowed.**
You can still use `configuration.yaml` to set the additional parameter as explained below.

## Configuration options

From the Home Assistant front-end, navigate to 'Configuration' then 'Integrations'. Identify the '**SamsungTV Smart**'
integration configured for your TV and click the `OPTIONS` button.<br/>
Here you chan change the following options:  

- **Applications list load mode at startup**<br/>
Possible values: `All Apps`, `Default Apps` and `Not Load`<br/>
This option determine the mode application list is automatic generated.<br>
With `All Apps` the list will contain all apps installed on the TV, with `Default Apps` will be generated a minimal list  
with only the most common application, with `Not Load` application list will be empty.<br/>
**Note: If a custom `app_list` in `configuration.yaml` file is defined this option is not used.**<br>

- **Applications launch method used**<br/>
Possible values: `Standard Web Socket Channel`, `Remote Web Socket Channel` and `Rest API Call`<br/>
This option determine the mode used to launch applications.<br/>
Use `Rest API Call` only if the other 2 methods do not work.<br/>

- **Use SmartThings TV Status information**<br/>
(default = True)<br/>
When enabled and SmartThings is configured, the component will try to retrieve from SmartThings the information
about the TV Status. This information is always used in conjunction with local ping result.<br/>

- **Use SmartThings TV Channels information**<br/>
(default = True)<br/>
When enabled and SmartThings is configured, the component will try to retrieve from SmartThings the information
about the TV Channel and TV Channel Name or the Running App<br/>
**Note: in some case this information is not properly updated, disabled it you have incorrect information.**<br/>

- **Use SmartThings TV Channels number information**<br/>
(default = False)<br/>
If the SmartThings API is enabled (by settings "api_key" and "device_id"), then the TV Channel Names will show as media 
titles, by setting this to True the TV Channel Number will also be attached to the end of the media title (when applicable).<br/>
**Note: not always SmartThings provide the information for channel_name and channel_number.**<br/>

- **Use volume mute status to detect fake power ON**<br/>
(default = True)<br/>
When enabled try to detect fake power on based on the Volume mute state, based on the assumption that when the
TV is powered on the volume is always unmuted.<br/>

- **Seconds to delay power ON status**<br/>
(default=30, range from 0 to 60)<br/>
This option allow to configure a delay to wait before setting the TV status to ON. This is used to avoid false
ON status for TV that enable the network interface on regular interval also when the TV status is OFF.<br/>

- **List of entity to Power OFF with TV (comma separated)**<br/>
A list of HA entity to Turn OFF when the TV entity is turned OFF (maximum 4). 
This call the service `homeassistant.turn_off` for maximum the first 4 entity in the provided list.<br/>

- **List of entity to Power ON with TV (comma separated)**<br/>
A list of HA entity to Turn ON when the TV entity is turned ON (maximum 4).
This call the service `homeassistant.turn_on` for maximum the first 4 entity in the provided list.<br/>

## Custom configuration parameters

You can configure additional option for the component using configuration variable in `configuration.yaml` section.<br/>
Some of this option are available only during component configuration because are stored in the registry during setup 
phase, other can be changed in `configuration.yaml` at any moment.<br/>

**Please refer to [readme](https://github.com/ollo69/ha-samsungtv-smart/blob/master/README.md) for details on optional parameter and additional configuration instruction.**

# Be nice!
If you like the component, why don't you support me by buying me a coffe?
It would certainly motivate me to further improve this work.

[![Buy me a coffe!](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/ollo69)
