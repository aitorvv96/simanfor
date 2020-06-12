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

from util import Tools

import logging


NOOP = 0
LOAD = 1
INIT = 2
EXECUTION = 3
HARVEST = 4


OPERATIONS = [('NOOP', 'Operación Nula'), ('LOAD', 'Carga de datos'), ('INIT', 'Inicialización de datos'), ('EXECUTION', 'Ejecución de modelo'), ('HARVEST', 'Corta')]


class OperationType:

    @staticmethod
    def get_avaliable_operations():
        return OPERATIONS

    def get_operation_code(self, action: str):
        op_upper = action.upper()
        for i in range(len(OPERATIONS)):
            if op_upper == OPERATIONS[i][0]:
                return i

    def __init__(self, operation: str = None):
        self.__op: str = self.get_operation_code(operation)

    @property
    def action(self):
        return self.__op

    def get_name(self):
        return OPERATIONS[self.__op][1]

    def get_code_name(self):
        return OPERATIONS[self.__op][0]


class Operation:

    def __init__(self, configuration=None):

        if configuration is not None:

            self.__name = configuration['name']
            self.__description = configuration['description']
            self.__type = OperationType(configuration['operation'])
            self.__model_path = configuration['model_path']
            self.__model_class = configuration['model_class']
            self.__variables = dict()

            for variable, value in configuration['variables'].items():
                self.__variables[variable] = value
        else:
            Tools.print_log_line('No configuration info for operation', logging.ERROR)

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def type(self):
        return self.__type

    @property
    def model_path(self):
        return self.__model_path

    @property
    def model_class(self):
        return self.__model_class

    @property
    def variables(self):
        return  self.__variables

    def get_variable(self, name):
        if name in self.__variables.keys():
            return self.__variables[name]
        Tools.print_log_line('Variable ' + name + ' is not defined into operation ' + self.__name, logging.INFO)
        return None

    def add_variable(self, variable, value):
        self.__variables[variable] = value

    def has(self, variable):
        return variable in self.__variables.keys()
