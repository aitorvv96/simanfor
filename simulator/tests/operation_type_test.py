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

from scenario import OperationType


def test_init():

    real_input: str = 'INIT'

    tmp_operation_type = OperationType(real_input)
    assert isinstance(tmp_operation_type, OperationType) is True


def test_action():

    real_input: str = 'INIT'

    tmp_operation_type = OperationType(real_input)
    real_output: int = tmp_operation_type.action
    expected_output: int = 2

    assert real_output == expected_output


def test_get_name():

    real_input: str = 'INIT'

    tmp_operation_type = OperationType(real_input)
    real_output: str = tmp_operation_type.get_name()
    expected_output: str = 'Inicialización de datos'

    assert real_output == expected_output


def test_get_code_name():

    real_input: str = 'INIT'

    tmp_operation_type = OperationType(real_input)
    real_output: str = tmp_operation_type.get_code_name()
    expected_output: str = 'INIT'

    assert real_output == expected_output


def test_get_avaliable_operations():

    real_output = OperationType.get_avaliable_operations()
    expected_output: tuple = ('NOOP', 'Operación Nula')

    assert real_output[0] == expected_output


def test_get_avaliable_operations_length():

    real_output = len(OperationType.get_avaliable_operations())
    expected_output: int = 5

    assert real_output == expected_output
