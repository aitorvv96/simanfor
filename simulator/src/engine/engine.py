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

from abc import ABCMeta
from abc import abstractmethod
from simulation.inventory import Inventory
from models import TreeModel
from models import HarvestModel
from models import LoadModel
from models import StandModel
from scenario import Operation
from scenario import LOAD
from scenario import INIT
from scenario import EXECUTION
from scenario import HARVEST

DEFAULT_CONFIG = {
    "processes": False,
    "threads_per_worker": 1,
    "num_workers": 1,
    "memory_limit": "1GB"
}


class Engine(metaclass=ABCMeta):

    def apply_model(self, model, operation: Operation, inventory: Inventory = None):

        new_inventory: Inventory = None
        
        print('##############################################################################')
        print('RUN OPERATION: ' + operation.type.get_name())
        print('##############################################################################')

        if isinstance(model, LoadModel) and operation.type.action == LOAD:
            new_inventory = self.apply_load_model(operation.get_variable('input'), model, operation)
        if isinstance(model, HarvestModel) and operation.type.action == HARVEST:
            new_inventory = self.apply_harvest_model(inventory, model, operation)  
        if isinstance(model, StandModel) and operation.type.action == HARVEST:
            new_inventory = self.apply_harvest_stand_model(inventory, model, operation)
        if isinstance(model, TreeModel) and operation.type.action == INIT:
            new_inventory = self.apply_initialize_tree_model(inventory, model, operation)
        if isinstance(model, StandModel) and operation.type.action == INIT:
            new_inventory = self.apply_initialize_stand_model(inventory, model, operation)
        if isinstance(model, TreeModel) and operation.type.action == EXECUTION:
            new_inventory = self.apply_tree_model(inventory, model, operation)
        if isinstance(model, StandModel) and operation.type.action == EXECUTION:
            new_inventory = self.apply_tree_stand_model(inventory, model, operation)

        new_inventory.correct_plots(inventory, operation)

        return new_inventory

    @abstractmethod
    def apply_harvest_model(self, inventory: Inventory, model: HarvestModel, operation: Operation):
        return

    @abstractmethod
    def apply_harvest_stand_model(self, inventory: Inventory, model: HarvestModel, operation: Operation):
        return

    @abstractmethod
    def apply_tree_model(self, inventory: Inventory, model: TreeModel, operation: Operation):
        return

    @abstractmethod
    def apply_tree_stand_model(self, inventory: Inventory, model: TreeModel, operation: Operation):
        return

    @abstractmethod
    def apply_initialize_tree_model(self, file_path: str, model: LoadModel, operation: Operation):
        return

    @abstractmethod
    def apply_initialize_stand_model(self, file_path: str, model: LoadModel, operation: Operation):
        return

    @abstractmethod
    def apply_load_model(self, file_path: str, model: LoadModel, operation: Operation):
        return

    @abstractmethod
    def close(self):
        return
