# Tests attribute function and validation.

import pytest

from datetime import datetime, timezone

from pydantic import ValidationError

from py_iec61850_cdc.attributes import (
    AnalogueValue,
    AnalogueValueCtl,
    RangeConfig,
    Vector,
    CalendarTime
)
from py_iec61850_cdc.basetypes import FLOAT32, INT32
from py_iec61850_cdc.enums import ValidityKind


# Test the "i or f" validator.
def test_analogue_i_or_f():
    with pytest.raises(ValidationError) as exc:
        myobj=AnalogueValue()

# Test instantiating with f only
@pytest.fixture
def fix_analoguetestf():
    return AnalogueValue(f=0.0)

def test_analoguevaluef(fix_analoguetestf):
    myobj = fix_analoguetestf
    # myobj.i should be None
    assert myobj.i is None
    myobj.f = 0.0
    assert type(myobj.f) is FLOAT32.__origin__

# Test instantiating with i only
@pytest.fixture
def fix_analoguetesti():
    return AnalogueValue(i=0)

def test_analoguevaluei(fix_analoguetesti):
    myobj = fix_analoguetesti
    # myobj.i should be None
    assert myobj.f is None
    myobj.i = 0
    assert type(myobj.i) is INT32.__origin__

# Test > comparison with aligned f and i
@pytest.fixture
def get_big_analoguevalue():
    return AnalogueValue(i=50,f=50.0)

@pytest.fixture
def get_small_analoguevalue():
    return AnalogueValue(i=25,f=25.0)

@pytest.fixture
def get_wonkyf_analoguevalue():
    return AnalogueValue(i=50,f=0.0)

@pytest.fixture
def get_wonkyi_analoguevalue():
    return AnalogueValue(i=0,f=50.0)

def test_analoguevalue_gt1(get_big_analoguevalue,get_small_analoguevalue):
    bigobj = get_big_analoguevalue
    smallobj = get_small_analoguevalue
    assert bigobj > smallobj

def test_analoguevalue_gt2(get_wonkyf_analoguevalue,get_small_analoguevalue):
    bigobj = get_wonkyf_analoguevalue
    smallobj = get_small_analoguevalue
    with pytest.raises(ValueError) as exc:
        assert bigobj > smallobj

def test_analoguevalue_gt3(get_wonkyi_analoguevalue,get_small_analoguevalue):
    bigobj = get_wonkyi_analoguevalue
    smallobj = get_small_analoguevalue
    with pytest.raises(ValueError) as exc:
        assert bigobj > smallobj

def test_analoguevalue_lt1(get_big_analoguevalue,get_small_analoguevalue):
    bigobj = get_big_analoguevalue
    smallobj = get_small_analoguevalue
    assert smallobj < bigobj

def test_analoguevalue_ge(get_big_analoguevalue,get_small_analoguevalue):
    bigobj = get_big_analoguevalue
    smallobj = get_small_analoguevalue
    assert bigobj >= smallobj

def test_analoguevalue_le(get_big_analoguevalue,get_small_analoguevalue):
    bigobj = get_big_analoguevalue
    smallobj = get_small_analoguevalue
    assert smallobj <= bigobj

@pytest.fixture
def get_small_analoguevalue_ionly():
    return AnalogueValue(i=0)

def test_analoguevalue_gt_ionly(get_big_analoguevalue,get_small_analoguevalue_ionly):
    bigobj = get_big_analoguevalue
    smallobj = get_small_analoguevalue_ionly
    assert bigobj > smallobj

@pytest.fixture
def get_small_analoguevalue_fonly():
    return AnalogueValue(f=0.0)

def test_analoguevalue_gt_fonly(get_big_analoguevalue,get_small_analoguevalue_fonly):
    bigobj = get_big_analoguevalue
    smallobj = get_small_analoguevalue_fonly
    assert bigobj > smallobj

# Test the "i or f" validator.
def test_analoguectl_i_or_f():
    with pytest.raises(ValidationError) as exc:
        myobj=AnalogueValueCtl()

# Test the "i and f" validator.
def test_analoguectl_i_and_f():
    with pytest.raises(ValidationError) as exc:
        myobj=AnalogueValueCtl(i=0,f=0.0)

# Test instantiating with f only
@pytest.fixture
def fix_analoguectltestf():
    return AnalogueValue(f=0.0)

