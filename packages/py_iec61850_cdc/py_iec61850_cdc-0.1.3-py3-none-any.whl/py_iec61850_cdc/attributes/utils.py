# py_iec61850_cdc attributes/utils.py
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

from py_iec61850_cdc.attributes.scaledvalueconfig import ScaledValueConfig
from py_iec61850_cdc.attributes.unit import Unit


def get_process_value(f_val:  Optional[float] = 0.0,
                      i_val:  Optional[int]   = 0,
                      from_i: bool = False,
                      svc:    Optional[ScaledValueConfig] = None,
                      units:  Optional[Unit] = None
                      ) -> float:
    if from_i and svc is None:
        raise ValueError("Need svc to get process value from i")
    elif from_i and svc is not None:
        p_val = i_val * svc.scale_factor + svc.offset
    elif not from_i and units is not None:
        p_val = f_val * 10**units.multiplier
    else:
        p_val = f_val
    return p_val

def set_process_value(p_val: float | int = 0.0,
                      use_f: bool = True,
                      use_i: bool = False,
                      svc:   Optional[ScaledValueConfig] = None,
                      units: Optional[Unit] = None
                      ):
    if use_f == True:
        if units is not None:
            if units.multiplier is not None:
                f = p_val * units.multiplier
            else:
                f = p_val
        else:
            f = p_val
    else:
        f = None
    if use_i == True and svc is not None:
        i = (p_val - svc.offset) / svc.scale_factor
    else:
        i = None
    return f,i

