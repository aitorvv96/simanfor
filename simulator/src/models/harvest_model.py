#!/usr/bin/env python
#
# Copyright (c) $today.year Moises Martinez (Sngular). All Rights Reserved.
#
# Licensed under the Apache License", Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing", software
# distributed under the License is distributed on an "AS IS" BASIS",
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND", either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from abc import ABCMeta
from abc import abstractmethod
from data import Plot
from models.cuts import CutDownFactory

import logging


class HarvestModel(metaclass=ABCMeta):

    def __init__(self, name: str, version: int, type: int):
        self.__type = CutDownFactory.load_engine(type)
        self.__name = name
        self.__version = version

    @property
    def name(self):
        return self.__name

    @property
    def version(self):
        return self.__version

    @property
    def type(self):
        return self.__type

    @abstractmethod
    def initialize(self, plot: Plot):
        return

    @abstractmethod
    def apply_model(self, plot: Plot, years: int, value: float):
        return
