# py_iec61850_cdc measurand.py
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

from typing import Any, Optional

from pydantic import Field, model_validator

from py_iec61850_cdc import prescond
from py_iec61850_cdc.abstracts import BaseComposedCDC, BasePrimitiveCDC, SubstitutionCDC
from py_iec61850_cdc.attributes import AnalogueValue, Quality, RangeConfig, ScaledValueConfig, Timestamp, Unit, Vector
from py_iec61850_cdc.basetypes import BOOLEAN, FLOAT32, INT32U, VisString255
from py_iec61850_cdc.enums import PhaseAngleReferenceKind, PhaseReferenceKind, RangeKind, SequenceKind

# IEC 61850-7-3 7.4.3
class MV(SubstitutionCDC):
    cdc_name:    VisString255                = Field(default = 'MV',
                                                     pattern = 'MV',
                                                     serialization_alias = 'cdcName')
    inst_mag:    Optional[AnalogueValue]     = Field(default = None,
                                                     serialization_alias = "instMag")
    mag:         AnalogueValue               = Field(default_factory = AnalogueValue,
                                                     serialization_alias = "mag")
    # 'range' from the standard is renamed to 'range_v' (range value) due to 'range'
    # being a protected word in Python.
    range_v:     Optional[RangeKind]         = Field(default = None,
                                                     serialization_alias = "range")
    q:           Quality                     = Field(default_factory = Quality,
                                                     serialization_alias = "q")
    t:           Timestamp                   = Field(default_factory = Timestamp,
                                                     serialization_alias = "t")
    sub_mag:     Optional[AnalogueValue]     = Field(default = None,
                                                     serialization_alias = "subMag")
    units:       Optional[Unit]              = Field(default = None,
                                                     serialization_alias = "units")
    db:          Optional[INT32U]            = Field(default = None,
                                                     serialization_alias = "db")
    zero_db:     Optional[INT32U]            = Field(default = None,
                                                     serialization_alias = "zeroDb")
    svc:         Optional[ScaledValueConfig] = Field(default = None,
                                                     serialization_alias = "sVC")
    range_c:     Optional[RangeConfig]       = Field(default = None,
                                                     serialization_alias = "rangeC")
    smp_rate:    Optional[INT32U]            = Field(default = None,
                                                     serialization_alias = "smpRate")
    db_ref:      Optional[FLOAT32]           = Field(default = None,
                                                     serialization_alias = "dbRef")
    zero_db_ref: Optional[FLOAT32]           = Field(default = None,
                                                     serialization_alias = "zeroDbRef")

    # range_v / range_c, zero_db / zero_db_ref, and db / db_ref
    # must be used in pairs per IEC.
    @model_validator(mode='before')
    @classmethod
    def mo_sibling_before_validator(cls, data: Any) -> Any:
        prescond.mo_sibling(data,"range_v",["range_c"])
        prescond.mo_sibling(data,"db",["db_ref"])
        prescond.mo_sibling(data,"zero_db",["zero_db_ref"])

    # ScaledValueConfig must appear if Analogue.i elements are used per the
    # standard.
    @model_validator(mode='before')
    @classmethod
    def mf_scaled_av(cls, data: Any) -> Any:
        prescond.mf_scaled_av(data,
                              svc_var    = "svc",
                              param_list = ["inst_mag","mag","sub_mag"])
        return data

    # Add sub_val checker
    @model_validator(mode='before')
    @classmethod
    def mf_subst_before_validator(cls,data):
        prescond.mf_subst(data,True,["sub_ena","sub_mag","sub_q","sub_id"])
        return data

    # Updates inst_mag from process value.
    def inst_mag_from_process_value(self, value: float | int) -> None:
        pass

    # Returns process value as float and int from inst_mag.
    def inst_mag_to_process_value(self) -> float | int:
        pass

    # Updates mag, q, and others based on inst_mag, range_c, db, and zero_db if configured.
    def update(self) -> None:
        pass

