#!/usr/bin/env python3
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

from .tree import Tree
from util import Tools
from .search.order_criteria import OrderCriteria
from constants import PLOT_VARIABLE_NAMES
from constants import OUTPUT_NAMES

import numpy as np
import logging
import math
import i18n

# from time import sleep

ID = 'PLOT_ID'

DESC = 1
ASC = 2


class Plot:

    @staticmethod
    def get_index_by_name(name):
        return PLOT_VARIABLE_NAMES.index(name)

    @staticmethod
    def get_name_by_index(index):
        return PLOT_VARIABLE_NAMES[index]

    def __init__(self, data=None):

        self.__values = dict()
        self.__trees = dict()
        self.__dead_trees = dict()
        self.__cut_trees = dict()
        self.__added_trees = dict()

        if data is None:
            Tools.print_log_line("No data info. The Plot has been created empty.", logging.WARNING)
            for variable in PLOT_VARIABLE_NAMES:
                self.__values[variable] = 0.0
        else:

            for variable in PLOT_VARIABLE_NAMES:
                if variable not in data.keys():
                    Tools.print_log_line(str(variable) + ' is not in data document', logging.WARNING)
                    self.__values[variable] = 0.0
                else:
                    self.__values[variable] = data[variable]

            self.__values[ID] = int(self.__values[ID])

            if 'plot' in data: # json input
                self.map_json_to_xl(data)


    def map_json_to_xl(self, data):
        self.__values['PLOT_ID'] = data['plot']
        self.__values['PROVINCE'] = data['provincia']
        self.__values['LATITUDE'] = data['plotlat']
        self.__values['LONGITUDE'] = data['plotlong']
        self.__values['AGE'] = data['age']
        

    def get_value(self, var: str):
        return self.__values[var]

    def add_tree(self, tree: Tree):
        if tree.get_value('status') is None:
            self.__trees[tree.id] = tree
        elif tree.get_value('status') == 'M':
            self.__dead_trees[tree.id] = tree
        elif tree.get_value('status') == 'C':
            self.__cut_trees[tree.id] = tree
        elif tree.get_value('status') == 'I':
            self.__added_trees[tree.id] = tree

    def add_trees(self, trees: list):
        for tree in trees:
            if tree.get_value('status') is None:
                self.__trees[tree.id] = tree
            elif tree.get_value('status') == 'M':
                self.__dead_trees[tree.id] = tree
            elif tree.get_value('status') == 'C':
                self.__cut_trees[tree.id] = tree
            elif tree.get_value('status') == 'I':
                self.__added_trees[tree.id] = tree

    def get_tree(self, id: int):
        return self.__trees[id] if id in self.__trees.keys() else None

    def get_tree_by_position(self, position: int):
        count = 0
        for tree in self.__trees:
            if count == position:
                return tree
            count += 1
        return None

    def get_trees_order_by(self, variable, value):
        return sorted(self.__trees, key=lambda x: x.get_values(variable) <= value, reverse=True)

    def get_first_tree_order_by(self, variable, value):
        return None

    @property
    def id(self):
        return self.__values[ID] if ID in self.__values.keys() else None

    @property
    def trees(self):
        return self.__trees.values()

    @property
    def values(self):
        return self.__values

    def get_number_trees(self):
        return len(self.__trees)

    def get_trees_array(self):
        tmp = list()
        for tree in self.__trees.values():
            tmp.append(tree.get_array())
        return tmp

    def get_np_trees_array(self):
        tmp = np.array([])
        for tree in self.__trees.values():
            tmp.append(tree.get_array())
        return tmp

    def short_trees_on_list(self, variable: str, order: int = DESC):
        if order == DESC:
            return sorted(self.__trees.values(), key=lambda tree: tree.get_value(variable), reverse=True)
        else:
            return sorted(self.__trees.values(), key=lambda tree: tree.get_value(variable), reverse=False)

    def add_value(self, variable, value):
        self.__values[variable] = value

    def set_value(self, variable, value):
        self.__values[variable] = value

    def sum_value(self, variable, value):
        self.__values[variable] += value

    def sub_value(self, variable, value):
        self.__values[variable] -= value


#########################################################################################################################
######################################################  IDs #############################################################
#########################################################################################################################

    @property
    def inventory_id(self):
        return self.__values['INVENTORY_ID']

    @property
    def plot_id(self):
        return self.__values['PLOT_ID']


