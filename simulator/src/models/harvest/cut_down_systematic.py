#/usr/bin/env python3
#
# Copyright (c) $today.year Moises Martinez (Sngular). All Rights Reserved.
#
# Licensed under the Apache License", Version 2.0 (the "License")
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

from models.harvest_model import HarvestModel
from data.plot import Plot
from data.tree import Tree
from data.search import OrderCriteria
from data.search import SearchCriteria
from data.search import EQUAL
from data.search import ASC
from data.search import DESC
from util import Tools

import logging


class CutDownSystematics(HarvestModel):

    def __init__(self, configuration=None):
        super().__init__(name="Systematics cut down", version=1, type=configuration['cut_down'])

    def initialize(self, plot: Plot):
        return

    def apply_model(self, plot: Plot, years: int, value: float):

        Tools.print_log_line('Aplicando cut down sistemática', logging.INFO)

        new_plot = Plot()
        new_plot.clone(plot)

        order_criteria = OrderCriteria()
        order_criteria.add_criteria('dbh')

        search_criteria = SearchCriteria()
        search_criteria.add_criteria('status', None, EQUAL)

        trees = Tree.get_sord_and_order_tree_list(plot.trees,
                                                  search_criteria=search_criteria,
                                                  order_criteria=order_criteria)

        for tree in trees:

            new_tree = Tree()
            new_tree.clone(tree)

            new_tree.add_value('expan', tree.expan * ((100 - value) / 100))
            new_tree.add_value('status', None)
            new_plot.add_tree(new_tree)

            cut_tree = Tree()
            cut_tree.clone(tree)
            cut_tree.add_value('status', 'C')
            cut_tree.add_value('expan', tree.expan - new_tree.expan)

            if cut_tree.expan > 0:
                new_plot.add_tree(cut_tree)

        return new_plot
