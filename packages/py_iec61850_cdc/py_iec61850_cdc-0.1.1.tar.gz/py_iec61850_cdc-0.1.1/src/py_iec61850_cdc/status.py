# py_iec61850_cdc status.py
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

# This file provides the binary object datatypes described in
# IEC 61850-7-2:2010+AMD1:2020 CSV and IEC 61850-7-3:2010+AMD1:2020 CSV
# as (e.g. BOOLEAN-based classes).

from __future__ import annotations

from typing import Any, Optional, Generic

from pydantic import Field, model_validator

from py_iec61850_cdc import prescond
from py_iec61850_cdc.abstracts import BasePrimitiveCDC, SubstitutionCDC
from py_iec61850_cdc.attributes import Cell, Originator, Quality, Timestamp, Unit
from py_iec61850_cdc.basetypes import (
    BOOLEAN,
    FLOAT32,
    INT16U,
    INT32,
    INT32U,
    INT64,
    ObjectReference,
    Octet64,
    Unicode255,
    VisString64,
    VisString255,
)
from py_iec61850_cdc.enums import DpStatusKind, EnumDA, FaultDirectionKind, PhaseFaultDirectionKind, SeverityKind


# IEC 61850-7-3 7.3.2
class SPS(SubstitutionCDC):
    cdc_name: VisString255      = Field(default = 'SPS',
                                        pattern = 'SPS',
                                        serialization_alias = 'cdcName')
    st_val:   BOOLEAN           = Field(default = False,
                                        serialization_alias = "stVal")
    q:        Quality           = Field(default_factory = Quality,
                                        serialization_alias = "q")
    t:        Timestamp         = Field(default_factory = Timestamp,
                                        serialization_alias = "t")
    sub_val:  Optional[BOOLEAN] = Field(default = None,
                                        serialization_alias = "subVal")

# IEC 61850-7-3 7.3.3
class DPS(SubstitutionCDC):
    cdc_name: VisString255           = Field(default = 'DPS',
                                             pattern = 'DPS',
                                             serialization_alias = 'cdcName')
    st_val:   DpStatusKind           = Field(default = DpStatusKind.off,
                                             serialization_alias = "stVal")
    q:        Quality                = Field(default_factory = Quality,
                                             serialization_alias = "q")
    t:        Timestamp              = Field(default_factory = Timestamp,
                                             serialization_alias = "t")
    sub_val:  Optional[DpStatusKind] = Field(default = None,
                                             serialization_alias = "subVal")

# IEC 61850-7-3 7.3.4
class INS(SubstitutionCDC):
    cdc_name: VisString255   = Field(default = 'INS',
                                     pattern = 'INS',
                                     serialization_alias = 'cdcName')
    st_val:  INT32           = Field(default = 0,
                                     serialization_alias = "stVal")
    q:       Quality         = Field(default_factory = Quality,
                                     serialization_alias = "q")
    t:       Timestamp       = Field(default_factory = Timestamp,
                                     serialization_alias = "t")
    sub_val: Optional[INT32] = Field(default = 0,
                                     serialization_alias = "subVal")
    units:   Unit            = Field(default_factory = Unit,
                                     serialization_alias = "units")

# IEC 61850-7-3 7.3.5
class ENS(SubstitutionCDC, Generic[EnumDA]):
    cdc_name: VisString255    = Field(default = 'ENS',
                                      pattern = 'ENS',
                                      serialization_alias = 'cdcName')
    st_val:  EnumDA           = Field(default = 0,
                                      serialization_alias = "stVal")
    q:       Quality          = Field(default_factory = Quality,
                                      serialization_alias = "q")
    t:       Timestamp        = Field(default_factory = Timestamp,
                                      serialization_alias = "t")
    sub_val: Optional[EnumDA] = Field(default = 0,
                                      serialization_alias = "subVal")

