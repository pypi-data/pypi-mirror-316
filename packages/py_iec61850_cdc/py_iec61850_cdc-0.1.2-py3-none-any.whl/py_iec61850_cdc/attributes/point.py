# py_iec61850_cdc attributes/point.py
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

from typing import Optional

from pydantic import BaseModel, Field

from py_iec61850_cdc.basetypes import (
    FLOAT32,
)


# IEC 61850-7-3 6.8 Point
class Point(BaseModel, validate_assignment = True):
    x_val: FLOAT32           = Field(default = 0.0, serialization_alias = "xVal")
    y_val: FLOAT32           = Field(default = 0.0, serialization_alias = "yVal")
    z_val: Optional[FLOAT32] = Field(default = None, serialization_alias = "zVal")

