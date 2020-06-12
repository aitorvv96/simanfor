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

# Modelo de carga básico

from models import LoadModel
from reader import ExcelReader
from simulation import Inventory
from util import Tools

import logging

DEFAULT_EXCEL_FILE_STRUCTURE = ['Parcelas', 'PiesMayores']


class BasicLoad(LoadModel):

    def __init__(self, configuration =None):
        super().__init__(name="Basic loader file from excel", version=1)

    def apply_model(self, file_path: str, years: int):

        if file_path is None:
            return None

        Tools.print_log_line('Generating initial inventory', logging.INFO)
        reader: ExcelReader = ExcelReader(file_path, DEFAULT_EXCEL_FILE_STRUCTURE)
        return Inventory(reader)