# IEC 61850-7-3 7.3.6
class ACT(BasePrimitiveCDC):
    cdc_name:      VisString255         = Field(default = 'ACT',
                                                pattern = 'ACT',
                                                serialization_alias = 'cdcName')
    general:       BOOLEAN              = Field(default = False,
                                                serialization_alias = "general")
    phs_a:         Optional[BOOLEAN]    = Field(default = None,
                                                serialization_alias = "phsA")
    phs_b:         Optional[BOOLEAN]    = Field(default = None,
                                                serialization_alias = "phsB")
    phs_c:         Optional[BOOLEAN]    = Field(default = None,
                                                serialization_alias = "phsC")
    neut:          Optional[BOOLEAN]    = Field(default = None,
                                                serialization_alias = "neut")
    q:             Quality              = Field(default_factory = Quality,
                                                serialization_alias = "q")
    t:             Timestamp            = Field(default_factory = Timestamp,
                                                serialization_alias = "t")
    origin_src:    Optional[Originator] = Field(default = None,
                                                serialization_alias = "originSrc")
    oper_tm_phs_a: Optional[Timestamp]  = Field(default = None,
                                                serialization_alias = "operTmPhsA")
    oper_tm_phs_b: Optional[Timestamp]  = Field(default = None,
                                                serialization_alias = "operTmPhsB")
    oper_tm_phs_c: Optional[Timestamp]  = Field(default = None,
                                                serialization_alias = "operTmPhsC")

# IEC 61850-7-3 7.3.7
class ACD(BasePrimitiveCDC):
    cdc_name:    VisString255                      = Field(default = 'ACD',
                                                           pattern = 'ACD',
                                                           serialization_alias = 'cdcName')
    general:     BOOLEAN                           = Field(default = False,
                                                           serialization_alias = "general")
    dir_general: FaultDirectionKind                = Field(default = FaultDirectionKind.unknown,
                                                           serialization_alias = "dirGeneral")
    phs_a:       Optional[BOOLEAN]                 = Field(default = None,
                                                           serialization_alias = "phsA")
    dir_phs_a:   Optional[PhaseFaultDirectionKind] = Field(default = None,
                                                           serialization_alias = "dirPhsA")
    phs_b:       Optional[BOOLEAN]                 = Field(default = None,
                                                           serialization_alias = "phsB")
    dir_phs_b:   Optional[PhaseFaultDirectionKind] = Field(default = None,
                                                           serialization_alias = "dirPhsB")
    phs_c:       Optional[BOOLEAN]                 = Field(default = None,
                                                           serialization_alias = "phsC")
    dir_phs_c:   Optional[PhaseFaultDirectionKind] = Field(default = None,
                                                           serialization_alias = "dirPhsC")
    neut:        Optional[BOOLEAN]                 = Field(default = None,
                                                           serialization_alias = "neut")
    dir_neut:    Optional[PhaseFaultDirectionKind] = Field(default = None,
                                                           serialization_alias = "dirNeut")
    q:           Quality                           = Field(default_factory = Quality,
                                                           serialization_alias = "q")
    t:           Timestamp                         = Field(default_factory = Timestamp,
                                                           serialization_alias = "t")

    @model_validator(mode='before')
    @classmethod
    def m_all_or_none_per_group_before_validator(cls, data:Any) -> Any:
        if isinstance(data,dict):
            prescond.m_all_or_none_per_group(data,["phs_a","dir_phs_a"])
            prescond.m_all_or_none_per_group(data,["phs_b","dir_phs_b"])
            prescond.m_all_or_none_per_group(data,["phs_c","dir_phs_c"])
            prescond.m_all_or_none_per_group(data,["neut" ,"dir_neut" ])
        return data

# IEC 61850-7-3 7.3.8
class SEC(BasePrimitiveCDC):
    cdc_name: VisString255          = Field(default = 'SEC',
                                            pattern = 'SEC',
                                            serialization_alias = 'cdcName')
    cnt:      INT32U                = Field(default = 0,
                                            serialization_alias = "cnt")
    sev:      SeverityKind          = Field(default = SeverityKind.unknown,
                                            serialization_alias = "sev")
    t:        Timestamp             = Field(default_factory = Timestamp,
                                            serialization_alias = "t")
    addr:     Optional[Octet64]     = Field(default = None,
                                            serialization_alias = "addr")
    add_info: Optional[VisString64] = Field(default = None,
                                            serialization_alias = "addInfo")

