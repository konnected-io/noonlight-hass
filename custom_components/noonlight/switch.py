"""Create a switch to trigger an alarm in Noonlight."""

import logging

from hass.helpers.dispatcher import async_dispatcher_connect

try:
    from homeassistant.components.switch import SwitchEntity
except ImportError:
    from homeassistant.components.switch import SwitchDevice as SwitchEntity

from .const import (
    DOMAIN,
    EVENT_NOONLIGHT_ALARM_CANCELED,
    EVENT_NOONLIGHT_ALARM_CREATED,
    EVENT_NOONLIGHT_TOKEN_REFRESHED,
)

DEFAULT_NAME = "Noonlight Switch"

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Create a switch to create an alarm with the Noonlight service."""
    noonlight_integration = hass.data[DOMAIN]
    noonlight_switch = NoonlightSwitch(noonlight_integration)
    async_add_entities([noonlight_switch])

    def noonlight_token_refreshed():
        noonlight_switch.schedule_update_ha_state()

    def noonlight_alarm_canceled():
        noonlight_switch._state = False
        noonlight_switch.schedule_update_ha_state()

    def noonlight_alarm_created():
        noonlight_switch._state = True
        noonlight_switch.schedule_update_ha_state()

    async_dispatcher_connect(
        hass, EVENT_NOONLIGHT_TOKEN_REFRESHED, noonlight_token_refreshed
    )

    async_dispatcher_connect(
        hass, EVENT_NOONLIGHT_ALARM_CANCELED, noonlight_alarm_canceled
    )

    async_dispatcher_connect(
        hass, EVENT_NOONLIGHT_ALARM_CREATED, noonlight_alarm_created
    )


class NoonlightSwitch(SwitchEntity):
    """Representation of a Noonlight alarm switch."""

    def __init__(self, noonlight_integration):
        """Initialize the Noonlight switch."""
        self.noonlight = noonlight_integration
        self._name = DEFAULT_NAME
        self._state = False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def available(self):
        """Ensure that the Noonlight access token is valid."""
        return self.noonlight.access_token_expires_in.total_seconds() > 0

    @property
    def extra_state_attributes(self):
        """Return the current alarm attributes, when active."""
        attr = {}
        if self.noonlight._alarm is not None:
            alarm = self.noonlight._alarm
            attr["alarm_status"] = alarm.status
            attr["alarm_id"] = alarm.id
            attr["alarm_services"] = alarm.services
        return attr

    @property
    def is_on(self):
        """Return the status of the switch."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Activate an alarm. Defaults to `police` services."""
        if self.noonlight._alarm is None:
            await self.noonlight.create_alarm()
            if self.noonlight._alarm is not None:
                self._state = True

    async def async_turn_off(self, **kwargs):
        """Turn off the switch if the active alarm is canceled."""
        if self.noonlight._alarm is None:
            self._state = False
