# py_iec61850_cdc utils.py
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

# This file provides a selection of utility functions for dealing with the
# IEC 61850 types presented in this standard.

from __future__ import annotations

import json

from py_iec61850_cdc.controls import (
    APC,
    BAC,
    BSC,
    DPC,
    INC,
    ISC,
    SPC,
)
from py_iec61850_cdc.description import (
    CSD,
    DPL,
    LPL,
    VSD,
)
from py_iec61850_cdc.measurand import (
    CMV,
    DEL,
    HDEL,
    HMV,
    HWYE,
    MV,
    SAV,
    SEQ,
    WYE,
)
from py_iec61850_cdc.service import (
    BTS,
    CST,
    CTS,
    GTS,
    LTS,
    MTS,
    NTS,
    STS,
    UTS,
)
from py_iec61850_cdc.settings import (
    ASG_SE,
    ASG_SG,
    ASG_SP,
    CSG_SE,
    CSG_SG,
    CSG_SP,
    CURVE_SE,
    CURVE_SG,
    CURVE_SP,
    ENG_SE,
    ENG_SG,
    ENG_SP,
    ING_SE,
    ING_SG,
    ING_SP,
    SPG_SE,
    SPG_SG,
    SPG_SP,
    VSG_SE,
    VSG_SG,
    VSG_SP,
)

#from pydantic import Field
#from py_iec61850_cdc.basetypes import (
#)
#from py_iec61850_cdc.enums import (
#)
from py_iec61850_cdc.status import (
    ACD,
    ACT,
    BCR,
    DPS,
    ENS,
    HST,
    INS,
    ORS,
    SEC,
    SPS,
    TCS,
    VSS,
)


