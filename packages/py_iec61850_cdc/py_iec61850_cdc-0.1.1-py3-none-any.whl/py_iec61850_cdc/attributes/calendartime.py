# py_iec61850_cdc attributes/calendartime.py
# Copyright 2024 Kyle Hawkings
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file provides the attribute classes described under various
# IEC 61850-7-2:2010+AMD1:2020 CSV clauses and clause 6 of
# IEC 61850-7-3:2010+AMD1:2020 CSV as Python classes for use with other
# CDCs.

# Follows PEP-8 rules on function / variable naming (e.g. underscores).

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from py_iec61850_cdc.basetypes import (
    INT8U,
    INT16U,
)
from py_iec61850_cdc.enums import (
    MonthKind,
    OccurrenceKind,
    PeriodKind,
    WeekdayKind,
)


# IEC 61850-7-3 6.10 CalendarTime
class CalendarTime(BaseModel, validate_assignment = True):
    occ:      INT16U         = Field(default = 0,                   serialization_alias = "occ")
    occ_type: OccurrenceKind = Field(default = OccurrenceKind.none, serialization_alias = "occType")
    occ_per:  PeriodKind     = Field(default = PeriodKind.year,     serialization_alias = "occPer")
    week_day: WeekdayKind    = Field(default = WeekdayKind.monday,  serialization_alias = "weekDay")
    month:    MonthKind      = Field(default = MonthKind.january,   serialization_alias = "month")
    day:      INT8U          = Field(default = 1,                   serialization_alias = "day")
    hr:       INT8U          = Field(default = 0,                   serialization_alias = "hr")
    mn:       INT8U          = Field(default = 0,                   serialization_alias = "mn")

    @field_validator('day',mode='after')
    @classmethod
    def _day_after_validator(cls, value: INT8U) -> INT8U:
        if value < 1 or value > 31:
            raise ValueError(f'"{value}" must be between 1-31 for days of the month.')
        return value

    @field_validator('hr',mode='after')
    @classmethod
    def _hr_after_validator(cls, value: INT8U) -> INT8U:
        if value < 0 or value > 23:
            raise ValueError(f'"{value}" must be between 0-23 for hours of the day.')
        return value

    @field_validator('mn',mode='after')
    @classmethod
    def _mn_after_validator(cls, value: INT8U) -> INT8U:
        if value < 0 or value > 59:
            raise ValueError(f'"{value}" must be between 0-59 for minutes in the hour.')
        return value

    @classmethod
    def factory_from_py_datetime(cls,
                                 py_datetime: Optional[datetime] = None
                                 ) -> CalendarTime:
        if py_datetime is None:
            py_datetime = datetime.now(timezone.utc)
        return CalendarTime(occ      = 0,
                            occ_type = OccurrenceKind.none,
                            occ_per  = PeriodKind.year,
                            week_day = py_datetime.weekday()+1, # Python numbers weekdays from 0-6
                            month    = py_datetime.month,
                            day      = py_datetime.day,
                            hr       = py_datetime.hour,
                            mn       = py_datetime.minute)

    @classmethod
    def factory_now(cls) -> CalendarTime:
        return CalendarTime.factory_from_py_datetime()

    def to_py_datetime(self):
        now = datetime.now(timezone.utc)
        return datetime(year   = now.year,
                        month  = self.month.value,
                        day    = self.day,
                        hour   = self.hr,
                        minute = self.mn)

