# py_iec61850_cdc attributes/vector.py
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

from math import atan2, cos, pi, sin, sqrt
from typing import Optional

from pydantic import BaseModel, Field

from py_iec61850_cdc.attributes.analoguevalues import AnalogueValue


# IEC 61850-7-3 6.7 Vector
class Vector(BaseModel, validate_assignment = True):
    mag: AnalogueValue           = Field(default_factory = AnalogueValue, serialization_alias = "mag")
    ang: Optional[AnalogueValue] = Field(default = None, serialization_alias = "ang")

    def x(self,
          force_i: Optional[bool]              = False,
          svc:     Optional[ScaledValueConfig] = None,
          units:   Optional[Unit]              = None) -> float:

        retmag = self.mag.p_val(force_i = force_i,
                                svc     = svc,
                                units   = units)

        if self.ang is not None:
            retang = self.ang.p_val(force_i = force_i,
                                    svc     = svc,
                                    units   = units)
        else:
            retang = 0

        return retmag * cos(retang/180*pi)

    def y(self,
          force_i: Optional[bool]              = False,
          svc:     Optional[ScaledValueConfig] = None,
          units:   Optional[Unit]              = None) -> float:

        retmag = self.mag.p_val(force_i = force_i,
                                svc     = svc,
                                units   = units)

        if self.ang is not None:
            retang = self.ang.p_val(force_i = force_i,
                                    svc     = svc,
                                    units   = units)
        else:
            retang = 0

        return retmag * sin(retang/180*pi)

    @classmethod
    def factory_from_xy(cls,
                        x: float | int = 0.0,
                        y: float | int = 0.0,
                        force_i: Optional[bool] = False,
                        svc: Optional[ScaledValueConfig] = None,
                        units: Optional[Unit] = None
                        ) -> Vector:
        mag_av = AnalogueValue.factory(p_val = sqrt((x**2)+(y**2)))
        ang_av = AnalogueValue.factory(p_val = atan2(y,x)/pi*180)
        return Vector(mag=mag_av,
                      ang=ang_av)

