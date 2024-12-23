# py_iec61850_cdc settings.py
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

# Follows PEP-8 rules on function / variable naming (e.g. underscores).

# This file provides the settings classes described in
# IEC 61850-7-2:2010+AMD1:2020 CSV and IEC 61850-7-3:2010+AMD1:2020 CSV
# as Python ABCs.

from __future__ import annotations
from typing import Optional, Any, Generic

from pydantic import Field, model_validator

from py_iec61850_cdc.abstracts import ASG, CSG, CUG, CURVE, ENG, ING, SPG, TSG, VSG, BasePrimitiveCDC
from py_iec61850_cdc.attributes import AnalogueValueCtl, CalendarTime, Point, Timestamp
from py_iec61850_cdc.basetypes import BOOLEAN, FLOAT32, INT16U, INT32, Currency, VisString255
from py_iec61850_cdc.enums import CurveCharKind, EnumDA
from py_iec61850_cdc.listobjects import DAList


# IEC 61850-7-3 7.7.2.3
class ASG_SP(ASG):
    cdc_name: VisString255     = Field(default = 'ASG_SP',
                                       pattern = 'ASG_SP',
                                       serialization_alias = 'cdcName')
    set_mag:  AnalogueValueCtl = Field(default_factory = AnalogueValueCtl,
                                       serialization_alias = "setMag")

    # ScaledValueConfig must appear if Analogue.i elements are used per the
    # standard.
    @model_validator(mode='before')
    @classmethod
    def mf_scaled_av(cls, data: Any) -> Any:
        prescond.mf_scaled_av(data,
                              svc_var    = "svc",
                              param_list = ["set_mag","min_val","max_val","step_size"])
        return data

# IEC 61850-7-3 7.7.2.4
class ASG_SG(ASG):
    cdc_name: VisString255     = Field(default = 'ASG_SG',
                                       pattern = 'ASG_SG',
                                       serialization_alias = 'cdcName')
    set_mag: AnalogueValueCtl = Field(default_factory = AnalogueValueCtl,
                                      serialization_alias = "setMag")

    # ScaledValueConfig must appear if Analogue.i elements are used per the
    # standard.
    @model_validator(mode='before')
    @classmethod
    def mf_scaled_av(cls, data: Any) -> Any:
        prescond.mf_scaled_av(data,
                              svc_var    = "svc",
                              param_list = ["set_mag","min_val","max_val","step_size"])
        return data

# IEC 61850-7-3 7.7.2.5
class ASG_SE(ASG):
    cdc_name: VisString255     = Field(default = 'ASG_SE',
                                       pattern = 'ASG_SE',
                                       serialization_alias = 'cdcName')
    set_mag: AnalogueValueCtl = Field(default_factory = AnalogueValueCtl,
                                      serialization_alias = "setMag")

    # ScaledValueConfig must appear if Analogue.i elements are used per the
    # standard.
    @model_validator(mode='before')
    @classmethod
    def mf_scaled_av(cls, data: Any) -> Any:
        prescond.mf_scaled_av(data,
                              svc_var    = "svc",
                              param_list = ["set_mag","min_val","max_val","step_size"])
        return data

# IEC 61850-7-3 7.7.4.3
class CSG_SP(CSG):
    cdc_name: VisString255     = Field(default = 'CSG_SP',
                                       pattern = 'CSG_SP',
                                       serialization_alias = 'cdcName')
    point_z: FLOAT32     = Field(default = 0,
                                 serialization_alias = "pointZ")
    num_pts: INT16U      = Field(default = 0,
                                 serialization_alias = "numPts")
    crv_pts: DAList[Point] = Field(default = None,
                                   serialization_alias = "crvPts")

# IEC 61850-7-3 7.7.4.4
class CSG_SG(CSG):
    cdc_name: VisString255     = Field(default = 'CSG_SG',
                                       pattern = 'CSG_SG',
                                       serialization_alias = 'cdcName')
    point_z: FLOAT32     = Field(default = 0,
                                 serialization_alias = "pointZ")
    num_pts: INT16U      = Field(default = 0,
                                 serialization_alias = "numPts")
    crv_pts: DAList[Point] = Field(default = None,
                                   serialization_alias = "crvPts")

# IEC 61850-7-3 7.7.4.5
class CSG_SE(CSG):
    cdc_name: VisString255     = Field(default = 'CSG_SE',
                                       pattern = 'CSG_SE',
                                       serialization_alias = 'cdcName')
    point_z: FLOAT32     = Field(default = 0,
                                 serialization_alias = "pointZ")
    num_pts: INT16U      = Field(default = 0,
                                 serialization_alias = "numPts")
    crv_pts: DAList[Point] = Field(default = None,
                                   serialization_alias = "crvPts")

# IEC 61850-7-3 7.6.7.3
class CUG_SP(CUG):
    cdc_name: VisString255     = Field(default = 'CUG_SP',
                                       pattern = 'CUG_SP',
                                       serialization_alias = 'cdcName')
    cur: Currency = Field(default = "XXX",
                          serialization_alias = "cur")

