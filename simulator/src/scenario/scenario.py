#!/usr/bin/env python3
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

from .operation import Operation
from util import Tools

import logging
import json


class Scenario:

    def __init__(self, configuration_file=None):

        self.__operations = list()

        if configuration_file is not None:
            with open(configuration_file, 'r', encoding='utf-8', errors='ignore') as f:

                configuration = json.loads(f.read())

                self.__name = configuration['name']
                self.__overwrite_output_file = True if configuration['operations'] == "YES" else False
                self.__output_path = configuration['output_path']
                self.__zip_compression = True if configuration['zip_compression'] == "YES" else False
                #TODO: THE VALUE 0 MUST A GLOBAL VALUE
                self.__ext = 0 if 'output_type' not in configuration.keys() else configuration['output_type']
                self.__decimal_numbers = configuration['decimal_numbers']

                for item in configuration['operations'].values():
                    self.__operations.append(Operation(item))
                    if item['operation'] == 'INIT':
                        self.__modelo = item['model_path']
        else:
            Tools.print_log_line('No configuration file provided.', logging.WARNING)

    @property
    def operations(self):
        return self.__operations

    def add_operator(self, operation: Operation):
        self.__operations.append(operation)

    @property
    def overwrite_output_file(self):
        return self.__overwrite_output_file

    @property
    def output_path(self):
        return self.__output_path

    @property
    def zip_compression(self):
        return self.__zip_compression

    @property
    def decimal_numbers(self):
        return self.__decimal_numbers

    @property
    def modelo(self):
        return self.__modelo

    @property
    def name(self):
        return self.__name

    @property
    def ext(self):
        return self.__ext