# IEC 61850-7-3 7.4.4
class CMV(SubstitutionCDC):
    cdc_name:    VisString255                      = Field(default = 'CMV',
                                                           pattern = 'CMV',
                                                           serialization_alias = 'cdcName')
    inst_c_val:  Optional[Vector]                  = Field(default = None,
                                                           serialization_alias = "instCVal")
    c_val:       Vector                            = Field(default_factory = Vector,
                                                           serialization_alias = "cVal")
    # 'range' is renamed to 'range_v' to avoid name conflict with Python.
    range_v:     Optional[RangeKind]               = Field(default = None,
                                                           serialization_alias = "range")
    range_ang:   Optional[RangeKind]               = Field(default = None,
                                                           serialization_alias = "rangeAng")
    q:           Quality                           = Field(default_factory = Quality,
                                                           serialization_alias = "q")
    t:           Timestamp                         = Field(default_factory = Timestamp,
                                                           serialization_alias = "t")
    sub_c_val:   Optional[Vector]                  = Field(default = None,
                                                           serialization_alias = "subCVal")
    units:       Optional[Unit]                    = Field(default = None,
                                                           serialization_alias = "units")
    db:          Optional[INT32U]                  = Field(default = None,
                                                           serialization_alias = "db")
    db_ang:      Optional[INT32U]                  = Field(default = None,
                                                           serialization_alias = "dbAng")
    zero_db:     Optional[INT32U]                  = Field(default = None,
                                                           serialization_alias = "zeroDb")
    range_c:     Optional[RangeConfig]             = Field(default = None,
                                                           serialization_alias = "rangeC")
    range_ang_c: Optional[RangeConfig]             = Field(default = None,
                                                           serialization_alias = "rangeAngC")
    mag_svc:     Optional[ScaledValueConfig]       = Field(default = None,
                                                           serialization_alias = "magSVC")
    ang_svc:     Optional[ScaledValueConfig]       = Field(default = None,
                                                           serialization_alias = "angSVC")
    ang_ref:     Optional[PhaseAngleReferenceKind] = Field(default = None,
                                                           serialization_alias = "angRef")
    smp_rate:    Optional[INT32U]                  = Field(default = None,
                                                           serialization_alias = "smpRate")
    db_ref:      Optional[FLOAT32]                 = Field(default = None,
                                                           serialization_alias = "dbRef")
    zero_db_ref: Optional[FLOAT32]                 = Field(default = None,
                                                           serialization_alias = "zeroDbRef")
    db_ang_ref:  Optional[FLOAT32]                 = Field(default = None,
                                                           serialization_alias = "dbAngRef")

    # range_v / range_c, zero_db / zero_db_ref, and db / db_ref
    # must be used in pairs per IEC.
    @model_validator(mode='before')
    @classmethod
    def mo_sibling_before_validator(cls, data: Any) -> Any:
        prescond.mo_sibling(data,"range_v",["range_c"])
        prescond.mo_sibling(data,"range_ang",["range_ang_c"])
        prescond.mo_sibling(data,"db",["db_ref"])
        prescond.mo_sibling(data,"zero_db",["zero_db_ref"])
        return data

    # ScaledValueConfig must appear if Analogue.i elements are used per the
    # standard.
    @model_validator(mode='before')
    @classmethod
    def mf_scaled_x_v(cls, data: Any) -> Any:
        prescond.mf_scaled_x_v(data,
                               svc_var="mag_svc",
                               mag_or_ang="mag",
                               param_list=["inst_c_val","c_val","sub_c_val"])
        prescond.mf_scaled_x_v(data,
                               svc_var="ang_svc",
                               mag_or_ang="ang",
                               param_list=["inst_c_val","c_val","sub_c_val"])
        return data

    # Add sub_val checker
    @model_validator(mode='before')
    @classmethod
    def mf_subst_before_validator(cls,data):
        prescond.mf_subst(data,True,["sub_ena","sub_c_val","sub_q","sub_id"])
        return data

