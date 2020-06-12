#!/usr/bin/env python3
#
# Copyright (c) $today.year Moisés Martínez (Sngular). All Rights Reserved.
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

import json

from .tools import Tools


class ConfigHandler:

    def __init__(self, file_path, basic_features=None):

        self.__features = None

        if file_path is not None:
            with open(file_path, 'r') as f:
                config_data = json.load(f)
                self.__features = config_data

        else:
            Tools.print_log_line('Config file ' + file_path + ' cannot be open or exits.')

    def __get_value__(self, node, keys):

        if node is None or not node:
            Tools.print_log_line('There is no config information')
            return None

        if isinstance(node, dict):
            if keys[0] in node.keys():
                if len(keys[1:]) is not 0:
                    return self.__get_value__(node.get(keys[0]), keys[1:])
                return node.get(keys[0])
            return None
        else:
            return node

    def get_feature(self, key):

        if key is None:
            return None

        a = self.__get_value__(self.__features, key if isinstance(key, list) else [key])
        return a

    def set_feature(self, key, value):
        self.__features[key] = value
