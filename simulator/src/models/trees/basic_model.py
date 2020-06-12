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

from models import TreeModel
from data import Distribution
from data import DESC
from data import Plot
from data import Tree
from scipy import integrate
from util import Tools
from data.tree import VARIABLE_NAMES
from constants import PLOT_VARIABLE_NAMES

import math
import sys
import logging
import numpy as np
import os

class BasicTreeModel(TreeModel):

    def __init__(self, configuration=None):
        return 0.0

    def catch_model_exception(self):
        return 0.0

    def initialize(self, plot: Plot):
        return 0.0

    def survives(self, time: int, plot: Plot, tree: Tree):
        return 0.0

    def grow(self, time: int, plot: Plot, old_tree: Tree, new_tree: Tree):
        return 0.0

    def add_tree(self, time: int, plot: Plot):
        return 0.0

    def new_tree_distribution(self, time: int, plot: Plot, area: float):
        return 0.0

    def process_plot(self, time: int, plot: Plot, trees: list):
        return 0.0

    def taper_equation_with_bark(self, tree: Tree, hr: float):
        return 0.0

    def taper_equation_without_bark(self, tree: Tree, hr: float):
        return 0.0

    def merch_classes(self, tree: Tree):
        return 0.0

    def merch_classes_plot(self, plot: Plot):
        return 0.0

    def crown(self, tree: Tree, plot: Plot, func):
        return 0.0

    def vol(self, tree: Tree, plot: Plot):
        return 0.0

    def biomass(self, tree: Tree):
        return 0.0

    def biomass_plot(self, plot: Plot):
        return 0.0

    def vars():
        return 0.0