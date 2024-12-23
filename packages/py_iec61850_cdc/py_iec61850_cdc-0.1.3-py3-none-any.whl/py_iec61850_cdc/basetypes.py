# py_iec61850_cdc basetypes.py
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

# This file provides the basic IEC types described under clause 6.2.2 of
# IEC 61850-7-2:2010+AMD1:2020 CSV as a Python class. The types are
# deliberately cast to Python types using NewType, mostly so the documentation
# can follow the standard. In reality, simple Python types are used.

# Some helper functions are provided to set up Pydantic Fields in other files.

from __future__ import annotations

from typing import Annotated, NewType

from pydantic import AfterValidator

# BOOLEAN - IEC 61850-7-2 6.2.2.2
BOOLEAN        = NewType('BOOLEAN',bool)

# INT8 - IEC 61850-7-2 6.2.2.3
INT8_MIN_VALUE = -128
INT8_MAX_VALUE = 127

def int8_minmax_after_validator(value: int) -> int:
    if value < INT8_MIN_VALUE:
        raise ValueError(f'{value} is lower than allowable minimum for INT32U')
    elif value > INT8_MAX_VALUE:
        raise ValueError(f'{value} is greater than allowable maximum for INT32U')
    return value

INT8 = Annotated[int, AfterValidator(int8_minmax_after_validator)]


# INT16 - IEC 61850-7-2 6.2.2.4
INT16_MIN_VALUE = -32768
INT16_MAX_VALUE = 32767

def int16_minmax_after_validator(value: int) -> int:
    if value < INT16_MIN_VALUE:
        raise ValueError(f'{value} is lower than allowable minimum for INT32U')
    elif value > INT16_MAX_VALUE:
        raise ValueError(f'{value} is greater than allowable maximum for INT32U')
    return value

INT16 = Annotated[int, AfterValidator(int16_minmax_after_validator)]


# INT32 - IEC 61850-7-2 6.2.2.5
INT32_MIN_VALUE = -2147483648
INT32_MAX_VALUE = 2147483647

def int32_minmax_after_validator(value: int) -> int:
    if value < INT32_MIN_VALUE:
        raise ValueError(f'{value} is lower than allowable minimum for INT32U')
    elif value > INT32_MAX_VALUE:
        raise ValueError(f'{value} is greater than allowable maximum for INT32U')
    return value

INT32 = Annotated[int, AfterValidator(int32_minmax_after_validator)]


# INT64 - IEC 61850-7-2 6.2.2.6
INT64_MIN_VALUE = -2**63
INT64_MAX_VALUE = (2**63)-1

def int64_minmax_after_validator(value: int) -> int:
    if value < INT64_MIN_VALUE:
        raise ValueError(f'{value} is lower than allowable minimum for INT32U')
    elif value > INT64_MAX_VALUE:
        raise ValueError(f'{value} is greater than allowable maximum for INT32U')
    return value

INT64 = Annotated[int, AfterValidator(int64_minmax_after_validator)]


# INT8U - IEC 61850-7-2 6.2.2.7
INT8U_MIN_VALUE = 0
INT8U_MAX_VALUE = 255

def int8u_minmax_after_validator(value: int) -> int:
    if value < INT8U_MIN_VALUE:
        raise ValueError(f'{value} is lower than allowable minimum for INT32U')
    elif value > INT8U_MAX_VALUE:
        raise ValueError(f'{value} is greater than allowable maximum for INT32U')
    return value

INT8U = Annotated[int, AfterValidator(int8u_minmax_after_validator)]


# INT16U - IEC 61850-7-2 6.2.2.8
INT16U_MIN_VALUE = 0
INT16U_MAX_VALUE = 65535

def int16u_minmax_after_validator(value: int) -> int:
    if value < INT16U_MIN_VALUE:
        raise ValueError(f'{value} is lower than allowable minimum for INT32U')
    elif value > INT16U_MAX_VALUE:
        raise ValueError(f'{value} is greater than allowable maximum for INT32U')
    return value

