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
import argparse
import logging
import datetime
import i18n
import os

from util.tools import Tools
from scenario.scenario import Scenario
from simulation.inventory import Inventory
from engine import EngineFactory
from engine import MACHINE
from engine import CLUSTER
from engine import SUPER
from simulation import Simulation

# import time


def main():
        
    # start = time.time()
    
    parser = argparse.ArgumentParser(
        description='Simanfor simulator')

    parser.add_argument('-s',
                        metavar='scenario_file',
                        required=True,
                        default=None,
                        type=str,
                        help='scenario file (json format)')
    parser.add_argument('-c',
                        metavar='configuration_file',
                        required=False,
                        default=None,
                        type=str,
                        help='configuration file in json format')
    parser.add_argument('-e',
                        metavar='engine',
                        required=False,
                        default=MACHINE,
                        type=int,
                        help='execution engine')
    parser.add_argument('-l',
                        metavar='language',
                        required=False,
                        default='es',
                        type=str,
                        help='printing language')
    parser.add_argument('-logging_config_file',
                        metavar='logging_config_file',
                        help='log config_file',
                        type=str,
                        default='../config_files/logging.conf')
    parser.add_argument('-log_path',
                        metavar='log_path',
                        type=str,
                        help='log data name for the logging file',
                        default='log-data-' + str(datetime.date.today()))
    parser.add_argument("-v",
                        metavar='verbosity_level',
                        default=0,
                        type=int,
                        help="increase output verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL). "
                             "The default value is None")

    args = parser.parse_args()

    translations_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "translations")
    i18n.load_path.append(translations_path)
    i18n.set('locale', args.l)
    i18n.set('fallback', 'es')

    Tools.load_logger_config(args.logging_config_file, level=args.v)

    inventory: Inventory = None
    configuration = None

    scenario: Scenario = Scenario(args.s)
    simulation = Simulation()

    engine = EngineFactory.load_engine(args.e, configuration)
    step = 1

    for operation in scenario.operations:

        Tools.print_log_line('Executing operation: ' + operation.name, logging.INFO, name='logger_dev')
        model = Tools.import_module(operation.model_class, operation.model_path, operation.variables)
        inventory = engine.apply_model(model, operation, inventory)
        simulation.add_step(step, inventory, operation, model)

        step += 1

    # mid = time.time()
    # print("Models executions finished after", (mid - start), "seconds.")

    if args.e == MACHINE:
        simulation.generate_results(
            scenario.name,
            scenario.output_path,
            scenario.modelo,
            scenario.ext,
            scenario.zip_compression,
            scenario.decimal_numbers)
    elif args.e in [CLUSTER, SUPER]:
        simulation.generate_results_parallel(
            scenario.name,
            scenario.output_path,
            scenario.modelo,
            scenario.ext,
            scenario.zip_compression,
            scenario.decimal_numbers)        

    engine.close()

    # end = time.time()
    # print("Program finished after", (end - start), "seconds.")


if __name__ == "__main__":
    main()
