# py_iec61850_cdc attributes/timestamp.py
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

import time
from datetime import datetime

from pydantic import BaseModel, Field

from py_iec61850_cdc.attributes.timequality import TimeQuality
from py_iec61850_cdc.basetypes import (
    INT24U,
    INT32U,
)


# IEC 61850-7-2 6.2.3.7 Timestamp
class Timestamp(BaseModel, validate_assignment = True):
    seconds_since_epoch: INT32U      = Field(default = 0,                   serialization_alias = "SecondSinceEpoch")
    fraction_of_second:  INT24U      = Field(default = 0,                   serialization_alias = "FractionOfSecond")
    time_quality:        TimeQuality = Field(default_factory = TimeQuality, serialization_alias = "TimeQuality")

    @classmethod
    def factory_local(cls):
        time_in_ns = time.time_ns()
        seconds_since_epoch = int(time_in_ns * 10**-9)
        nanoseconds = int(time_in_ns-seconds_since_epoch/10**-9)
        fraction_of_second = int(nanoseconds / (10**9) * (2**24))
        new_tq = TimeQuality(leap_seconds_known     = False,
                             clock_failure          = False,
                             clock_not_synchronized = False,
                             time_accuracy          = 0)
        return Timestamp(seconds_since_epoch = seconds_since_epoch,
                         fraction_of_second  = fraction_of_second,
                         time_quality        = new_tq)

    def as_python_datetime(self, tz=None):
        timestamp_data = self.seconds_since_epoch + self.fraction_of_second / (2**24)
        return datetime.fromtimestamp(timestamp_data, tz)

