"""Select entity for plant health status."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    DRAINAGE_QUALITY_OPTIONS,
    HEALTH_OPTIONS,
    LIGHT_POSITION_OPTIONS,
    OPT_DRAINAGE_QUALITY,
    OPT_LIGHT_POSITION,
    OPT_POT_MATERIAL,
    OPT_SOIL_RETENTION,
    OPT_WINDOW_ORIENTATION,
    POT_MATERIAL_OPTIONS,
    SOIL_RETENTION_OPTIONS,
    WINDOW_ORIENTATION_OPTIONS,
    label_environment_option,
)
from .plant import PlantData


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    plant: PlantData = hass.data[DOMAIN][entry.entry_id]
    entities: list[SelectEntity] = [HealthSelect(plant, entry)]

    if plant.enable_environment_context:
        entities.extend([
            EnvironmentSelect(
                plant,
                entry,
                OPT_WINDOW_ORIENTATION,
                "Window orientation",
                WINDOW_ORIENTATION_OPTIONS,
                lambda: plant.window_orientation,
                plant.set_window_orientation,
            ),
            EnvironmentSelect(
                plant,
                entry,
                OPT_LIGHT_POSITION,
                "Light position",
                LIGHT_POSITION_OPTIONS,
                lambda: plant.light_position,
                plant.set_light_position,
            ),
            EnvironmentSelect(
                plant,
                entry,
                OPT_POT_MATERIAL,
                "Pot material",
                POT_MATERIAL_OPTIONS,
                lambda: plant.pot_material,
                plant.set_pot_material,
            ),
            EnvironmentSelect(
                plant,
                entry,
                OPT_SOIL_RETENTION,
                "Soil retention",
                SOIL_RETENTION_OPTIONS,
                lambda: plant.soil_retention,
                plant.set_soil_retention,
            ),
            EnvironmentSelect(
                plant,
                entry,
                OPT_DRAINAGE_QUALITY,
                "Drainage quality",
                DRAINAGE_QUALITY_OPTIONS,
                lambda: plant.drainage_quality,
                plant.set_drainage_quality,
            ),
        ])

    async_add_entities(entities)


class HealthSelect(SelectEntity):
    """Select entity representing the current health status of a plant."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_translation_key = "health"
    _attr_options = HEALTH_OPTIONS
    _attr_icon = "mdi:leaf"

    def __init__(self, plant: PlantData, entry: ConfigEntry) -> None:
        self._plant = plant
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_health"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._plant.plant_name,
            manufacturer="Adaptive Plant",
            model="Plant Monitor",
        )

    @property
    def current_option(self) -> str:
        return self._plant.health

    @property
    def extra_state_attributes(self) -> dict:
        """Expose health timing data for the companion card overdue indicator."""
        return {
            "health_last_updated": self._plant.health_last_updated,
            "health_prompt_interval": self._plant.health_prompt_interval,
            "health_check_in_overdue": self._plant.health_check_in_overdue,
        }

    async def async_added_to_hass(self) -> None:
        self._plant.add_listener(self._on_plant_update)

    async def async_will_remove_from_hass(self) -> None:
        self._plant.remove_listener(self._on_plant_update)

    @callback
    def _on_plant_update(self) -> None:
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        await self._plant.set_health(option)

class EnvironmentSelect(SelectEntity):
    """Select entity for editable plant environment metadata."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_icon = "mdi:leaf"

    def __init__(
        self,
        plant: PlantData,
        entry: ConfigEntry,
        key: str,
        name: str,
        raw_options: list[str],
        current_value,
        set_value,
    ) -> None:
        self._plant = plant
        self._entry = entry
        self._key = key
        self._current_value = current_value
        self._set_value = set_value
        self._label_to_raw = {
            label_environment_option(option): option for option in raw_options
        }

        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_options = list(self._label_to_raw)

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._plant.plant_name,
            manufacturer="Adaptive Plant",
            model="Plant Monitor",
        )

    @property
    def current_option(self) -> str:
        return label_environment_option(self._current_value())

    async def async_added_to_hass(self) -> None:
        self._plant.add_listener(self._on_plant_update)

    async def async_will_remove_from_hass(self) -> None:
        self._plant.remove_listener(self._on_plant_update)

    @callback
    def _on_plant_update(self) -> None:
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        await self._set_value(self._label_to_raw[option])