def test_analoguevaluectlf(fix_analoguectltestf):
    myobj = fix_analoguectltestf
    # myobj.i should be None
    assert myobj.i is None
    myobj.f = 0.0
    assert type(myobj.f) is FLOAT32.__origin__

# Test instantiating with i only
@pytest.fixture
def fix_analoguectltesti():
    return AnalogueValue(i=0)

def test_analoguevaluectli(fix_analoguectltesti):
    myobj = fix_analoguectltesti
    # myobj.i should be None
    assert myobj.f is None
    myobj.i = 0
    assert type(myobj.i) is INT32.__origin__

# Test > comparison with aligned f and i
@pytest.fixture
def get_big_analoguevaluectl_i():
    return AnalogueValueCtl(i=50)

@pytest.fixture
def get_small_analoguevaluectl_i():
    return AnalogueValueCtl(i=25)

@pytest.fixture
def get_big_analoguevaluectl_f():
    return AnalogueValueCtl(f=50.0)

@pytest.fixture
def get_small_analoguevaluectl_f():
    return AnalogueValueCtl(f=25.0)

def test_analoguevaluectl_i_gt(get_big_analoguevaluectl_i,get_small_analoguevaluectl_i):
    bigobj = get_big_analoguevaluectl_i
    smallobj = get_small_analoguevaluectl_i
    assert bigobj > smallobj

def test_analoguevaluectl_f_gt(get_big_analoguevaluectl_f,get_small_analoguevaluectl_f):
    bigobj = get_big_analoguevaluectl_f
    smallobj = get_small_analoguevaluectl_f
    assert bigobj > smallobj

def test_analoguevaluectl_mix1_gt(get_big_analoguevaluectl_i,get_small_analoguevaluectl_f):
    bigobj = get_big_analoguevaluectl_i
    smallobj = get_small_analoguevaluectl_f
    with pytest.raises(ValueError) as exc:
        assert bigobj > smallobj

def test_analoguevaluectl_mix2_gt(get_big_analoguevaluectl_f,get_small_analoguevaluectl_i):
    bigobj = get_big_analoguevaluectl_f
    smallobj = get_small_analoguevaluectl_i
    with pytest.raises(ValueError) as exc:
        assert bigobj > smallobj

@pytest.fixture
def get_qualtest_rangec():
    return RangeConfig(maximum = AnalogueValue(i=9),
                       hh_lim  = AnalogueValue(i=6),
                       h_lim   = AnalogueValue(i=3),
                       l_lim   = AnalogueValue(i=-3),
                       ll_lim  = AnalogueValue(i=-6),
                       minimum = AnalogueValue(i=-9))

@pytest.fixture
def get_undermin_analoguevalue():
    return AnalogueValue(i=-10)

@pytest.fixture
def get_overmax_analoguevalue():
    return AnalogueValue(i=10)

@pytest.fixture
def get_mid_analoguevalue():
    return AnalogueValue(i=0)

def test_rangec_normal(get_qualtest_rangec,get_mid_analoguevalue):
    rangeobject = get_qualtest_rangec
    av = get_mid_analoguevalue
    validity, detailqual = rangeobject.check_quality(av)
    assert validity == ValidityKind.good
    assert not detailqual.out_of_range

def test_rangec_undermin(get_qualtest_rangec,get_undermin_analoguevalue):
    rangeobject = get_qualtest_rangec
    av = get_undermin_analoguevalue
    validity, detailqual = rangeobject.check_quality(av)
    assert validity == ValidityKind.questionable
    assert detailqual.out_of_range

def test_rangec_overmax(get_qualtest_rangec,get_overmax_analoguevalue):
    rangeobject = get_qualtest_rangec
    av = get_overmax_analoguevalue
    validity, detailqual = rangeobject.check_quality(av)
    assert validity == ValidityKind.questionable
    assert detailqual.out_of_range

@pytest.fixture
def get_345_vector():
    return Vector.factory_from_xy(x=3,y=4)

def test_vector_xy_345(get_345_vector):
    vec = get_345_vector
    assert round(vec.x()) == 3
    assert round(vec.y()) == 4

def test_calendar_factorynow():
    nowtime = datetime.now(timezone.utc)

    cal = CalendarTime.factory_from_py_datetime(py_datetime = nowtime)
    date = cal.to_py_datetime()

    assert nowtime.year   == date.year
    assert nowtime.month  == date.month
    assert nowtime.day    == date.day
    assert nowtime.hour   == date.hour
    assert nowtime.minute == date.minute

