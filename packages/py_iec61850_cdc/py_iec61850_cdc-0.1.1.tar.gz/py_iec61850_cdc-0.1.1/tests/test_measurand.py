import pytest

from py_iec61850_cdc.attributes import (
    AnalogueValue,
    Vector,
    Quality,
    Timestamp,
)

from py_iec61850_cdc.measurand import (
    CMV,
    DEL,
)

@pytest.fixture
def fix_test1_create_bad_del():
    new_q   = Quality()
    new_t   = Timestamp.factory_local()
    new_mag = AnalogueValue.factory(22.0)
    new_ang = AnalogueValue.factory(90.0)
    new_vec = Vector(mag=new_mag,
                     ang=new_ang)
    new_cmv = CMV(c_val   = new_vec,
                  q       = new_q,
                  t       = new_t,
                  sub_ena = False,
                  sub_c_val = new_vec,
                  sub_q   = new_q,
                  sub_id  = "")
    with pytest.raises(ValueError) as exc:
        return DEL()

def test_test1_prescond(fix_test1_create_bad_del):
    delobj= fix_test1_create_bad_del
'''
@pytest.fixture
def fix_test2_create_good_del():
    new_q = Quality()
    new_t = Timestamp.factory_local()
    return DEL(phs_ab=)

def test_test2_prescond(fix_test2_create_good_del):
    delobj= fix_test2_create_good_acd
    assert isinstance(delobj,DEL)

@pytest.fixture
def fix_test3_create_bad_del():
    new_q = Quality()
    new_t = Timestamp.factory_local()
    with pytest.raises(ValueError) as exc:
        return DEL(general   = True,
                   q         = new_q,
                   t         = new_t,
                   phs_a     = True)

def test_test3_prescond(fix_test3_create_bad_del):
    pass
'''
