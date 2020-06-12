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

from util import Tools
from .search.order_criteria import DESC

import logging
import json


VARIABLE_NAMES = [

    # IDs
    "INVENTORY_ID",
    "PLOT_ID",
    "TREE_ID",

    # Tree general information
    "number_of_trees",
    "specie",
    "quality",
    "shape",
    "special_param",
    "remarks",
    "age_130",
    "social_class",
    "tree_age",
    "coord_x",
    "coord_y",

    # Basic variables measured
    "expan",  # expan  # expansion factor
    "dbh_1",  # dbh 1  # diameter mesasurement 1 (cm)
    "dbh_2",  # dbh 2  # diameter mesasurement 1 (cm)
    "dbh",  # dbh  # diameter at breast height (cm)
    "stump_h",  # stump height  # (m)
    "height",  # height  # total height (m)
    "bark_1",  # bark thickness 1  # bark thickness mesasurement 1 (mm)
    "bark_2",  # bark thickness 2  # bark thickness mesasurement 2 (mm)
    "bark",  # bark thickness  # mean bark thickness (mm)

   # Basic variables calculated
    "normal_circumference",  # normal circumference  # circumference at breast height (cm)
    "hd_ratio",  # slentherness  # (%)
    "basal_area",  # basal area  #  (m2)
    "bal",  # basal area acumulated  # (m2)
    "ba_ha",  # basal area per ha  # (m2/ha) 

    # Crown variables
    "cr",  # crown ratio  # (%)
    "lcw",  # lcw  #  largest crown width (m)
    "hcb",  # hcb  # height crown base (m)
    "hlcw",  # hlcw  # height of largest crown width (m)

    # Volume variables
    "vol",  # volume  # volume with bark (dm3)
    "bole_vol",  # bole volume  # volume without bark (dm3)
    "bark_vol",  # bark vol  # volume of bark (dm3)
    "firewood_vol",  # fuelwood volume  # (dm3)
    "vol_ha",  # volume per ha  # volume with bark per hectare (m3/ha)

    # Biomass variables
    "wsw",  # wsw  # wsw = stem wood (Kg)
    "wsb",  # wsb # wsb = stem bark (Kg)
    "w_cork",  # w fresh cork  # w_cork = fresh cork biomass (Kg)
    "wthickb",  # wthickb  # wthickb = Thick branches > 7 cm (Kg)
    "wstb",  # wstb  # wstb = wsw + wthickb, stem + branches >7 cm (Kg)
    "wb2_7",  # wb2_7  # wb2_7 = branches (2-7 cm) (Kg)
    "wb2_t",  # wb2_t  # wb2_t = wb2_7 + wthickb; branches >2 cm (Kg)
    "wthinb",  # wthinb  # wthinb = Thin branches (2-0.5 cm) (Kg)
    "wb05",  # wb0.5  # wb05 = thinniest branches (<0.5 cm) (Kg)
    "wl",  # wl  # wl = leaves (Kg)
    "wtbl",  # wtbl  # wtbl = wthinb + wl; branches <2 cm and leaves (Kg)
    "wbl0_7",  # wbl0_7  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Kg)
    "wr",  # wr  # wr = roots (Kg)
    "wt",  # wt  # wt = biomasa total (Kg)

    # Wood uses variables
    "unwinding",  # unwinding  # unwinding = useful volume for unwinding destiny (dm3)
    "veneer",  # veneer  # veneer = useful volume for veneer destiny (dm3)
    "saw_big",  # saw big  # saw_big = useful volume for big saw destiny (dm3)
    "saw_small",  # saw small  # saw_small = useful volume for small saw destiny (dm3)
    "saw_canter",  # saw canter  # saw_canter = useful volume for canter saw destiny (dm3)
    "post",  # post  # post = useful volume for post destiny (dm3)
    "stake",  # stake  # stake = useful volume for stake destiny (dm3)
    "chips",  # chips  # chips = useful volume for chips destiny (dm3)

    # Quercus suber special variables
    "dbh_oc",  # dbh over cork  # dbh over cork (cm) - Quercus suber
    "h_uncork",  # uncork height  # uncork height on main stem (m) - Quercus suber
    "nb",  # uncork boughs  # number of main bough stripped - Quercus suber
    "cork_cycle"  # cork cycle  # moment to obtain cork data; 0 to the moment just immediately before the stripping process
]

