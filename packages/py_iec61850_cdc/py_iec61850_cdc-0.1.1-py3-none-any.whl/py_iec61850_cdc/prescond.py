# py_iec61850_cdc prescond.py
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

# This file provides generalized presence condition validators for use
# with Pydantic and py_iec61850_cdc.  The intent is to avoid code duplication.

from __future__ import annotations

from py_iec61850_cdc.enums import (
    CtlModelKind,
    HvReferenceKind,
    PhaseReferenceKind,
)


# MOsbo
def mo_sbo(data:            dict,
           ctl_model_param: str,
           param_list:      list[str] = None) -> None:
    if isinstance(data,dict) and param_list is not None:
        if ctl_model_param not in data:
            raise ValueError("MOsbo: "+ctl_model_param+" does not exist in object data.")
        if isinstance(data[ctl_model_param],CtlModelKind):
            if (data[ctl_model_param] == CtlModelKind.sbo_with_normal_security or
                data[ctl_model_param] == CtlModelKind.sbo_with_enhanced_security):
                for i in param_list:
                    if i not in data:
                        raise ValueError("MOsbo: "+i+" despite not present in sbo CtlModelKind")
        else:
            raise ValueError("MOsbo: ctl_model is not CtlModelKind")


# MOenahnced
def mo_enhanced(data:            dict,
                ctl_model_param: str       = "",
                param_list:      list[str] = None) -> None:
    if isinstance(data,dict) and param_list is not None:
        if ctl_model_param not in data:
            raise ValueError("MOenhanced: "+ctl_model_param+" does not exist in object data.")
        if isinstance(data[ctl_model_param],CtlModelKind):
            if (data[ctl_model_param] == CtlModelKind.direct_with_enhanced_security or
                data[ctl_model_param] == CtlModelKind.sbo_with_enhanced_security):
                for i in param_list:
                    if i not in data:
                        raise ValueError("MOenhanced: "+i+" despite not present in enhanced security CtlModelKind")
        else:
            raise ValueError("MOenhanced: ctl_model is not CtlModelKind")

# MFsubst
def mf_subst(data:       dict,
             subst_ena:  bool      = True,
             param_list: list[str] = None) -> None:
    if param_list is not None and isinstance(data,dict) and subst_ena == True:
        for i in param_list:
            if i not in data:
                raise ValueError("MFsubst: All substitution elements are required, since substitution is supported.")

# MAllOrNonePerGroup(n)
def m_all_or_none_per_group(data:        dict,
                            param_list: list[str] = None) -> None:
    at_least_one = False
    if param_list is not None and isinstance(data,dict):
        for i in param_list:
            if i in data:
                at_least_one = True
        if at_least_one:
            for i in param_list:
                if i not in data:
                    raise ValueError("MAllOrNonePerGroup(n): If one element is present, all from the group must be present.")

# MOrms
def mo_rms(data:       dict,
           hv_ref:     str,
           param_list: list[str] = None) -> None:
    if isinstance(data,dict) and param_list is not None:
        if hv_ref not in data:
            return
        if isinstance(data[hv_ref],HvReferenceKind):
            if (data[hv_ref] == HvReferenceKind.rms):
                for i in param_list:
                    if i not in data:
                        raise ValueError("MOrms: "+i+" not present despite rms reference kind.")

# OMSynPh
def om_syn_ph(data:       dict,
              phs_ref:    str,
              param_list: list[str] = None) -> None:
    if isinstance(data,dict) and param_list is not None:
        if phs_ref not in data:
            return
        if isinstance(data[phs_ref],PhaseReferenceKind):
            if (data[phs_ref] == PhaseReferenceKind.synchrophasor):
                for i in param_list:
                    if i not in data:
                        raise ValueError("OMSynPh: "+i+" not present despite synchrophasor reference kind.")

# AtLeastOne(n)
def at_least_one(data:       dict,
                 param_list: list[str] = None) -> None:
    at_least_one = False
    if param_list is not None and isinstance(data,dict):
        for i in param_list:
            if i in data:
                at_least_one = True
        if not at_least_one:
            message = ""
            counter = 0
            for i in param_list:
                counter = counter + 1
                message = message + i
                if counter < len(param_list): message = message + ","
            raise ValueError("AtLeastOne(n): Must have at least one of: "+message+".")


# MO(sibling)
def mo_sibling(data:            dict,
               sibling:         str,
               param_list:      list[str] = None) -> None:
    if isinstance(data,dict) and param_list is not None:
        if sibling not in data:
            return
        for i in param_list:
            if i not in data:
                raise ValueError("MO("+sibling+"): "+i+" must be present with "+sibling+".")

# OF(sibling)
def of_sibling(data:            dict,
               sibling:         str,
               param_list:      list[str] = None) -> None:
    if isinstance(data,dict) and param_list is not None:
        if sibling not in data:
            for i in param_list:
                if i in data:
                    raise ValueError("OF("+sibling+"): "+i+" must not be present unless "+sibling+" is present.")


# MFscaledAV
def mf_scaled_av(data:       dict,
                 svc_var:    str,
                 param_list: list[str] = None) -> None:
    if isinstance(data,dict) and param_list is not None:
        for av in param_list:
            if av in data:
                if ((av.i is not None and svc_var not in data) or
                    (av.i is None and svc_var in data)):
                    raise ValueError("Must use "+mag_or_ang+"SVC together with "+i+"."+mag_or_ang+".i variable.")

# MFscaledMagV / MFscaledAngV
def mf_scaled_x_v(data:       dict,
                  svc_var:    str,
                  mag_or_ang: str,
                  param_list: list[str] = None) -> None:
    if isinstance(data,dict) and param_list is not None:
        for i in param_list:
            if i in data:
                vector = data[i]
                if vector.__dict__[mag_or_ang] is not None:
                    ma = vector.__dict__[mag_or_ang]
                    if ((ma.i is not None and svc_var not in data) or
                        (ma.i is None and svc_var in data)):
                        raise ValueError("Must use "+mag_or_ang+"SVC together with "+i+"."+mag_or_ang+".i variable.")

def all_at_least_one_group(data: dict,
                           groups: list[list[str]]
                           ):
    if isinstance(data,dict) and groups is not None:
        for group in groups:
            at_least_one = False
            at_least_one_in_group = False
            for parameter in group:
                if parameter in data:
                    at_least_one_in_group = True
                    at_least_one = True
            if at_least_one_in_group:
                for parameter in group:
                    if parameter not in data:
                        err_msg = ""
                        cnt     = 0
                        for err_param in group:
                            cnt = cnt + 1
                            err_msg = err_msg + err_param
                            if cnt < len(group):
                                err_msg = err_msg+", "
                        raise ValueError("AllAtLeastOneGroup(n): Parameter "+parameter+" is not used, despite others in "+err_msg+" being used.")
            if not at_least_one:
                raise ValueError("AllAtLeastOneGroup(n): No parameters were used, but at least one group must be used.")