# IEC 61850-7-3 7.3.9
class BCR(BasePrimitiveCDC):
    cdc_name:    VisString255     = Field(default = 'BCR',
                                          pattern = 'BCR',
                                          serialization_alias = 'cdcName')
    act_val:  Optional[INT64]     = Field(default = 0,
                                          serialization_alias = "actVal")
    fr_val:   Optional[INT64]     = Field(default = None,
                                          serialization_alias = "frVal")
    fr_tm:    Optional[Timestamp] = Field(default = None,
                                          serialization_alias = "frTm")
    q:        Quality             = Field(default_factory = Quality,
                                          serialization_alias = "q")
    t:        Optional[Timestamp] = Field(default_factory = Timestamp,
                                          serialization_alias = "t")
    units:    Optional[Unit]      = Field(default = None,
                                          serialization_alias = "units")
    puls_qty: FLOAT32             = Field(default = 0.0,
                                          serialization_alias = "pulsQty")
    fr_ena:   Optional[BOOLEAN]   = Field(default = None,
                                          serialization_alias = "frEna")
    str_tm:   Optional[Timestamp] = Field(default = None,
                                          serialization_alias = "strTm")
    fr_pd:    Optional[INT32]     = Field(default = None,
                                          serialization_alias = "frPd")
    fr_rs:    Optional[BOOLEAN]   = Field(default = None,
                                          serialization_alias = "frRs")

    @model_validator(mode='before')
    @classmethod
    def all_at_least_one_group(cls, data: Any) -> Any:
        prescond.all_at_least_one_group(data,
                                        groups = [["fr_val","fr_tm","fr_ena","fr_pd","fr_rs"],
                                                  ["act_val","t"]]
                                        )
        return data
    '''
    def actVal_t_pair_before_validator(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # One pair of actVal / t or frX points must appear as
            # per the standard.  So if we don't have one pair or
            # the other group... the data is not OK.
            if (not ('actVal' in data and 't'    in data) or
                not ('frVal'  in data and 'frTm' in data and
                     'frEna'  in data and 'frPd' in data and
                     'frRs'   in data)):
                raise ValueError("phs_a and dir_phs_a must be used together!")
        return data
    '''

# IEC 61850-7-3 7.3.10
class HST(BasePrimitiveCDC):
    cdc_name:    VisString255          = Field(default = 'HST',
                                               pattern = 'HST',
                                               serialization_alias = 'cdcName')
    hst_val:    list[INT32]            = None # Probably needs field for the serialization_alias...
    q:          Quality                = Field(default_factory = Quality,
                                               serialization_alias = "q")
    t:          Timestamp              = Field(default_factory = Timestamp,
                                               serialization_alias = "t")
    num_pts:    INT16U                 = Field(default = 0,
                                               serialization_alias = "numPts")
    hst_rangec: list[Cell]             = None # Probably needs field for the serialization_alias...
    x_units:    Unit                   = Field(default_factory = Unit,
                                               serialization_alias = "xUnits")
    y_Units:    Optional[Unit]         = Field(default_factory = Unit,
                                               serialization_alias = "yUnits")
    units:      Optional[Unit]         = Field(default_factory = Unit,
                                               serialization_alias = "units")
    max_pts:    INT16U                 = Field(default = 0,
                                               serialization_alias = "maxPts")
    xd:         VisString255           = Field(default = "",
                                               serialization_alias = "xD")
    xdu:        Optional[Unicode255]   = Field(default = "",
                                               serialization_alias = "xDU")
    yd:         Optional[VisString255] = Field(default = "",
                                               serialization_alias = "yD")
    ydu:        Optional[Unicode255]   = Field(default = "",
                                               serialization_alias = "yDU")

# IEC 61850-7-3 7.3.11
class VSS(BasePrimitiveCDC):
    cdc_name: VisString255 = Field(default = 'VSS',
                                   pattern = 'VSS',
                                   serialization_alias = 'cdcName')
    st_val:   VisString255 = Field(default = "",
                                   serialization_alias = "stVal")
    q:        Quality      = Field(default_factory = Quality,
                                   serialization_alias = "q")
    t:        Timestamp    = Field(default_factory = Timestamp,
                                   serialization_alias = "t")

# IEC 61850-7-3 7.3.12
class ORS(BasePrimitiveCDC):
    cdc_name: VisString255  = Field(default = 'ORS',
                                    pattern = 'ORS',
                                    serialization_alias = 'cdcName')
    st_val: ObjectReference = Field(default = "",
                                    serialization_alias = "stVal")
    q:      Quality         = Field(default_factory = Quality,
                                    serialization_alias = "q")
    t:      Timestamp       = Field(default_factory = Timestamp,
                                    serialization_alias = "t")

# IEC 61850-7-3 7.3.13
class TCS(BasePrimitiveCDC):
    cdc_name: VisString255 = Field(default = 'TCS',
                                   pattern = 'TCS',
                                   serialization_alias = 'cdcName')
    st_val:   Timestamp    = Field(default_factory = Timestamp,
                                   serialization_alias = "stVal")
    q:        Quality      = Field(default_factory = Quality,
                                   serialization_alias = "q")
    t:        Timestamp    = Field(default_factory = Timestamp,
                                   serialization_alias = "t")