INT16U = Annotated[int, AfterValidator(int16u_minmax_after_validator)]


# INT24U - IEC 61850-7-2 6.2.2.9
INT24U_MIN_VALUE = 0
INT24U_MAX_VALUE = 16777215

def int24u_minmax_after_validator(value: int) -> int:
    if value < INT24U_MIN_VALUE:
        raise ValueError(f'{value} is lower than allowable minimum for INT32U')
    elif value > INT24U_MAX_VALUE:
        raise ValueError(f'{value} is greater than allowable maximum for INT32U')
    return value

INT24U = Annotated[int, AfterValidator(int24u_minmax_after_validator)]


# INT32U - IEC 61850-7-2 6.2.2.10
INT32U_MIN_VALUE = 0
INT32U_MAX_VALUE = 4294967295

def int32u_minmax_after_validator(value: int) -> int:
    if value < INT32U_MIN_VALUE:
        raise ValueError(f'{value} is lower than allowable minimum for INT32U')
    elif value > INT32U_MAX_VALUE:
        raise ValueError(f'{value} is greater than allowable maximum for INT32U')
    return value

INT32U = Annotated[int, AfterValidator(int32u_minmax_after_validator)]

# FLOAT32 - IEC 61850-7-2 6.2.2.11
FLOAT32_MIN_VALUE = -3.40*(10**38)
FLOAT32_MAX_VALUE = 3.40*(10**38)

def float32_minmax_after_validator(value: float) -> float:
    if value < FLOAT32_MIN_VALUE:
        raise ValueError(f'{value} is lower than allowable minimum for FLOAT32')
    elif value > FLOAT32_MAX_VALUE:
        raise ValueError(f'{value} is greater than allowable maximum for FLOAT32')
    return value

FLOAT32 = Annotated[float, AfterValidator(float32_minmax_after_validator)]

# OCTET64 - IEC 61850-7-2 6.2.2.12
def octet64_length_after_validator(value: str) -> str:
    if len(value) > 64:
        raise ValueError(f'"{value}" has more than 64 characters.)')
    return value

Octet64 = Annotated[str, AfterValidator(octet64_length_after_validator)]

# VISSTRING64 - IEC 61850-7-2 6.2.2.13
def visstring64_length_after_validator(value: str) -> str:
    if len(value) > 64:
        raise ValueError(f'"{value}" has more than 64 characters.)')
    return value

VisString64 = Annotated[str, AfterValidator(visstring64_length_after_validator)]


# VISSTRING129 - IEC 61850-7-2 6.2.2.14
def visstring129_length_after_validator(value: str) -> str:
    if len(value) > 129:
        raise ValueError(f'"{value}" has more than 129 characters.)')
    return value

VisString129 = Annotated[str, AfterValidator(visstring129_length_after_validator)]


# VISSTRING255 - IEC 61850-7-2 6.2.2.15
def visstring255_length_after_validator(value: str) -> str:
    if len(value) > 255:
        raise ValueError(f'"{value}" has more than 255 characters.)')
    return value

VisString255 = Annotated[str, AfterValidator(visstring255_length_after_validator)]


# UNICODE255 - IEC 61850-7-2 6.2.2.16
def unicode255_length_after_validator(value: str) -> str:
    if len(value) > 255:
        raise ValueError(f'"{value}" has more than 255 characters.)')
    return value

Unicode255 = Annotated[str, AfterValidator(unicode255_length_after_validator)]


# OBJECTREFERENCE - IEC 61850-7-2 6.2.3.4
ObjectReference = NewType('ObjectReference',VisString129)
def octet64_length_after_validator(value: str) -> str:
    if len(value) > 64:
        raise ValueError(f'"{value}" has more than 64 characters.)')
    return value

Octet64 = Annotated[str, AfterValidator(octet64_length_after_validator)]


# PHYCOMADDR - IEC 61850-7-2 6.2.3.2
PhyComAddr   = NewType('PhyComAddr',str)
def octet64_length_after_validator(value: str) -> str:
    if len(value) > 64:
        raise ValueError(f'"{value}" has more than 64 characters.)')
    return value

