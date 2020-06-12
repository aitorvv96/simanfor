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

from models.stand_model import StandModel
from data import Tree
from data import Plot
from data import DESC
from data import ASC
# from util import Tools
# from data.search.order_criteria import OrderCriteria
from constants import CUTTYPES_DICT
from constants import PLOT_VARIABLE_NAMES

import math
import sys
import logging
import numpy as np
import os


#/// --------------------------------------------------------------------------------------
#/// Stand Model for Scots pine stands. Based on app SILVES.
#/// del Río M, Montero G (2011). Modelo de simulación de claras en masas de Pinus sylvestris L. Monografias INIA: Forestal n. 3
#/// -------------------------------------------------------------------------------------

# Stand models in Simanfor are make up of 3 functions
#            -> initialize()             <--- for setting up initial variables and calculate productivity of the area: SI = site index
#            -> apply_grow_model()       <--- for calculus of stand variables variations after a simulation of "time" years
#            -> apply_cut_down_model()   <--- for simulate thinning behabiour of stands variables

class Sylves(StandModel):

    def __init__(self, configuration=None):
        super().__init__(name="Sylves", version=1)


    def catch_model_exception(self):  # that function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)


    ### initial function. Only run after importing inventory    
    ## "plot" are variables of the plot in database
    ## This function is the more suitable for calculate Site Index, constant value along all simulation
    ##
    def initialize(self, plot: Plot):
        """
        Function that update the gaps on the information with the inventory data
        Reineke Index equation (value):
            Doc.: del Río M, Montero G (2011). Modelo de simulación de claras en masas de Pinus sylvestris L. Monografias INIA: Forestal n. 3
            Ref.: del Río and Montero, 2011
        Site Index equation:
            Doc.: del Río M, Montero G (2011). Modelo de simulación de claras en masas de Pinus sylvestris L. Monografias INIA: Forestal n. 3
            Ref.: del Río and Montero, 2011
        Volume equation:
            Doc.: del Río M, Montero G (2011). Modelo de simulación de claras en masas de Pinus sylvestris L. Monografias INIA: Forestal n. 3
            Ref.: del Río and Montero, 2011        
        """

        print('#----------------------------------------------------------------------------#')
        print('               Pinus sylvestris "SILVES" model (Spain) is running             ')
        print('#----------------------------------------------------------------------------#')

        try:

        #-----------------------------------FIRST: calculate PLOT data by using TREE data-----------------------------------------#

            tree_expansion: float = 0.0

            expansion_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC) 
            selection_trees = list()

            for tree in expansion_trees:   
                if tree_expansion < 100:
                    tree_expansion += tree.expan
                    selection_trees.append(tree)
                else:
                    break

            sum_expan: float = 0
            sum_prod_basal_area_expan: float = 0
            ## sum_edad: float = 0
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

            # sum_canopy_cover: float = 0
            # sum_vol_expan: float = 0
            # sum_bole_vol_expan: float = 0

            for tree in expansion_trees:

                sum_expan += tree.expan
                sum_prod_basal_area_expan += tree.basal_area * tree.expan
                ## sum_edad += tree.tree_age * tree.expan
                sum_dbh_expan += tree.dbh * tree.expan
                sum_dbh_2_expan += math.pow(tree.dbh, 2) * tree.expan

                max_dbh = tree.dbh if tree.dbh > max_dbh else max_dbh
                min_dbh = tree.dbh if tree.dbh < min_dbh else min_dbh

                max_h = tree.height if tree.height > max_h else max_h
                min_h = tree.height if tree.height < min_h else min_h

                max_ba = tree.basal_area if tree.basal_area > max_ba else max_ba
                min_ba = tree.basal_area if tree.basal_area < min_ba else min_ba

                sum_height_expan += tree.height * tree.expan
                # if tree.lcw != '':
                    # sum_lcw_expan += tree.lcw * tree.expan
                    # prod_lcw_lcw_expan += math.pow(tree.lcw, 2) * tree.expan

                    # sum_canopy_cover += math.pi * (math.pow(tree.lcw, 2) / 4) * tree.expan
                # sum_vol_expan += tree.vol * tree.expan
                # sum_bole_vol_expan += tree.bole_vol * tree.expan

            plot.add_value('BASAL_AREA', sum_prod_basal_area_expan / 10000)
            plot.add_value('DOMINANT_H', plot.get_dominant_height(selection_trees))
            plot.add_value('DENSITY', sum_expan)

            if sum_expan != 0:
                plot.add_value('MEAN_DBH', sum_dbh_expan / sum_expan)
                plot.add_value('QM_DBH', math.sqrt(sum_dbh_2_expan / sum_expan))

            plot.add_value('DOMINANT_DBH', plot.get_dominant_diameter(selection_trees))
            plot.add_value('DBH_MAX', max_dbh)
            plot.add_value('DBH_MIN', min_dbh)
            plot.add_value('BA_MAX', max_ba)
            plot.add_value('BA_MIN', min_ba)

            if sum_expan != 0:
                plot.add_value('MEAN_H', sum_height_expan / sum_expan)
                # plot.add_value('CROWN_MEAN_D', sum_lcw_expan / sum_expan)
                plot.add_value('MEAN_BA', sum_prod_basal_area_expan / sum_expan)

            plot.add_value('H_MAX', max_h)
            plot.add_value('H_MIN', min_h)
                
            plot.add_value('SEC_DOMINANTE', plot.get_dominant_section(selection_trees))

            # if sum_expan != 0:
                # plot.add_value('CROWN_DOM_D', math.sqrt(prod_lcw_lcw_expan / sum_expan))

            if plot.qm_dbh != 0:
                # plot.add_value('REINEKE', sum_expan * math.pow(25/plot.qm_dbh, -1.605))
                plot.add_value('REINEKE', sum_expan * math.pow(25/plot.qm_dbh, -1.75))
            else:
                plot.add_value('REINEKE', 0)

            if sum_expan != 0:
                if Plot.dominant_h != 0:
                    plot.add_value('HART', 10000 / (plot.dominant_h * math.sqrt(sum_expan)))

            # plot.add_value('CANOPY_COVER', sum_canopy_cover / 10000)
            # plot.add_value('VOL', sum_vol_expan / 1000)
            # plot.add_value('BOLE_VOL', sum_bole_vol_expan / 1000)
            # if plot.vol > plot.bole_vol:  # sometimes, only bole_vol is calculated
            #     plot.bark_vol = plot.vol - plot.bole_vol


        #-----------------------------------SECOND: calculate PLOT data by using PLOT data-----------------------------------------#

            # Site Index
            parA = 0.8534446
            parB = -0.27
            parC = 0.439
            SiteIndex =  parA * plot.dominant_h / pow( 1 - math.exp( parB * plot.age / 10 ) , 1 / parC )  # equation for Site Index
            plot.add_value('SI', SiteIndex)  # store Site Index in database
            IC = plot.si / 10
            plot.add_value('QI', IC)  

            # Initial Volume
            parB0 = 1.42706
            parB1 = 0.388317
            parB2 = -30.691629
            parB3 = 1.034549
            Volume_W_Bark = math.exp(parB0 + parB1*plot.si/10 + parB2/plot.age + parB3*math.log(plot.basal_area))  # equation for stand volumen
            plot.add_value('VOL', Volume_W_Bark)  # store initial stand volume in database
        
        except Exception:
            self.catch_model_exception()


    ### simulation function. run in every simulation process to simulate growth. Change of stand variables after "time" years
    ##  old_plot are variables in initial state
    ##  new_plot are variables after "time" years
    ## 
    def apply_grow_model(self, old_plot: Plot, new_plot: Plot, time: int):
        """
        Function that includes the equations needed in the executions.
        BE CAREFUL!! Is not needed to store the new plot age on the 'AGE' variable, the simulator will do it by his own.
        Dominant Height equation:
            Doc.: del Río M, Montero G (2011). Modelo de simulación de claras en masas de Pinus sylvestris L. Monografias INIA: Forestal n. 3
            Ref.: del Río and Montero, 2011
        Basal Area Growth equation:
            Doc.: del Río M, Montero G (2011). Modelo de simulación de claras en masas de Pinus sylvestris L. Monografias INIA: Forestal n. 3
            Ref.: del Río and Montero, 2011
        Survive equation:
            Doc.: del Río M, Montero G (2011). Modelo de simulación de claras en masas de Pinus sylvestris L. Monografias INIA: Forestal n. 3
            Ref.: del Río and Montero, 2011
        Reineke Index equation (value):
            Doc.: del Río M, Montero G (2011). Modelo de simulación de claras en masas de Pinus sylvestris L. Monografias INIA: Forestal n. 3
            Ref.: del Río and Montero, 2011
        Site Index equation:
            Doc.: del Río M, Montero G (2011). Modelo de simulación de claras en masas de Pinus sylvestris L. Monografias INIA: Forestal n. 3
            Ref.: del Río and Montero, 2011
        Volume equation:
            Doc.: del Río M, Montero G (2011). Modelo de simulación de claras en masas de Pinus sylvestris L. Monografias INIA: Forestal n. 3
            Ref.: del Río and Montero, 2011  

        """

        print('#----------------------------------------------------------------------------#')
        print('               Pinus sylvestris "SILVES" model (Spain) is running             ')
        print('#----------------------------------------------------------------------------#')

        if time != 5:
            print('BE CAREFUL! That model was developed to xx year execution, and you are trying to make a', time, 'years execution!')
            print('Please, change your execution conditions to the recommended (xx year execution). If not, the output values will be not correct.')

        try:

            # new_plot.add_value('AGE', old_plot.age + time)  # store new age in database
            # BE CAREFUL!! Is not needed to store the new plot age on the 'AGE' variable, the simulator will do it by his own.
            # if you need to use the "actualised" age, just create another new variable to do it.
            new_age = old_plot.age + time

            # That line is not needed; at the start, old_plot and new_plot values are the same
            # new_plot.add_value('SI', old_plot.si)  # store Site Index in database, constant value for each plot

            # Dominant Height
            parA17 = 1.9962
            parB17 = 0.2642
            parC17 = 0.46
            parA29 = 3.1827
            parB29 = 0.3431
            parC29 = 0.3536
            H0_17 = 10 * parA17 * pow(1 - math.exp(float(-1 * parB17 * new_age / 10)), 1 / parC17)  # Dominant height at plot age if site index was 17
            H0_29 = 10 * parA29 * pow(1 - math.exp(float(-1 * parB29 * new_age / 10)), 1 / parC29)  # Dominant height at plot age if site index was 29
            Dom_Height = H0_17 + (H0_29 - H0_17) * ( old_plot.si / 10 - 1.7 ) / 1.2  # Dominant height at plot age for actual site index 
            new_plot.add_value('DOMINANT_H', Dom_Height)  # store Dominant height in database

            # Basal Area        
            parA0 = 5.103222
            parB0 = 1.42706
            parB1 = 0.388317
            parB2 = -30.691629
            parB3 = 1.034549
            Basal_area =  pow(old_plot.basal_area, old_plot.age/new_age) * math.exp(parA0*(1 - old_plot.age/new_age))  # basal area calculus
            new_plot.add_value('BASAL_AREA', Basal_area)  # store basal area in database

            # Mortality
            parA0 = -2.34935
            parA1 = 0.000000099
            parA2 = 4.87390
            TPH = pow( pow( old_plot.density, parA0) + parA1 * ( pow( new_age / 100, parA2) - pow( old_plot.age / 100, parA2 ) ), 1 / parA0 )  # density calculus; new value of trees per hectare
            new_plot.add_value('DENSITY', TPH)  # store trees per hectare in database

            # VOLUME
            # Volume_W_Bark_new = math.exp(parB0 + parB1*old_plot.si/10 + parB2/old_plot.age + parB3*math.log(old_plot.basal_area))  # calculate new volume 
            # Volume_W_Bark = math.exp(parB0 + parB1*old_plot.si/10 + parB2/new_age + parB3*(old_plot.age/new_age)*math.log(old_plot.basal_area) + parB3*parA0*(1 - old_plot.age/new_age))  # calculate new volume
            # new_plot.add_value('VOL', Volume_W_Bark)  # store total stand volume with bark in database

            # as temporal solution, I used the vol equation changing the values to the new situation, because INIT and CUTS are using the same equation
            Volume_W_Bark_mix = math.exp(parB0 + parB1*old_plot.si/10 + parB2/new_age + parB3*math.log(new_plot.basal_area))  # calculate new volume 
            new_plot.add_value('VOL', Volume_W_Bark_mix) 

            # Mean Height 
            parA0 = -1.155649
            parA1 = 0.976772
            H_mean = parA0 + parA1 * new_plot.dominant_h  # calculus of mean height
            new_plot.add_value('MEAN_H', H_mean)  # store mean height in database


            # QUADRATIC Mean Diameter:      
            MTBA = new_plot.basal_area * 10000 / new_plot.density  # Mean Tree Basal Area
            QMD  = 2 * math.sqrt( MTBA / math.pi )  # Quadratic mean diameter
            new_plot.add_value('QM_DBH',  QMD)  # store quadratic mean diameter

            # Reineke Index
            Reineke = new_plot.density * pow(25 / new_plot.qm_dbh, -1.75)  # Reineke density index
            new_plot.add_value('REINEKE', Reineke)  # store Reineke index in database

            # Hart index
            Hart = 10000 / (new_plot.dominant_h * math.sqrt(new_plot.density)) # Hart index
            new_plot.add_value('HART', Hart)  # Store Hart index in database

        except Exception:
            self.catch_model_exception()


    ###  calculus of variables changes after thinning
    ##  old_plot are variables before thinning
    ##  new_plot are variables after thinning
    ## 
    def apply_cut_down_model( self, old_plot: Plot, new_plot: Plot, #cut_down, 
                             cut_criteria, volume, time, 
                             min_age, max_age):
        """
        Function that includes the equations needed in the cuts.
        Harvest equations:
            Doc.: del Río M, Montero G (2011). Modelo de simulación de claras en masas de Pinus sylvestris L. Monografias INIA: Forestal n. 3
            Ref.: del Río and Montero, 2011
        """

        # trimType values: ( ByTallest, BySmallest, Systematic ) --> Thinning types
        # cutDownType values: ( PercentOfTrees, Volume, Area )   --> Variable used to evaluate the thinning
        # volume ---> value: (% of "Variable" reduced after the thinning) 

        print('#----------------------------------------------------------------------------#')
        print('               Pinus sylvestris "SILVES" model (Spain) is running             ')
        print('#----------------------------------------------------------------------------#')

        if time != 0:
            print('BE CAREFUL! When you plan a HARVEST the time must be 0, and you wrote a', time, 'years for the harvest period!')
            print('Please, change your time value to 0 and run your scenario again.')

        try:

            value = volume
            # new_plot.add_value('VAR_9', value);
                     
            # That line is not needed; at the start, old_plot and new_plot values are the same
            # new_plot.add_value('AGE', old_plot.age)  # store new age in database, it is supposed to be the same
            # new_plot.add_value('SI', old_plot.si)  # Dominant height at plot age for actual site index 

            # DOMINANT Height  -->  nothing changes with time = 0
            # parA17 = 1.9962
            # parB17 = 0.2642
            # parC17 = 0.46
            # parA29 = 3.1827
            # parB29 = 0.3431
            # parC29 = 0.3536
            # H0_17 = 10 * parA17 * pow( 1 - math.exp( -1 * parB17 * old_plot.age / 10 ), 1 / parC17 )
            # H0_29 = 10 * parA29 * pow( 1 - math.exp( -1 * parB29 * old_plot.age / 10 ), 1 / parC29 )
            # Dom_Height = H0_17 + ( H0_29 - H0_17 ) * ( old_plot.si / 10 - 1.7 ) / 1.2   # Dominant height at plot age for actual site index 
            # new_plot.add_value('DOMINANT_H', Dom_Height)  # store Dominant height in database

            # Parameter for Volume and Basal Area equations
            # parA0 = 5.103222
            parB0 = 1.42706
            parB1 = 0.388317
            parB2 = -30.691629
            parB3 = 1.034549

            # Thinning parameters
            if cut_criteria == CUTTYPES_DICT['PERCENTOFTREES']:
                tpuN = value/100  # ratio of thinning trees per hectare and total before thinning
                TPH = (1 - tpuN)*old_plot.density  # trees per hectare after thinning
                
                parC0 = 0.531019
                parC1 = 0.989792
                parC2 = 0.517850
                QMD = parC0 + parC1*old_plot.qm_dbh + parC2*old_plot.qm_dbh*pow(tpuN, 2)  # equation to calculate quadratic mean diameter
                MTBA = math.pi*pow(QMD/2, 2)  # average mean basal area
                SBA = MTBA*TPH/10000  # trees per hectare
                Volume = math.exp(parB0 + parB1*old_plot.si/10 + parB2/old_plot.age + parB3*math.log(SBA))  # equation to calculate volume

                      
            elif cut_criteria == CUTTYPES_DICT['AREA']:
                tpuBA = value/100  # ratio of thinning basal area and total before thinning
                SBA = (1 - tpuBA)*old_plot.basal_area  # basal area after thinning
                
                parC0 = 0.144915
                parC1 = 0.969819
                parC2 = 0.678010
                QMD = pow(parC0 + parC1*pow(old_plot.qm_dbh, 0.5) + parC2*tpuBA, 2)  # equation to calculate quadratic mean diameter
                MTBA = math.pi*pow(QMD/2, 2)  # average mean basal area
                TPH = SBA * 10000 / MTBA  # trees per hectare
                Volume = math.exp(parB0 + parB1*old_plot.si/10 + parB2/old_plot.age + parB3*math.log(SBA))  # equation to calculate volume


            elif cut_criteria == CUTTYPES_DICT['VOLUME']:
                tpuVOL = value/100  # ratio of thinning volume and total before thinning
                Volume = ( 1 - tpuVOL )*old_plot.vol  # volume after thinning
                
                ### Provided we do not have equations for thinning by volume, stimations are based on stimations by basal area
                parC0 = 0.144915
                parC1 = 0.969819
                parC2 = 0.678010
                SBA = math.exp( -1*parB0 - parB1*old_plot.si/10 - parB2/old_plot.age + math.log(Volume)/parB3)  # equation to calculate stand basal area
                tpuBA = 1 - SBA/old_plot.basal_area  # ratio of thinning basal area and total before thinning
                QMD = pow(parC0 + parC1*pow(old_plot.qm_dbh, 0.5) + parC2*tpuBA, 2)  # equation to calculate quadratic mean diameter
                MTBA = math.pi*pow(QMD/2, 2)  # average mean basal area
                TPH = SBA*10000/MTBA # trees per hectare

            
            new_plot.add_value('DENSITY', TPH)  # store trees per hectare in database
            new_plot.add_value('QM_DBH', QMD)  # store quadratic mean diameter
            new_plot.add_value('BASAL_AREA', SBA)  # store basal area in database
            new_plot.add_value('VOL', Volume)  # store total stand volume with bark in database

        except Exception:
            self.catch_model_exception()


    def vars():
        """
        That function will add some needed variables to the output, calculated during the model, and it will remove another variables that are not needed.
        It can only be added variable to tree, but no to the plot (it will return an error).
        """

