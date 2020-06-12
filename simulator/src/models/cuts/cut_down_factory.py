#!/usr/bin/env python
#
# Copyright (c) $today.year Moises Martinez (Sngular). All Rights Reserved.
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

from .percent_of_trees import PercentOfTrees
from .volumen import Volumen
from .area import Area
# from .cut_down import CUTTYPES
from constants import CUTTYPES_LIST


class CutDownFactory:

    @staticmethod
    def load_engine(type_engine, configuration=None):

        engine = 0

        for i in range(len(CUTTYPES_LIST)):
            if CUTTYPES_LIST[i][0] == type_engine:
                engine = i

        if engine == 0:
            return PercentOfTrees()

        if engine == 1:
            return Volumen()

        if engine == 2:
            return Area()

        return PercentOfTrees(configuration)
