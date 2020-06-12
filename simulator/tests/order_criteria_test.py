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

from data.search import OrderCriteria
from data.search import ASC
from data.search import DESC


def test_init():

    tmp_order_criteria = OrderCriteria()
    assert isinstance(tmp_order_criteria, OrderCriteria) is True


def test_type_without_value():

    tmp_order_criteria = OrderCriteria()
    real_output: int = tmp_order_criteria.type
    expected_output: int = DESC

    assert real_output == expected_output


def test_type_with_value():

    real_input: int = ASC

    tmp_order_criteria = OrderCriteria(real_input)
    real_output: int = tmp_order_criteria.type
    expected_output: int = ASC

    assert real_output == expected_output


def test_criterion_1():

    real_input: str = 'VALUE'

    tmp_order_criteria = OrderCriteria()
    tmp_order_criteria.add_criteria(real_input)
    real_output: list = tmp_order_criteria.criterion
    expected_output: list = [real_input]

    assert real_output == expected_output


def test_criterion_2():

    real_input_1: str = 'VALUE1'
    real_input_2: str = 'VALUE2'

    tmp_order_criteria = OrderCriteria()
    tmp_order_criteria.add_criteria(real_input_1)
    tmp_order_criteria.add_criteria(real_input_2)
    real_output: list = tmp_order_criteria.criterion
    expected_output: list = [real_input_1, real_input_2]

    assert real_output == expected_output


def test_get_criteria_1():

    real_input: str = 'VALUE'

    tmp_order_criteria = OrderCriteria()
    tmp_order_criteria.add_criteria(real_input)
    real_output: str = tmp_order_criteria.get_criteria(0)
    expected_output: str = 'VALUE'

    assert real_output == expected_output


def test_get_criteria_2():

    real_input_1: str = 'VALUE1'
    real_input_2: str = 'VALUE2'
    real_input_3: str = 'VALUE3'

    tmp_order_criteria = OrderCriteria()
    tmp_order_criteria.add_criteria(real_input_1)
    tmp_order_criteria.add_criteria(real_input_2)
    tmp_order_criteria.add_criteria(real_input_3)
    real_output: str = tmp_order_criteria.get_criteria(2)
    expected_output: str = 'VALUE3'

    assert real_output == expected_output

def test_get_criteria_2():

    real_input_1: str = 'VALUE1'
    real_input_2: str = 'VALUE2'
    real_input_3: str = 'VALUE3'

    tmp_order_criteria = OrderCriteria()
    tmp_order_criteria.add_criteria(real_input_1)
    tmp_order_criteria.add_criteria(real_input_2)
    tmp_order_criteria.add_criteria(real_input_3)
    real_output: str = tmp_order_criteria.get_criteria(5)
    expected_output: str = None

    assert real_output == expected_output

def test_get_first_1():

    real_input_1: str = 'VALUE1'

    tmp_order_criteria = OrderCriteria()
    tmp_order_criteria.add_criteria(real_input_1)
    real_output: str = tmp_order_criteria.get_first()
    expected_output: str = 'VALUE1'

    assert real_output == expected_output


def test_get_first_2():

    real_input_1: str = 'VALUE0'
    real_input_2: str = 'VALUE1'

    tmp_order_criteria = OrderCriteria()
    tmp_order_criteria.add_criteria(real_input_1)
    tmp_order_criteria.add_criteria(real_input_2)
    real_output: str = tmp_order_criteria.get_first()
    expected_output: str = 'VALUE0'

    assert real_output == expected_output


def test_get_len():

    real_input_1: str = 'VALUE0'
    real_input_2: str = 'VALUE1'

    tmp_order_criteria = OrderCriteria()
    tmp_order_criteria.add_criteria(real_input_1)
    tmp_order_criteria.add_criteria(real_input_2)
    real_output: int = tmp_order_criteria.len()
    expected_output: int = 2

    assert real_output == expected_output