INT_VALUES = ['INVENTORY_ID',
              'PLOT_ID',
              'TREE_ID']
              # 'TREE_ID',
              # 'EDAD']

STR_VALUES = ['status']

JSON_STR_VALUES = ['PLOT_ID', 'TREE_ID', 'specie']


class Tree:

    def __init__(self, data=None):

        self.__values = dict()

        if data is None:
            Tools.print_log_line("No data info when tree is generated", logging.WARNING)

            for var_name in VARIABLE_NAMES:
                self.__values[var_name] = 0
        else:
            for var_name in VARIABLE_NAMES:
                if var_name not in data.keys():
                    Tools.print_log_line(var_name + ' is not in data document', logging.WARNING)
                    self.__values[var_name] = 0
                else:
                    self.__values[var_name] = data[var_name]

            if 'tree' in data: # json input
                self.map_json_to_xl(data)

        self.__values['status'] = None


    def map_json_to_xl(self, data):
        self.__values['TREE_ID'] = data['tree']
        self.__values['specie'] = data['species']
        self.__values['coord_x'] = data['treelat']
        self.__values['coord_y'] = data['treelong']
        self.__values['height'] = float(data['height'])
        self.__values['dbh_1'] = float(data['dbh1'])
        self.__values['dbh_2'] = float(data['dbh2'])
        self.__values['PLOT_ID'] = data['plot']
        self.__values['dbh'] = float(data['dbh'])
        self.__values['expan'] = float(data['expan'])
        
    # def get_value(self, var):
    #     try:
    #         if self.__values[var] is None:
    #             return self.__values[var]
    #         elif var in STR_VALUES:
    #             return str(self.__values[var])
    #         if var in INT_VALUES:
    #             return int(self.__values[var])
    #         else:
    #             return self.__values[var]
    #     except Exception as e:
    #         Tools.print_log_line(str(e) + ' when it tried to access variable ' + var, logging.ERROR)

    def get_value(self, var, json = False):
        try:
            if self.__values[var] is None:
                return self.__values[var]
            elif var in STR_VALUES or json == True:
                return str(self.__values[var])
            if var in INT_VALUES:
                return int(self.__values[var])
            else:
                return self.__values[var]
        except Exception as e:
            Tools.print_log_line(str(e) + ' when it tried to access variable ' + var, logging.ERROR)

    def add_value(self, var, value):
        try:
            if value is None:
                self.__values[var] = value
            elif var in STR_VALUES:
                self.__values[var] = str(value)
            elif var in INT_VALUES:
                self.__values[var] = int(value)
            else:
                self.__values[var] = float(value)
        except Exception as e:
            Tools.print_log_line(str(e) + ' when it tried to update variable ' + var + ' with value ' + value, logging.ERROR)

    def set_value(self, var, value):
        try:
            if var in STR_VALUES:
                self.__values[var] = str(value)
            elif var in INT_VALUES:
                self.__values[var] = int(value)
            else:
                self.__values[var] = float(value)
        except Exception as e:
            Tools.print_log_line(str(e) + ' when it tried to update variable ' + var + ' with value ' + str(value), logging.ERROR)

    def sum_value(self, var, value):
        try:
            if var in INT_VALUES:
                self.__values[var] += int(value)
            else:
                self.__values[var] += float(value)
        except Exception as e:
            Tools.print_log_line(str(e) + ' when it tried to update variable ' + var + ' with value ' + str(value), logging.ERROR)

    def sub_value(self, var, value):
        try:
            if var in INT_VALUES:
                self.__values[var] += int(value)
            else:
                self.__values[var] -= float(value)
        except Exception as e:
            Tools.print_log_line(str(e) + ' when it tried to update variable ' + var + ' with value ' + str(value), logging.ERROR)

    @property
    def plot_id(self):
        return int(self.__values['PLOT_ID'])

    @property
    def tree_id(self):
        return int(self.__values['TREE_ID'])

    @property
    def id(self):
        if isinstance(self.__values['PLOT_ID'], int):
            return int(self.__values['TREE_ID'])
        else:
            return self.__values['TREE_ID']

    def get_array(self):
        tmp = list()
        for key, value in self.__values.iteritems():
            tmp.append(value)
        return tmp

    @staticmethod
    def variables_names():
        return VARIABLE_NAMES + STR_VALUES

