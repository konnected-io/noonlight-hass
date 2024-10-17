# Noonlight for HomeAssistant

This is the [Noonlight](https://noonlight.com) integration for HomeAssistant.

[Noonlight](https://noonlight.com) connects your smart home to local emergency services to help keep you safe in case of a break-in, fire, or medical emergency.

### Noonlight service is currently only available in the United States

## How it Works

Noonlight connects to emergency 9-1-1 services in all 50 U.S. states. Backed by a UL-compliant alarm monitoring center and staffed 24/7 with live operators in the United States, Noonlight is standing by to send help to your home at a moment's notice.

When integrated with Home Assistant, a **Noonlight Alarm** switch will appear in your list of entities. When the Noonlight Alarm switch is turned _on_, this will send an emergency signal to Noonlight. You will be contacted by text and voice at the phone number associated with your Noonlight account. If you confirm the emergency with the Noonlight operator, or if you're unable to respond, Noonlight will dispatch local emergency services to your home using the [longitude and latitude coordinates](https://www.home-assistant.io/docs/configuration/basic/#latitude) specified in your Home Assistant configuration or an address you specify in the Noonlight configuration.

Additionally, a new service will be exposed to Home Assistant: `noonlight.create_alarm`, which allows you to explicitly specify the type of emergency service required by the alarm: medical, fire, or police. By default, the switch entity assumes "police".

**False alarm?** No problem. Just tell the Noonlight operator your PIN when you are contacted and the alarm will be canceled. We're glad you're safe!

The _Noonlight Switch_ can be activated by any Home Assistant automation, just like any type of switch! [See examples below](#automation-examples).

## Initial set up

Setup requires a U.S. based mobile phone number.

1. Ensure that your [longitude and latitude coordinates](https://www.home-assistant.io/docs/configuration/basic/#latitude) are set accurately so that Noonlight knows where to send help.

1. Click the link below to set up a Noonlight account and authorize Home Assistant to create alarms on your behalf:

    * [Connect to Noonlight](https://noonlight.konnected.io/ha/auth)

1. Save the resulting YAML snippet. You will need to enter these details into Home Assistant when adding the integration.

### Configuration

* `Noonlight ID`: A unique identifier assigned to you when you complete the [initial setup steps](#initial-set-up)

* `Noonlight Secret`: A secret key associated with your id

* `Noonlight API Endpoint`: The Noonlight API endpoint used when creating an alarm

* `Token Endpoint`: The OAuth endpoint used to refresh your Noonlight auth token (hosted by [Konnected](https://konnected.io))

* `Location Mode`: Choose between Latitude/Longitude or Address

#### If Latitude/Longitude:

* `Latitude`: Will default to Latitude in Home Assistant

* `Longitude`: Will default to Longitude in Home Assistant

#### If Address:

* `Address`: Street address

* `Address 2`: Apartment, suite, etc. (optional)

* `City`: City/town name

* `State`: Two-letter state abbreviation

* `Zip`: Zip code

## Automation Examples

### Notify Noonlight when an intrusion alarm is triggered

This example is using the [Manual Alarm component](https://www.home-assistant.io/integrations/manual/)

```yaml
automation:
  - alias: 'Activate the Noonlight Alarm when the security system is triggered'
    trigger:
      - platform: state
        entity_id: 
          - alarm_control_panel.ha_alarm
        to: 'triggered'
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.noonlight_alarm
```

### Notify Noonlight when a smoke detector detects smoke

```yaml
automation:
  - alias: 'Activate the Noonlight Alarm when smoke is detected'
    trigger:
      - platform: state
        entity_id: 
          - binary_sensor.smoke_alarm
        to: 'on'        
    action:
      - service: noonlight.create_alarm
        data:
          service: fire
```

## Warnings & Disclaimers

<p class='note warning'>
<b>Requires an Internet connection!</b> Home Assistant must have an active internet connection for this to work!
</p>

### NO GUARANTEE

**This integration is provided as-is without warranties of any kind. Using Noonlight with Home Assistant involves multiple service providers and potential points of failure, including (but not limited to) your internet service provider, 3rd party hosting services such as Amazon Web Services, and the Home Assistant software platform.**
Please read and understand the [Noonlight terms of use](https://noonlight.com/terms), [Konnected terms of use](https://konnected.io/terms) and [Home Assistant terms of Service](https://www.home-assistant.io/tos/), each of which include important limitations of liability and indemnification provisions.
