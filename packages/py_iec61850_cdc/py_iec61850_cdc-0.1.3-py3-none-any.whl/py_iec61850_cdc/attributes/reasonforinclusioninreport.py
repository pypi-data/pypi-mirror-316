# py_iec61850_cdc attributes/reasonforinclusioninreport.py
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


# IEC 61850-7-2 6.3.3.3 ReasonForInclusionInReport
class ReasonForInclusionInReport(BaseModel, validate_assignment = True):
    data_change:           BOOLEAN = Field(default=False,
                                           serialization_alias="data-change")
    quality_change:        BOOLEAN = Field(default=False,
                                           serialization_alias="quality-change")
    data_update:           BOOLEAN = Field(default=False,
                                           serialization_alias="data-update")
    integrity:             BOOLEAN = Field(default=False,
                                           serialization_alias="integrity")
    general_interrogation: BOOLEAN = Field(default=False,
                                           serialization_alias="general-interrogation")

    # Note to self: Add model validators.
    # data-change and quality-change can appear together
    # data-update and quality-change can appear together
    # otherwise everything is mutually exclusive (only one item can be True)

