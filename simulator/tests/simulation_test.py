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

from simulation import Simulation


def test_init():

    tmp_operation_type = Simulation()
    assert isinstance(tmp_operation_type, Simulation) is True