# IEC 61850-7-3 7.4.5
class SAV(BasePrimitiveCDC):
    cdc_name: VisString255                = Field(default = 'SAV',
                                                  pattern = 'SAV',
                                                  serialization_alias = 'cdcName')
    inst_mag: AnalogueValue               = Field(default_factory = AnalogueValue,
                                                  serialization_alias = "instMag")
    q:        Quality                     = Field(default_factory = Quality,
                                                  serialization_alias = "q")
    t:        Optional[Timestamp]         = Field(default = None,
                                                  serialization_alias = "t")
    units:    Optional[Unit]              = Field(default = None,
                                                  serialization_alias = "units")
    svc:      Optional[ScaledValueConfig] = Field(default = None,
                                                  serialization_alias = "sVC")
    minimum:  Optional[AnalogueValue]     = Field(default = None,
                                                  serialization_alias = "min")
    maximum:  Optional[AnalogueValue]     = Field(default = None,
                                                  serialization_alias = "max")


    # ScaledValueConfig must appear if Analogue.i elements are used per the
    # standard.
    @model_validator(mode='before')
    @classmethod
    def mf_scaled_av(cls, data: Any) -> Any:
        prescond.mf_scaled_av(data,
                              svc_var    = "svc",
                              param_list = ["inst_mag"])
        return data

# IEC 61850-7-3 7.4.6
class WYE(BaseComposedCDC):
    cdc_name:    VisString255                      = Field(default = 'WYE',
                                                           pattern = 'WYE',
                                                           serialization_alias = 'cdcName')
    phs_a:       Optional[CMV]                     = Field(default = None,
                                                           serialization_alias = "phsA")
    phs_b:       Optional[CMV]                     = Field(default = None,
                                                           serialization_alias = "phsB")
    phs_c:       Optional[CMV]                     = Field(default = None,
                                                           serialization_alias = "phsC")
    neut:        Optional[CMV]                     = Field(default = None,
                                                           serialization_alias = "neut")
    net:         Optional[CMV]                     = Field(default = None,
                                                           serialization_alias = "net")
    res:         Optional[CMV]                     = Field(default = None,
                                                           serialization_alias = "res")
    ang_ref:     Optional[PhaseAngleReferenceKind] = Field(default = None,
                                                           serialization_alias = "angRef")
    phs_to_neut: Optional[BOOLEAN]                 = Field(default = None,
                                                           serialization_alias = "phsToNeut")

    # At least one of the CMV options must exist.
    @model_validator(mode='before')
    @classmethod
    def at_least_one_before_validator(cls, data: Any) -> Any:
        prescond.at_least_one(data,["phs_a","phs_b","phs_c","neut","net","res"])
        return data    # At least one of the CMV options must exist.

# IEC 61850-7-3 7.4.7
class DEL(BaseComposedCDC):
    cdc_name: VisString255                         = Field(default = 'DEL',
                                                           pattern = 'DEL',
                                                           serialization_alias = 'cdcName')
    phs_ab:      Optional[CMV]                     = Field(default = None,
                                                           serialization_alias = "phsAB")
    phs_bc:      Optional[CMV]                     = Field(default = None,
                                                           serialization_alias = "phsBC")
    phs_ca:      Optional[CMV]                     = Field(default = None,
                                                           serialization_alias = "phsCA")
    ang_ref:     Optional[PhaseAngleReferenceKind] = Field(default = None,
                                                           serialization_alias = "angRef")

    # At least one of the CMV options must exist.
    @model_validator(mode='before')
    @classmethod
    def at_least_one_before_validator(cls, data: Any) -> Any:
        prescond.at_least_one(data,["phs_ab","phs_bc","phs_ca"])
        return data

# IEC 61850-7-3 7.4.8
class SEQ(BaseComposedCDC):
    cdc_name: VisString255                 = Field(default = 'SEQ',
                                                   pattern = 'SEQ',
                                                   serialization_alias = 'cdcName')
    c1:       CMV                          = Field(default_factory = CMV,
                                                   serialization_alias = "c1")
    c2:       Optional[CMV]                = Field(default = None,
                                                   serialization_alias = "c2")
    c3:       Optional[CMV]                = Field(default = None,
                                                   serialization_alias = "c3")# Zero sequence is 3 for some reason...
    seq_t:    SequenceKind                 = Field(default = SequenceKind.pos_neg_zero,
                                                   serialization_alias = "seqT")
    phs_ref:  Optional[PhaseReferenceKind] = Field(default = None,
                                                   serialization_alias = "phsRef")

    # C2 and C3 must exist of the PhaseReferenceKind is synchrophasor..
    @model_validator(mode='before')
    @classmethod
    def om_syn_ph(cls, data: Any) -> Any:
        prescond.om_syn_ph(data,
                           phs_ref = "phs_ref",
                           param_list = ["c2","c3"])
        return data

