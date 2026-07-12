"""Constants for the Adaptive Plant integration."""
from __future__ import annotations

import re

DOMAIN = "adaptive_plant"

PLATFORMS = ["sensor", "button", "number", "select", "text"]

# ── Uploaded-image ownership ───────────────────────────────────────────────────
# Uploaded photos are saved as a uuid4 hex + ".jpg" (see _save_uploaded_image in
# config_flow.py). Owned-file detection matches that exact shape — the folder
# prefix AND a 32-char hex filename — so an image a user hand-places in the same
# /www/adaptive_plant/ folder (e.g. /local/adaptive_plant/monstera.png) is never
# treated as ours and is never auto-deleted on re-upload, disable, or removal.
OWNED_IMAGE_PREFIX = f"/local/{DOMAIN}/"
_OWNED_IMAGE_RE = re.compile(rf"^{re.escape(OWNED_IMAGE_PREFIX)}[0-9a-f]{{32}}\.jpg$")


def is_owned_image_path(path: str | None) -> bool:
    """Return True only for image files this integration created and may delete."""
    return bool(path) and _OWNED_IMAGE_RE.match(path) is not None

# ── Config entry data keys (set at setup, not user-editable after) ─────────────
CONF_PLANT_NAME = "plant_name"
CONF_EARLY_WATERING_THRESHOLD = "early_watering_threshold"
CONF_HEALTH_PROMPT_INTERVAL = "health_prompt_interval_days"
CONF_ENABLE_FERTILIZATION = "enable_fertilization"
CONF_ENABLE_NOTES = "enable_notes"
CONF_ENABLE_IMAGE = "enable_image"
CONF_IMAGE_PATH = "image_path"
# Transient, form-only field for the file-upload selector — never persisted.
CONF_IMAGE_UPLOAD = "image_upload"
CONF_MOISTURE_SENSOR = "moisture_sensor"
CONF_DRY_THRESHOLD = "dry_threshold"
CONF_WET_THRESHOLD = "wet_threshold"
CONF_LABEL = "label"
CONF_ENABLE_LATIN_NAME = "enable_latin_name"
CONF_LATIN_NAME = "latin_name"
CONF_ENABLE_CARE_INSTRUCTIONS = "enable_care_instructions"
CONF_CARE_INSTRUCTIONS = "care_instructions"
CONF_NOTES_ENABLED = "notes_enabled"
CONF_ENABLE_REPOTTING = "enable_repotting"
CONF_ENABLE_ENVIRONMENT_CONTEXT = "enable_environment_context"

# ── Config entry options keys (mutable at runtime) ─────────────────────────────
OPT_WATERING_INTERVAL = "watering_interval_days"
OPT_FERTILIZATION_INTERVAL = "fertilization_interval_days"
OPT_FERT_SYNC_WINDOW = "fertilization_sync_window"
CONF_FERTILIZATION_ENABLED = "fertilization_enabled"
CONF_REPOTTING_ENABLED = "repotting_enabled"

# ── Environmental scheduling metadata ─────────────────────────────────────────
OPT_BASELINE_WATERING_INTERVAL = "baseline_watering_interval_days"
OPT_WINDOW_ORIENTATION = "window_orientation"
OPT_DISTANCE_TO_WINDOW_M = "distance_to_window_m"
OPT_LIGHT_POSITION = "light_position"
OPT_POT_MATERIAL = "pot_material"
OPT_POT_DIAMETER_CM = "pot_diameter_cm"
OPT_SOIL_RETENTION = "soil_retention"
OPT_DRAINAGE_QUALITY = "drainage_quality"

WINDOW_ORIENTATION_OPTIONS = [
    "unknown",
    "north",
    "east",
    "south",
    "west",
    "mixed",
    "internal",
]

LIGHT_POSITION_OPTIONS = [
    "unknown",
    "direct_sun",
    "bright_indirect",
    "medium",
    "low",
]

POT_MATERIAL_OPTIONS = [
    "unknown",
    "terracotta",
    "plastic",
    "glazed_ceramic",
    "metal",
]

