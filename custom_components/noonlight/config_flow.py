from __future__ import annotations

import logging
from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries, core
from homeassistant.const import CONF_ID, CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    CONF_ADDRESS_LINE1,
    CONF_ADDRESS_LINE2,
    CONF_API_ENDPOINT,
    CONF_CITY,
    CONF_SECRET,
    CONF_STATE,
    CONF_TOKEN_ENDPOINT,
    CONF_ZIP,
    DEFAULT_API_ENDPOINT,
    DEFAULT_NAME,
    DEFAULT_TOKEN_ENDPOINT,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)
STATES = [
    "AK",
    "AL",
    "AR",
    "AZ",
    "CA",
    "CO",
    "CT",
    "DC",
    "DE",
    "FL",
    "GA",
    "HI",
    "IA",
    "ID",
    "IL",
    "IN",
    "KS",
    "KY",
    "LA",
    "MA",
    "MD",
    "ME",
    "MI",
    "MN",
    "MO",
    "MS",
    "MT",
    "NC",
    "ND",
    "NE",
    "NH",
    "NJ",
    "NM",
    "NV",
    "NY",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VA",
    "VT",
    "WA",
    "WI",
    "WV",
    "WY",
]


async def validate_input(hass: core.HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """

    _LOGGER.debug(f"[config_flow validate_input] data: {data}")

    return {"title": data[CONF_NAME]}


class NoonlightConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""

        errors = {}
        if user_input is not None:
            _LOGGER.debug(f"[New Sensor] user_input: {user_input}")
            try:
                # info = await validate_input(self.hass, user_input)
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME), data=user_input
                )
            except Exception as err:
                _LOGGER.exception(
                    f"[config_flow async_step_user] Unexpected exception: {err}"
                )
                errors["base"] = "unknown"

        DATA_SCHEMA = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): selector.TextSelector(
                    selector.TextSelectorConfig()
                ),
                vol.Required(CONF_ID): selector.TextSelector(
                    selector.TextSelectorConfig()
                ),
                vol.Required(CONF_SECRET): selector.TextSelector(
                    selector.TextSelectorConfig()
                ),
                vol.Required(
                    CONF_API_ENDPOINT, default=DEFAULT_API_ENDPOINT
                ): selector.TextSelector(selector.TextSelectorConfig()),
                vol.Required(
                    CONF_TOKEN_ENDPOINT, default=DEFAULT_TOKEN_ENDPOINT
                ): selector.TextSelector(selector.TextSelectorConfig()),
                vol.Optional(
                    CONF_LATITUDE, default=self.hass.config.latitude
                ): cv.latitude,
                vol.Optional(
                    CONF_LONGITUDE, default=self.hass.config.longitude
                ): cv.longitude,
                vol.Optional(CONF_ADDRESS_LINE1): selector.TextSelector(
                    selector.TextSelectorConfig()
                ),
                vol.Optional(CONF_ADDRESS_LINE2): selector.TextSelector(
                    selector.TextSelectorConfig()
                ),
                vol.Optional(CONF_CITY): selector.TextSelector(
                    selector.TextSelectorConfig()
                ),
                vol.Optional(CONF_STATE): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=STATES,
                        multiple=False,
                        custom_value=False,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Optional(CONF_ZIP): selector.TextSelector(
                    selector.TextSelectorConfig()
                ),
            }
        )

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        """Add reconfigure step to allow to reconfigure a config entry."""

        errors = {}
        self.config_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        if user_input is not None:
            _LOGGER.debug(f"[Reconfigure] updated config: {user_input}")
            try:
                # info = await validate_input(self.hass, user_input)
                return self.async_update_reload_and_abort(
                    self.config_entry,
                    data={**self.config_entry.data, **user_input},
                    reason="reconfigure_successful",
                )

                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME), data=user_input
                )
            except Exception as err:
                _LOGGER.exception(
                    f"[config_flow async_step_reconfigure] Unexpected exception: {err}"
                )
                errors["base"] = "unknown"

            self.hass.config_entries.async_update_entry(
                self.config_entry, data=user_input, options=self.config_entry.options
            )
            await self.hass.config_entries.async_reload(self.config_entry.entry_id)
            return self.async_create_entry(title="", data={})

        OPTIONS_SCHEMA = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_ID): str,
                vol.Required(CONF_SECRET): str,
                vol.Required(CONF_API_ENDPOINT, default=DEFAULT_API_ENDPOINT): str,
                vol.Required(CONF_TOKEN_ENDPOINT, default=DEFAULT_TOKEN_ENDPOINT): str,
                vol.Inclusive(
                    CONF_LATITUDE, "coordinates", "Include both latitude and longitude"
                ): cv.latitude,
                vol.Inclusive(
                    CONF_LONGITUDE, "coordinates", "Include both latitude and longitude"
                ): cv.longitude,
                vol.Optional(CONF_ADDRESS_LINE1): str,
                vol.Optional(CONF_ADDRESS_LINE2): str,
                vol.Optional(CONF_CITY): str,
                vol.Optional(CONF_STATE): str,
                vol.Optional(CONF_ZIP): str,
            }
        )
        # _LOGGER.debug(f"[Options Update] initial config: {self.config_entry.data}")

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=OPTIONS_SCHEMA,
            errors=errors,
        )

    # this is run to import the configuration.yaml parameters\
    async def async_step_import(self, import_config=None) -> FlowResult:
        """Import a config entry from configuration.yaml."""

        _LOGGER.debug(f"[async_step_import] import_config: {import_config}")
        return await self.async_step_user(import_config)
