#!/usr/bin/env python
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


from abc import ABCMeta
from abc import abstractmethod
from data import Tree
from data import Plot
from util import Tools
from scipy import integrate
from models.trees import *

import logging
import math
import numpy as np


class TreeModel(metaclass=ABCMeta):

    def __init__(self, name: str, version: int):
        self.__tree = None
        self.__name = name
        self.__version = version

        Tools.print_log_line("Loading model " + str(self.name) + "(" + str(self.version) + ")", logging.INFO)

    @property
    def name(self):
        return self.__name

    @property
    def version(self):
        return self.__version

    @property
    def tree(self):
        return self.__tree

    def set_tree(self, tree: Tree):
        Tools.print_log_line("Loading tree (" + tree.id + ") into model" + self.tree + "(" + self.version + ")", logging.INFO)
        self.__tree = tree

    @abstractmethod
    def initialize(self, plot: Plot):
        return

    @abstractmethod
    def survives(self, years:int, plot: Plot, tree: Tree):
        return

    @abstractmethod
    def grow(self, years:int, plot: Plot, old_tree: Tree, new_tree: Tree):
        return

    @abstractmethod
    def add_tree(self, years: int, plot: Plot):
        return

    @abstractmethod
    def new_tree_distribution(self, years: int, plot: Plot, area: float):
        return

    @abstractmethod
    def process_plot(self, years: int, plot: Plot, trees: list):
        return

    @staticmethod
    def simps(a, b, epsilon, tree, f):
        """
        This function was programmed to use simps integral without import libraries.
        """

        h = 0
        s = 0
        s1 = 0
        s2 = 0
        s3 = 0
        x = 0

        s2 = 1
        h = b - a
        s = f(tree, a) + f(tree, b)

        while True:

            s3 = s2
            h = h / 2
            s1 = 0
            x = a + h
            while x < b:
                s1 = s1 + 2 * f(tree, x)
                x = x + 2 * h
            s = s + s1
            s2 = (s + s1) * h / 3
            x = abs(s3 - s2) / 15

            if x > epsilon:
                break

        return s2

    def merch_calculation(tree: Tree, class_conditions, model):
        """
        Function needed to calculate the merchantable volumen of the different wood uses.
        That function must be activated by using merch_classes function on the model, and it will need his taper_equation_with_bark function to calculate it
        """

        ht = tree.height  # total height as ht to simplify

        global usage  # share that dictionary to give access in other functions
        usage = {}  # that dictionary will obtain the values of usage acceptability for each tree

        if tree.stump_h != 0:   
            hro = tree.stump_h / ht  # initial height = stump height
        else:
            hro = 0.20 / ht  # initial height = stump height

        counter = -1
        for k in class_conditions:  # for each list (usage+conditions) on class_conditions...
            counter += 1
            if (class_conditions[counter][1] + hro) <= 1:
                usage[class_conditions[counter][0]] = True  # if stump + log <= 1 (total relative height), then the use is accepted
            else:
                usage[class_conditions[counter][0]] = False  # if not, the use is rejected

        count = -1
        global merch_list  # share that list to give access in other functions
        merch_list = []  # that list will obtain the results of calculate the different log volumes

        for k, i in usage.items():  # for each usage defined before...

            if tree.stump_h != 0:
                hro = tree.stump_h / ht  # initial height = stump height
            else:
                hro = 0.20 / ht  # initial height = stump height

            vol = 0
            count += 1  # that variable allow us to go over the lists
            if i == True:  # if the log satisfy the restrictions...
                dr = model().taper_equation_with_bark(tree, hro)  # diameter of tree at the stump height
                while dr > class_conditions[count][3] and (hro + 0.05/ht <= 1):  # if the diameter > dmax, and hr <= 1...
                    hro += 0.05 / ht  # we go over the log looking for the part with diameter <= dmax for that usage
                    dr = model().taper_equation_with_bark(tree, hro)  # we calculate the diameter on the next point, to verify the conditions
                while dr >= class_conditions[count][2] and (hro + class_conditions[count][1] <= 1):  # satisfying dmax, if diameter > dmin and hro is between integration limits (0-1)...
                    hro += class_conditions[count][1]  # from the start point on the tree, we add the length of a log with the usage specifications
                    dr = model().taper_equation_with_bark(tree, hro)  # we again calculate the diameter at this point; the second while condition has sense in here, to not get over 1 integration limit
                    if dr >= class_conditions[count][2] and hro <= 1:  # as taper equation reduce the diameter, it is not needed to check it
                    # if the log diameter > dmin, and hro doesn't overpass 1 (integration limit)
                        hr = np.arange((hro - class_conditions[count][1]), hro, 0.001)  # integration conditions for taper equation
                        d = model().taper_equation_with_bark(tree, hr)  # we get the taper equation with the previous conditions
                        f = (d / 20) ** 2  # to calculate the volume (dm3), we change the units of the result and calculate the radius^2 (instead of diameter)
                        vol += math.pi * ht * 10 * (integrate.simps(f, hr))  # volume calculation, using the previous information
                if i == True:  # once the tree finish all the while conditions, it comes here, because it continues verifying that condition
                    merch_list.append(vol)  # once we have the total volume for each usage, we add the value to that list
            else:  # if the tree is not useful for one usage, it comes here
                merch_list.append(0)  # as it is not useful, we add 0 value to that usage

        return usage, merch_list