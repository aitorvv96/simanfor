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

from engine.engines.basic_engine import BasicEngine
from engine.engines.dask_engine import DaskEngine
from util import Tools

import platform
import logging

MACHINE = 0
CLUSTER = 1
SUPER = 2

ENGINES = enumerate(['MACHINE', 'CLUSTER', 'SUPER'])


class EngineFactory:

    @staticmethod
    def load_engine(type_engine, configuration=None):

        engine = -1

        for key, value in ENGINES:
            if key == type_engine:
                engine = key

        if engine == 0:
            return BasicEngine(configuration)

        if engine == 1:
            return BasicEngine(configuration)

        if engine == 2:
            if platform.system() == 'Windows':
                Tools.print_log_line('Windows os system does not support DASK engine, using default', logging.WARNING)
                return BasicEngine(configuration)
            else:
                return DaskEngine(configuration)

        return BasicEngine(configuration)