#########################################################################################################################
##############################################  Plot general information  ###############################################
#########################################################################################################################

    @property
    def plot_type(self):
        return self.__values['PLOT_TYPE']

    @property
    def plot_area(self):
        return self.__values['PLOT_AREA']

    @property
    def province(self):
        return self.__values['PROVINCE']

    @property
    def study_area(self):
        return self.__values['STUDY_AREA']

    @property
    def municipality(self):
        return self.__values['MUNICIPALITY']

    @property
    def forest(self):
        return self.__values['FOREST']

    @property
    def main_specie(self):
        return self.__values['MAIN_SPECIE']

    @property
    def specie_ifn_id(self):
        return self.__values['SPECIE_IFN_ID']

    @property
    def slope(self):
        return self.__values['SLOPE']

    @property
    def aspect(self):
        return self.__values['ASPECT']

    @property
    def continentality(self):
        return self.__values['CONTINENTALITY']
 
    @property
    def altitude(self):
        return self.__values['ALTITUDE']

    @property
    def longitude(self):
        return self.__values['LONGITUDE']

    @property
    def latitude(self):
        return self.__values['LATITUDE']

#########################################################################################################################
############################################  Basic plot variables measured  ############################################
#########################################################################################################################

    @property
    def expan(self):
        return self.__values['EXPAN']

    @property
    def age(self):
        return self.__values['AGE']

    @property
    def density(self):
        return self.__values['DENSITY']

#########################################################################################################################
#####################################  Basic plot variables calculated - basal area  ####################################
#########################################################################################################################

    @property
    def basal_area(self):
        return self.__values['BASAL_AREA']

    @property
    def ba_max(self):
        return self.__values['BA_MAX']

    @property
    def ba_min(self):
        return self.__values['BA_MIN']

    @property
    def mean_ba(self):
        return self.__values['MEAN_BA']

#########################################################################################################################
######################################  Basic plot variables calculated - diameter  #####################################
#########################################################################################################################

    @property
    def dbh_max(self):
        return self.__values['DBH_MAX']

    @property
    def dbh_min(self):
        return self.__values['DBH_MIN']

    @property
    def mean_dbh(self):
        return self.__values['MEAN_DBH']

    @property
    def qm_dbh(self):
        return self.__values['QM_DBH']

    @property
    def dominant_dbh(self):
        return self.__values['DOMINANT_DBH']

#########################################################################################################################
######################################## Basic plot variables calculated - height #######################################
#########################################################################################################################

    @property
    def h_max(self):
        return self.__values['H_MAX']

    @property
    def h_min(self):
        return self.__values['H_MIN']

    @property
    def mean_h(self):
        return self.__values['MEAN_H']

    @property
    def dominant_h(self):
        return self.__values['DOMINANT_H']

#########################################################################################################################
#######################################  Basic plot variables calculated - crown  #######################################
#########################################################################################################################

    @property
    def crown_mean_d(self):
        return self.__values['CROWN_MEAN_D']

    @property
    def crown_dom_d(self):
        return self.__values['CROWN_DOM_D']

    @property
    def canopy_cover(self):
        return self.__values['CANOPY_COVER']

#########################################################################################################################
######################################## Basic plot variables calculated - plot  ########################################
#########################################################################################################################

    @property
    def reineke(self):
        return self.__values['REINEKE']

    @property
    def hart(self):
        return self.__values['HART']


    @property
    def si(self):
        return self.__values['SI']

    @property
    def qi(self):
        return self.__values['QI']

#########################################################################################################################
########################################### Plot variables calculated - volume ##########################################
#########################################################################################################################

    @property
    def vol(self):
        return self.__values['VOL']

    @property
    def bole_vol(self):
        return self.__values['BOLE_VOL']

    @property
    def bark_vol(self):
        return self.__values['BARK_VOL']

