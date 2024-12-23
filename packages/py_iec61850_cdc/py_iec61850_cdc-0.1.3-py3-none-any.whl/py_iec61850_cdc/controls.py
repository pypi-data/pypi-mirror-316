# py_iec61850_cdc controls.py
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

# This file provides the analog info CDCs described under Clause 7.4 of
# IEC 61850-7-3:2010+AMD1:2020 CSV as Python dataclasses.

from __future__ import annotations
from typing import Any, Optional, TypeVar, Generic

from pydantic import Field, model_validator

from py_iec61850_cdc import prescond
from py_iec61850_cdc.abstracts import ControlTestingCDC
from py_iec61850_cdc.attributes import (
    AnalogueValue,
    AnalogueValueCtl,
    Originator,
    PulseConfig,
    Quality,
    ScaledValueConfig,
    Timestamp,
    Unit,
    ValWithTrans,
)
from py_iec61850_cdc.basetypes import BOOLEAN, FLOAT32, INT8, INT8U, INT32, INT32U, VisString255
from py_iec61850_cdc.enums import CtlModelKind, DpStatusKind, SboClassKind, StepControlKind, EnumDA


# IEC 61850-7-3 7.5.3
class SPC(ControlTestingCDC):
    cdc_name:     VisString255           = Field(default = 'SPC',
                                                 pattern = 'SPC',
                                                 serialization_alias = 'cdcName')
    origin:       Optional[Originator]   = Field(default = None,
                                                 serialization_alias = 'origin')
    ctl_num:      Optional[INT8U]        = Field(default = None,
                                                 serialization_alias = "ctlNum")
    st_val:       Optional[BOOLEAN]      = Field(default = None,
                                                 serialization_alias = "stVal")
    q:            Optional[Quality]      = Field(default = None,
                                                 serialization_alias = "q")
    t:            Optional[Timestamp]    = Field(default = None,
                                                 serialization_alias = "t")
    st_seld:      Optional[BOOLEAN]      = Field(default = None,
                                                 serialization_alias = "stSeld")
    sub_val:      Optional[BOOLEAN]      = Field(default = None,
                                                 serialization_alias = "subVal")
    pulse_config: Optional[PulseConfig]  = Field(default = None,
                                                 serialization_alias = "pulseConfig")
    ctl_model:    CtlModelKind           = Field(default = CtlModelKind.direct_with_normal_security,
                                                 serialization_alias = "ctlModel")
    sbo_timeout:  Optional[INT32U]       = Field(default = None,
                                                 serialization_alias = "sboTimeout")
    sbo_class:    Optional[SboClassKind] = Field(default = None,
                                                 serialization_alias = "sboClass")
    oper_timeout: Optional[INT32U]       = Field(default = None,
                                                 serialization_alias = "operTimeout")
    ctl_val:      BOOLEAN                = Field(default = False,
                                                 serialization_alias = "ctlVal")

    # st_val, q, and t must be used as a set.
    @model_validator(mode='before')
    @classmethod
    def m_all_or_none_per_group_before_validator(cls,data):
        prescond.m_all_or_none_per_group(data,["st_val","q","t"])
        return data

    # MOsbo constraint based on CtlModelKind being direct-with-enchanced-security or sbo-with-enhanced-security
    @model_validator(mode='before')
    @classmethod
    def mo_sbo_before_validator(cls,data):
        prescond.mo_sbo(data,"ctl_model",["st_seld","sbo_timeout"])
        return data

    # MBenhanced constraint
    @model_validator(mode='before')
    @classmethod
    def mo_enhanced_before_validator(cls,data):
        prescond.mo_enhanced(data,"ctl_model",["oper_timeout"])
        return data

    # Add sub_val checker
    @model_validator(mode='before')
    @classmethod
    def mf_subst_before_validator(cls,data):
        prescond.mf_subst(data,True,["sub_ena","sub_val","sub_q","sub_id"])
        return data

