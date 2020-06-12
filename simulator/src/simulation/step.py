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

from simulation.inventory import Inventory
from scenario import OperationType
from scenario import Operation
# from util import Tools
from constants import CUTTYPES_DICT

# import logging
import i18n

#TODO: This must be added to global variables
# CUTTYPES = {'PERCENTOFTREES': 'Percent of trees',
#             'VOLUME': 'Volumen',
#             'AREA': 'Area'}


class Step:

    def __init__(self,
                 id: int,
                 inventory: Inventory,
                 op: OperationType,
                 description: str,
                 age: int,
                 min_age: int,
                 max_age: int,
                 operation: Operation,
                 cut_name: str):

        self.__id = id
        self.__operation = op
        self.__description = description
        self.__inventory = inventory
        self.__age = age
        self.__min_age = min_age
        self.__max_age = max_age
        self.__years = operation.get_variable('time') if operation.has('time') else 0
        self.__cut = cut_name
        self.__quantity = operation.get_variable('volumen') if operation.has('volumen') else None
        self.__by_means = CUTTYPES_DICT[operation.get_variable('cut_down')] if operation.has('cut_down') else 'Empty'
        self.__generate_output = True
        self.__full_operation = operation

    @property
    def id(self):
        return self.__id

    @property
    def action(self):
        return self.__action

    @property
    def age(self):
        return self.__age

    @property
    def years(self):
        return self.__years

    @property
    def inventory(self):
        return self.__inventory

    @property
    def description(self):
        return self.__description

    def is_printable(self):
        return self.__generate_output

    def generate_sheet(self):
        return self.__inventory.xslt()

    def generate_json_file(self, file_path):
        return self.__inventory.json()

    def plots_to_xslt(self, workbook):
        return

    def get_plot_ids(self):
        return self.inventory.get_plot_ids()

    def to_json(self, plot_id, names, row):

        content = dict()

        values = dict()

        values[i18n.t('simanfor.general.' + names[0])] = self.__id
        values[i18n.t('simanfor.general.' + names[1])] = self.__age
        values[i18n.t('simanfor.general.' + names[2])] = self.__min_age
        values[i18n.t('simanfor.general.' + names[3])] = self.__max_age
        values[i18n.t('simanfor.general.' + names[4])] = i18n.t('simanfor.general.' + self.__operation.get_code_name())
        values[i18n.t('simanfor.general.' + names[5])] = self.__years
        values[i18n.t('simanfor.general.' + names[6])] = self.__cut
        values[i18n.t('simanfor.general.' + names[7])] = self.__quantity
        values[i18n.t('simanfor.general.' + names[8])] = i18n.t('simanfor.general.' + self.__by_means)

        content['info'] = values
        content['inventory'] = self.inventory.to_json(plot_id, None)

        return content

    def to_xslt(self, labels: dict, workbook, plot_id: int, row: int, next_step, next_operation,
                summary_row: int, decimals: int = 2):
        
        ws_parcelas = workbook[labels['simanfor.general.Plots']]

        ws_parcelas.cell(row=self.__id+1, column=1).value = self.__id
        ws_parcelas.cell(row=self.__id+1, column=2).value = self.__age
        ws_parcelas.cell(row=self.__id+1, column=3).value = self.__min_age
        ws_parcelas.cell(row=self.__id+1, column=4).value = self.__max_age
        ws_parcelas.cell(row=self.__id+1, column=5).value = labels['simanfor.general.' + self.__operation.get_code_name()]
        ws_parcelas.cell(row=self.__id+1, column=6).value = self.__years
        ws_parcelas.cell(row=self.__id+1, column=7).value = self.__cut
        ws_parcelas.cell(row=self.__id+1, column=8).value = self.__quantity
        ws_parcelas.cell(row=self.__id+1, column=9).value = labels['simanfor.general.' + self.__by_means]

        next_inventory = None if next_step is None else next_step.__inventory

        summary_row = self.__inventory.to_xslt(labels, workbook, plot_id, self.__id, next_inventory, 
                                               next_operation, self.__full_operation, summary_row, decimals)
        return summary_row
