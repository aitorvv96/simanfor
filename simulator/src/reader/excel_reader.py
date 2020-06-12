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

import os
import xlrd
import logging

from .reader import Reader
from util import Tools


class ExcelReader(Reader):

    def __init__(self, filename, sheets):
        if not os.path.exists(filename):
            Tools.print_log_line('filename ' + filename + " does not exists.", logging.ERROR)
            exit(-1)

        self.__document = xlrd.open_workbook(filename)
        self.__cursor = 0
        self.__sheet = None
        self.__sheets = {j: i for i, j in enumerate(sheets)}
        self.__headers = None

        Tools.print_log_line('Inventory file ' + filename + ' loaded', logging.INFO)

    @property
    def document(self):
        return self.__document

    def choose_sheet(self, sheet, has_header=False):
        self.__sheet = self.__document.sheet_by_index(self.__sheets[sheet])
        self.__cursor = -1

        if has_header:
            self.__cursor = 0
            self.__headers = list()
            header = self.__sheet.row(self.__cursor)

            for item in header:
                self.__headers.append(item.value)

    def __iter__(self):
        return self

    def __next__(self):

        if self.__sheet is None:
            Tools.print_log_line("No sheet have been chosen.", logging.ERROR)
            raise StopIteration

        self.__cursor = self.__cursor + 1

        if self.__sheet.nrows <= self.__cursor:
            raise StopIteration
        else:
            result = {}
            data = self.__sheet.row(self.__cursor)

            if self.__headers is None:
                for i in range(len(data)):
                    result[i] = data[i].value
            else:
                for i in range(len(data)):
                    result[self.__headers[i]] = data[i].value

            return result

        raise StopIteration

    def read(self):
        return self.__next__()
