# py_iec61850_cdc abstracts.py
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

# This file provides the abstract base classes described in
# IEC 61850-7-2:2010+AMD1:2020 CSV and IEC 61850-7-3:2010+AMD1:2020 CSV
# as Python ABCs.

from __future__ import annotations

from abc import ABC
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from py_iec61850_cdc import prescond
from py_iec61850_cdc.attributes import AnalogueValue, Quality, ScaledValueConfig, Timestamp, Unit
from py_iec61850_cdc.basetypes import (
    BOOLEAN,
    FLOAT32,
    INT16U,
    INT32,
    INT32U,
    Unicode255,
    VisString64,
    VisString255,
)
from py_iec61850_cdc.enums import HvReferenceKind


# IEC 61850-7-3 7.2.2
class BasePrimitiveCDC(BaseModel, ABC):
    model_config = ConfigDict(validate_assignment = True)
    cdc_name: VisString255 = Field(default = 'BasePrimitiveCDC',
                                   pattern = 'BasePrimitiveCDC',
                                   serialization_alias = 'cdcName')
    d:        Optional[VisString255] = Field(default = None,
                                             serialization_alias = "d")
    du:       Optional[Unicode255]   = Field(default = "",
                                             serialization_alias = "dU")
    data_ns:  Optional[VisString255] = Field(default = "IEC 61850-7-3:2007B",
                                             serialization_alias = "dataNs")

# IEC 61850-7-3 7.2.3
class BaseComposedCDC(BaseModel, ABC, validate_assignment=True):
    model_config = ConfigDict(validate_assignment = True)
    cdc_name: VisString255 = Field(default = 'BaseComposedCDC',
                                   pattern = 'BaseComposedCDC',
                                   serialization_alias = 'cdcName')
    d:        Optional[VisString255] = Field(default = "",
                                             serialization_alias = "d")
    du:       Optional[Unicode255]   = Field(default = "",
                                             serialization_alias = "dU")
    data_ns:  Optional[VisString255] = Field(default = "IEC 61850-7-3:2007B",
                                             serialization_alias = "dataNs")

# IEC 61850-7-3 7.2.4
class SubstitutionCDC(BasePrimitiveCDC, ABC):
    model_config = ConfigDict(validate_assignment = True)
    cdc_name: VisString255 = Field(default = 'SubstitutionCDC',
                                   pattern = 'SubstitutionCDC',
                                   serialization_alias = 'cdcName')
    sub_q:    Optional[Quality]      = Field(default_factory = Quality,
                                             serialization_alias = "subQ")
    sub_id:   Optional[VisString64]  = Field(default = "",
                                             serialization_alias = "subID")
    sub_ena:  Optional[BOOLEAN]      = Field(default = False,
                                             serialization_alias = "subEna")
    blk_ena:  Optional[BOOLEAN]      = Field(default = False,
                                             serialization_alias = "blkEna")

# IEC 61850-7-3 7.4.2
class HarmonicMeasurandCDC(BaseComposedCDC, ABC):
    cdc_name:  VisString255              = Field(default = 'HarmonicMeasurandCDC',
                                                 pattern = 'HarmonicMeasurandCDC',
                                                 serialization_alias = 'cdcName')
    num_har:   INT16U                    = Field(default = 0,
                                                 serialization_alias = "numHar")
    num_cyc:   INT16U                    = Field(default = 0,
                                                 serialization_alias = "numCyc")
    eval_tm:   INT16U                    = Field(default = 0,
                                                 serialization_alias = "evalTm")
    smp_rate:  Optional[INT32U]          = Field(default = None,
                                                 serialization_alias = "smpRate")
    frequency: FLOAT32                   = Field(default = 0.0,
                                                 serialization_alias = "frequency")
    hv_ref:    Optional[HvReferenceKind] = Field(default = None,
                                                 serialization_alias = "hvRef")
    rms_cyc:   Optional[INT16U]          = Field(default = None,
                                                 serialization_alias = "rmsCyc")
    maxpts:    INT16U                    = Field(default = 0,
                                                 serialization_alias = "maxPts")

    # rms_cyc must be provided if hv_ref is rms
    @model_validator(mode='before')
    @classmethod
    def mo_rms(cls, data: Any) -> Any:
        prescond.mo_rms(data,
                        hv_ref = "hv_ref",
                        param_list = ["rms_cyc"])
        return data