# IEC 61850-7-3 7.6.7.4
class CUG_SG(CUG):
    cdc_name: VisString255     = Field(default = 'CUG_SG',
                                       pattern = 'CUG_SG',
                                       serialization_alias   = 'cdcName')
    cur: Currency = Field(default = "XXX",
                          serialization_alias = "cur")

# IEC 61850-7-3 7.6.7.5
class CUG_SE(CUG):
    cdc_name: VisString255     = Field(default = 'CUG_SE',
                                       pattern = 'CUG_SE',
                                       serialization_alias   = 'cdcName')
    cur: Currency = Field(default = "XXX",
                          serialization_alias = "cur")

# IEC 61850-7-3 7.7.3.3
class CURVE_SP(CURVE):
    cdc_name: VisString255     = Field(default = 'CURVE_SP',
                                       pattern = 'CURVE_SP',
                                       serialization_alias = 'cdcName')
    set_charact: CurveCharKind = Field(default = CurveCharKind.none,
                                       serialization_alias = "setCharact")
    set_par_a:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParA")
    set_par_b:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParB")
    set_par_c:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParC")
    set_par_d:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParD")
    set_par_e:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParE")
    set_par_f:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParF")

# IEC 61850-7-3 7.7.3.4
class CURVE_SG(CURVE):
    cdc_name: VisString255     = Field(default = 'CURVE_SG',
                                       pattern = 'CURVE_SG',
                                       serialization_alias = 'cdcName')
    set_charact: CurveCharKind = Field(default = CurveCharKind.none,
                                       serialization_alias = "setCharact")
    set_par_a:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParA")
    set_par_b:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParB")
    set_par_c:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParC")
    set_par_d:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParD")
    set_par_e:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParE")
    set_par_f:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParF")

# IEC 61850-7-3 7.7.3.5
class CURVE_SE(CURVE):
    cdc_name: VisString255     = Field(default = 'CURVE_SE',
                                       pattern = 'CURVE_SE',
                                       serialization_alias = 'cdcName')
    set_charact: CurveCharKind = Field(default = CurveCharKind.none,
                                       serialization_alias = "setCharact")
    set_par_a:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParA")
    set_par_b:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParB")
    set_par_c:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParC")
    set_par_d:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParD")
    set_par_e:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParE")
    set_par_f:   FLOAT32       = Field(default = 0,
                                       serialization_alias = "setParF")

# IEC 61850-7-3 7.6.4.3
class ENG_SP(ENG, Generic[EnumDA]):
    cdc_name: VisString255     = Field(default = 'ENG_SP',
                                       pattern = 'ENG_SP',
                                       serialization_alias = 'ENG_SP')
    set_val: EnumDA = Field(serialization_alias = "setVal")

# IEC 61850-7-3 7.6.4.4
class ENG_SG(ENG, Generic[EnumDA]):
    cdc_name: VisString255     = Field(default = 'ENG_SG',
                                       pattern = 'ENG_SG',
                                       serialization_alias = 'cdcName')
    set_val: EnumDA = Field(serialization_alias = "setVal")

# IEC 61850-7-3 7.6.4.5
class ENG_SE(ENG, Generic[EnumDA]):
    cdc_name: VisString255     = Field(default = 'ENG_SE',
                                       pattern = 'ENG_SE',
                                       serialization_alias = 'cdcName')
    set_val: EnumDA = Field(serialization_alias = "setVal")

# IEC 61850-7-3 7.6.3.3
class ING_SP(ING):
    cdc_name: VisString255     = Field(default = 'ING_SP',
                                       pattern = 'ING_SP',
                                       serialization_alias = 'cdcName')
    set_val: INT32 = Field(default = 0,
                           serialization_alias = "setVal")

# IEC 61850-7-3 7.6.3.4
class ING_SG(ING):
    cdc_name: VisString255     = Field(default = 'ING_SG',
                                       pattern = 'ING_SG',
                                       serialization_alias   = 'cdcName')
    set_val: INT32 = Field(default = 0,
                           serialization_alias = "setVal")

# IEC 61850-7-3 7.6.3.5
class ING_SE(ING):
    cdc_name: VisString255     = Field(default = 'ING_SE',
                                       pattern = 'ING_SE',
                                       serialization_alias   = 'cdcName')
    set_val: INT32 = Field(default = 0,
                           serialization_alias = "setVal")

# IEC 61850-7-3 7.6.2.3
class SPG_SP(SPG):
    cdc_name: VisString255     = Field(default = 'SPG_SP',
                                       pattern = 'SPG_SP',
                                       serialization_alias   = 'cdcName')
    set_val: BOOLEAN = Field(default = False,
                             serialization_alias = "setVal")