#########################################################################################################################
##############################################  Tree general information  ###############################################
#########################################################################################################################
  
    @property
    def number_of_trees(self):
        return self.__values['number_of_trees']

    @property
    def specie(self):
        return self.__values['specie']

    @property
    def quality(self):
        return self.__values['quality']

    @property
    def shape(self):
        return self.__values['shape']

    @property
    def special_param(self):
        return self.__values['special_param']

    @property
    def remarks(self):
        return self.__values['remarks']

    @property
    def age_130(self):
        return self.__values['age_130']

    @property
    def social_class(self):
        return self.__values['social_class']

    @property
    def tree_age(self):
        return self.__values['tree_age']

    @property
    def coord_x(self):
        return self.__values['coord_x']

    @property
    def coord_y(self):
        return self.__values['coord_y']

#########################################################################################################################
#########################################  Basic variables measured  ####################################################
#########################################################################################################################

    @property
    def dbh_1(self):
        return self.__values['dbh_1']

    @property
    def dbh_2(self):
        return self.__values['dbh_2']

    @property
    def dbh(self):
        return self.__values['dbh']

    @property
    def stump_h(self):
        return self.__values['stump_h']

    @property
    def height(self):
        return self.__values['height']

    @property
    def bark_1(self):
        return self.__values['bark_1']

    @property
    def bark_2(self):
        return self.__values['bark_2']

    @property
    def bark(self):
        return self.__values['bark']

    @property
    def expan(self):
        return self.__values['expan']

#########################################################################################################################
#########################################  Basic variables calculated  ##################################################
#########################################################################################################################

    @property
    def normal_circumference(self):
        return self.__values['normal_circumference']

    @property
    def hd_ratio(self):
        return self.__values['hd_ratio']

    @property
    def basal_area(self):
        return self.__values['basal_area']

    @property
    def bal(self):
        return self.__values['bal']

    @property
    def ba_ha(self):
        return self.__values['ba_ha']

#########################################################################################################################
##############################################  Crown variables  ########################################################
#########################################################################################################################

    @property
    def cr(self):
        return self.__values['cr']

    @property
    def lcw(self):
        return self.__values['lcw']

    @property
    def hcb(self):
        return self.__values['hcb']

    @property
    def hlcw(self):
        return self.__values['hlcw']

#########################################################################################################################
##############################################  Volume variables ########################################################
#########################################################################################################################

    @property
    def vol(self):
        return self.__values['vol']

    @property
    def bole_vol(self):
        return self.__values['bole_vol']

    @property
    def bark_vol(self):
        return self.__values['bark_vol']

    @property
    def firewood_vol(self):
        return self.__values['firewood_vol']

    @property
    def vol_ha(self):
        return self.__values['vol_ha']

#########################################################################################################################
##############################################  Biomass variables #######################################################
#########################################################################################################################

    @property
    def wsw(self):
        return self.__values['wsw']

    @property
    def wsb(self):
        return self.__values['wsb']

    @property
    def w_cork(self):
        return self.__values['w_cork']

    @property
    def wthickb(self):
        return self.__values['wthickb']

    @property
    def wstb(self):
        return self.__values['wstb']

    @property
    def wb2_7(self):
        return self.__values['wb2_7']

    @property
    def wb2_t(self):
        return self.__values['wb2_t']

    @property
    def wthinb(self):
        return self.__values['wthinb']

    @property
    def wb05(self):
        return self.__values['wb05']

    @property
    def wl(self):
        return self.__values['wl']

    @property
    def wtbl(self):
        return self.__values['wtbl']

    @property
    def wbl0_7(self):
        return self.__values['wbl0_7']

    @property
    def wr(self):
        return self.__values['wr']

    @property
    def wt(self):
        return self.__values['wt']

