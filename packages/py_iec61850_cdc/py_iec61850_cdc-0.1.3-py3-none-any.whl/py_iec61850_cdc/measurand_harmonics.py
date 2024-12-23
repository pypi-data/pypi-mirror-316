# py_iec61850_cdc measurand_harmonics.py
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

from py_iec61850_cdc import prescond as prescond
from py_iec61850_cdc.basetypes import VisString255
from py_iec61850_cdc.enums import PhaseAngleReferenceKind
from py_iec61850_cdc.listobjects import DOList
from py_iec61850_cdc.measurand import CMV
from py_iec61850_cdc.abstracts import HarmonicMeasurandCDC

# IEC 61850-7-3 7.4.9
class HMV(HarmonicMeasurandCDC):
    cdc_name:  VisString255    = Field(default = 'HMV',
                                       pattern = 'HMV',
                                       serialization_alias = 'cdcName')
    har:       DOList[CMV]     = Field(default = None,
                                       serialization_alias = 'har')


# IEC 61850-7-3 7.4.10
class HWYE(HarmonicMeasurandCDC):
    cdc_name:  VisString255                      = Field(default = 'HWYE',
                                                         pattern = 'HWYE',
                                                         serialization_alias = 'cdcName')
    phs_a_har: DOList[CMV]                       = Field(default = None,
                                                         serialization_alias = "phsAHar")
    phs_b_har: Optional[DOList[CMV]]             = Field(default = None,
                                                         serialization_alias = "phsBHar")
    phs_c_har: Optional[DOList[CMV]]             = Field(default = None,
                                                         serialization_alias = "phsCHar")
    neut_har:  Optional[DOList[CMV]]             = Field(default = None,
                                                         serialization_alias = "neutHar")
    net_har:   Optional[DOList[CMV]]             = Field(default = None,
                                                         serialization_alias = "netHar")
    res_har:   Optional[DOList[CMV]]             = Field(default = None,
                                                         serialization_alias = "resHar")
    ang_ref:   Optional[PhaseAngleReferenceKind] = Field(default = None,
                                                         serialization_alias = "angRef")

# IEC 61850-7-3 7.4.11
class HDEL(HarmonicMeasurandCDC):
    cdc_name:   VisString255                      = Field(default = 'HDEL',
                                                          pattern = 'HDEL',
                                                          serialization_alias = 'cdcName')
    phs_ab_har: DOList[CMV]                       = Field(default = None,
                                                          serialization_alias = "phsABHar")
    phs_bc_har: Optional[DOList[CMV]]             = Field(default = None,
                                                          serialization_alias = "phsBCHar")
    phs_ca_har: Optional[DOList[CMV]]             = Field(default = None,
                                                          serialization_alias = "phsCAHar")
    ang_ref:    Optional[PhaseAngleReferenceKind] = Field(default = None,
                                                          serialization_alias = "angRef")

