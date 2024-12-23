# py_iec61850_cdc service.py
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

# This file provides the service status CDCs described under Clause 7.9 of
# IEC 61850-7-3:2010+AMD1:2020 CSV as Python dataclasses.

from __future__ import annotations
from typing import Any, Optional

from pydantic import Field

from py_iec61850_cdc.abstracts import BasePrimitiveCDC
from py_iec61850_cdc.attributes import (
    CheckConditions,
    EntryTime,
    Originator,
    RCBReportOptions,
    SVMessageOptions,
    Timestamp,
    TriggerConditions,
)
from py_iec61850_cdc.basetypes import (
    BOOLEAN,
    INT8U,
    INT16,
    INT16U,
    INT32U,
    EntryID,
    ObjectReference,
    Octet64,
    PhyComAddr,
    Unicode255,
    VisString129,
    VisString255,
)
from py_iec61850_cdc.enums import ControlServiceStatusKind, SamplingModeKind, ServiceNameKind, ServiceStatusKind


# IEC 61850-7-3 7.9.10
class CTS(BasePrimitiveCDC):
    cdc_name:       VisString255             = Field(default = 'CTS',
                                                     pattern = 'CTS',
                                                     serialization_alias = 'cdcName')
    obj_ref:        ObjectReference          = Field(default = "",
                                               serialization_alias = "objRef")
    service_type:   ServiceNameKind          = Field(default = ServiceNameKind.unknown,
                                               serialization_alias = "serviceType")
    error_code:     ServiceStatusKind        = Field(default = ServiceStatusKind.no_error,
                                               serialization_alias = "errorCode")
    originator_id:  Optional[Octet64]        = Field(default = None,
                                                     serialization_alias = "originatorID")
    t:              Timestamp                = Field(default_factory = Timestamp,
                                                     serialization_alias = "t")
    cert_issuer:    Optional[Unicode255]     = Field(default = None,
                                                     serialization_alias = "certIssuer"),
    ctl_val:        Any                      = None
    oper_tm:        Timestamp                = Field(default_factory = Timestamp,
                                                     serialization_alias = "operTm")
    origin:         Originator               = Field(default_factory = Originator,
                                                     serialization_alias = "originator")
    ctl_num:        INT8U                    = Field(default = 0,
                                                     serialization_alias = "ctlNum")
    T:              Timestamp                = Field(default_factory = Timestamp,
                                                     serialization_alias = "T")
    test:           BOOLEAN                  = Field(default = False,
                                                     serialization_alias = "test")
    check:          CheckConditions          = Field(default_factory = CheckConditions,
                                                     serialization_alias = "check")
    resp_add_cause: ControlServiceStatusKind = Field(default = ControlServiceStatusKind.unknown,
                                                     serialization_alias = "respAddCause")

    # MOoperTm constraint on oper_tm is left to the logical node / IED developer.  If at
    # least one controllable object on the IED supports time activation service, this
    # must be implemented.


# IEC 61850-7-3 7.9.9
class STS(BasePrimitiveCDC):
    cdc_name:      VisString255         = Field(default = 'STS',
                                                pattern = 'STS',
                                                serialization_alias = 'cdcName')
    obj_ref:       ObjectReference      = Field(default = "",
                                                serialization_alias = "objRef")
    service_type:  ServiceNameKind      = Field(default = ServiceNameKind.unknown,
                                                serialization_alias = "serviceType")
    error_code:    ServiceStatusKind    = Field(default = ServiceStatusKind.no_error,
                                                serialization_alias = "errorCode")
    originator_id: Optional[Octet64]    = Field(default = None,
                                                serialization_alias = "originatorID")
    t:             Timestamp            = Field(default_factory = Timestamp,
                                                serialization_alias = "t")
    cert_issuer:   Optional[Unicode255] = Field(default = None,
                                                serialization_alias = "certIssuer")
    num_of_sg:     INT8U                = Field(default = 0,
                                                serialization_alias = "numOfSG")
    act_sg:        INT8U                = Field(default = 0,
                                                serialization_alias = "actSG")
    edit_sg:       INT8U                = Field(default = 0,
                                                serialization_alias = "editSG")
    cnf_edit:      BOOLEAN              = Field(default = False,
                                                serialization_alias = "cnfEdit")
    i_act_tm:      Timestamp            = Field(default_factory = Timestamp,
                                                serialization_alias = "iActTm")
    resv_tms:      INT16U               = Field(default = 0,
                                                serialization_alias = "resvTms")