def factory_json(json_string: str | bytes | bytearray) -> BasePrimitiveCDC | BaseComposedCDC:
    imported = json.loads(json_string)
    if 'cdcName' in imported:
        if imported['cdcName'] == 'SPS': return SPS.model_validate_json(json_string)
        elif imported['cdcName'] == 'DPS': return DPS.model_validate_json(json_string)
        elif imported['cdcName'] == 'INS': return INS.model_validate_json(json_string)
        elif imported['cdcName'] == 'ENS': return ENS.model_validate_json(json_string)
        elif imported['cdcName'] == 'ACT': return ACT.model_validate_json(json_string)
        elif imported['cdcName'] == 'ACD': return ACD.model_validate_json(json_string)
        elif imported['cdcName'] == 'SEC': return SEC.model_validate_json(json_string)
        elif imported['cdcName'] == 'BCR': return BCR.model_validate_json(json_string)
        elif imported['cdcName'] == 'HST': return HST.model_validate_json(json_string)
        elif imported['cdcName'] == 'VSS': return VSS.model_validate_json(json_string)
        elif imported['cdcName'] == 'ORS': return ORS.model_validate_json(json_string)
        elif imported['cdcName'] == 'TCS': return TCS.model_validate_json(json_string)
        elif imported['cdcName'] == 'CTS': return CTS.model_validate_json(json_string)
        elif imported['cdcName'] == 'STS': return STS.model_validate_json(json_string)
        elif imported['cdcName'] == 'NTS': return NTS.model_validate_json(json_string)
        elif imported['cdcName'] == 'MTS': return MTS.model_validate_json(json_string)
        elif imported['cdcName'] == 'GTS': return GTS.model_validate_json(json_string)
        elif imported['cdcName'] == 'LTS': return LTS.model_validate_json(json_string)
        elif imported['cdcName'] == 'UTS': return UTS.model_validate_json(json_string)
        elif imported['cdcName'] == 'BTS': return BTS.model_validate_json(json_string)
        elif imported['cdcName'] == 'CST': return CST.model_validate_json(json_string)
        elif imported['cdcName'] == 'ASG_SP': return ASG_SP.model_validate_json(json_string)
        elif imported['cdcName'] == 'ASG_SG': return ASG_SG.model_validate_json(json_string)
        elif imported['cdcName'] == 'ASG_SE': return ASG_SE.model_validate_json(json_string)
        elif imported['cdcName'] == 'CSG_SP': return CSG_SP.model_validate_json(json_string)
        elif imported['cdcName'] == 'CSG_SG': return CSG_SG.model_validate_json(json_string)
        elif imported['cdcName'] == 'CSG_SE': return CSG_SE.model_validate_json(json_string)
        elif imported['cdcName'] == 'CURVE_SP': return CURVE_SP.model_validate_json(json_string)
        elif imported['cdcName'] == 'CURVE_SG': return CURVE_SG.model_validate_json(json_string)
        elif imported['cdcName'] == 'CURVE_SE': return CURVE_SE.model_validate_json(json_string)
        elif imported['cdcName'] == 'ENG_SP': return ENG_SP.model_validate_json(json_string)
        elif imported['cdcName'] == 'ENG_SG': return ENG_SG.model_validate_json(json_string)
        elif imported['cdcName'] == 'ENG_SE': return ENG_SE.model_validate_json(json_string)
        elif imported['cdcName'] == 'ING_SP': return ING_SP.model_validate_json(json_string)
        elif imported['cdcName'] == 'ING_SG': return ING_SG.model_validate_json(json_string)
        elif imported['cdcName'] == 'ING_SE': return ING_SE.model_validate_json(json_string)
        elif imported['cdcName'] == 'SPG_SP': return SPG_SP.model_validate_json(json_string)
        elif imported['cdcName'] == 'SPG_SG': return SPG_SG.model_validate_json(json_string)
        elif imported['cdcName'] == 'SPG_SE': return SPG_SE.model_validate_json(json_string)
        elif imported['cdcName'] == 'VSG_SP': return VSG_SP.model_validate_json(json_string)
        elif imported['cdcName'] == 'VSG_SG': return VSG_SG.model_validate_json(json_string)
        elif imported['cdcName'] == 'VSG_SE': return VSG_SE.model_validate_json(json_string)
        elif imported['cdcName'] == 'DPL': return DPL.model_validate_json(json_string)
        elif imported['cdcName'] == 'LPL': return LPL.model_validate_json(json_string)
        elif imported['cdcName'] == 'CSD': return CSD.model_validate_json(json_string)
        elif imported['cdcName'] == 'VSD': return VSD.model_validate_json(json_string)
        elif imported['cdcName'] == 'SPC': return SPC.model_validate_json(json_string)
        elif imported['cdcName'] == 'DPC': return DPC.model_validate_json(json_string)
        elif imported['cdcName'] == 'INC': return INC.model_validate_json(json_string)
        elif imported['cdcName'] == 'BSC': return BSC.model_validate_json(json_string)
        elif imported['cdcName'] == 'ISC': return ISC.model_validate_json(json_string)
        elif imported['cdcName'] == 'APC': return APC.model_validate_json(json_string)
        elif imported['cdcName'] == 'BAC': return BAC.model_validate_json(json_string)
        elif imported['cdcName'] == 'MV': return MV.model_validate_json(json_string)
        elif imported['cdcName'] == 'CMV': return CMV.model_validate_json(json_string)
        elif imported['cdcName'] == 'SAV': return SAV.model_validate_json(json_string)
        elif imported['cdcName'] == 'WYE': return WYE.model_validate_json(json_string)
        elif imported['cdcName'] == 'DEL': return DEL.model_validate_json(json_string)
        elif imported['cdcName'] == 'SEQ': return SEQ.model_validate_json(json_string)
        elif imported['cdcName'] == 'HMV': return HMV.model_validate_json(json_string)
        elif imported['cdcName'] == 'HWYE': return HWYE.model_validate_json(json_string)
        elif imported['cdcName'] == 'HDEL': return HDEL.model_validate_json(json_string)
        else:
            raise ValueError("cdcName does not match a class in this library!")
    else:
        raise ValueError("Object does not contain cdcName!  Cannot determine the appropriate type!")

