# py_iec61850_cdc factory.py
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

# This file provides factory functions for incoming data to instantiate
# IEC 61850-7-3 objects.

from __future__ import annotations
from typing import TypeVar, NewType, Generic

from pydantic import RootModel

from py_iec61850_cdc.attributes import (
    Point,
)

from py_iec61850_cdc.controls import (
    SPC,
    APC,
    DPC,
    INC,
)
from py_iec61850_cdc.measurand import (
    CMV,
    MV,
)
from py_iec61850_cdc.status import (
    BCR,
    SPS,
)

#IECDA = TypeVar('IECDA', Point)
IECDA = NewType('IECDA',Point)
IECDO = TypeVar('IECDO',
                SPC,
                APC,
                DPC,
                INC,
                CMV,
                MV ,
                BCR,
                SPS
                )

class DAList(RootModel[IECDO]):
    root: list[IECDA]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def append(self, item):
        self.root.append(item)

class DOList(RootModel[IECDO]):
    root: list[IECDO]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def append(self, item):
        self.root.append(item)