Octet64 = Annotated[str, AfterValidator(octet64_length_after_validator)]


# ENTRYID - IEC 61850-7-2 6.2.3.5
EntryID      = NewType('EntryID',str)
def octet64_length_after_validator(value: str) -> str:
    if len(value) > 64:
        raise ValueError(f'"{value}" has more than 64 characters.)')
    return value

Octet64 = Annotated[str, AfterValidator(octet64_length_after_validator)]


# List below sourced from Wikipedia rather than
# the actual standard.  Apologies for errors.
ISO4217_CURRENCY_LIST = [
    "AED",
    "AFN",
    "ALL",
    "AMD",
    "ANG",
    "AOA",
    "ARS",
    "AUD",
    "AWG",
    "AZN",
    "BAM",
    "BBD",
    "BDT",
    "BGN",
    "BHD",
    "BIF",
    "BMD",
    "BND",
    "BOB",
    "BOV",
    "BRL",
    "BSD",
    "BTN",
    "BWP",
    "BYN",
    "BZD",
    "CAD",
    "CDF",
    "CHE",
    "CHF",
    "CHW",
    "CLF",
    "CLP",
    "CNY",
    "COP",
    "COU",
    "CRC",
    "CUP",
    "CVE",
    "CZK",
    "DJF",
    "DKK",
    "DOP",
    "DZD",
    "EGP",
    "ERN",
    "ETB",
    "EUR",
    "FJD",
    "FKP",
    "GBP",
    "GEL",
    "GHS",
    "GIP",
    "GMD",
    "GNF",
    "GTQ",
    "GYD",
    "HKD",
    "HNL",
    "HTG",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "IQD",
    "IRR",
    "ISK",
    "JMD",
    "JOD",
    "JPY",
    "KES",
    "KGS",
    "KHR",
    "KMF",
    "KPW",
    "KRW",
    "KWD",
    "KYD",
    "KZT",
    "LAK",
    "LBP",
    "LKR",
    "LRD",
    "LSL",
    "LYD",
    "MAD",
    "MDL",
    "MGA",
    "MKD",
    "MMK",
    "MNT",
    "MOP",
    "MRU",
    "MUR",
    "MVR",
    "MWK",
    "MXN",
    "MXV",
    "MYR",
    "MZN",
    "NAD",
    "NGN",
    "NIO",
    "NOK",
    "NPR",
    "NZD",
    "OMR",
    "PAB",
    "PEN",
    "PGK",
    "PHP",
    "PKR",
    "PLN",
    "PYG",
    "QAR",
    "RON",
    "RSD",
    "RUB",
    "RWF",
    "SAR",
    "SBD",
    "SCR",
    "SDG",
    "SEK",
    "SGD",
    "SHP",
    "SLE",
    "SOS",
    "SRD",
    "SSP",
    "STN",
    "SVC",
    "SYP",
    "SZL",
    "THB",
    "TJS",
    "TMT",
    "TND",
    "TOP",
    "TRY",
    "TTD",
    "TWD",
    "TZS",
    "UAH",
    "UGX",
    "USD",
    "USN",
    "UYI",
    "UYU",
    "UYW",
    "UZS",
    "VED",
    "VES",
    "VND",
    "VUV",
    "WST",
    "XAF",
    "XAG",
    "XAU",
    "XBA",
    "XBB",
    "XBC",
    "XBD",
    "XCD",
    "XDR",
    "XOF",
    "XPD",
    "XPF",
    "XPT",
    "XSU",
    "XTS",
    "XUA",
    "XXX",
    "YER",
    "ZAR",
    "ZMW",
    "ZWG"
]

# CURRENCY - IEC 61850-7-2 6.2.3.6
def currency_content_after_validator(value: str) -> str:
    if value not in ISO4217_CURRENCY_LIST:
        raise ValueError(f'"{value}" is not a valid currency code.')
    return value

Currency = Annotated[str, AfterValidator(currency_content_after_validator)]



