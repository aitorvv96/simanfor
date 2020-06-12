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

DESC = 1
ASC = 2


class OrderCriteria:

    def __init__(self, type=DESC):
        self.__criterion = list()
        self.__type = type

    @property
    def type(self):
        return self.__type

    @property
    def criterion(self):
        return self.__criterion

    def add_criteria(self, variable: str):
        self.__criterion.append(variable)

    def get_criteria(self, position: int):
        if position < len(self.__criterion):
            return self.__criterion[position]
        return None

    def get_first(self):
        return self.__criterion[0]

    def len(self):
        return len(self.criterion)
