# HomeAssistant - SamsungTV Smart Component

## ***Enable SmartThings*** - Setup instructions 

### Create personal access token

1. Log into the [personal access tokens page](https://account.smartthings.com/tokens) and click '[Generate new token](https://account.smartthings.com/tokens/new)'
2. Enter a token name (can be whatever you want), for example, 'Home Assistant' and select the following authorized scopes:
    - Devices (all)
    - Installed Apps (all)
    - Locations (all)
    - Apps (all)
    - Schedules (all)
    - Scenes (all)
3. Click 'Generate token'. When the token is displayed, copy and save it somewhere safe (such as your keystore) as you will not be able to retrieve it again.

### Configure Home Assistant

Once the SmartThings token has been generated, you need to configure the component with it in order to make it work.
There are two ways of doing so:
- Using the web interface (Lovelace) [**recommended**]
- Manually editing the `configuration.yaml` file

**Note:** if the component has been already configured for your TV, you must delete it from the HA web interface and then re-configure it to enable SmartThings integration.<br/>

#### Option A: Configuration using the web UI [**recommended**]

1. Make sure your TV is logged into your SmartThings account.
2. From the Home Assistant front-end, navigate to 'Configuration' then 'Integrations'. Under 'Set up a new integration' locate     '**SamsungTV Smart**' and click 'Configure'.
3. In the configuration mask, enter the IP address of the TV, the name for the entity and the personal access token created above and click 'Submit'

#### Option B: Configuration via editing `configuration.yaml`

1. Make sure your TV is logged into your SmartThings account.
2. In your `configuration.yaml` add:

```
samsungtv_smart:
  - host: <YOUR TV IP ADDRES>
    name: My TV name
    api_key: <YOUR SMARTTHINGS TOKEN>
    ...
```

3. Restart Home Assistant.


***Benefits of Enabling SmartThings***
---------------

- Better states for running apps (read [app_list guide](https://github.com/ollo69/ha-samsungtv-smart/blob/master/App_list.md) for more information)
- New keys available (read more below about [SmartThings Keys](https://github.com/ollo69/ha-samsungtv-smart/blob/master/Smartthings.md#smartthings-keys))
- Shows TV channel names
- Shows accurate states for HDMI or TV input sources


***SmartThings Keys***
---------------

*Input Keys*
____________
Key|Description
---|-----------
ST_TV|TV
ST_HDMI1|HDMI1
ST_HDMI2|HDMI2
ST_HDMI3|HDMI3
ST_HDMI4|HDMI4
...

*Channel Keys*
______________
Key|Description
---|-----------
ST_CHUP|ChannelUp
ST_CHDOWN|ChannelDown
ST_CH1|Channel1
ST_CH2|Channel2
ST_CH3|Channel3
...