# IEC 61850-7-3 7.9.8
class NTS(BasePrimitiveCDC):
    cdc_name:      VisString255         = Field(default = 'NTS',
                                                pattern = 'NTS',
                                                serialization_alias = 'cdcName')
    obj_ref:       ObjectReference      = Field(default = "",
                                                serialization_alias = "objRef")
    service_type:  ServiceNameKind      = Field(default = ServiceNameKind.unknown,
                                                serialization_alias = "serviceType")
    error_code:    ServiceStatusKind    = Field(default = ServiceStatusKind.no_error,
                                                serialization_alias = "errorCode")
    originator_id: Optional[Octet64]    = Field(default = None,
                                                serialization_alias = "originatorID")
    t:             Timestamp            = Field(default_factory = Timestamp,
                                                serialization_alias = "t")
    sv_ena:        BOOLEAN              = Field(default = False,
                                                serialization_alias = "svEna")
    resv:          BOOLEAN              = Field(default = False,
                                                serialization_alias = "resv")
    usv_id:        VisString129         = Field(default = "",
                                                serialization_alias = "usvID")
    dat_set:       ObjectReference      = Field(default = "",
                                                serialization_alias = "datSet")
    conf_rev:      INT32U               = Field(default = 0,
                                                serialization_alias = "confRev")
    smp_mod:       SamplingModeKind     = Field(default = SamplingModeKind.samples_per_second,
                                                serialization_alias = "smpMod")
    smp_rate:      INT16U               = Field(default = 0,
                                                serialization_alias = "smpRate")
    opt_flds:      SVMessageOptions     = Field(default_factory = SVMessageOptions,
                                                serialization_alias = "optFlds")
    dst_address:   PhyComAddr           = Field(default = "",
                                                serialization_alias = "dstAddress")

# IEC 61850-7-3 7.9.7
class MTS(BasePrimitiveCDC):
    cdc_name:      VisString255         = Field(default = 'MTS',
                                                pattern = 'MTS',
                                                serialization_alias = 'cdcName')
    obj_ref:       ObjectReference      = Field(default = "",
                                                serialization_alias = "objRef")
    service_type:  ServiceNameKind      = Field(default = ServiceNameKind.unknown,
                                                serialization_alias = "serviceType")
    error_code:    ServiceStatusKind    = Field(default = ServiceStatusKind.no_error,
                                                serialization_alias = "errorCode")
    originator_id: Optional[Octet64]    = Field(default = None,
                                                serialization_alias = "originatorID")
    t:             Timestamp            = Field(default_factory = Timestamp,
                                                serialization_alias = "t")
    cert_issuer:   Optional[Unicode255] = Field(default = None,
                                                serialization_alias = "certIssuer")
    sv_ena:        BOOLEAN              = Field(default = False,
                                                serialization_alias = "svEna")
    msv_id:        VisString129         = Field(default = "",
                                                serialization_alias = "msvID")
    dat_set:       ObjectReference      = Field(default = "",
                                                serialization_alias = "datSet")
    conf_rev:      INT32U               = Field(default = 0,
                                                serialization_alias = "confRev")
    smp_rate:      INT16U               = Field(default = 0,
                                                serialization_alias = "smpMod")
    opt_flds:      SVMessageOptions     = Field(default_factory = SVMessageOptions,
                                                serialization_alias = "optFlds")
    smp_mod:       SamplingModeKind     = Field(default = SamplingModeKind.samples_per_second,
                                                serialization_alias = "smpMod")
    dst_address:   PhyComAddr           = Field(default = "",
                                                serialization_alias = "dstAddress")