# IEC 61850-7-3 7.5.4
class DPC(ControlTestingCDC):
    cdc_name:     VisString255           = Field(default = 'DPC',
                                                 pattern = 'DPC',
                                                 serialization_alias = 'cdcName')
    origin:       Optional[Originator]   = Field(default = None,
                                                 serialization_alias = "origin")
    ctl_num:      Optional[INT8U]        = Field(default = None,
                                                 serialization_alias = "ctlNum")
    st_val:       DpStatusKind           = Field(default = DpStatusKind.off,
                                                 serialization_alias = "stVal")
    q:            Quality                = Field(default_factory = Quality,
                                                 serialization_alias = "q")
    t:            Timestamp              = Field(default_factory = Timestamp,
                                                 serialization_alias = "t")
    st_seld:      Optional[BOOLEAN]      = Field(default = None,
                                                 serialization_alias = "stSeld")
    sub_val:      Optional[DpStatusKind] = Field(default = None,
                                                 serialization_alias = "subVal")
    pulse_config: Optional[PulseConfig]  = Field(default = None,
                                                 serialization_alias = "pulseConfig")
    ctl_model:    CtlModelKind           = Field(default = CtlModelKind.direct_with_normal_security,
                                                 serialization_alias = "ctlModel")
    sbo_timeout:  Optional[INT32U]       = Field(default = None,
                                                 serialization_alias = "sboTimeout")
    sbo_class:    Optional[SboClassKind] = Field(default = None,
                                                 serialization_alias = "sboClass")
    oper_timeout: Optional[INT32U]       = Field(default = None,
                                                 serialization_alias = "operTimeout")
    ctl_val:      BOOLEAN                = Field(default = False,
                                                 serialization_alias = "ctlVal")

    # MOsbo constraint based on CtlModelKind being direct-with-enchanced-security or sbo-with-enhanced-security
    @model_validator(mode='before')
    @classmethod
    def mo_sbo_before_validator(cls,data):
        prescond.mo_sbo(data,"ctl_model",["st_seld","sbo_timeout"])
        return data

    # MBenhanced constraint
    @model_validator(mode='before')
    @classmethod
    def mo_enhanced_before_validator(cls,data):
        prescond.mo_enhanced(data,"ctl_model",["oper_timeout"])
        return data

    # Add sub_val checker
    @model_validator(mode='before')
    @classmethod
    def mf_subst_before_validator(cls,data):
        prescond.mf_subst(data,True,["sub_ena","sub_val","sub_q","sub_id"])
        return data

# IEC 61850-7-3 7.5.5
class INC(ControlTestingCDC):
    cdc_name:     VisString255           = Field(default = 'INC',
                                                 pattern = 'INC',
                                                 serialization_alias = 'cdcName')
    origin:       Optional[Originator]   = Field(default_factory = Originator,
                                                 serialization_alias = "origin")
    ctl_num:      Optional[INT8U]        = Field(default = 0,
                                                 serialization_alias = "ctlNum")
    st_val:       INT32                  = Field(default = 0,
                                                 serialization_alias = "stVal")
    q:            Quality                = Field(default_factory = Quality,
                                                 serialization_alias = "q")
    t:            Timestamp              = Field(default_factory = Timestamp,
                                                 serialization_alias = "t")
    st_seld:      Optional[BOOLEAN]      = Field(default = False,
                                                 serialization_alias = "stSeld")
    sub_val:      Optional[INT32]        = Field(default = 0,
                                                 serialization_alias = "subVal")
    ctl_model:    CtlModelKind           = Field(default = CtlModelKind.direct_with_normal_security,
                                                 serialization_alias = "ctlModel")
    sbo_timeout:  Optional[INT32U]       = Field(default = 0,
                                                 serialization_alias = "sboTimeout")
    sbo_class:    Optional[SboClassKind] = Field(default = SboClassKind.operate_once,
                                                 serialization_alias = "sboClass")
    min_val:      Optional[INT32]        = Field(default = 0,
                                                 serialization_alias = "minVal")
    max_val:      Optional[INT32]        = Field(default = 0,
                                                 serialization_alias = "maxVal")
    step_size:    Optional[INT32U]       = Field(default = 0,
                                                 serialization_alias = "stepSize")
    oper_timeout: Optional[INT32U]       = Field(default = 0,
                                                 serialization_alias = "operTimeout")
    units:        Optional[Unit]         = Field(default_factory = Unit,
                                                 serialization_alias = "units")
    ctl_val:      INT32                  = Field(default = 0,
                                                 serialization_alias = "ctlVal")

    # MOsbo constraint based on CtlModelKind being direct-with-enchanced-security or sbo-with-enhanced-security
    @model_validator(mode='before')
    @classmethod
    def mo_sbo_before_validator(cls,data):
        prescond.mo_sbo(data,"ctl_model",["st_seld","sbo_timeout"])
        return data

    # MBenhanced constraint
    @model_validator(mode='before')
    @classmethod
    def mo_enhanced_before_validator(cls,data):
        prescond.mo_enhanced(data,"ctl_model",["oper_timeout"])
        return data

    # Add sub_val checker
    @model_validator(mode='before')
    @classmethod
    def mf_subst_before_validator(cls,data):
        prescond.mf_subst(data,True,["sub_ena","sub_val","sub_q","sub_id"])
        return data

