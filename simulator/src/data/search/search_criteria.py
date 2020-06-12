#!/usr/bin/env python3
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

EQUAL = 1
LESS = 2
GREATER = 3
LESSEQUAL = 4
GREATEREQUAL = 5


class Criteria:

    def __init__(self, variable, value, comparison):
        self.__variable = variable
        self.__value = value
        self.__comparison = comparison

    @property
    def variable(self):
        return self.__variable

    @property
    def value(self):
        return self.__value

    @property
    def comparison(self):
        return self.__comparison

    def is_valid(self, value):

        if self.__comparison == EQUAL:
            return value == self.__value
        if self.__comparison == LESS:
            return value < self.__value
        if self.__comparison == GREATER:
            return value > self.__value
        if self.__comparison == LESSEQUAL:
            return value <= self.__value
        if self.__comparison == GREATEREQUAL:
            return value >= self.__value


class SearchCriteria:

    def __init__(self):
        self.__criterios = list()

    @property
    def criterion(self):
        return self.__criterios

    def add_criteria(self, variable, valor, comparison):
        self.__criterios.append(Criteria(variable, valor, comparison))