# IEC 61850-7-3 7.9.6
class GTS(BasePrimitiveCDC):
    cdc_name:      VisString255         = Field(default = 'GTS',
                                                pattern = 'GTS',
                                                serialization_alias = 'cdcName')
    obj_ref:       ObjectReference      = Field(default = "",
                                                serialization_alias = "objRef")
    service_type:  ServiceNameKind      = Field(default = ServiceNameKind.unknown,
                                                serialization_alias = "serviceType")
    error_code:    ServiceStatusKind    = Field(default = ServiceStatusKind.no_error,
                                                serialization_alias = "errorCode")
    originator_id: Optional[Octet64]    = Field(default = None,
                                                serialization_alias = "originatorID")
    t:             Timestamp            = Field(default_factory = Timestamp,
                                                serialization_alias = "t")
    cert_issuer:   Optional[Unicode255] = Field(default = None,
                                                serialization_alias = "certIssuer")
    go_ena:        BOOLEAN              = Field(default = False,
                                                serialization_alias = "goEna")
    go_id:         VisString129         = Field(default = "",
                                                serialization_alias = "goID")
    dat_set:       ObjectReference      = Field(default = "",
                                                serialization_alias = "datSet")
    conf_rev:      INT32U               = Field(default = 0,
                                                serialization_alias = "confRev")
    nds_com:       BOOLEAN              = Field(default = False,
                                                serialization_alias = "ndsCom")
    dst_address:   PhyComAddr           = Field(default = "",
                                                serialization_alias = "dstAddress")

# IEC 61850-7-3 7.9.5
class LTS(BasePrimitiveCDC):
    cdc_name:      VisString255         = Field(default = 'LTS',
                                                pattern = 'LTS',
                                                serialization_alias = 'cdcName')
    obj_ref:       ObjectReference      = Field(default = "",
                                                serialization_alias = "objRef")
    service_type:  ServiceNameKind      = Field(default = ServiceNameKind.unknown,
                                                serialization_alias = "serviceType")
    error_code:    ServiceStatusKind    = Field(default = ServiceStatusKind.no_error,
                                                serialization_alias = "errorCode")
    originator_id: Optional[Octet64]    = Field(default = None,
                                                serialization_alias = "originatorID")
    t:             Timestamp            = Field(default_factory = Timestamp,
                                                serialization_alias = "t")
    cert_issuer:   Optional[Unicode255] = Field(default = None,
                                                serialization_alias = "certIssuer")
    log_ena:       BOOLEAN              = Field(default = False,
                                                serialization_alias = "logEna")
    log_ref:       ObjectReference      = Field(default = "",
                                                serialization_alias = "logRef")
    dat_set:       ObjectReference      = Field(default = "",
                                                serialization_alias = "datSet")
    old_entr_tm:   EntryTime            = Field(default_factory = EntryTime,
                                                serialization_alias = "oldEntrTm")
    new_entr_tm:   EntryTime            = Field(default_factory = EntryTime,
                                                serialization_alias = "newEntrTm")
    old_ent:       EntryID              = Field(default = "",
                                                serialization_alias = "oldEnt")
    new_ent:       EntryID              = Field(default = "",
                                                serialization_alias = "newEnt")
    trg_ops:       TriggerConditions    = Field(default_factory = TriggerConditions,
                                                serialization_alias = "trgOps")
    intg_pd:       INT32U               = Field(default = 0,
                                                serialization_alias = "intgPd")

# IEC 61850-7-3 7.9.4
class UTS(BasePrimitiveCDC):
    cdc_name:      VisString255         = Field(default = 'UTS',
                                                pattern = 'UTS',
                                                serialization_alias = 'cdcName')
    obj_ref:       ObjectReference      = Field(default = "",
                                                serialization_alias = "objRef")
    service_type:  ServiceNameKind      = Field(default = ServiceNameKind.unknown,
                                                serialization_alias = "serviceType")
    error_code:    ServiceStatusKind    = Field(default = ServiceStatusKind.no_error,
                                                serialization_alias = "errorCode")
    originator_id: Optional[Octet64]    = Field(default = None,
                                                serialization_alias = "originatorID")
    t:             Timestamp            = Field(default_factory = Timestamp,
                                                serialization_alias = "t")
    cert_issuer:   Optional[Unicode255] = Field(default = None,
                                                serialization_alias = "certIssuer")
    rpt_id:        VisString129         = Field(default = "",
                                                serialization_alias = "rptID")
    rpt_ena:       BOOLEAN              = Field(default = False,
                                                serialization_alias = "rptEna")
    resv:          BOOLEAN              = Field(default = False,
                                                serialization_alias = "resv")
    dat_set:       ObjectReference      = Field(default = "",
                                                serialization_alias = "datSet")
    conf_rev:      INT32U               = Field(default = 0,
                                                serialization_alias = "confRev")
    opt_flds:      RCBReportOptions     = Field(default_factory = RCBReportOptions,
                                                serialization_alias = "optFlds")
    buf_tm:        INT32U               = Field(default = 0,
                                                serialization_alias = "bufTm")
    sq_num:        INT8U                = Field(default = 0,
                                                serialization_alias = "sqNum")
    trg_ops:       TriggerConditions    = Field(default_factory = TriggerConditions,
                                                serialization_alias = "trgOps")
    intg_pd:       INT32U               = Field(default = 0,
                                                serialization_alias = "intgPd")
    gi:            BOOLEAN              = Field(default = False,
                                                serialization_alias = "gi")
    owner:         Optional[Octet64]    = Field(default = None,
                                                serialization_alias = "owner")

