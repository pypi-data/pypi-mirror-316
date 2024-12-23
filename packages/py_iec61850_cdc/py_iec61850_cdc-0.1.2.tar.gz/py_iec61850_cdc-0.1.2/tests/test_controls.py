import pytest

from py_iec61850_cdc.attributes import (
    Quality,
    Timestamp,
)

from py_iec61850_cdc.enums import (
    CtlModelKind,
)

from py_iec61850_cdc.controls import (
    SPC,
)

@pytest.fixture
def fix_test1_create_bad_spc():
    with pytest.raises(ValueError) as exc:
        return SPC(st_val=True)

def test_test1_prescond(fix_test1_create_bad_spc):
    spcobj= fix_test1_create_bad_spc

@pytest.fixture
def fix_test2_create_good_spc():
    new_q = Quality()
    new_t = Timestamp.factory_local()
    return SPC(st_val    = True,
               q         = new_q,
               t         = new_t,
               ctl_model = CtlModelKind.status_only,
               ctl_val   = False,
               sub_ena   = False,
               sub_val   = False,
               sub_q     = new_q,
               sub_id    = "")

def test_test2_prescond(fix_test2_create_good_spc):
    spcobj= fix_test2_create_good_spc
    assert isinstance(spcobj,SPC)

@pytest.fixture
def fix_test3_create_bad_spc():
    new_q = Quality()
    new_t = Timestamp.factory_local()
    with pytest.raises(ValueError) as exc:
        return SPC(st_val    = True,
                   q         = new_q,
                   t         = new_t,
                   ctl_model = CtlModelKind.sbo_with_normal_security,
                   ctl_val   = False)

def test_test3_prescond(fix_test3_create_bad_spc):
    pass

@pytest.fixture
def fix_test4_create_good_spc():
    new_q = Quality()
    new_t = Timestamp.factory_local()
    return SPC(st_val      = True,
               q           = new_q,
               t           = new_t,
               st_seld     = False,
               sbo_timeout = 32,
               ctl_model   = CtlModelKind.sbo_with_normal_security,
               ctl_val     = False,
               sub_ena     = False,
               sub_val     = False,
               sub_q       = new_q,
               sub_id      = "")

def test_test4_prescond(fix_test4_create_good_spc):
    pass

@pytest.fixture
def fix_test5_create_bad_spc():
    new_q = Quality()
    new_t = Timestamp.factory_local()
    with pytest.raises(ValueError) as exc:
        return SPC(st_val    = True,
                   q         = new_q,
                   t         = new_t,
                   ctl_model = CtlModelKind.direct_with_enhanced_security,
                   ctl_val   = False,
                   sub_ena   = False,
                   sub_val   = False,
                   sub_q     = new_q,
                   sub_id    = "")

def test_test5_prescond(fix_test5_create_bad_spc):
    pass

@pytest.fixture
def fix_test6_create_good_spc():
    new_q = Quality()
    new_t = Timestamp.factory_local()
    return SPC(st_val       = True,
               q            = new_q,
               t            = new_t,
               oper_timeout = 1,
               ctl_model    = CtlModelKind.direct_with_enhanced_security,
               ctl_val      = False,
               sub_ena     = False,
               sub_val     = False,
               sub_q       = new_q,
               sub_id      = "")

def test_test6_prescond(fix_test6_create_good_spc):
    pass