# IEC 61850-7-3 7.5.6
class ENC(ControlTestingCDC, Generic[EnumDA]):
    cdc_name:     VisString255           = Field(default = 'ENC',
                                                 pattern = 'ENC',
                                                 serialization_alias = 'cdcName')
    origin:       Optional[Originator]   = Field(default = None,
                                                 serialization_alias = "origin")
    ctl_num:      Optional[INT8U]        = Field(default = None,
                                                 serialization_alias = "ctlNum")
    st_val:       EnumDA                 = Field(default = 0,
                                                 serialization_alias = "stVal") # Not sure what to do here.
    q:            Quality                = Field(default_factory = Quality,
                                                 serialization_alias = "q")
    t:            Timestamp              = Field(default_factory = Timestamp,
                                                 serialization_alias = "t")
    st_seld:      Optional[BOOLEAN]      = Field(default = False,
                                                 serialization_alias = "stSeld")
    sub_val:      Optional[EnumDA]       = Field(default = 0,
                                                 serialization_alias = "subVal") # Not sure what to do here.
    ctl_model:    CtlModelKind           = Field(default = CtlModelKind.status_only,
                                                 serialization_alias = "ctlModel")
    sbo_timeout:  Optional[INT32U]       = Field(default = 0,
                                                 serialization_alias = "sboTimeout")
    sbo_class:    Optional[SboClassKind] = Field(default = SboClassKind.operate_once,
                                                 serialization_alias = "sboClass")
    oper_timeout: Optional[INT32U]       = Field(default = 0,
                                                 serialization_alias = "operTimeout")
    ctl_val:      EnumDA                 = Field(default = 0,
                                                 serialization_alias = "ctlVal") # Not sure what to do here.

    # MOsbo constraint based on CtlModelKind being direct-with-enchanced-security or sbo-with-enhanced-security
    @model_validator(mode='before')
    @classmethod
    def mo_sbo_before_validator(cls,data):
        prescond.mo_sbo(data,"ctl_model",["st_seld","sbo_timeout"])
        return data

    # MBenhanced constraint
    @model_validator(mode='before')
    @classmethod
    def mo_enhanced_before_validator(cls,data):
        prescond.mo_enhanced(data,"ctl_model",["oper_timeout"])
        return data

    # Add sub_val checker
    @model_validator(mode='before')
    @classmethod
    def mf_subst_before_validator(cls,data):
        prescond.mf_subst(data,True,["sub_ena","sub_val","sub_q","sub_id"])
        return data