#########################################################################################################################
############################################  Wood uses variables #######################################################
#########################################################################################################################

    @property
    def unwinding(self):
        return self.__values['unwinding']

    @property
    def veneer(self):
        return self.__values['veneer']

    @property
    def saw_big(self):
        return self.__values['saw_big']

    @property
    def saw_small(self):
        return self.__values['saw_small']

    @property
    def saw_canter(self):
        return self.__values['saw_canter']

    @property
    def post(self):
        return self.__values['post']

    @property
    def stake(self):
        return self.__values['stake']

    @property
    def chips(self):
        return self.__values['chips']

#########################################################################################################################
######################################  Quercus suber special variables #################################################
#########################################################################################################################

    @property
    def dbh_oc(self):
        return self.__values['dbh_oc']

    @property
    def h_uncork(self):
        return self.__values['h_uncork']

    @property
    def nb(self):
        return self.__values['nb']

    @property
    def cork_cycle(self):
        return self.__values['cork_cycle']
        
#########################################################################################################################
################################################### STATUS ##############################################################
#########################################################################################################################

    @property
    def status(self):
        return self.__values['status']





    def set_status(self, value):
        self.__values['status'] = value

    def clone(self, tree):
        for var_name in VARIABLE_NAMES:
            self.__values[var_name] = tree.get_value(var_name)

    def json(self, tree):
        return json.dumps(self.__values)

    @staticmethod
    def sum_tree_list(trees: list, variable: str):
        sum = 0

        for tree in trees:
            sum += tree.get_value(variable)

        return sum

    @staticmethod
    def get_sord_and_order_tree_list(input, search_criteria=None, order_criteria=None):

        def sort_key(element: Tree):
            if element.get_value(order_criteria.get_first()) is None:
                return 0.0
            return element.get_value(order_criteria.get_first())

        if isinstance(input, dict):
            data = input.values()
        elif isinstance(input, list) or isinstance(input, {}.values().__class__):
            data = input
        else:
            Tools.print_log_line('Input list must be list and dict', logging.WARNING)
            return None

        tmp = list()

        if search_criteria is not None:
            for tree in data:
                valid = 0
                for criteria in search_criteria.criterion:
                    if criteria.is_valid(tree.get_value(criteria.variable)):
                        valid += 1

                if valid == len(search_criteria.criterion):
                    tmp.append(tree)
        else:
            for tree in data:
                tmp.append(tree)

        if order_criteria is not None:
            tmp = sorted(tmp, key=sort_key, reverse=False if order_criteria.type == DESC else True)

        return tmp

    def calculate_tree_from_plot(self, plot):
        
        self.__values['expan'] = plot.density
        self.__values['height'] = plot.dominant_h
        self.__values['basal_area'] = plot.basal_area * 10000 / self.__values['expan']
        # self.__values['dbh'] = 2 * math.sqrt(self.__values['basal_area'] / math.pi)
        self.__values['hd_ratio'] = self.__values['height'] * 100 / self.__values['dbh']
        self.__values['tree_age'] = plot.age
        self.__values['vol'] = plot.vol / self.__values['expan']
        self.__values['bole_vol'] = plot.bole_vol / self.__values['expan']
        self.__values['lcw'] = plot.crown_dom_d
        #self.__values['VAR_1'] = plot.mean_dbh
        #self.__values['VAR_2'] = plot.dominant_dbh
        #self.__values['VAR_3'] = plot.mean_h
        #self.__values['VAR_4'] = plot.dbh_max
        #self.__values['VAR_5'] = plot.dbh_min
        #self.__values['VAR_6'] = plot.crown_mean_d

    def print_value(self, variable, decimals: int = 2):
        
        if variable not in STR_VALUES:
            if isinstance(self.__values[variable], str):
                if len(self.__values[variable]) > 0 and variable not in JSON_STR_VALUES:
                    return self.__values[variable]
            elif variable not in JSON_STR_VALUES:
                if self.__values[variable] == None:
                    self.__values[variable] = 0
                return round(float(self.__values[variable]), decimals)
        return self.__values[variable]

    def to_json(self):

        content = dict()

        for key, value in self.__values.items():
            content[key] = value

        return content

    def to_xslt(self, sheet, row, decimals: int = 2):

        column = 0

        for key in self.__values.keys():
            column += 1
            sheet.cell(row=row, column=column).value = self.print_value(key, decimals)
