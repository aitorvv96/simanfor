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

from .cut_down import CutDownType
from data.plot import Plot
from data.tree import Tree
from util import Tools

import logging


class Area(CutDownType):

    def __init__(self):
        super().__init__(type='Area')
        Tools.print_log_line('Creating percents of trees cut technique', logging.INFO)

    def cut_discriminator(self, trees, value):

        sum_basal_area_expan: float = 0

        for tree in trees:
            sum_basal_area_expan += tree.basal_area * tree.expan / 10000

        return sum_basal_area_expan * ((100 - value) / 100.0)

    def accumulator(self, tree: Tree):
        return tree.basal_area * tree.expan / 10000

    def compute_expan(self, tree: Tree, accumulator: float, cut_discriminator: float):
        return ((accumulator - cut_discriminator) / (tree.expan * tree.basal_area / 10000)) * tree.expan
