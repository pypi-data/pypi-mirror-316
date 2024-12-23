# py_iec61850_cdc cdc_description.py
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

# This file provides the description CDCs described under Clause 7.8 of
# IEC 61850-7-3:2010+AMD1:2020 CSV as Python dataclasses.

from __future__ import annotations

from pydantic import Field

from py_iec61850_cdc.abstracts import BasePrimitiveCDC
from py_iec61850_cdc.attributes import Point, Unit
from py_iec61850_cdc.basetypes import FLOAT32, INT16U, INT32, Unicode255, VisString64, VisString255
from py_iec61850_cdc.listobjects import DAList

# IEC 61850-7-3 7.8.2
class DPL(BasePrimitiveCDC):
    cdc_name:    VisString255           = Field(default = 'DPL',
                                                pattern = 'DPL',
                                                serialization_alias = 'cdcName')
    vendor:      VisString255           = Field(default = "",
                                                serialization_alias = "vendor")
    hw_rev:      Optional[VisString255] = Field(default = None,
                                                serialization_alias = "hwRev")
    sw_rev:      Optional[VisString255] = Field(default = None,
                                                serialization_alias = "swRev")
    ser_num:     Optional[VisString255] = Field(default = None,
                                                serialization_alias = "serNum")
    model:       Optional[VisString255] = Field(default = None,
                                                serialization_alias = "model")
    location:    Optional[VisString255] = Field(default = None,
                                                serialization_alias = "location")
    name:        Optional[VisString64]  = Field(default = None,
                                                serialization_alias = "name")
    owner:       Optional[VisString255] = Field(default = None,
                                                serialization_alias = "owner")
    eps_name:    Optional[VisString255] = Field(default = None,
                                                serialization_alias = "ePSName")
    prime_oper:  Optional[VisString255] = Field(default = None,
                                                serialization_alias = "primeOper")
    second_oper: Optional[VisString255] = Field(default = None,
                                                serialization_alias = "secondOper")
    latitude:    Optional[FLOAT32]      = Field(default = None,
                                                serialization_alias = "latitude")
    longitude:   Optional[FLOAT32]      = Field(default = None,
                                                serialization_alias = "longitude")
    altitude:    Optional[FLOAT32]      = Field(default = None,
                                                serialization_alias = "altitude")
    mrid:        Optional[VisString255] = Field(default = None,
                                                serialization_alias = "mRID")

# IEC 61850-7-3 7.8.3
class LPL(BasePrimitiveCDC):
    cdc_name:   VisString255           = Field(default = 'LPL',
                                               pattern = 'LPL',
                                               serialization_alias = 'cdcName')
    param_rev:  Optional[INT32]        = Field(default = 0,
                                               serialization_alias = "paramRev")
    val_rev:    Optional[INT32]        = Field(default = 0,
                                               serialization_alias = "valRev")
    vendor:     VisString255           = Field(default = "",
                                               serialization_alias = "vendor")
    sw_rev:     VisString255           = Field(default = "",
                                               serialization_alias = "swRev")
    ld_ns:      Optional[VisString255] = Field(default = None,
                                               serialization_alias = "ldNs")
    ln_ns:      Optional[VisString255] = Field(default = None,
                                               serialization_alias = "lnNs")
    config_rev: Optional[VisString255] = Field(default = None,
                                               serialization_alias = "configRev")
    # ld_ns, ln_ns, and config_rev presence conditions depend on the parent
    # logical node. It is left to the containing logical node implementer to
    # add or don't add these.

# IEC 61850-7-3 7.8.4
class CSD(BasePrimitiveCDC):
    cdc_name: VisString255           = Field(default = 'CSD',
                                             pattern = 'CSD',
                                             serialization_alias   = 'cdcName')
    x_units:  Unit                   = Field(default_factory = Unit,
                                             serialization_alias = "xUnits")
    xd:       VisString255           = Field(default = "",
                                             serialization_alias = "xD")
    xdu:      Optional[Unicode255]   = Field(default = None,
                                             serialization_alias = "xDU")
    y_units:  Unit                   = Field(default_factory = Unit,
                                             serialization_alias = "yUnits")
    yd:       VisString255           = Field(default = "",
                                             serialization_alias = "yD")
    ydu:      Optional[Unicode255]   = Field(default = None,
                                             serialization_alias = "yDU")
    z_units:  Optional[Unit]         = Field(default = None,
                                             serialization_alias = "zUnits")
    zd:       Optional[VisString255] = Field(default = None,
                                             serialization_alias = "zD")
    zdu:      Optional[Unicode255]   = Field(default = None,
                                             serialization_alias = "zDU")
    num_pts:  INT16U                 = Field(default = 0,
                                             serialization_alias = "numPts")
    crv_pts:  DAList[Point]          = Field(default = None,
                                             serialization_alias = "crvPts")
    max_pts:  INT16U                 = Field(default = 0,
                                             serialization_alias = "maxPts")

# IEC 61850-7-3 7.8.5
class VSD(BasePrimitiveCDC):
    cdc_name: VisString255 = Field(default = 'VSD',
                                   pattern = 'VSD',
                                   serialization_alias = 'cdcName')
    val:      VisString255 = Field(default = "",
                                   serialization_alias = "val")