#########################################################################################################################
############################################  PLOT variables ############################################################
#########################################################################################################################

#------------------------------------------- REMOVE -------------------------------------------------------#

        # Basic plot variables measured
        #PLOT_VARIABLE_NAMES.remove('EXPAN')  # Expan  # expansion factor

        # Basic plot variables calculated - basal area
        #PLOT_VARIABLE_NAMES.remove('BASAL_AREA')  # Basal area  # (m2/ha)
        PLOT_VARIABLE_NAMES.remove('BA_MAX')  # BA Max  # (m2)
        PLOT_VARIABLE_NAMES.remove('BA_MIN')  # BA Min  # (m2)
        PLOT_VARIABLE_NAMES.remove('MEAN_BA')  # Mean BA  # (m2)

        # Basic plot variables calculated - diameter
        PLOT_VARIABLE_NAMES.remove('DBH_MAX')  # D Max  # (cm)
        PLOT_VARIABLE_NAMES.remove('DBH_MIN')  # D Min  # (cm)
        PLOT_VARIABLE_NAMES.remove('MEAN_DBH')  # Mean dbh  # (cm)
        #PLOT_VARIABLE_NAMES.remove('QM_DBH')  # Quadratic mean dbh  # (m2)
        #PLOT_VARIABLE_NAMES.remove('DOMINANT_DBH')  # Dominant dbh  # (cm)

        # Basic plot variables calculated - height
        PLOT_VARIABLE_NAMES.remove('H_MAX')  # H Max  # (m)
        PLOT_VARIABLE_NAMES.remove('H_MIN')  # H Min  # (m)
        PLOT_VARIABLE_NAMES.remove('MEAN_H')  # Mean height  # (m)
        #PLOT_VARIABLE_NAMES.remove('DOMINANT_H')  # Dominant height  # (m)

        # Basic plot variables calculated - crown
        PLOT_VARIABLE_NAMES.remove('CROWN_MEAN_D')  # Mean crown diameter  # (m)
        PLOT_VARIABLE_NAMES.remove('CROWN_DOM_D')  # Dominant crown diameter  # (m)
        PLOT_VARIABLE_NAMES.remove('CANOPY_COVER')  # Canopy cover  # (%)

        # Basic plot variables calculated - plot
        #PLOT_VARIABLE_NAMES.remove('REINEKE')  # Reineke Index  # Stand Density Index - SDI
        #PLOT_VARIABLE_NAMES.remove('HART')  # Hart-Becking Index  # Hart-Becking Index - S
        #PLOT_VARIABLE_NAMES.remove('SI')  # Site Index  # (m)
        #PLOT_VARIABLE_NAMES.remove('QI')  # Quality Index

        # Basic plot variables calculated - volume
        #PLOT_VARIABLE_NAMES.remove('VOL')  # Volume  # (m3)
        PLOT_VARIABLE_NAMES.remove('BOLE_VOL')  # Bole Volume  # (m3)
        PLOT_VARIABLE_NAMES.remove('BARK_VOL')  # Bark Volumen  # (m3)

        # Plot variables calculated - biomass
        PLOT_VARIABLE_NAMES.remove('WSW')  # Wsw  # wsw = stem wood (Kg)
        PLOT_VARIABLE_NAMES.remove('WSB')  # Wsb  # wsb = stem bark (Kg)
        PLOT_VARIABLE_NAMES.remove('W_CORK')  # W Fresh Cork  # w_cork = fresh cork biomass (Kg)
        PLOT_VARIABLE_NAMES.remove('WTHICKB')  # Wthickb  # wthickb = Thick branches > 7 cm (Kg)
        PLOT_VARIABLE_NAMES.remove('WSTB')  # Wstb  # wstb = wsw + wthickb, stem + branches >7 cm (Kg)
        PLOT_VARIABLE_NAMES.remove('WB2_7')  # Wb2_7  # wb2_7 = branches (2-7 cm) (Kg)
        PLOT_VARIABLE_NAMES.remove('WB2_T')  # Wb2_t  # wb2_t = wb2_7 + wthickb; branches >2 cm (Kg)
        PLOT_VARIABLE_NAMES.remove('WTHINB')  # Wthinb  # wthinb = Thin branches (2-0.5 cm) (Kg)
        PLOT_VARIABLE_NAMES.remove('WB05')  # wb05 = thinniest branches (<0.5 cm) (Kg)
        PLOT_VARIABLE_NAMES.remove('WL')  # Wl  # wl = leaves (Kg)
        PLOT_VARIABLE_NAMES.remove('WTBL')  # Wtbl  # wtbl = wthinb + wl; branches <2 cm and leaves (Kg)
        PLOT_VARIABLE_NAMES.remove('WBL0_7')  # Wbl0_7  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Kg)
        PLOT_VARIABLE_NAMES.remove('WR')  # Wr  # wr = roots (Kg)
        PLOT_VARIABLE_NAMES.remove('WT')  # Wt  # wt = biomasa total (Kg) 

        # Plot variables calculated - wood uses
        PLOT_VARIABLE_NAMES.remove('UNWINDING')  # Unwinding  # unwinding = useful volume for unwinding destiny (m3)
        PLOT_VARIABLE_NAMES.remove('VENEER')  # Veneer  # veneer = useful volume for veneer destiny (m3)
        PLOT_VARIABLE_NAMES.remove('SAW_BIG')  # Saw big  # saw_big = useful volume for big saw destiny (m3)
        PLOT_VARIABLE_NAMES.remove('SAW_SMALL')  # Saw small  # saw_small = useful volume for small saw destiny (m3)
        PLOT_VARIABLE_NAMES.remove('SAW_CANTER')  # Saw canter  # saw_canter = useful volume for canter saw destiny (m3)
        PLOT_VARIABLE_NAMES.remove('POST')  # Post  # post = useful volume for post destiny (m3)
        PLOT_VARIABLE_NAMES.remove('STAKE')  # Stake  # stake = useful volume for stake destiny (m3)
        PLOT_VARIABLE_NAMES.remove('CHIPS')  # Chips  # chips = useful volume for chips destiny (m3)

Sylves.vars()