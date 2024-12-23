# py_iec61850_cdc logical_nodes.py
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

# This file provides a selection of logical node classes from
# IEC 61850-7-4:2010+AMD1:2020 CSV as Python classes.

from __future__ import annotations
from typing import Optional, Any

from abc import ABC

from pydantic import BaseModel

from py_iec61850_cdc.abstracts import (
    ENG,
    ING,
    SPG,
)
from py_iec61850_cdc.controls import (
    ENC,
    INC,
    SPC,
)

#from py_iec61850_cdc.basetypes import (
#)
from py_iec61850_cdc.enums import (
    BehaviourModeKind,
)
from py_iec61850_cdc.description import (
    DPL,
    LPL,
)
from py_iec61850_cdc.settings import (
    ORG,
)
from py_iec61850_cdc.status import (
    ENS,
    INS,
    SPS,
)

# Everything is set to optional for now.
# The non-derived vs derived statistics contexts, and how to set this
# are kinda messing things up.

class DomainLN(BaseModel, ABC, validate_assignment=True):
    nam_plt: Optional[LPL]
    beh:     Optional[ENS[BehaviourModeKind]]
    health:  Optional[ENS[HealthKind]]
    mir:     Optional[SPS]
    mod:     Optional[ENC[BehaviourModeKind]]
    in_ref:  Optional[ORG]

class StatisticsLN(DomainLN, ABC):
    clc_exp:       Optional[SPS]
    clc_nxt_tmms:  Optional[INS]
    clc_str:       Optional[SPC]
    clc_mth:       Optional[ENG[CalcMethodKind]]
    clc_mod:       Optional[ENG[CalcModeKind]]
    clc_intv_type: Optional[ENG[CalcIntervalKind]]
    clc_intv_per:  Optional[ING]
    num_sub_intv:  Optional[ING]
    clc_rf_typ:    Optional[ENG[CalcIntervalKind]]
    clc_rf_per:    Optional[ING]
    clc_src:       Optional[ORG]
    in_syn:        Optional[ORG]

class FunctionLN(StatisticsLN, ABC):
    blk:     Optional[SPS]
    blk_ref: Optional[ORG]

class ControllingLN(FunctionLN, ABC):
    loc:     Optional[SPS]
    loc_key: Optional[SPS]
    loc_sta: Optional[SPC]

class ControlledLN(ControllingLN, ABC):
    cmb_blk:   Optional[SPC]
    op_cnt_rs: Optional[INC]

class ControlEquipmentInterfaceLN(ControlledLN, ABC):
    e_e_name:   Optional[DPL]
    e_e_health: Optional[ENS[HealthKind]]
    op_tmh:     Optional[INS]

class GGIO(ControlEquipmentInterfaceLN):
    int_in:  Optional[INS]
    alm:     Optional[list[SPS]]
    wrn:     Optional[list[SPS]]
    ind:     Optional[list[SPS]]
    cnt_val: Optional[list[BCR]]
    an_in:   Optional[list[MV]]
    an_out:  Optional[list[APC]]
    spcso:   Optional[list[SPC]]
    dpcso:   Optional[list[DPC]]
    iscso:   Optional[list[INC]]

class LPHD(BaseModel, validate_assignment=True):
    nam_plt:     Optional[LPL]
    phy_nam:     Optional[DPL]
    phy_health:  Optional[ENS[HealthKind]]
    out_ov:      Optional[SPS]
    proxy:       Optional[SPS]
    in_ov:       Optional[SPS]
    op_tmh:      Optional[INS]
    num_pwr_up:  Optional[INS]
    wrm_str:     Optional[INS]
    wac_trg:     Optional[INS]
    pwr_up:      Optional[SPS]
    pwr_dn:      Optional[SPS]
    pwr_sup_alm: Optional[SPS]
    rs_stat:     Optional[SPC]
    sim:         Optional[SPC]
    max_dl:      Optional[ING]

class LLN0(BaseModel, validate_assignment=True):
    nam_plt:    Optional[LPL]
    beh:        Optional[ENS[BehaviourModeKind]]
    health:     Optional[ENS[HealthKind]]
    loc_key:    Optional[SPS]
    loc:        Optional[SPS]
    mod:        Optional[ENC[BehaviourModeKind]]
    loc_sta:    Optional[SPC]
    diag:       Optional[SPC]
    led_rs:     Optional[SPC]
    sw_mod_key: Optional[SPC]
    in_ref:     Optional[ORG]
    gr_ref:     Optional[ORG]
    mlt_lev:    Optional[SPG]

