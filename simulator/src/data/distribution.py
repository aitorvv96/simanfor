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
# ==========================================================================


class Distribution:

    def __init__(self):

        self.__diametro_menor = 0.0
        self.__diametro_mayor = 0.0
        self.__area_basimetrica_to_add = 0.0

    @property
    def diametro_menor(self):
        return self.__diametro_menor

    @property
    def diametro_mayor(self):
        return self.__diametro_mayor

    @property
    def area_basimetrica_to_add(self):
        return self.__area_basimetrica_to_add

    def set_diametro_menor(self, value):
        self.__diametro_menor = value

    def set_diametro_mayor(self, value):
        self.__diametro_mayor = value

    def set_area_basimetrica_to_add(self, value):
        self.__area_basimetrica_to_add = value