#########################################################################################################################
########################################## Plot variables calculated - biomass ##########################################
#########################################################################################################################

    @property
    def wsw(self):
        return self.__values['WSW']

    @property
    def wsb(self):
        return self.__values['WSB']

    @property
    def w_cork(self):
        return self.__values['W_CORK']

    @property
    def wthickb(self):
        return self.__values['WTHICKB']

    @property
    def wstb(self):
        return self.__values['WSTB']

    @property
    def wb2_7(self):
        return self.__values['WB2_7']

    @property
    def wb2_t(self):
        return self.__values['WB2_T']

    @property
    def wthinb(self):
        return self.__values['WTHINB']

    @property
    def wb05(self):
        return self.__values['WB05']

    @property
    def wl(self):
        return self.__values['WL']

    @property
    def wtbl(self):
        return self.__values['WTBL']

    @property
    def wbl0_7(self):
        return self.__values['WBL0_7']

    @property
    def wr(self):
        return self.__values['WR']

    @property
    def wt(self):
        return self.__values['WT']

#########################################################################################################################
######################################### Plot variables calculated - wood uses #########################################
#########################################################################################################################
    
    @property
    def unwinding(self):
        return self.__values['UNWINDING']

    @property
    def veneer(self):
        return self.__values['VENEER']

    @property
    def saw_big(self):
        return self.__values['SAW_BIG']

    @property
    def saw_small(self):
        return self.__values['SAW_SMALL']

    @property
    def saw_canter(self):
        return self.__values['SAW_CANTER']

    @property
    def post(self):
        return self.__values['POST']

    @property
    def stake(self):
        return self.__values['STAKE']

    @property
    def chips(self):
        return self.__values['CHIPS'] 




        
    def clone(self, plot, full=False):

        for variable in PLOT_VARIABLE_NAMES:
            self.__values[variable] = plot.get_value(variable)

        if full:
            for tree in plot.trees:
                tmp_tree = Tree()
                tmp_tree.clone(tree)
                self.__trees[tmp_tree.id] = tmp_tree

    def clone_by_variable(self, plot, variable: str, value):

        for variable in PLOT_VARIABLE_NAMES:
            self.__values[variable] = plot.get_value(variable)
        for tree in plot.trees:
            if tree.get_value(variable) == value:
                tmp_tree = Tree()
                tmp_tree.clone(tree)
                self.__trees[tmp_tree.id] = tmp_tree

    def get_dominant_height(self, selection_trees: list):

        acumulate: float = 0
        result: float = 0

        for tree in selection_trees:
            if acumulate + tree.expan < 100:
                result += tree.height * tree.expan
                acumulate += tree.expan
            else:
                result += (100 - acumulate) * tree.height
        return result / 100

    def get_dominant_diameter(self, selection_trees: list):

        acumulate: float = 0
        result: float = 0

        for tree in selection_trees:
            if acumulate + tree.expan < 100:
                result += tree.dbh * tree.expan
                acumulate += tree.expan
            else:
                result += (100 - acumulate) * tree.dbh
        return result / 100

    def get_dominant_section(self, selection_trees: list):

        acumulate: float = 0
        result: float = 0

        for tree in selection_trees:
            if acumulate + tree.expan < 100:
                result += tree.basal_area * tree.expan
                acumulate += tree.expan
            else:
                result += (100 - acumulate) * tree.basal_area
        return result / 100

    def recalculate(self):

        tree_expansion: float = 0.0

        order_criteria = OrderCriteria(ASC)
        order_criteria.add_criteria('dbh')

        expansion_trees = Tree.get_sord_and_order_tree_list(self.__trees.values(), order_criteria=order_criteria)
        selection_trees = list()

        for tree in expansion_trees:
            if tree_expansion < 100:
                tree_expansion += tree.expan
                selection_trees.append(tree)
            else:
                break

        sum_expan: float = 0
        sum_prod_basal_area_expan: float = 0
        # sum_edad: float = 0
        sum_dbh_expan: float = 0
        sum_dbh_2_expan: float = 0
        max_dbh: float = 0
        min_dbh: float = 9999
        max_h: float = 0
        min_h: float = 9999
        max_ba: float = 0
        min_ba: float = 9999

        sum_height_expan: float = 0
        sum_lcw_expan: float = 0
        prod_lcw_lcw_expan: float = 0

        sum_canopy_cover: float = 0
        sum_vol_expan: float = 0
        sum_bole_vol_expan: float = 0

        for tree in self.__trees.values():

            sum_expan += tree.expan
            sum_prod_basal_area_expan += tree.basal_area * tree.expan
            # sum_edad += tree.tree_age * tree.expan
            sum_dbh_expan += tree.dbh * tree.expan
            sum_dbh_2_expan += math.pow(tree.dbh, 2) * tree.expan

            max_dbh = tree.dbh if tree.dbh > max_dbh else max_dbh
            min_dbh = tree.dbh if tree.dbh < min_dbh else min_dbh

            max_h = tree.height if tree.height > max_h else max_h
            min_h = tree.height if tree.height < min_h else min_h

            max_ba = tree.basal_area if tree.basal_area > max_ba else max_ba
            min_ba = tree.basal_area if tree.basal_area < min_ba else min_ba

            sum_height_expan += tree.height * tree.expan

            if tree.lcw != '':
                sum_lcw_expan += tree.lcw * tree.expan
                prod_lcw_lcw_expan += math.pow(tree.lcw, 2) * tree.expan

                sum_canopy_cover += math.pi * (math.pow(tree.lcw, 2) / 4) * tree.expan

            sum_vol_expan += tree.vol * tree.expan
            sum_bole_vol_expan += tree.bole_vol * tree.expan

        self.__values['BASAL_AREA'] = sum_prod_basal_area_expan / 10000
        self.__values['DOMINANT_H'] = self.get_dominant_height(selection_trees)
        self.__values['DENSITY'] = sum_expan

        if sum_expan != 0:
            self.__values['MEAN_DBH'] = sum_dbh_expan / sum_expan
            self.__values['QM_DBH'] = math.sqrt(sum_dbh_2_expan / sum_expan)

        self.__values['DOMINANT_DBH'] = self.get_dominant_diameter(selection_trees)
        self.__values['DBH_MAX'] = max_dbh
        self.__values['DBH_MIN'] = min_dbh
        self.__values['BA_MAX'] = max_ba
        self.__values['BA_MIN'] = min_ba

        if sum_expan != 0:
            self.__values['MEAN_H'] = sum_height_expan / sum_expan
            self.__values['CROWN_MEAN_D'] = sum_lcw_expan / sum_expan
            self.__values['MEAN_BA'] = sum_prod_basal_area_expan / sum_expan

        self.__values['H_MAX'] = max_h
        self.__values['H_MIN'] = min_h
            
        self.__values['SEC_DOMINANTE'] = self.get_dominant_section(selection_trees)

        if sum_expan != 0:
            self.__values['CROWN_DOM_D'] = math.sqrt(prod_lcw_lcw_expan / sum_expan)

        if self.__values['QM_DBH'] != 0:
            self.__values['REINEKE'] = sum_expan * math.pow(25/self.qm_dbh, -1.605)
        else:
            self.__values['REINEKE'] = 0

        if sum_expan != 0:
            if self.dominant_h != 0:
                self.__values['HART'] = 10000 / (self.dominant_h * math.sqrt(sum_expan))

        self.__values['CANOPY_COVER'] = sum_canopy_cover / 10000
        self.__values['VOL'] = sum_vol_expan / 1000
        self.__values['BOLE_VOL'] = sum_bole_vol_expan / 1000
        if self.__values['VOL'] > self.__values['BOLE_VOL']:  # sometimes, only bole_vol is calculated
            self.__values['BARK_VOL'] = self.__values['VOL'] - self.__values['BOLE_VOL']

        return self


    def calculate_plot_from_tree(self):

        for tree in self.__trees.values():

            if tree is not None:
                self.__values['BASAL_AREA'] = tree.basal_area * tree.expan / 10000;
                self.__values['DOMINANT_H'] = tree.height
                self.__values['DENSITY'] = tree.expan
                self.__values['AGE'] = tree.tree_age
                self.__values['MEAN_DBH'] = tree.var_1
                self.__values['QM_DBH'] = tree.dbh
                self.__values['DOMINANT_DBH'] = tree.var_2
                self.__values['DBH_MAX'] = tree.var_4
                self.__values['DBH_MIN'] = tree.var_5
                self.__values['MEAN_H'] = tree.var_3
                self.__values['CROWN_MEAN_D'] = tree.var_6
                self.__values['CROWN_DOM_D'] = tree.lcw

                if self.qm_dbh != 0:
                    self.__values['REINEKE'] = tree.expan * math.pow(25 / self.qm_dbh, -1.605)

                if self.dominant_h != 0 and tree.expan != 0:
                    self.__values['HART'] = 10000 / (self.dominant_h * math.sqrt(tree.expan))

                if self.__values['DOMINANT_H'] != 0:
                    self.__values['CANOPY_COVER'] = math.pi * (tree.lcw * tree.lcw / 4) * tree.expan / 10000

                self.__values['VOL'] = tree.vol * tree.expan
                self.__values['BOLE_VOL'] = tree.bole_vol * tree.expan
                self.__values['BARK_VOL'] = self.__values['VOL'] - self.__values['BOLE_VOL']
            else:
                Tools.print_log_line('Tree is None', logging.ERROR)

    def get_first(self):
        for tree in self.__trees:
            return tree
        return None

    def get_first_tree(self, variable: str, value: float):

        for tree in self.__trees:
            if tree.get_value(variable) == value:
                return tree
        return None

    def update_trees(self, variables: dict, action: int = 1):
        for tree in self.__trees.values():
            for key, value in variables.items():
                if action == 1:
                    tree.sum_value(key, value)
                elif action == 2:
                    tree.sub_value(key, value)
                else:
                    tree.set_value(key, value)

    def plot_to_json(self):

        content = dict()

        for i in range(len(PLOT_VARIABLE_NAMES)):
            content[PLOT_VARIABLE_NAMES] = self.__values[PLOT_VARIABLE_NAMES[i]]

        return content

    def print_value(self, variable, dec_pts: int = 2):
        if isinstance(self.__values[variable], float):
            return round(self.__values[variable], dec_pts)
        return self.__values[variable]

    def trees_to_json(self):

        content = dict()

        for tree in self.__trees.values():
            content[tree.id] = tree.to_json()

        return content


    def antes(self, plot, ws_general, summary_row, dec_pts):

        ws_general.cell(row=summary_row, column=1).value = plot.__values['AGE']                          # Edad
        ws_general.cell(row=summary_row, column=2).value = round(plot.__values['DOMINANT_H'], dec_pts)   # Ho m    

        # 
        # Masa principal antes de la clara
        # 
        ws_general.cell(row=summary_row, column=3).value = round(plot.__values['DENSITY'], dec_pts)      # N pies/ha
        ws_general.cell(row=summary_row, column=4).value = round(plot.__values['QM_DBH'], dec_pts)  # Dg cm

        global ba_antes
        ba_antes = plot.__values['BASAL_AREA']  # that variable is needed to calculate DG extraida for stand models

        ws_general.cell(row=summary_row, column=5).value = round(plot.__values['BASAL_AREA'], dec_pts) # G m2/ha                
        ws_general.cell(row=summary_row, column=6).value = round(plot.__values['VOL'], dec_pts)           # V m3/ha
    

    def muerta(self, plot, ws_general, summary_row, dec_pts):

        if len(plot.__dead_trees) != 0:  # to the case of tree models
            # 
            # Masa muerta
            #                 
            n_piesha_masa_muerta = 0
            a_basi_masa_muerta = 0
            volumen_masa_muerta = 0
    
            for tree in plot.__dead_trees.values():
                n_piesha_masa_muerta += tree.expan
                a_basi_masa_muerta += tree.expan * tree.basal_area / 10000
                volumen_masa_muerta += tree.expan * tree.vol / 1000
    
            ws_general.cell(row=summary_row, column=14).value = round(n_piesha_masa_muerta, 
                                                                      dec_pts)                    # N pies/ha
    
            try:
                dg_cm = 200 * math.pow((a_basi_masa_muerta/math.pi/n_piesha_masa_muerta), 0.5)
                ws_general.cell(row=summary_row, column=15).value = round(dg_cm, dec_pts)         # Dg cm
            except ZeroDivisionError as e:
                print(e)

            ws_general.cell(row=summary_row, column=16).value = round(volumen_masa_muerta, 
                                                                  dec_pts)                    # V m3/ha    

        else:  # to the case of plot models

            if isinstance(ws_general.cell(row=(summary_row - 1), column=3).value, float):  # if it is not the first line...

                if isinstance(ws_general.cell(row=(summary_row - 1), column=7).value, float):  # if it was a previus harvest process...
                    n_pies_muerta_plot = ws_general.cell(row=(summary_row - 1), column=3).value - ws_general.cell(row=summary_row, column=3).value - ws_general.cell(row=(summary_row - 1), column=7).value
                else:
                    n_pies_muerta_plot = ws_general.cell(row=(summary_row - 1), column=3).value - ws_general.cell(row=summary_row, column=3).value
                ws_general.cell(row=summary_row, column=14).value = round(n_pies_muerta_plot, dec_pts) 

    
    def extraida(self, plot, ws_general, summary_row, dec_pts):

        if len(plot.__cut_trees) != 0:  # to the case of tree models
            # 
            # Masa extraída
            # 
    
            n_piesha_masa_extraida = 0
            a_basi_masa_extraida = 0
            volumen_masa_extraida = 0
    
            for tree in plot.__cut_trees.values():
                n_piesha_masa_extraida += tree.expan
                a_basi_masa_extraida += tree.expan * tree.basal_area / 10000
                volumen_masa_extraida += tree.expan * tree.vol / 1000
    
            ws_general.cell(row=summary_row, column=7).value = round(n_piesha_masa_extraida, 
                                                                      dec_pts)                    # N pies/ha
    
            try:
                dg_cm = 200 * math.pow((a_basi_masa_extraida/math.pi/n_piesha_masa_extraida), 0.5)
                ws_general.cell(row=summary_row, column=8).value = round(dg_cm, dec_pts)         # Dg cm
            except ZeroDivisionError as e:
                print(e)

            ws_general.cell(row=summary_row, column=9).value = round(volumen_masa_extraida, 
                                                                  dec_pts)                    # V m3/ha

        else:  # to the case of plot models

            self.despues(plot, ws_general, summary_row, dec_pts)  # its needed to run that before, in order to use that data

            n_pies_extraida_plot = ws_general.cell(row=summary_row, column=3).value - ws_general.cell(row=summary_row, column=10).value
            ws_general.cell(row=summary_row, column=7).value = round(n_pies_extraida_plot, dec_pts) 

            # DG
            global ba_antes
            global ba_despues
            a_basi_masa_extraida = ba_antes - ba_despues

            try:
                dg_cm = 200 * math.pow((a_basi_masa_extraida/math.pi/n_pies_extraida_plot), 0.5)
                ws_general.cell(row=summary_row, column=8).value = round(dg_cm, dec_pts)         
            except ZeroDivisionError as e:
                print(e)

            # VOL
            volumen_masa_extraida = ws_general.cell(row=summary_row, column=6).value - ws_general.cell(row=summary_row, column=13).value
            ws_general.cell(row=summary_row, column=9).value = round(volumen_masa_extraida, dec_pts)


    def despues(self, plot, ws_general, summary_row, dec_pts):
        # 
        # Masa principal después de la clara
        #                         
        ws_general.cell(row=summary_row, column=10).value = round(plot.__values['DENSITY'],         
                                                                  dec_pts)                    # N pies/ha
        ws_general.cell(row=summary_row, column=11).value = round(plot.__values['QM_DBH'], 
                                                                  dec_pts)                    # Dg cm

        global ba_despues
        ba_despues = plot.__values['BASAL_AREA']  # that variable is needed to calculate DG extraida for stand models

        ws_general.cell(row=summary_row, column=12).value = round(plot.__values['BASAL_AREA'], 
                                                                  dec_pts)                    # G m2/ha
        ws_general.cell(row=summary_row, column=13).value = round(plot.__values['VOL'], 
                                                                  dec_pts)                    # V m3/ha

        
    def incorporada(self, plot, ws_general, summary_row, dec_pts):

        if len(plot.__added_trees) != 0:
            # 
            # Masa incorporada
            #                 
            n_piesha_masa_incorporada = 0
            a_basi_masa_incorporada = 0
    
            for tree in plot.__added_trees.values():
                n_piesha_masa_incorporada += tree.expan
                a_basi_masa_incorporada += tree.expan * tree.basal_area / 10000
    
            ws_general.cell(row=summary_row, column=17).value = round(n_piesha_masa_incorporada, 
                                                                      dec_pts)                    # N pies/ha
            ws_general.cell(row=summary_row, column=18).value = round(a_basi_masa_incorporada, 
                                                                      dec_pts)                    # G m2/ha  


    def plot_to_xslt(self, labels, workbook, row: int, next_plot, next_operation, operation, 
                       summary_row: int, dec_pts: int = 2):

        # 
        # Resumen
        # 
        # ws_general = workbook[i18n.t('simanfor.general.Summary')]   
        ws_general = workbook[labels['simanfor.general.Summary']]   
        
        operation_code = operation.type.get_code_name()    
        
        min = next_operation.get_variable('min_age') if (next_operation != None and next_operation.has('min_age')) else 0
        max = next_operation.get_variable('max_age') if (next_operation != None and next_operation.has('max_age')) else 1000

        if min <= self.age <= max:
        
            # The algorithm is a little state machine..
            # .. with 3 states I(nit), E(xecution), and H(arvest)
            # .. should make a little drawing and put in the Readme...
            # 
            # if self_op_code == 'EXECUTION' or 'INIT'
            #     if next_op_code == 'EXECUTION':
            #         self -> print Antes
            #         next -> print Muerta
            #     elif next_op_code == 'HARVEST':
            #         self -> print Antes + Muerta
            #         next -> print Extraida + Despues
            #     elif next_op_code == '':
            #         self -> print Antes + Muerta
            # elif self_op_code == 'HARVEST':
            #     if next_op_code == 'HARVEST':
            #         self -> print Antes
            #         next -> print Extraida + Despues
            # 
            # ..that's it, there shouldn't be any more printable cases in Resumen
    
            if operation_code == 'HARVEST' and next_operation != None and next_operation.type.get_code_name() == 'HARVEST':

                self.antes(self, ws_general, summary_row, dec_pts)
                self.extraida(next_plot, ws_general, summary_row, dec_pts)
                self.despues(next_plot, ws_general, summary_row, dec_pts)

                summary_row += 1
                
            elif operation_code in ['EXECUTION', 'INIT']:
    
                if next_operation != None and next_operation.type.get_code_name() == 'EXECUTION':
                    self.antes(self, ws_general, summary_row, dec_pts)
                    self.muerta(next_plot, ws_general, summary_row, dec_pts)
                    self.incorporada(next_plot, ws_general, summary_row, dec_pts)
    
                elif next_operation != None and next_operation.type.get_code_name() == 'HARVEST':
                    self.antes(self, ws_general, summary_row, dec_pts)
                    if operation_code == 'EXECUTION':
                        self.muerta(self, ws_general, summary_row, dec_pts)
                        self.incorporada(self, ws_general, summary_row, dec_pts)
                    self.extraida(next_plot, ws_general, summary_row, dec_pts)
                    self.despues(next_plot, ws_general, summary_row, dec_pts)
    
                elif next_operation == None:
                    self.antes(self, ws_general, summary_row, dec_pts)
                    self.muerta(self, ws_general, summary_row, dec_pts)
                    self.incorporada(self, ws_general, summary_row, dec_pts)
                    
                summary_row += 1
    
        # 
        # Parcelas
        # 
        ws_parcelas = workbook[labels['simanfor.general.Plots']]

        for i in range(len(PLOT_VARIABLE_NAMES)):
            ws_parcelas.cell(row=row+1, 
                column=i+1 + len(OUTPUT_NAMES)).value = self.print_value(PLOT_VARIABLE_NAMES[i], 
                    dec_pts=dec_pts)

        return summary_row


    def trees_to_xlst(self, labels, workbook, node, print_trees=False, decimals: int = 2):

        # try:
        row = 1
        # ws_node = workbook.create_sheet('Node ' + str(node) + ' - ' + i18n.t('simanfor.general.Trees'))
        ws_node = workbook.create_sheet('Node ' + str(node) + ' - ' + labels['simanfor.general.Trees'])

        if print_trees:
            for i in range(len(Tree.variables_names())):
                # ws_node.cell(row=row, column=i+1).value = i18n.t('simanfor.tree.' + Tree.variables_names()[i])
                ws_node.cell(row=row, column=i+1).value = labels['simanfor.tree.' + Tree.variables_names()[i]]

            for tree in self.__trees.values():
                row += 1
                tree.to_xslt(ws_node, row, decimals)

            for tree in self.__dead_trees.values():
                row += 1
                tree.to_xslt(ws_node, row, decimals)

            for tree in self.__cut_trees.values():
                row += 1
                tree.to_xslt(ws_node, row, decimals)

            for tree in self.__added_trees.values():
                row += 1
                tree.to_xslt(ws_node, row, decimals)

        # except Exception as e:
        #     Tools.print_log_line('Generating xlst file: ' + str(e), logging.ERROR)