SOIL_RETENTION_OPTIONS = [
    "unknown",
    "fast_draining",
    "standard",
    "moisture_retaining",
    "dense",
]

DRAINAGE_QUALITY_OPTIONS = [
    "unknown",
    "good",
    "limited",
    "none",
]

ENVIRONMENT_OPTION_LABELS = {
    "unknown": "Unknown",
    "north": "North",
    "east": "East",
    "south": "South",
    "west": "West",
    "mixed": "Mixed",
    "internal": "Internal room",
    "direct_sun": "Direct sun",
    "bright_indirect": "Bright indirect",
    "medium": "Medium",
    "low": "Low",
    "terracotta": "Terracotta",
    "plastic": "Plastic",
    "glazed_ceramic": "Glazed ceramic",
    "metal": "Metal",
    "fast_draining": "Fast draining",
    "standard": "Standard",
    "moisture_retaining": "Moisture retaining",
    "dense": "Dense",
    "good": "Good",
    "limited": "Limited",
    "none": "None",
}


def label_environment_option(value: str) -> str:
    return ENVIRONMENT_OPTION_LABELS.get(value, value.replace("_", " ").title())


def label_environment_options(values: list[str]) -> list[dict[str, str]]:
    return [{"value": value, "label": label_environment_option(value)} for value in values]

# ── State keys (stored in config entry options) ────────────────────────────────
STATE_LAST_WATERED = "last_watered"
STATE_NEXT_WATERING = "next_watering"
STATE_EARLY_WATERING_COUNT = "early_watering_count"
STATE_HEALTH = "health"
STATE_HEALTH_LAST_UPDATED = "health_last_updated"
STATE_LAST_FERTILIZED = "last_fertilized"
STATE_NEXT_FERTILIZED = "next_fertilized"
STATE_NOTES = "notes"
STATE_LAST_REPOTTED = "last_repotted"
STATE_REPOTTED_DATE_INPUT = "repotted_date_input"
# Internal marker — date the last "health check-in overdue" notification fired.
# Used by daily_rollover to prevent re-firing more than once per day.
STATE_HEALTH_NOTIF_DATE = "_health_notif_date"

# ── Setup-wizard resolved keys (stored in entry.data, seeded to options) ──────
CONF_RESOLVED_LAST_REPOTTED = "_resolved_last_repotted"

# ── Health select options ──────────────────────────────────────────────────────
HEALTH_OPTIONS = ["excellent", "good", "poor", "sick"]
DEFAULT_HEALTH = "good"

# ── Defaults ──────────────────────────────────────────────────────────────────
DEFAULT_WATERING_INTERVAL = 7
DEFAULT_EARLY_WATERING_THRESHOLD = 3
DEFAULT_HEALTH_PROMPT_INTERVAL = 14
DEFAULT_FERTILIZATION_INTERVAL = 30
# Fertilization sync: when > 0, marking a plant watered will snap an upcoming
# fertilization date onto that watering day if it falls within this many days.
# 0 disables the feature. Kept below the watering interval in practice so only
# one candidate watering day is ever in range.
DEFAULT_FERT_SYNC_WINDOW = 0

# ── Misc ──────────────────────────────────────────────────────────────────────
NOTIFICATION_ID_PREFIX = "adaptive_plant_health_"
CONF_AREA = "area"
CONF_INITIAL_LAST_WATERED = "initial_last_watered"
CONF_INITIAL_NEXT_WATERING = "initial_next_watering"
CONF_INITIAL_LAST_FERTILIZED = "initial_last_fertilized"
CONF_INITIAL_NEXT_FERTILIZED = "initial_next_fertilized"
CONF_SNOOZE_THRESHOLD = "snooze_threshold"
STATE_SNOOZE_COUNT = "snooze_count"
STATE_SNOOZED_THIS_PERIOD = "snoozed_this_period"
DEFAULT_SNOOZE_THRESHOLD = 3
