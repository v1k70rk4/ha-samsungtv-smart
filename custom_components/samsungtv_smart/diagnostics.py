"""Diagnostics support for Samsung TV Smart."""
from __future__ import annotations

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_MAC
from homeassistant.core import HomeAssistant

from .const import DOMAIN


TO_REDACT = {CONF_API_KEY, CONF_MAC}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    diag_data = {"entry": async_redact_data(entry.as_dict(), TO_REDACT)}

    yaml_data = hass.data[DOMAIN].get(entry.unique_id, {})
    if yaml_data:
        diag_data["config_data"] = async_redact_data(yaml_data, TO_REDACT)

    return diag_data