# IEC 61850-7-3 7.5.7
class BSC(ControlTestingCDC):
    cdc_name:     VisString255           = Field(default = 'BSC',
                                                 pattern = 'BSC',
                                                 serialization_alias = 'cdcName')
    origin:       Optional[Originator]   = Field(default = Originator,
                                                 serialization_alias = "origin")
    ctl_num:      Optional[INT8U]        = Field(default = 0,
                                                 serialization_alias = "ctlNum")
    val_w_tr:     Optional[ValWithTrans] = Field(default_factory = ValWithTrans,
                                                 serialization_alias = "valWTr")
    q:            Optional[Quality]      = Field(default_factory = Quality,
                                                 serialization_alias = "q")
    t:            Optional[Timestamp]    = Field(default_factory = Timestamp,
                                                 serialization_alias = "t")
    st_seld:      Optional[BOOLEAN]      = Field(default = False,
                                                 serialization_alias = "stSeld")
    sub_val:      Optional[ValWithTrans] = Field(default_factory = ValWithTrans,
                                                 serialization_alias = "subVal")
    persistent:   BOOLEAN                = Field(default = False,
                                                 serialization_alias = "persistent")
    ctl_model:    CtlModelKind           = Field(default = CtlModelKind.direct_with_normal_security,
                                                 serialization_alias = "ctlModel")
    sbo_timeout:  Optional[INT32U]       = Field(default = 0,
                                                 serialization_alias = "sboTimeout")
    sbo_class:    Optional[SboClassKind] = Field(default = SboClassKind.operate_once,
                                                 serialization_alias = "sboClass")
    min_val:      Optional[INT8]         = Field(default = 0,
                                                 serialization_alias = "minVal")
    max_val:      Optional[INT8]         = Field(default = 0,
                                                 serialization_alias = "maxVal")
    oper_timeout: Optional[INT32U]       = Field(default = 0,
                                                 serialization_alias = "operTimeout")
    ctl_val:      StepControlKind        = Field(default = StepControlKind.stop,
                                                 serialization_alias = "ctlVal")

    # MAllOrNonePerGroup(1) constraint
    # MOsbo constraint
    # MOenhanced constraint

# IEC 61850-7-3 7.5.8
class ISC(ControlTestingCDC):
    cdc_name:     VisString255           = Field(default = 'ISC',
                                                 pattern = 'ISC',
                                                 serialization_alias = 'cdcName')
    origin:       Optional[Originator]   = Field(default_factory = Originator,
                                                 serialization_alias = "origin")
    ctl_num:      Optional[INT8U]        = Field(default = 0,
                                                 serialization_alias = "ctlNum")
    val_w_tr:     Optional[ValWithTrans] = Field(default_factory = ValWithTrans,
                                                 serialization_alias = "valWTr")
    q:            Optional[Quality]      = Field(default_factory = Quality,
                                                 serialization_alias = "q")
    t:            Optional[Timestamp]    = Field(default_factory = Timestamp,
                                                 serialization_alias = "t")
    st_seld:      Optional[BOOLEAN]      = Field(default = False,
                                                 serialization_alias = "stSeld")
    sub_val:      Optional[ValWithTrans] = Field(default_factory = ValWithTrans,
                                                 serialization_alias = "subVal")
    ctl_model:    CtlModelKind           = Field(default = CtlModelKind.direct_with_normal_security,
                                                 serialization_alias = "ctlModel")
    sbo_timeout:  Optional[INT32U]       = Field(default = 0,
                                                 serialization_alias = "sboTimeout")
    min_val:      Optional[INT8]         = Field(default = 0,
                                                 serialization_alias = "minVal")
    max_val:      Optional[INT8]         = Field(default = 0,
                                                 serialization_alias = "maxVal")
    oper_timeout: Optional[INT32U]       = Field(default = 0,
                                                 serialization_alias = "operTimeout")
    ctl_val:      INT8                   = Field(default = 0,
                                                 serialization_alias = "ctlVal")

    # st_val, q, and t must be used as a set.
    @model_validator(mode='before')
    @classmethod
    def m_all_or_none_per_group_before_validator(cls,data):
        prescond.m_all_or_none_per_group(data,["val_w_tr","q","t"])
        return data

    # MOsbo constraint based on CtlModelKind being direct-with-enchanced-security or sbo-with-enhanced-security
    @model_validator(mode='before')
    @classmethod
    def mo_sbo_before_validator(cls,data):
        prescond.mo_sbo(data,"ctl_model",["st_seld","sbo_timeout"])
        return data

    # MBenhanced constraint
    @model_validator(mode='before')
    @classmethod
    def mo_enhanced_before_validator(cls,data):
        prescond.mo_enhanced(data,"ctl_model",["oper_timeout"])
        return data

    # Add sub_val checker
    @model_validator(mode='before')
    @classmethod
    def mf_subst_before_validator(cls,data):
        prescond.mf_subst(data,True,["sub_ena","sub_val","sub_q","sub_id"])
        return data

