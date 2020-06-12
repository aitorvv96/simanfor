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

from data import Tree
from util import Tools
from data import Plot
from datetime import datetime
from reader import ExcelReader, JSONReader

import logging

from scenario import Operation


PARCEL_CODE = 'Parcelas'
TREE_CODE = 'PiesMayores'


class Inventory:

    def __init__(self, reader=None, date=datetime.now()):

        self.__date = date
        self.__plots = dict()
        self.__plots_to_print = dict()

        if reader is None:
            Tools.print_log_line("No reader information, generated empty plots list", logging.WARNING)

        elif isinstance(reader, ExcelReader):
            reader.choose_sheet(PARCEL_CODE, True)

            for plot in reader:
                p = Plot(plot)
                self.__plots[p.id] = p
                self.__plots_to_print[p.id] = True

            reader.choose_sheet(TREE_CODE, True)

            for data in reader:
                tree = Tree(data)
                plot_id = tree.get_value('PLOT_ID')
                self.__plots[plot_id].add_tree(tree)

        elif isinstance(reader, JSONReader):

            reader.choose_sheet('plots', True)

            for plot in reader:
                p = Plot(plot)
                self.__plots[p.id] = p
                self.__plots_to_print[p.id] = True

            reader.choose_sheet('trees', True)

            for data in reader:
                tree = Tree(data)
                plot_id = tree.get_value('PLOT_ID', True) # True, it's in json format
                self.__plots[plot_id].add_tree(tree)


    @property
    def plots(self):
        return self.__plots.values()

    @property
    def empty(self):
        return len(self.__plots) == 0

    @property
    def date(self):
        return self.__date

    def must_be_printed(self, id_plot):
        return self.__plots_to_print[id_plot]

    def get_number_plots(self):
        return len(self.__plots)

    def get_plot_ids(self):
        return self.__plots.keys()

    def add_plot(self, plot: Plot, print: bool = True):
        self.__plots[plot.id] = plot
        self.__plots_to_print[plot.id] = print


    def add_plots(self, plots: list):
        
        count = 0
        for plot in plots:
            count += 1
            self.add_plot(plot)
            
        return self


    def get_plot(self, position: int):
        if self.get_number_plots() > position:
            count: int = 0
            for value in self.__plots.values():
                if count == position:
                    return value
                count += 1
        return None

    def get_first_plot(self):
        return self.get_plot(0)

    def get_tree(self, plot_id: str, tree_id: str):
        if plot_id in self.__plots.keys():
            return self.__plots[plot_id].get_tree(tree_id)
        else:
            Tools.print_log_line("There is not any plot with id " + str(plot_id), logging.ERROR)
            return None

    def clone(self, inventory):

        self.__date = datetime.now()

        for plot in inventory.plots:
            new_plot: Plot = plot.clone(plot)
            self.__plots[new_plot.id] = new_plot

    def correct_plots(self, inventory, operation: Operation):

        if inventory is None:
            return

        min = operation.get_variable('min_age') if operation.has('min_age') else 0
        max = operation.get_variable('max_age') if operation.has('max_age') else 1000
        time = 0

        for plot in inventory.plots:

            if min <= plot.age <= max:
                time = operation.get_variable('time')
                
            if plot.id not in self.__plots.keys():

                new_plot = Plot()
                new_plot.clone(plot, True)
                new_plot.sum_value('AGE', time)

                self.__plots_to_print[plot.id] = False
                self.__plots[plot.id] = new_plot

            self.__plots[plot.id].sum_value('AGE', time)
            # self.__plots[plot.id].update_trees({'AGE': time}, 1)
            time = 0

    def to_json(self, plot_id: int , node):

        content = dict()

        if plot_id in self.__plots.keys():
            content['plot'] = self.__plots[plot_id].plot_to_json()
            content['trees'] = self.__plots[plot_id].trees_to_json()

        return content

    def to_xslt(self, labels, workbook, plot_id, node, next_inventory, next_operation: Operation, 
                operation: Operation, summary_row: id, decimals: int = 2):

        if plot_id in self.__plots.keys():

            next_plot = None
            if next_inventory is not None and plot_id in next_inventory.__plots.keys():
                next_plot = next_inventory.__plots[plot_id]

            summary_row = self.__plots[plot_id].plot_to_xslt(labels, workbook, node, next_plot, next_operation, 
                                                                   operation, summary_row, decimals)
            self.__plots[plot_id].trees_to_xlst(labels, workbook, node, self.__plots_to_print[plot_id], 
                                                    decimals)
            return summary_row
    