# IEC 61850-7-3 7.6.2.4
class SPG_SG(SPG):
    cdc_name: VisString255     = Field(default = 'SPG_SG',
                                       pattern = 'SPG_SG',
                                       serialization_alias   = 'cdcName')
    set_val: BOOLEAN = Field(default = False,
                             serialization_alias = "setVal")

# IEC 61850-7-3 7.6.2.5
class SPG_SE(SPG):
    cdc_name: VisString255     = Field(default = 'SPG_SE',
                                       pattern = 'SPG_SE',
                                       serialization_alias   = 'cdcName')
    set_val: BOOLEAN = Field(default = False,
                             serialization_alias = "setVal")

# IEC 61850-7-3 7.6.8.3
class VSG_SP(VSG):
    cdc_name: VisString255     = Field(default = 'VSG_SP',
                                       pattern = 'VSG_SP',
                                       serialization_alias   = 'cdcName')
    set_val: VisString255 = Field(default = "",
                                  serialization_alias = "setVal")

# IEC 61850-7-3 7.6.8.4
class VSG_SG(VSG):
    cdc_name: VisString255     = Field(default = 'VSG_SG',
                                       pattern = 'VSG_SG',
                                       serialization_alias   = 'cdcName')
    set_val: VisString255 = Field(default = "",
                                  serialization_alias = "setVal")

# IEC 61850-7-3 7.6.8.5
class VSG_SE(VSG):
    cdc_name: VisString255     = Field(default = 'VSG_SE',
                                       pattern = 'VSG_SE',
                                       serialization_alias = 'cdcName')
    set_val: VisString255 = Field(default = "",
                                  serialization_alias = "setVal")

# IEC 61850-7-3 7.6.5.2
# This needs Optional[] work.
class ORG(BasePrimitiveCDC):
    cdc_name:    VisString255    = Field(default = 'ORG',
                                         pattern = 'ORG',
                                         serialization_alias   = 'cdcName')
    set_src_ref: ObjectReference = Field(default = "",
                                         serialization_alias   = "setSrcRef")
    set_tst_ref: ObjectReference = Field(default = "",
                                         serialization_alias   = "setTstRef")
    set_src_cb:  ObjectReference = Field(default = "",
                                         serialization_alias   = "setSrcCB")
    set_tst_cb:  ObjectReference = Field(default = "",
                                         serialization_alias   = "setTstCB")
    int_addr:    VisString255    = Field(default = "",
                                         serialization_alias   = "intAddr")
    tst_ena:     BOOLEAN         = Field(default = False,
                                         serialization_alias   = "tstEna")
    purpose:     VisString255    = Field(default = "",
                                         serialization_alias   = "purpose")

    @model_validator(mode='before')
    @classmethod
    def m_all_or_none_per_group_before_validator(cls,data):
        prescond.m_all_or_none_per_group(data,["set_tst_ref","tst_ena"])
        return data

    @model_validator(mode='before')
    @classmethod
    def of_sibling_before_validator(cls, data: Any) -> Any:
        prescond.of_sibling(data,"set_tst_ref",["set_tst_cb"])

# IEC 61850-7-3 7.6.6.3
class TSG_SP(TSG):
    cdc_name: VisString255     = Field(default = 'TSG_SP',
                                       pattern = 'TSG_SP',
                                       serialization_alias = 'cdcName')
    set_tm:   Optional[Timestamp]    = Field(default = None,
                                             serialization_alias = "setTm")
    set_cal:  Optional[CalendarTime] = Field(default = None,
                                             serialization_alias = "setCal")

    @model_validator(mode='before')
    @classmethod
    def at_least_one_before_validator(cls, data: Any) -> Any:
        prescond.at_least_one(data,["set_tm","set_cal"])
        return data

# IEC 61850-7-3 7.6.6.3
class TSG_SG(TSG):
    cdc_name: VisString255     = Field(default = 'TSG_SG',
                                       pattern = 'TSG_SG',
                                       serialization_alias = 'cdcName')
    set_tm:   Optional[Timestamp]    = Field(default = None,
                                             serialization_alias = "setTm")
    set_cal:  Optional[CalendarTime] = Field(default = None,
                                             serialization_alias = "setCal")

    @model_validator(mode='before')
    @classmethod
    def at_least_one_before_validator(cls, data: Any) -> Any:
        prescond.at_least_one(data,["set_tm","set_cal"])
        return data

# IEC 61850-7-3 7.6.6.3
class TSG_SE(TSG):
    cdc_name: VisString255     = Field(default = 'TSG_SE',
                                       pattern = 'TSG_SE',
                                       serialization_alias = 'cdcName')
    set_tm:   Optional[Timestamp]    = Field(default = None,
                                             serialization_alias = "setTm")
    set_cal:  Optional[CalendarTime] = Field(default = None,
                                             serialization_alias = "setCal")

    @model_validator(mode='before')
    @classmethod
    def at_least_one_before_validator(cls, data: Any) -> Any:
        prescond.at_least_one(data,["set_tm","set_cal"])
        return data


