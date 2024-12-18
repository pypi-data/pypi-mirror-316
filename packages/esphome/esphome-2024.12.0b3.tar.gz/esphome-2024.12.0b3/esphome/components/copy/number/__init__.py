import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import (
    CONF_ENTITY_CATEGORY,
    CONF_ICON,
    CONF_MODE,
    CONF_SOURCE_ID,
    CONF_UNIT_OF_MEASUREMENT,
)
from esphome.core.entity_helpers import inherit_property_from

from .. import copy_ns

CopyNumber = copy_ns.class_("CopyNumber", number.Number, cg.Component)


CONFIG_SCHEMA = (
    number.number_schema(CopyNumber)
    .extend(
        {
            cv.Required(CONF_SOURCE_ID): cv.use_id(number.Number),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
)

FINAL_VALIDATE_SCHEMA = cv.All(
    inherit_property_from(CONF_ICON, CONF_SOURCE_ID),
    inherit_property_from(CONF_ENTITY_CATEGORY, CONF_SOURCE_ID),
    inherit_property_from(CONF_UNIT_OF_MEASUREMENT, CONF_SOURCE_ID),
    inherit_property_from(CONF_MODE, CONF_SOURCE_ID),
)


async def to_code(config):
    var = await number.new_number(config, min_value=0, max_value=0, step=0)
    await cg.register_component(var, config)

    source = await cg.get_variable(config[CONF_SOURCE_ID])
    cg.add(var.set_source(source))
