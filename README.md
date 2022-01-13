# Noonlight for HomeAssistant

This is the [Noonlight](https://noonlight.com) integration for HomeAssistant.

[Noonlight](https://noonlight.com) connects your smart home to local emergency services to help keep you safe in case of a break-in, fire, or medical emergency.

<p class='note info'>
Noonlight service is currently available in the United States.
</p> 

## How it Works

Noonlight connects to emergency 9-1-1 services in all 50 U.S. states. Backed by a UL-compliant alarm monitoring center and staffed 24/7 with live operators in the United States, Noonlight is standing by to send help to your home at a moment's notice.

When integrated with Home Assistant, a **Noonlight Alarm** switch will appear in your list of entities. When the Noonlight Alarm switch is turned _on_, this will send an emergency signal to Noonlight. You will be contacted by text and voice at the phone number associated with your Noonlight account. If you confirm the emergency with the Noonlight operator, or if you're unable to respond, Noonlight will dispatch local emergency services to your home using the [longitude and latitude coordinates](https://www.home-assistant.io/docs/configuration/basic/#latitude) specified in your Home Assistant configuration using version 1 of the noonlight API.  The code has been updated to also support the noonlight version 2 API.  Should you configure the system for V2 the system will communicate the alarm location based on a street address.

**False alarm?** No problem. Just tell the Noonlight operator your PIN when you are contacted and the alarm will be canceled. We're glad you're safe!

The _Noonlight Switch_ can be activated by any Home Assistant automation, just like any type of switch! [See examples below](#automation-examples).

## Initial set up

Setup requires a U.S. based mobile phone number.

1. Ensure that your [longitude and latitude coordinates](https://www.home-assistant.io/docs/configuration/basic/#latitude) are set accurately so that Noonlight knows where to send help.

2. Click the link below to set up a Noonlight account and authorize Home Assistant to create alarms on your behalf:
    
    [Connect to Noonlight](https://noonlight.konnected.io/ha/auth)

3. Copy and paste the resulting YAML snippet into your configuration.yaml and restart Home Assistant

### Configuration

A `noonlight` section must be present in the `configuration.yaml` file to enable the Noonlight Alarm entity.

**Note:** This configuration snippet will be generated for you automatically to copy and paste when you follow the [initial setup steps](#initial-set-up)

```yaml
# Example configuration.yaml entry
noonlight:
  id: NOONLIGHT_ID
  secret: NOONLIGHT_SECRET
  api_endpoint: https://api.noonlight.com/platform/v1
  token_endpoint: https://noonlight.konnected.io/ha/token
```

* `id`: A unique identifier assigned to you when you complete the [initial setup steps](#initial-set-up)
* `secret`: A secret key associated with your id
* `api_endpoint`: The Noonlight API endpoint used when creating an alarm
* `token_endpoint`: The OAuth endpoint used to refresh your Noonlight auth token (hosted by [Konnected](https://konnected.io))

**Note:** To utilize the noonlight V2 API you will need to modify the api_endpoint and add these additional tags

```yaml
# V2 API Example configuration.yaml entry
noonlight:
  id: NOONLIGHT_ID
  secret: NOONLIGHT_SECRET
  api_endpoint: https://api.noonlight.com/dispatch/v1
  token_endpoint: https://noonlight.konnected.io/ha/token
  line1: '222 State Street'
  line2: 'apt 22'
  city: 'Baltimore'
  state: 'MD' 
  zip: '21140' 
  name: 'John Doe'
  phone: '12552551234'
  pin: '1234'
  name2: 'John Doe home Cell'
  phone2: '14104101234'
  instructions: 'Initial alarm setup, please call so client can verify everything is working'
```

* `id`: A unique identifier assigned to you when you complete the [initial setup steps](#initial-set-up)
* `secret`: A secret key associated with your id
* `api_endpoint`: The Noonlight API endpoint used when creating an alarm
* `token_endpoint`: The OAuth endpoint used to refresh your Noonlight auth token (hosted by [Konnected](https://konnected.io))
* `line1`: Street Adress associated with the alarms
* `line2`: This line is optional an is only required if you have a second line such as apartment number
* `state`: 2 character uppercase state code for alarm address
* `zip`: 5 character zip code for alarm addreess
* `name`: Primary POC contact name
* `phone`: Primary POC phone number
* `pin`: Pin for disabling alarm
* `name2`: Optional secondary POC contact name
* `phone2`: Optional secnodary POC phone number
* `instructions`: This line is optional and may be used to provide additional information with the generated alarms however it doesn't appear the operators can see this information

**Note:** The version 2 API also allows for two Home assistant input_text fields that can to be used to provide additional information 
associated with the alarm message sent to Noonlight.  The fields are input_text.noonlight_service and input_text.alarm_cause. The expected values for
input_text.noonlight_service are: `police`, `fire` and `medical`, which is provided as the emergency service in the alarm.  Text in the alarm_cause
input_text is prepended to any instructions with "Alarm reason was XXXXX", where XXXXX is replaced with text from alarm_cause.  
The expectation is that you set these values in your automation that handles your alarm causing event trigger.

```yaml
# V2 API Example configuration.yaml entries to establish the input_text fields
input_text:
  noonlight_service:
    name: Noonlight Service Called
    initial: police
  alarm_cause:
    name: Alarm Cause
    initial: unknown
```


## Automation Examples

### Notify Noonlight when an intrusion alarm is triggered

This example is using the [Manual Alarm component](https://www.home-assistant.io/integrations/manual/)

```yaml
automation:
  - alias: 'Activate the Noonlight Alarm when the security system is triggered'
    trigger:
      - platform: state
        entity_id: alarm_control_panel.ha_alarm
        to: 'triggered'
    action:
      - service: homeassistant.turn_on
        entity_id: switch.noonlight_alarm

```

### Notify Noonlight when a smoke detector detects smoke

```yaml
automation:
  - alias: 'Activate the Noonlight Alarm when smoke is detected'
    trigger:
      - platform: state
        entity_id: binary_sensor.smoke_alarm
        to: 'on'
    action:
      - service: homeassistant.turn_on
        entity_id: switch.noonlight_alarm

```

## Warnings & Disclaimers

<p class='note warning'>
**Requires an Internet connection!** Home Assistant must have an active internet connection for this to work!
</p> 

**NO GUARANTEE**

**This integration is provided as-is without warranties of any kind. Using Noonlight with Home Assistant involves multiple service providers and potential points of failure, including (but not limited to) your internet service provider, 3rd party hosting services such as Amazon Web Services, and the Home Assistant software platform.**
Please read and understand the [Noonlight terms of use](https://noonlight.com/terms), [Konnected terms of use](https://konnected.io/terms) and [Home Assistant terms of Service](https://www.home-assistant.io/tos/), each of which include important limitations of liability and indemnification provisions.
