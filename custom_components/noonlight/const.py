from homeassistant.const import Platform
from noonlight import (
    NOONLIGHT_SERVICES_FIRE,
    NOONLIGHT_SERVICES_MEDICAL,
    NOONLIGHT_SERVICES_POLICE,
)

VERSION = "v1.2.0"
DOMAIN = "noonlight"

PLATFORMS = [Platform.SWITCH]

DEFAULT_NAME = "Noonlight"
DEFAULT_API_ENDPOINT = "https://api.noonlight.com/platform/v1"
DEFAULT_TOKEN_ENDPOINT = "https://noonlight.konnected.io/ha/token"

CONF_SECRET = "secret"
CONF_API_ENDPOINT = "api_endpoint"
CONF_TOKEN_ENDPOINT = "token_endpoint"
CONF_ADDRESS_LINE1 = "address1"
CONF_ADDRESS_LINE2 = "address2"
CONF_CITY = "city"
CONF_STATE = "state"
CONF_ZIP = "zip"
CONF_LOCATION_MODE = "location_mode"

CONST_ALARM_STATUS_ACTIVE = "ACTIVE"
CONST_ALARM_STATUS_CANCELED = "CANCELED"
CONST_NOONLIGHT_HA_SERVICE_CREATE_ALARM = "create_alarm"

CONST_NOONLIGHT_SERVICE_TYPES = (
    NOONLIGHT_SERVICES_POLICE,
    NOONLIGHT_SERVICES_FIRE,
    NOONLIGHT_SERVICES_MEDICAL,
)

EVENT_NOONLIGHT_TOKEN_REFRESHED = "noonlight_token_refreshed"
EVENT_NOONLIGHT_ALARM_CANCELED = "noonlight_alarm_canceled"
EVENT_NOONLIGHT_ALARM_CREATED = "noonlight_alarm_created"

NOTIFICATION_TOKEN_UPDATE_FAILURE = "noonlight_token_update_failure"
NOTIFICATION_TOKEN_UPDATE_SUCCESS = "noonlight_token_update_success"
NOTIFICATION_ALARM_CREATE_FAILURE = "noonlight_alarm_create_failure"
