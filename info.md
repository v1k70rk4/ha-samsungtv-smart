
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

- **Use SmartThings TV Channels information**<br/>
When enabled and SmartThings is configured, the component will try to retrieve from SmartThings the information
about the TV Channel and TV Channel Name or Running App<br/>
**Note: in many case this information is not properly updated, so this option is disabled by default.**<br/>

## Custom configuration parameters

You can configure additional option for the component using configuration variable in `configuration.yaml` section.<br/>
Some of this option are available only during component configuration because are stored in the registry during setup 
phase, other can be changed in `configuration.yaml` at any moment.<br/>

**Please refer to [readme](https://github.com/ollo69/ha-samsungtv-smart/blob/master/README.md) for details on optional parameter and additional configuration instruction.**

# Be nice!
If you like the component, why don't you support me by buying me a coffe?
It would certainly motivate me to further improve this work.

[![Buy me a coffe!](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/ollo69)
