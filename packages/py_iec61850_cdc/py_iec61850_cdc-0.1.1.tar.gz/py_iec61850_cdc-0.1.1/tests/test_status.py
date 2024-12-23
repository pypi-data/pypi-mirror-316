import pytest

from py_iec61850_cdc.attributes import (
    Quality,
    Timestamp,
)

from py_iec61850_cdc.enums import (
    PhaseFaultDirectionKind,
)

from py_iec61850_cdc.status import (
    ACD,
    BCR,
)

@pytest.fixture
def fix_test1_create_bad_acd():
    with pytest.raises(ValueError) as exc:
        return ACD(phs_a=True)

def test_test1_prescond(fix_test1_create_bad_acd):
    acdobj= fix_test1_create_bad_acd

@pytest.fixture
def fix_test2_create_good_acd():
    new_q = Quality()
    new_t = Timestamp.factory_local()
    return ACD(general   = True,
               q         = new_q,
               t         = new_t)

def test_test2_prescond(fix_test2_create_good_acd):
    acdobj= fix_test2_create_good_acd
    assert isinstance(acdobj,ACD)

@pytest.fixture
def fix_test3_create_bad_acd():
    new_q = Quality()
    new_t = Timestamp.factory_local()
    with pytest.raises(ValueError) as exc:
        return ACD(general   = True,
                   q         = new_q,
                   t         = new_t,
                   phs_a     = True)

def test_test3_prescond(fix_test3_create_bad_acd):
    pass

@pytest.fixture
def fix_test4_create_bad_bcr():
    new_q = Quality()
    with pytest.raises(ValueError) as exc:
        return BCR(puls_qty = 1.0,
                   q        = new_q)


def test_test4_prescond(fix_test4_create_bad_bcr):
    pass

@pytest.fixture
def fix_test5_create_bad_bcr():
    new_q = Quality()
    with pytest.raises(ValueError) as exc:
        return BCR(puls_qty = 1.0,
                   q        = new_q,
                   fr_val   = 62)

def test_test5_prescond(fix_test5_create_bad_bcr):
    new_q = Quality()
    with pytest.raises(ValueError) as exc:
        return BCR(puls_qty = 1.0,
                   q        = new_q,
                   act_val  = 62)

@pytest.fixture
def fix_test6_create_bad_bcr():
    pass

def test_test6_prescond(fix_test6_create_bad_bcr):
    pass

@pytest.fixture
def fix_test7_create_good_bcr():
    new_q  = Quality()
    new_tm = Timestamp.factory_local()
    with pytest.raises(ValueError) as exc:
        return BCR(puls_qty = 1.0,
                   q        = new_q,
                   fr_val   = 62,
                   fr_tm    = new_tm,
                   fr_ena   = False,
                   fr_pd    = 32,
                   fr_rs    = False)

def test_test7_prescond(fix_test7_create_good_bcr):
    pass

@pytest.fixture
def fix_test8_create_good_bcr():
    new_q = Quality()
    new_tm = Timestamp.factory_local()
    with pytest.raises(ValueError) as exc:
        return BCR(puls_qty = 1.0,
                   q        = new_q,
                   act_val  = 62,
                   t        = new_tm)

def test_test8_prescond(fix_test8_create_good_bcr):
    pass