# IEC 61850-7-3 7.9.3
class BTS(BasePrimitiveCDC):
    cdc_name:      VisString255         = Field(default = 'BTS',
                                                pattern = 'BTS',
                                                serialization_alias = 'cdcName')
    obj_ref:       ObjectReference      = Field(default = "",
                                                serialization_alias = "objRef")
    service_type:  ServiceNameKind      = Field(default = ServiceNameKind.unknown,
                                                serialization_alias = "serviceType")
    error_code:    ServiceStatusKind    = Field(default = ServiceStatusKind.no_error,
                                                serialization_alias = "errorCode")
    originator_id: Optional[Octet64]    = Field(default = None,
                                                serialization_alias = "originatorID")
    t:             Timestamp            = Field(default_factory = Timestamp,
                                                serialization_alias = "t")
    cert_issuer:   Optional[Unicode255] = Field(default = None,
                                                serialization_alias = "certIssuer")
    rpt_id:        VisString129         = Field(default = "",
                                                serialization_alias = "rptID")
    rpt_ena:       BOOLEAN              = Field(default = False,
                                                serialization_alias = "rptEna")
    dat_set:       ObjectReference      = Field(default = "",
                                                serialization_alias = "datSet")
    conf_rev:      INT32U               = Field(default = 0,
                                                serialization_alias = "confRev")
    opt_flds:      RCBReportOptions     = Field(default_factory = RCBReportOptions,
                                                serialization_alias = "optFlds")
    buf_tm:        INT32U               = Field(default = 0,
                                                serialization_alias = "bufTm")
    sq_num:        INT16U               = Field(default = 0,
                                                serialization_alias = "sqNum")
    trg_ops:       TriggerConditions    = Field(default_factory = TriggerConditions,
                                                serialization_alias = "trgOps")
    intg_pd:       INT32U               = Field(default = 0,
                                                serialization_alias = "intgPd")
    gi:            BOOLEAN              = Field(default = False,
                                                serialization_alias = "gi")
    purge_buf:     BOOLEAN              = Field(default = False,
                                                serialization_alias = "purgeBuf")
    entry_id:      EntryID              = Field(default = "",
                                                serialization_alias = "entryID")
    time_of_entry: EntryTime            = Field(default_factory = EntryTime,
                                                serialization_alias = "timeOfEntry")
    resv_tms:      Optional[INT16]      = Field(default = None,
                                                serialization_alias = "resvTms")
    owner:         Optional[Octet64]    = Field(default = None,
                                                serialization_alias = "owner")

# IEC 61850-7-3 7.9.2
class CST(BasePrimitiveCDC):
    cdc_name:      VisString255         = Field(default = 'CST',
                                                pattern = 'CST',
                                                serialization_alias = 'cdcName')
    obj_ref:       ObjectReference      = Field(default = "",
                                                serialization_alias = "objRef")
    service_type:  ServiceNameKind      = Field(default = ServiceNameKind.unknown,
                                                serialization_alias = "serviceType")
    error_code:    ServiceStatusKind    = Field(default = ServiceStatusKind.no_error,
                                                serialization_alias = "errorCode")
    originator_id: Optional[Octet64]    = Field(default = None,
                                                serialization_alias = "originatorID")
    t:             Timestamp            = Field(default_factory = Timestamp,
                                                serialization_alias = "t")
    cert_issuer:   Optional[Unicode255] = Field(default = None,
                                                serialization_alias = "certIssuer")

