# py_iec61850_cdc attributes/rangeconfig.py
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

from py_iec61850_cdc.attributes.analoguevalues import AnalogueValue
from py_iec61850_cdc.attributes.detailqual import DetailQual
from py_iec61850_cdc.attributes.scaledvalueconfig import ScaledValueConfig
from py_iec61850_cdc.attributes.unit import Unit
from py_iec61850_cdc.basetypes import (
    INT32U,
)
from py_iec61850_cdc.enums import (
    RangeKind,
    ValidityKind,
)


#IEC 61850-7-3 6.3 RangeConfig
class RangeConfig(BaseModel, validate_assignment = True):
    hh_lim:  Optional[AnalogueValue] = Field(default = None,
                                             serialization_alias = "hhLim")
    h_lim:   Optional[AnalogueValue] = Field(default = None,
                                             serialization_alias = "hLim")
    l_lim:   Optional[AnalogueValue] = Field(default = None,
                                             serialization_alias = "lLim")
    ll_lim:  Optional[AnalogueValue] = Field(default = None,
                                             serialization_alias = "llLim")
    minimum: AnalogueValue           = Field(default_factory = AnalogueValue.factory_fi_min,
                                             serialization_alias = "min")
    maximum: AnalogueValue           = Field(default_factory = AnalogueValue.factory_fi_max,
                                             serialization_alias = "max")
    lim_db:  Optional[INT32U]        = Field(default = None,
                                             serialization_alias = "limDb")

    def validate_range_v(self, value: AnalogueValue) -> RangeKind:
        if self.hh_lim is not None:
            if   (value > self.hh_lim): return RangeKind.high_high
        if self.h_lim is not None:
            if   (value > self.h_lim):  return RangeKind.high
        if self.ll_lim is not None:
            if   (value < self.ll_lim): return RangeKind.low_low
        if self.l_lim is not None:
            if   (value < self.l_lim):  return RangeKind.low
        return RangeKind.normal

    # Utility function for obtaining a validity and detailQual based on RangeConfig
    def check_quality(self, value: AnalogueValue) -> tuple[ValidityKind, DetailQual]:
        if value > self.maximum:
            return ValidityKind.questionable, DetailQual(out_of_range=True)
        if value < self.minimum:
            return ValidityKind.questionable, DetailQual(out_of_range=True)
        else:
            return ValidityKind.good, DetailQual()

    @classmethod
    def factory(cls,
                use_f:     bool                        = True,
                use_i:     bool                        = False,
                p_maximum: Optional[float|int]         = None,
                p_hh_lim:  Optional[float|int]         = None,
                p_h_lim:   Optional[float|int]         = None,
                p_l_lim:   Optional[float|int]         = None,
                p_ll_lim:  Optional[float|int]         = None,
                p_minimum: Optional[float|int]         = None,
                lim_db:    Optional[int]               = None,
                svc:       Optional[ScaledValueConfig] = None,
                units:     Optional[Unit]              = None
                ):

        # Prepare the max value
        if p_maximum is not None:
            av_maximum = AnalogueValue.factory(p_val = p_maximum,
                                               use_f = use_f,
                                               use_i = use_i,
                                               svc   = svc,
                                               units = units)
        else:
            av_maximum = AnalogueValue.factory(set_max = True,
                                               use_f   = use_f,
                                               use_i   = use_i)

        # Prepare the hh_lim value
        if p_hh_lim is not None:
            av_hh_lim  = AnalogueValue.factory(p_val = p_hh_lim,
                                               use_f = use_f,
                                               use_i = use_i,
                                               svc   = svc,
                                               units = units)
        else:
            av_hh_lim  = None

        # Prepare the h_lim value
        if p_h_lim is not None:
            av_h_lim   = AnalogueValue.factory(p_val = p_h_lim,
                                               use_f = use_f,
                                               use_i = use_i,
                                               svc   = svc,
                                               units = units)
        else:
            av_h_lim   = None

        # Prepare the l_lim value
        if p_l_lim is not None:
            av_l_lim   = AnalogueValue.factory(p_val = p_l_lim,
                                               use_f = use_f,
                                               use_i = use_i,
                                               svc   = svc,
                                               units = units)
        else:
            av_l_lim   = None

        # Prepare the ll_lim value
        if p_ll_lim is not None:
            av_ll_lim  = AnalogueValue.factory(p_val = p_ll_lim,
                                               use_f = use_f,
                                               use_i = use_i,
                                               svc   = svc,
                                               units = units)
        else:
            av_ll_lim  = None

    # Prepare the min value
        if p_minimum is not None:
            av_minimum = AnalogueValue.factory(p_val = p_minimum,
                                               use_f = use_f,
                                               use_i = use_i,
                                               svc   = svc,
                                               units = units)
        else:
            av_minimum = AnalogueValue.factory(set_min = True,
                                               use_f   = use_f,
                                               use_i   = use_i)

        return RangeConfig(maximum = av_maximum,
                           hh_lim  = av_hh_lim,
                           h_lim   = av_h_lim,
                           l_lim   = av_l_lim,
                           ll_lim  = av_ll_lim,
                           minimum = av_minimum)

