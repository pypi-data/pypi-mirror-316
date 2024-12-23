# Test to confirm behavior of base IEC types.
# Basic IEC types are intended for use with Pydantic
# BaseModel to validate that the allowable ranges
# are obeyed (e.g. -128 <= INT8 <= 127).


# Note that TYPE_MIN_VALUE and TYPE_MAX_VALUE are
# not imported, as the field_TYPE functions should
# have optional parameters that auto-set maximums.
from py_iec61850_cdc import factory

factory.factory_json('''
{
    "cdcName" : "HMV"
}'''
)

