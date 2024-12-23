# py_iec61850_cdc attributes/analoguevalues.py
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

from functools import total_ordering
from typing import Any, Optional

from pydantic import BaseModel, Field, model_validator

from py_iec61850_cdc.attributes import utils
from py_iec61850_cdc.attributes.scaledvalueconfig import ScaledValueConfig
from py_iec61850_cdc.attributes.unit import Unit
from py_iec61850_cdc.basetypes import (
    FLOAT32,
    FLOAT32_MAX_VALUE,
    FLOAT32_MIN_VALUE,
    INT32,
    INT32_MAX_VALUE,
    INT32_MIN_VALUE,
)


# IEC 61850-7-3 6.11.2 AnalogueValue
@total_ordering
class AnalogueValue(BaseModel, validate_assignment = True):
    i: Optional[INT32]   = Field(default = None, serialization_alias = "i")
    f: Optional[FLOAT32] = Field(default = None, serialization_alias = "f")

    @model_validator(mode='before')
    @classmethod
    def has_at_least_one_before_validator(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not ('f' in data or 'i' in data):
                raise ValueError("Need one of 'f' or 'i' at least!")
            elif 'f' not in data and 'i' in data:
                if data['i'] is None:
                    raise ValueError("Passed i = None, and no f. Need one of 'f' or 'i' at least!")
            elif 'f' in data and 'i' not in data:
                if data['f'] is None:
                    raise ValueError("Passed f = None, and no i. Need one of 'f' or 'i' at least!")
            elif data['f'] is None and data['i'] is None:
                raise ValueError("Passed f = None, and i = None. Need one of 'f' or 'i' at least!")
        return data

    def __gt__(self, other):
        if (type(self.f) is FLOAT32.__origin__ and
            type(self.i) is INT32.__origin__ and
            type(other.f) is FLOAT32.__origin__ and
            type(other.i) is INT32.__origin__):
            if self.f > other.f and self.i > other.i:
                return True
            elif self.f <= other.f and self.i <= other.i:
                return False
            else:
                raise ValueError("f and i comparison issue!")
        if ((self.f is None or
             other.f is None) and
             type(self.i) is INT32.__origin__ and
             type(other.i) is INT32.__origin__):
            return self.i > other.i
        if ((self.i is None or
             other.i is None) and
             type(self.f) is FLOAT32.__origin__ and
             type(other.f) is FLOAT32.__origin__):
            return self.f > other.f
        raise ValueError("Cannot compare i or f")

    @classmethod
    def factory_fi_min(cls):
        return cls.factory(set_min=True, use_f=True, use_i=True)

    @classmethod
    def factory_fi_max(cls):
        return cls.factory(set_max=True, use_f=True, use_i=True)

    @classmethod
    def factory(cls,
                p_val:   float | int                 = 0.0,
                use_f:   bool                        = True,
                use_i:   bool                        = False,
                svc:     Optional[ScaledValueConfig] = None,
                units:   Optional[Unit]              = None,
                set_min: bool                        = False,
                set_max: bool                        = False
                ):

        if set_min:
            if use_i and use_f:
                return AnalogueValue(i=INT32_MIN_VALUE,f=FLOAT32_MIN_VALUE)
            elif use_i and not use_f:
                return AnalogueValue(i=INT32_MIN_VALUE)
            elif not use_i and use_f:
                return AnalogueValue(f=FLOAT32_MIN_VALUE)
            else:
                raise ValueError("AnalogueValue.factory() cannot create empty AnalogueValue")

        if set_max:
            if use_i and use_f:
                return AnalogueValue(i=INT32_MAX_VALUE,f=FLOAT32_MAX_VALUE)
            elif use_i and not use_f:
                return AnalogueValue(i=INT32_MAX_VALUE)
            elif not use_i and use_f:
                return AnalogueValue(f=FLOAT32_MAX_VALUE)
            else:
                raise ValueError("AnalogueValue.factory() cannot create empty AnalogueValue")

        if use_i and svc is None:
            raise ValueError("Cannot set AnalogueValue.i without svc!")

        f,i = utils.set_process_value(p_val = p_val,
                                      use_f = use_f,
                                      use_i = use_i,
                                      svc = svc,
                                      units = units)
        av_return = AnalogueValue(
                        f = f,
                        i = i
                        )
        return av_return

    def p_val(self,
              force_i: Optional[bool]              = False,
              svc:     Optional[ScaledValueConfig] = None,
              units:   Optional[Unit]              = None,
              ):
        return utils.get_process_value(f_val  = self.f,
                                       i_val  = self.i,
                                       from_i = force_i,
                                       svc    = svc,
                                       units  = units)

# IEC 61850-7-3 6.11.3 AnalogueValueCtl
@total_ordering
class AnalogueValueCtl(BaseModel, validate_assignment = True):
    i: Optional[INT32]   = Field(default = None, serialization_alias = "i")
    f: Optional[FLOAT32] = Field(default = None, serialization_alias = "f")

    @model_validator(mode='before')
    @classmethod
    def has_only_one_group_before_validator(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not ('f' in data or 'i' in data):
                raise ValueError("Must have one of 'f' or 'i'!")
            if 'f' in data and 'i' in data:
                raise ValueError("May only have one of 'f' or 'i'!")
        return data

    def __gt__(self, other):
        if (type(self.f) is FLOAT32.__origin__ and
            type(self.i) is INT32.__origin__ and
            type(other.f) is FLOAT32.__origin__ and
            type(other.i) is INT32.__origin__):
            if self.f > other.f and self.i > other.i:
                return True
            elif self.f <= other.f and self.i <= other.i:
                return False
            else:
                raise ValueError("f and i comparison issue!")
        if ((self.f is None or
             other.f is None) and
             type(self.i) is INT32.__origin__ and
             type(other.i) is INT32.__origin__):
            return self.i > other.i
        if ((self.i is None or
             other.i is None) and
             type(self.f) is FLOAT32.__origin__ and
             type(other.f) is FLOAT32.__origin__):
            return self.f > other.f
        raise ValueError("Cannot compare i or f")

    @classmethod
    def factory_fi_min(cls):
        return cls.factory(set_min=True, use_i=False)

    @classmethod
    def factory_fi_max(cls):
        return cls.factory(set_max=True, use_i=False)

    @classmethod
    def factory(cls,
                p_val:   float | int                 = 0.0,
                use_i:   bool                        = False,
                svc:     Optional[ScaledValueConfig] = None,
                units:   Optional[Unit]              = None,
                set_min: bool                        = False,
                set_max: bool                        = False
                ):

        if set_min:
            if use_i:
                return AnalogueValueCtl(i=INT32_MIN_VALUE)
            else:
                return AnalogueValueCtl(f=FLOAT32_MIN_VALUE)

        if set_max:
            if use_i:
                return AnalogueValueCtl(i=INT32_MAX_VALUE)
            else:
                return AnalogueValueCtl(f=FLOAT32_MAX_VALUE)

        if use_i and svc is None:
            raise ValueError("Cannot set AnalogueValue.i without svc!")

        f,i = utils.set_process_value(p_val = p_val,
                                      use_f = use_f,
                                      use_i = use_i,
                                      svc = svc,
                                      units = units)
        if use_i:
            av_return = AnalogueValueCtl(
                            i = i
                            )
        else:
            av_return = AnalogueValueCtl(
                            f = f
                            )
        return av_return

    def p_val(self,
              force_i: Optional[bool]              = False,
              svc:     Optional[ScaledValueConfig] = None,
              units:   Optional[Unit]              = None,
              ):
        if self.f is not None:
            return utils.get_process_value(f_val  = self.f,
                                           i_val  = self.i,
                                           from_i = False,
                                           svc    = svc,
                                           units  = units)
        if self.i is not None:
            return utils.get_process_value(f_val  = self.f,
                                           i_val  = self.i,
                                           from_i = True,
                                           svc    = svc,
                                           units  = units)

# IEC 61850-7-3 6.11.4 AnalogueValueCtlF
@total_ordering
class AnalogueValueCtlF(BaseModel, validate_assignment = True):
    f: FLOAT32 = Field(default = 0.0, serialization_alias = "f")

    def __gt__(self, other):
        return self.f > other.f

    @classmethod
    def factory_min(cls):
        return cls.factory(set_min=True)

    @classmethod
    def factory_max(cls):
        return cls.factory(set_max=True)

    @classmethod
    def factory(cls,
                p_val:   float                       = 0.0,
                units:   Optional[Unit]              = None,
                set_min: bool                        = False,
                set_max: bool                        = False
                ):

        if set_min:
            return AnalogueValueCtlF(f=FLOAT32_MIN_VALUE)

        if set_max:
            return AnalogueValueCtlF(f=FLOAT32_MAX_VALUE)

        if use_i and svc is None:
            raise ValueError("Cannot set AnalogueValue.i without svc!")

        f,i = utils.set_process_value(p_val = p_val,
                                      use_f = True,
                                      use_i = False,
                                      svc   = None,
                                      units = units)
        av_return = AnalogueValueCtlF(f = f)
        return av_return

    def p_val(self,
              units: Optional[Unit] = None,
              ):
        return utils.get_process_value(f_val  = self.f,
                                       i_val  = 0,
                                       from_i = False,
                                       svc    = None,
                                       units  = units)

# IEC 61850-7-3 6.11.5 AnalogueValueCtlInt
@total_ordering
class AnalogueValueCtlInt(BaseModel, validate_assignment = True):
    i: INT32   = Field(default = 0, serialization_alias = "i")

    def __gt__(self, other):
        return self.i > other.i

    @classmethod
    def factory_min(cls):
        return cls.factory(set_min=True)

    @classmethod
    def factory_max(cls):
        return cls.factory(set_max=True)

    @classmethod
    def factory(cls,
                p_val:   int                         = 0,
                svc:     Optional[ScaledValueConfig] = None,
                set_min: bool                        = False,
                set_max: bool                        = False
                ):

        if set_min:
            return AnalogueValueCtlI(i=INT32_MIN_VALUE)

        if set_max:
            return AnalogueValueCtlI(i=INT32_MAX_VALUE)

        if use_i and svc is None:
            raise ValueError("Cannot set AnalogueValue.i without svc!")

        f,i = utils.set_process_value(p_val = p_val,
                                      use_f = False,
                                      use_i = True,
                                      svc   = svc,
                                      units = None)
        av_return = AnalogueValueCtlI(i = i)
        return av_return

    def p_val(self,
              svc: ScaledValueConfig = None,
              ):
        return utils.get_process_value(f_val  = 0.0,
                                       i_val  = self.i,
                                       from_i = True,
                                       svc    = svc,
                                       units  = None)