# IEC 61850-7-3 7.5.9
class APC(ControlTestingCDC):
    cdc_name:     VisString255                = Field(default = 'APC',
                                                      pattern = 'APC',
                                                      serialization_alias = 'cdcName')
    origin:       Optional[Originator]        = Field(default_factory = Originator,
                                                      serialization_alias = "origin")
    ctl_num:      Optional[INT8U]             = Field(default = 0,
                                                      serialization_alias = "ctlNum")
    mx_val:       Optional[AnalogueValue]     = Field(default_factory = AnalogueValue,
                                                      serialization_alias = "mxVal")
    q:            Optional[Quality]           = Field(default_factory = Quality,
                                                      serialization_alias = "q")
    t:            Optional[Timestamp]         = Field(default_factory = Timestamp,
                                                      serialization_alias = "t")
    st_seld:      Optional[BOOLEAN]           = Field(default = False,
                                                      serialization_alias = "stSeld")
    sub_val:      Optional[AnalogueValue]     = Field(default_factory = AnalogueValue,
                                                      serialization_alias = "subVal")
    ctl_model:    CtlModelKind                = Field(default = CtlModelKind.direct_with_normal_security,
                                                      serialization_alias = "ctlModel")
    sbo_timeout:  Optional[INT32U]            = Field(default = 0,
                                                      serialization_alias = "sboTimeout")
    sbo_class:    Optional[SboClassKind]      = Field(default = SboClassKind.operate_once,
                                                      serialization_alias = "sboClass")
    units:        Optional[Unit]              = Field(default_factory = Unit,
                                                      serialization_alias = "units")
    db:           Optional[INT32U]            = Field(default = 0,
                                                      serialization_alias = "db")
    svc:          Optional[ScaledValueConfig] = Field(default_factory = ScaledValueConfig,
                                                      serialization_alias = "sVC")
    min_val:      Optional[AnalogueValue]     = Field(default_factory = AnalogueValue,
                                                      serialization_alias = "minVal")
    max_val:      Optional[AnalogueValue]     = Field(default_factory = AnalogueValue,
                                                      serialization_alias = "maxVal")
    step_size:    Optional[AnalogueValue]     = Field(default_factory = AnalogueValue,
                                                      serialization_alias = "stepSize")
    oper_timeout: Optional[INT32U]            = Field(default = 0,
                                                      serialization_alias = "operTimeout")
    db_ref:       FLOAT32                     = Field(default = 0.0,
                                                      serialization_alias = "operTimeout")
    ctl_val:      AnalogueValueCtl            = Field(default_factory = AnalogueValueCtl,
                                                      serialization_alias = "ctlVal")

    # st_val, q, and t must be used as a set.
    @model_validator(mode='before')
    @classmethod
    def m_all_or_none_per_group_before_validator(cls,data):
        prescond.m_all_or_none_per_group(data,["mx_val","q","t"])
        return data

    # MOsbo constraint based on CtlModelKind being direct-with-enchanced-security or sbo-with-enhanced-security
    @model_validator(mode='before')
    @classmethod
    def mo_sbo_before_validator(cls,data):
        prescond.mo_sbo(data,"ctl_model",["st_seld","sbo_timeout"])
        return data

    # MBenhanced constraint
    @model_validator(mode='before')
    @classmethod
    def mo_enhanced_before_validator(cls,data):
        prescond.mo_enhanced(data,"ctl_model",["oper_timeout"])
        return data

    # Add sub_val checker
    @model_validator(mode='before')
    @classmethod
    def mf_subst_before_validator(cls,data):
        prescond.mf_subst(data,True,["sub_ena","sub_val","sub_q","sub_id"])
        return data

    # ScaledValueConfig must appear if Analogue.i elements are used per the
    # standard.
    @model_validator(mode='before')
    @classmethod
    def mf_scaled_av(cls, data: Any) -> Any:
        prescond.mf_scaled_av(data,
                              svc_var    = "svc",
                              param_list = ["mx_val","sub_val","min_val","max_val","step_size","ctl_val"])
        return data

