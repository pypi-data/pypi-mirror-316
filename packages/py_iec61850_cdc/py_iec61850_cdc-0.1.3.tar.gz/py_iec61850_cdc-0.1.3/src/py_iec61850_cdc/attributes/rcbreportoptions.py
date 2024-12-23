# py_iec61850_cdc attributes/rcbreportoptions.py
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

from pydantic import BaseModel, Field

from py_iec61850_cdc.basetypes import (
    BOOLEAN,
)


# IEC 61850-7-2 6.2.3.13 RCBReportOptions
class RCBReportOptions(BaseModel, validate_assignment = True):
    sequence_number:      BOOLEAN = Field(default = False, serialization_alias = "sequence-number")
    report_time_stamp:    BOOLEAN = Field(default = False, serialization_alias = "report-time-stamp")
    reason_for_inclusion: BOOLEAN = Field(default = False, serialization_alias = "reason-for-inclusion")
    data_set_name:        BOOLEAN = Field(default = False, serialization_alias = "data-set-name")
    data_reference:       BOOLEAN = Field(default = False, serialization_alias = "data-reference")
    buffer_overflow:      BOOLEAN = Field(default = False, serialization_alias = "buffer-overflow")
    entry_id:             BOOLEAN = Field(default = False, serialization_alias = "entryID")
    conf_revision:        BOOLEAN = Field(default = False, serialization_alias = "conf-revision")
    segmentation:         BOOLEAN = Field(default = False, serialization_alias = "segmentation")

