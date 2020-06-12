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

import importlib
import logging.config
import inspect
import i18n


class Tools:

    @staticmethod
    def import_module(class_name, class_path, configuration=None):

        module_loaded = importlib.import_module(class_path)
        class_definition = getattr(module_loaded, class_name)
        if inspect.isclass(class_definition):
            return class_definition(configuration)

        return None

    @staticmethod
    def load_logger_config(config_file, level=logging.DEBUG, name=None):
        logger_name = 'logger_'  if name is None else name
        logging.config.fileConfig(config_file, disable_existing_loggers=False)
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

    @staticmethod
    def get_logger():
        return logging.getLogger('logger_')

    @staticmethod
    def shutdown_logger():
        logging.shutdown()

    @staticmethod
    def print_log_line(message, level=logging.DEBUG, name='logger_'):

        logger_name = 'logger_' if name is None else name
        logger = logging.getLogger(logger_name)

        if level == logging.INFO:
            logger.info(message)
        if level == logging.DEBUG:
            logger.debug(message)
        if level == logging.WARNING:
            logger.warning(message)
        if level == logging.ERROR:
            logger.error(message)
        if level == logging.CRITICAL:
            logger.error(message)