# IEC 61850-7-3 7.5.10
class BAC(ControlTestingCDC):
    cdc_name:     VisString255                = Field(default = 'BAC',
                                                      pattern = 'BAC',
                                                      serialization_alias = 'cdcName')
    origin:       Optional[Originator]        = Field(default_factory = Originator,
                                                      serialization_alias = "origin")
    ctl_num:      Optional[INT8U]             = Field(default = 0,
                                                      serialization_alias = "ctlNum")
    mx_val:       Optional[AnalogueValue]     = Field(default_factory = AnalogueValue,
                                                      serialization_alias = "mxVal")
    q:            Optional[Quality]           = Field(default_factory = Quality,
                                                      serialization_alias = "q")
    t:            Optional[Timestamp]         = Field(default_factory = Timestamp,
                                                      serialization_alias = "t")
    st_seld:      Optional[BOOLEAN]           = Field(default = False,
                                                      serialization_alias = "stSeld")
    sub_val:      Optional[AnalogueValue]     = Field(default_factory = AnalogueValue,
                                                      serialization_alias = "subVal")
    persistent:   BOOLEAN                     = Field(default = False,
                                                      serialization_alias = "persistent")
    ctl_model:    CtlModelKind                = Field(default = CtlModelKind.direct_with_normal_security,
                                                      serialization_alias = "ctlModel")
    sbo_timeout:  Optional[INT32U]            = Field(default = 0,
                                                      serialization_alias = "sboTimeout")
    sbo_class:    Optional[SboClassKind]      = Field(default = SboClassKind.operate_once,
                                                      serialization_alias = "sboClass")
    units:        Optional[Unit]              = Field(default_factory = Unit,
                                                      serialization_alias = "units")
    db:           Optional[INT32U]            = Field(default = 0,
                                                      serialization_alias = "db")
    svc:          Optional[ScaledValueConfig] = Field(default_factory = ScaledValueConfig,
                                                      serialization_alias = "sVC")
    min_val:      Optional[AnalogueValue]     = Field(default_factory = AnalogueValue,
                                                      serialization_alias = "minVal")
    max_val:      Optional[AnalogueValue]     = Field(default_factory = AnalogueValue,
                                                      serialization_alias = "maxVal")
    step_size:    Optional[AnalogueValue]     = Field(default_factory = AnalogueValue,
                                                      serialization_alias = "stepSize")
    oper_timeout: Optional[INT32U]            = Field(default = 0,
                                                      serialization_alias = "operTimeout")
    db_ref:       FLOAT32                     = Field(default = 0,
                                                      serialization_alias = "dbRef")
    ctl_val:      StepControlKind             = Field(default = StepControlKind.stop,
                                                      serialization_alias = "ctlVal")

    # st_val, q, and t must be used as a set.
    @model_validator(mode='before')
    @classmethod
    def m_all_or_none_per_group_before_validator(cls,data):
        prescond.m_all_or_none_per_group(data,["mx_val","q","t"])
        return data

    # MOsbo constraint based on CtlModelKind being direct-with-enchanced-security or sbo-with-enhanced-security
    @model_validator(mode='before')
    @classmethod
    def mo_sbo_before_validator(cls,data):
        prescond.mo_sbo(data,"ctl_model",["st_seld","sbo_timeout"])
        return data

    # MBenhanced constraint
    @model_validator(mode='before')
    @classmethod
    def mo_enhanced_before_validator(cls,data):
        prescond.mo_enhanced(data,"ctl_model",["oper_timeout"])
        return data

    # Add sub_val checker
    @model_validator(mode='before')
    @classmethod
    def mf_subst_before_validator(cls,data):
        prescond.mf_subst(data,True,["sub_ena","sub_val","sub_q","sub_id"])
        return data

    # ScaledValueConfig must appear if Analogue.i elements are used per the
    # standard.
    @model_validator(mode='before')
    @classmethod
    def mf_scaled_av(cls, data: Any) -> Any:
        prescond.mf_scaled_av(data,
                              svc_var    = "svc",
                              param_list = ["mx_val","sub_val","min_val","max_val","step_size"])
        return data