# IEC 61850-7-3 7.5.2
class ControlTestingCDC(SubstitutionCDC, ABC):
    cdc_name: VisString255        = Field(default = 'ControlTestingCDC',
                                          pattern = 'ControlTestingCDC',
                                          serialization_alias = 'cdcName')
    op_rcvd:  Optional[BOOLEAN]   = Field(default = None,
                                          serialization_alias = "opRcvd")
    op_ok:    Optional[BOOLEAN]   = Field(default = None,
                                          serialization_alias = "opOk")
    t_op_ok:  Optional[Timestamp] = Field(default = None,
                                          serialization_alias = "tOpOk")

# IEC 61850-7-3 7.7.2.2
class ASG(BasePrimitiveCDC, ABC):
    cdc_name:  VisString255                = Field(default = 'ASG',
                                                   pattern = 'ASG',
                                                   serialization_alias = 'cdcName')
    units:     Optional[Unit]              = Field(default = None,
                                                   serialization_alias = "units")
    svc:       Optional[ScaledValueConfig] = Field(default = None,
                                                   serialization_alias = "sVC")
    min_val:   Optional[AnalogueValue]     = Field(default = None,
                                                   serialization_alias = "minVal")
    max_val:   Optional[AnalogueValue]     = Field(default = None,
                                                   serialization_alias = "maxVal")
    step_size: Optional[AnalogueValue]     = Field(default = None,
                                                   serialization_alias = "stepSize")

# IEC 61850-7-3 7.7.4.2
class CSG(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'CSG',
                                   pattern = 'CSG',
                                   serialization_alias = 'cdcName')
    x_units:  Unit                   = Field(default_factory = Unit,
                                             serialization_alias = "xUnits")
    y_units:  Unit                   = Field(default_factory = Unit,
                                             serialization_alias = "yUnits")
    z_units:  Optional[Unit]         = Field(default = None,
                                             serialization_alias = "zUnits")
    max_pts:  INT16U                 = Field(default = 1,
                                             serialization_alias = "maxPts")
    xd:       VisString255           = Field(default = "",
                                             serialization_alias = "xD")
    xdu:      Optional[Unicode255]   = Field(default = None,
                                             serialization_alias = "xDU")
    yd:       VisString255           = Field(default = "",
                                             serialization_alias = "yD")
    ydu:      Optional[Unicode255]   = Field(default = "",
                                             serialization_alias = "yDU")
    zd:       Optional[VisString255] = Field(default = "",
                                             serialization_alias = "zD")
    zdu:      Optional[Unicode255]   = Field(default = "",
                                             serialization_alias = "zDU")

# IEC 61850-7-3 7.6.7.2
class CUG(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'CUG',
                                   pattern = 'CUG',
                                   serialization_alias = 'cdcName')

# IEC 61850-7-3 7.7.3.2
class CURVE(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'CURVE',
                                   pattern = 'CURVE',
                                   serialization_alias = 'cdcName')

# IEC 61850-7-3 7.6.4.2
class ENG(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'ENG',
                                   pattern = 'ENG',
                                   serialization_alias = 'cdcName')

# IEC 61850-7-3 7.6.3.2
class ING(BasePrimitiveCDC, ABC):
    cdc_name:  VisString255 = Field(default = 'ING',
                                    pattern = 'ING',
                                    serialization_alias = 'cdcName')
    min_val:   Optional[INT32]  = Field(default = None,
                                        serialization_alias = "minVal")
    max_val:   Optional[INT32]  = Field(default = None,
                                        serialization_alias = "maxVal")
    step_size: Optional[INT32U] = Field(default = None,
                                        serialization_alias = "stepSize")
    units:     Optional[Unit]   = Field(default = None,
                                        serialization_alias = "units")

# IEC 61850-7-3 7.6.2.2
class SPG(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'SPG',
                                   pattern = 'SPG',
                                   serialization_alias   = 'cdcName')

# IEC 61850-7-3 7.6.8.3
class VSG(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'VSG',
                                   pattern = 'VSG',
                                   serialization_alias   = 'cdcName')

# IEC 61850-7-3 7.6.6.2 TSG
class TSG(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'TSG',
                                   pattern = 'TSG',
                                   serialization_alias   = 'cdcName')

