#!/usr/bin/env python3
#
# Copyright (c) $today.year Moisés Martínez (Sngular). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import

import os
import sys
import pytest

ROOT_FOLDER = os.getcwd()

sys.path.append(os.path.join(ROOT_FOLDER, 'src'))

from data.search import Criteria
from data.search import EQUAL
from data.search import LESS
from data.search import GREATER
from data.search import LESSEQUAL
from data.search import GREATEREQUAL


def test_init_1():

    real_input_1: str = 'VALUE1'
    real_input_2: float = 2.0
    real_input_3: int = EQUAL

    tmp_criteria = Criteria(real_input_1, real_input_2, real_input_3)
    assert isinstance(tmp_criteria, Criteria) is True


def test_init_2():

    real_input_1: str = 'VALUE1'
    real_input_2: float = 2.0
    real_input_3: int = LESS

    #TODO: Add exception here

    assert True == True


def test_variable():

        real_input_1: str = 'VALUE1'
        real_input_2: float = 2.0
        real_input_3: int = EQUAL

        tmp_criteria = Criteria(real_input_1, real_input_2, real_input_3)
        real_output: str = tmp_criteria.variable
        expected_output: str = 'VALUE1'

        assert real_output == expected_output


def test_value():

    real_input_1: str = 'VALUE1'
    real_input_2: float = 2.0
    real_input_3: int = GREATER

    tmp_criteria = Criteria(real_input_1, real_input_2, real_input_3)
    real_output: float = tmp_criteria.value
    expected_output: float = 2.0

    assert real_output == expected_output


def test_comparison():

    real_input_1: str = 'VALUE1'
    real_input_2: float = 2.0
    real_input_3: int = LESSEQUAL

    tmp_criteria = Criteria(real_input_1, real_input_2, real_input_3)
    real_output: int = tmp_criteria.comparison
    expected_output: int = LESSEQUAL

    assert real_output == expected_output


def test_is_valid():

    real_input_1: str = 'VALUE1'
    real_input_2: float = 2.0
    real_input_3: int = LESS
    real_input_4: float = 1.0

    tmp_criteria = Criteria(real_input_1, real_input_2, real_input_3)
    real_output: bool = tmp_criteria.is_valid(real_input_4)
    expected_output: bool = True

    assert real_output == expected_output


def test_is_not_valid():

    real_input_1: str = 'VALUE1'
    real_input_2: float = 2.0
    real_input_3: int = LESS
    real_input_4: float = 5.0

    tmp_criteria = Criteria(real_input_1, real_input_2, real_input_3)
    real_output: bool = tmp_criteria.is_valid(real_input_4)
    expected_output: bool = False

    assert real_output == expected_output
