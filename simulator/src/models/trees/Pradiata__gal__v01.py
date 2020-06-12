# /usr/bin/env python3
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


from models import TreeModel
from data import Distribution
from data import DESC
from data import Plot
from data import Tree
from scipy import integrate
from util import Tools
from data.tree import VARIABLE_NAMES
from constants import PLOT_VARIABLE_NAMES

import math
import sys
import logging
import numpy as np
import os

# Pinus radiata model (Galicia, Spain), version 01
# Written by iuFOR
# Sustainable Forest Management Research Institute UVa-INIA, iuFOR (University of Valladolid-INIA)
# Higher Technical School of Agricultural Engineering, University of Valladolid - Avd. Madrid s/n, 34004 Palencia (Spain)
# http://sostenible.palencia.uva.es/

class PinusRadiataGalicia(TreeModel):


    def __init__(self, configuration=None):
        super().__init__(name="Pinus radiata - Galicia", version=1)


    def catch_model_exception(self):  # that function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)


    def initialize(self, plot: Plot):
        """
        Function that update the gaps on the information with the inventory data
        Height/Diameter equation:
            Doc.: Dorado FC, Diéguez-Aranda U, Anta MB, Rodríguez MS, von Gadow K (2006). A generalized height–diameter model including random components for radiata pine plantations in northwestern Spain. Forest Ecology and Management, 229(1-3), 202-213
            Ref.: Dorado et al, 2006
        SI equation:
            Doc.: Diéguez-Aranda U, Burkhart HE, Rodríguez-Soalleiro R (2005). Modeling dominant height growth of radiata pine (Pinus radiata D. Don) plantations in north-western Spain. Forest Ecology and Management, 215(1-3), 271-284
            Ref.: Diéguez-Aranda et al, 2006
        """

        print('#----------------------------------------------------------------------------#')
        print('                   Pinus radiata model (Galicia) is running                   ')
        print('#----------------------------------------------------------------------------#')

        try:  # errors inside that construction will be announced
            
            #-----------------------------------SI-----------------------------------------#

            t = 20  # desired age to SI (years)
            Lo = math.log(1 - math.exp(-0.06738*plot.age))
            Xo = 0.5*(math.log(plot.dominant_h) + 1.755*Lo + math.sqrt((math.log(plot.dominant_h) + 1.755*Lo)**2 - 4*12.44*Lo))
            SI = plot.dominant_h * ((1 - math.exp(-0.06738*t) / (1 - math.exp(-0.06738*plot.age))) ** (-1.755 + 12.44/Xo))
            # site index is defined as top height at a base age of 20 years
            plot.add_value('SI', SI)  # Site Index (m) calculation
            
            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # stablish an order to calculate tree variables
            bal: float = 0

            for tree in plot_trees:  # for each tree...

                #-----------------------------------BASAL AREA-----------------------------------------#

                tree.add_value('bal', bal)  # the first tree must receive 0 value (m2)
                tree.add_value('basal_area', math.pi * (tree.dbh / 2) ** 2)  # normal (at 1.30m) section (cm2) calculation
                tree.add_value('ba_ha', tree.basal_area * tree.expan / 10000)  # basimetric area per ha (m2/ha)
                bal += tree.basal_area * tree.expan / 10000  # then, that value is acumulated

                tree.add_value('hd_ratio', tree.height * 100 / tree.dbh)  # height/diameter ratio (%) calculation
                tree.add_value('normal_circumference', math.pi * tree.dbh)  # normal (at 1.30m) circumference (cm) calculation

                #-----------------------------------HEIGHT-----------------------------------------#

                if tree.height == 0:  # if the tree hasn't height (m) value, it is calculated
                    a = 0.0296
                    b = 1.633
                    tree.add_value('height', (1.3**b + (plot.dominant_h**b - 1.3**b) * (1 - math.exp(-a*tree.dbh)) / (1 - math.exp(-a*plot.dominant_diameter))**(1/b)))

                #-----------------------------------FUNCTIONS-----------------------------------------#

                self.crown(tree, plot, 'initialize')  # activate crown variables calculation

                self.vol(tree, plot)  # activate volume variables calculation
                
                self.merch_classes(tree)  # activate wood uses variables calculation

                self.biomass(tree)  # activate biomass variables calculation

            self.merch_classes_plot(plot)  # activate wood uses (plot) variables calculation

            self.biomass_plot(plot)  # activate biomass (plot) variables calculation         

        except Exception:
            self.catch_model_exception()


    def survives(self, time: int, plot: Plot, tree: Tree):
        """
        Survive function. The trees that are death appear on the output with "M" on the "State of the tree" column
        Source:
            Doc.: Crecente-Campo F (2008). Modelo de crecimiento de árbol individual para Pinus radiata D. Don en Galicia. Univ Santiago de Compostela
            Ref.: Crecente-Campo, 2008
        """

        BALMOD = (1 - (1 - (tree.bal/plot.basal_area))) / plot.hart
        p_survive = 1 / (1 + math.exp(-2.093 - 3.214*(tree.dbh/plot.qm_dbh) - 0.001096*(tree.dbh**2) + 0.03703*plot.basal_area - 0.07873*plot.dominant_h + 0.3036*BALMOD))
        
        return p_survive  # calculated to 1 year execution


    def grow(self, time: int, plot: Plot, old_tree: Tree, new_tree: Tree):
        """
        Function that run the diameter and height growing equations
        Source:
            Doc.: Crecente-Campo F (2008). Modelo de crecimiento de árbol individual para Pinus radiata D. Don en Galicia. Univ Santiago de Compostela
            Ref.: Crecente-Campo, 2008
        """

        BALMOD = (1 - (1 - (old_tree.bal/plot.basal_area))) / plot.hart
        BAR = (old_tree.basal_area*0.01)/plot.basal_area  # is a basal area ratio (g/G, where g is the basal area of the tree (m2))

        ig = 0.3674 * (old_tree.dbh**2.651) * (plot.basal_area**(-0.7540)) * math.exp(-0.05207*old_tree.tree_age - 0.05291*BALMOD -102*BAR)

        dbhg1 = ((ig/math.pi) ** 0.5) * 2
        new_tree.sum_value("dbh", dbhg1)  # annual diameter increment (cm)



        RBA_D = ((old_tree.basal_area*0.01)/plot.basal_area) ** (old_tree.dbh/plot.qm_dbh)  # a ratio basal area-diameter ([g/G]d/Dg)

        if plot.si == 0:
            htg1: float = 0
        else:
            htg1 = 0.05287 * (old_tree.height**(-0.5733)) * (old_tree.dbh**0.5437) * (plot.si**1.084) * math.exp(-0.03242*old_tree.tree_age - 50.87*RBA_D)

        new_tree.sum_value("height", htg1)  # annual height increment (m)


    def add_tree(self, time: int, plot: Plot):
        """
        Ingrowth stand function.
        That function calculates the probability that trees are added to the plot, and if that probability is higher than a limit value, then basal area
        incorporated are calculated. The next function will order how to divide that basal area on the different diametric classes.
        Source:
            Doc.: Castedo-Dorado F, Diéguez-Aranda U, Barrio-Anta M, Álvarez-González JG (2007). Modelling stand basal area growth for radiata pine plantations in Northwestern Spain using the GADA. Annals of Forest Science, 64(6), 609-619
            Ref.: Castedo-Dorado et al, 2007
        """

        t = plot.age  # age of the stand (years)
        # SI at 20 years old

        ING = -52.23 + 2.676*t + 1.306*plot.si + 0.0101*plot.density
        return ING


    def new_tree_distribution(self, time: int, plot: Plot, area: float):
        """
        Tree diametric classes distribution
        That function must return a list with different sublists for each diametric class, where the conditions to ingrowth function are written
        That function has the aim to divide the ingrowth (added basal area of add_tree) in different proportions depending on the orders given
        On the cases that a model hasn´t a good known distribution, just return None to share that ingrowth between all the trees of the plot
        """

        distribution = []  # that list will contain the different diametric classes conditions to calculate the ingrowth distribution

        return None


    def process_plot(self, time: int, plot: Plot, trees: list):
        """
        Function that update the trees information once the grow function was executed
        The equations on that function are the same that in "initialize" function
        """

        print('#----------------------------------------------------------------------------#')
        print('                   Pinus radiata model (Galicia) is running                   ')
        print('#----------------------------------------------------------------------------#')

        if time != 1:
            print('BE CAREFUL! That model was developed to 1 year execution, and you are trying to make a', time, 'years execution!')
            print('Please, change your execution conditions to the recommended (1 year execution). If not, the output values will be not correct.')

        try:  # errors inside that construction will be announced

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # stablish an order to calculate tree variables
            bal: float = 0.0

            for tree in plot_trees:  # for each tree...

                if tree.status is None:  # only update tree alive data

                #-----------------------------------BASAL AREA-----------------------------------------#

                    tree.add_value('bal', bal)  # the first tree must receive 0 value (m2)
                    tree.add_value('basal_area', math.pi * (tree.dbh / 2) ** 2)  # normal (at 1.30m) section (cm2) calculation
                    tree.add_value('ba_ha', tree.basal_area * tree.expan / 10000)  # basimetric area per ha (m2/ha)
                    bal += tree.basal_area * tree.expan / 10000  # then, that value is acumulated

                    tree.add_value('hd_ratio', tree.height * 100 / tree.dbh)  # height/diameter ratio (%) calculation
                    tree.add_value('normal_circumference', math.pi * tree.dbh)  # normal (at 1.30m) circumference (cm) calculation

                    #-----------------------------------FUNCTIONS-----------------------------------------#

                    self.crown(tree, plot, 'process_plot')  # activate crown variables calculation

                    self.vol(tree, plot)  # activate volume variables calculation
                    
                    self.merch_classes(tree)  # activate wood uses variables calculation

                    self.biomass(tree)  # activate biomass variables calculation

            self.merch_classes_plot(plot)  # activate wood uses (plot) variables calculation

            self.biomass_plot(plot)  # activate biomass (plot) variables calculation       

        except Exception:
            self.catch_model_exception()


    def taper_equation_with_bark(self, tree: Tree, hr: float):
        """
        Function that returns the taper equation to calculate the diameter (cm, over bark) at different height
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually
        Source for Stud model:
            Doc.: Badía M, Rodríguez F, Broto M (2001). Modelos del perfil del árbol. Aplicación al pino radiata (Pinus radiata D. Don). In Congresos Forestales
            Ref.: Badía et al, 2001
        Source for Fang model:
            Doc.: Diéguez-Aranda U, Rojo A, Castedo-Dorado F, et al (2009). Herramientas selvícolas para la gestión forestal sostenible en Galicia. Forestry, 82, 1-16
            Ref.: Diéguez-Aranda et al, 2009
        """

        # Stud model

        # a1 = 0.7123
        # a11 = 0.002009
        # a2 = -0.8252
        # a3 = 0.36695
        # a4 = 12.6006
        # a5 = 0.820038

        # h = tree.height * 100  # height in cm
        # z = hr * 100  # relative height in cm

        # dob = a5*tree.dbh*((1 - z/h)**(a1 + a11*h/tree.dbh + a2*(1 - z/h))) * (1 + a3*(2.7182818284 ** (-a4*z/h)))


        # Fang model

        ao = 4.851e-5
        a1 = 1.883
        a2 = 1.004
        b1 = 8.702e-6
        b2 = 3.302e-5
        b3 = 2.899e-5
        p1 = 0.06526
        p2 = 0.6560

        hst = 0.0  # stump height (m) --> 0.2 on merch_classes function
        ht = tree.height
        h = ht - hst  # height from stump to comercial diameter (m)
        dbh = tree.dbh
        k = math.pi / 40000
        alpha1 = (1 - p1) ** (((b2 - b1) * k) / (b1 * b2))
        alpha2 = (1 - p2) ** (((b3 - b2) * k) / (b2 * b3))

        if isinstance(hr, float) == False:  # on the cases where hr is an array...
            I1 = []  # we create two lists of values
            I2 = []
            for i in hr:  # for each hr value, we calculate the values of the other 2 parameters
                if p1 <= i and i <= p2:
                    a = 1
                else:
                    a = 0
                if p2 <= i and i <= 1:
                    b = 1
                else:
                    b = 0
                I1.append(a)  # we add the parameters to the lists
                I2.append(b)
            I1 = np.array(I1)  # when the lists are full, we transform list into array to simplify the following calculations
            I2 = np.array(I2)
        else:  # on the case we have only 1 value to hr, we add the values to the parameters directly
            if p1 <= hr and hr <= p2:
                I1 = 1
            else:
                I1 = 0
            if p2 <= hr and hr <= 1:
                I2 = 1
            else:
                I2 = 0


        beta = (b1 ** (1 - (I1 + I2))) * (b2 ** I1) * (b3 ** I2)
        ro = (1 - hst / ht) ** (k / b1)
        r1 = (1 - p1) ** (k / b1)
        r2 = (1 - p2) ** (k / b2)
        c1 = math.sqrt((ao * (dbh ** a1) * (h ** (a2 - (k / b1))) / (b1 * (ro - r1) + b2 * (r1 - alpha1 * r2) + b3 * alpha1 * r2)))

        if isinstance(hr, float) == False:  # on the cases where hr is an array...    
            dob = []
            counter = 0
            for x in hr:  # for each hr value, we calculate the values of dob
                d = (c1 * (math.sqrt(ht ** ((k - b1) / b1) * (1 - hr[counter]) ** ((k - beta[counter]) / beta[counter]) * alpha1 ** (I1[counter] + I2[counter]) * alpha2 ** (I2[counter]))))
                dob.append(d)  # we add the value to a list
                counter += 1
            dob = np.array(dob)  # and transform the list to an array 
        else:  # on the case we have only 1 value to hr, we calculate dob directly
            dob = (c1 * (math.sqrt(ht ** ((k - b1) / b1) * (1 - hr) ** ((k - beta) / beta) * alpha1 ** (I1 + I2) * alpha2 ** (I2))))
 
        return dob  # diameter over bark (cm)     


    def taper_equation_without_bark(self, tree: Tree, hr: float):
        """
        Function that returns the taper equation to calculate the diameter (cm, without bark) at different height
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually
        Source:
            Doc.: Badía M, Rodríguez F, Broto M (2001). Modelos del perfil del árbol. Aplicación al pino radiata (Pinus radiata D. Don). In Congresos Forestales
            Ref.: Badía et al, 2001
        """

        # a1 = 0.6665
        # a11 = 0.002472
        # a2 = -0.7668
        # a3 = 0.18857
        # a4 = 11.4727
        # a5 = 0.90117

        # h = tree.height * 100  # height in cm
        # z = hr * 100  # relative height in cm

        # dub = a5*tree.dbh*((1 - z/h)**(a1 + a11*h/tree.dbh + a2*(1 - z/h))) * (1 + a3*(2.7182818284 ** (-a4*z/h)))

        # return dub


    def merch_classes(self, tree: Tree):
        """
        Function used to calcule the different comercial volumes depending on the wood purposes
        That function is run by initialize and process_plot functions
        The data criteria to clasify the wood by different uses was obtained from:
            Doc.: Rodriguez F (2009). Cuantificación de productos forestales en la planificación forestal:
                  Análisis de casos con cubiFOR. In Congresos Forestales
            Ref.: Rodriguez 2009
        """

        ht = tree.height  # total height as ht to simplify
        # class_conditions has different lists for each usage, following that: [wood_usage, hmin/ht, dmin, dmax]
        # [WOOD USE NAME , LOG RELATIVE LENGTH RESPECT TOTAL TREE HEIGHT, MINIMUM DIAMETER, MAXIMUM DIAMETER]
        class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]
        
        # usage and merch_list are a dictionary and a list that are returned from merch_calculation
        # to that function, we must send the following information: tree, class_conditions, and the name of our class on this model you are using
        usage, merch_list = TreeModel.merch_calculation(tree, class_conditions, PinusRadiataGalicia)

        counter = -1
        for k,i in usage.items():
            counter += 1
            tree.add_value(k, merch_list[counter])  # add merch_list values to each usage


    def merch_classes_plot(self, plot: Plot):
        """
        Function to calculate the wood uses values to the plot.
        That function is run by initialize and process_plot functions.
        """

        plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # stablish an order to calculate tree variables

        plot_unwinding = plot_veneer = plot_saw_big = plot_saw_small = plot_saw_canter = plot_post = plot_stake = plot_chips =  0

        for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

            # plot_unwinding += tree.unwinding
            # plot_veneer += tree.veneer 
            plot_saw_big += tree.saw_big
            plot_saw_small += tree.saw_small
            plot_saw_canter += tree.saw_canter
            # plot_post += tree.post
            # plot_stake += tree.stake
            plot_chips += tree.chips

        # plot.add_value('UNWINDING', plot_unwinding/1000)  # now, we add the plot value to each variable, changing the unit to m3
        # plot.add_value('VENEER', plot_veneer/1000)
        plot.add_value('SAW_BIG', plot_saw_big/1000)
        plot.add_value('SAW_SMALL', plot_saw_small/1000)
        plot.add_value('SAW_CANTER', plot_saw_canter/1000)
        # plot.add_value('POST', plot_post/1000)
        # plot.add_value('STAKE', plot_stake/1000)
        plot.add_value('CHIPS', plot_chips/1000)


    def crown(self, tree: Tree, plot: Plot, func):
        """
        Function to calculate crown variables for each tree.
        That function is run by initialize and process_plot functions.
        Crown equations:
            Doc.: Crecente-Campo F (2008). Modelo de crecimiento de árbol individual para Pinus radiata D. Don en Galicia. Univ Santiago de Compostela
            Ref.: Crecente-Campo, 2008
        """

        if func == 'initialize':  # if that function is called from initilize, first we must check if that variables are available on the initial inventory
            if tree.hlcw == 0:  # if the tree hasn't height maximum crown-width (m) value, it is calculated
                tree.add_value('hlcw', - 4.7570 - 0.08092*tree.dbh + 0.6408*tree.height + 0.1881*tree.tree_age + 0.1998*plot.si)
            if tree.hcb == 0:  # if the tree hasn't basal crown (m) value, it is calculated
                tree.add_value('hcb', - 3.265 - 0.1415*tree.dbh + 0.5117*tree.height + 0.1430*tree.tree_age + 0.1691*plot.dominant_h)
        else:
            tree.add_value('hlcw', - 4.7570 - 0.08092*tree.dbh + 0.6408*tree.height + 0.1881*tree.tree_age + 0.1998*plot.si)
            tree.add_value('hcb', - 3.265 - 0.1415*tree.dbh + 0.5117*tree.height + 0.1430*tree.tree_age + 0.1691*plot.dominant_h)

        tree.add_value('cr', 1 - tree.hcb / tree.height)  # crown ratio calculation (%)
        tree.add_value('lcw', 0.06185*(tree.dbh**1.185)*math.exp(-0.009319*plot.basal_area -0.009502*plot.age))  # maximum crown-width (m) calculation


    def vol(self, tree: Tree, plot: Plot):
        """
        Function to calculate volume variables for each tree.
        That function is run by initialize and process_plot functions.
        """

        hr = np.arange(0, 1, 0.001)  # that line stablish the integrate conditions for volume calculation
        dob = self.taper_equation_with_bark(tree, hr)  # diameter over bark using taper equation (cm)
        # dub = self.taper_equation_without_bark(tree, hr)  # diameter under/without bark using taper equation (cm)
        fwb = (dob / 20) ** 2  # radius^2 using dob (dm2)
        # fub = (dub / 20) ** 2  # radius^2 using dub (dm2)
        tree.add_value('vol', math.pi * tree.height * 10 * integrate.simps(fwb, hr))  # volume over bark using simpson integration (dm3)
        # tree.add_value('bole_vol', math.pi * tree.height * 10 * integrate.simps(fub, hr))  # volume under bark using simpson integration (dm3)
        # tree.add_value('bark_vol', tree.vol - tree.bole_vol)  # bark volume (dm3)
        tree.add_value('vol_ha', tree.vol * tree.expan / 1000)  # volume over bark per ha (m3/ha)


    def biomass(self, tree: Tree):
        """
        Function to calculate volume variables for each tree.
        That function is run by initialize and process_plot functions.
        Biomass equations:
            Doc.: Diéguez-Aranda U, Rojo A, Castedo-Dorado F, et al (2009). Herramientas selvícolas para la gestión forestal sostenible en Galicia. Forestry, 82, 1-16
            Ref.: Diéguez-Aranda et al, 2009
        """

        wstb = 0.01230*(tree.dbh**1.604)*(tree.height**1.413)
        wsb = 0.003600*(tree.dbh**2.656)
        wb2_7 = 1.938 + 0.001065*(tree.dbh**2)*tree.height
        wthinb = 0.03630*(tree.dbh**2.609)*(tree.height**(-0.9417)) 
        wb05 = 0.007800*(tree.dbh**1.961)
        wl = 0.04230*(tree.dbh**1.714)
        wr = 0.06174*(tree.dbh**2.144)
        wt = wstb + wsb + wb2_7 + wthinb + wb05 + wl + wr

        # tree.add_value('wsw', wsw)  # wsw = stem wood (Kg)
        tree.add_value('wsb', wsb)  # wsb = stem bark (Kg)
        # tree.add_value('w_cork', w_cork)   # w_cork = fresh cork biomass (Kg)
        # tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (Kg)
        tree.add_value('wstb', wstb)  # wstb = wsw + wthickb, stem + branches >7 cm (Kg)
        tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (Kg)
        # tree.add_value('wb2_t', wb2_t)  # wb2_t = wb2_7 + wthickb; branches >2 cm (Kg)
        tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (Kg)
        tree.add_value('wb05', wb05)  # wb05 = thinniest branches (<0.5 cm) (Kg)
        tree.add_value('wl', wl)  # wl = leaves (Kg)
        # tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches <2 cm and leaves (Kg)
        # tree.add_value('wbl0_7', wbl0_7)  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Kg)
        tree.add_value('wr', wr)  # wr = roots (Kg)
        tree.add_value('wt', wt)  # wt = biomasa total (Kg)


    def biomass_plot(self, plot: Plot):
        """
        Function to calculate the wood uses values to the plot.
        That function is run by initialize and process_plot functions.
        """

        plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # stablish an order to calculate tree variables

        plot_wsw = plot_wsb = plot_w_cork = plot_wthickb = plot_wstb = plot_wb2_7 = plot_wb2_t = plot_wthinb = plot_wl = plot_wtbl = plot_wbl0_7 = plot_wr = plot_wt =  0

        for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

            # plot_wsw += tree.wsw
            plot_wsb += tree.wsb 
            # plot_w_cork += tree.w_cork
            # plot_wthickb += tree.wthickb
            plot_wstb += tree.wstb
            plot_wb2_7 += tree.wb2_7
            # plot_wb2_t += tree.wb2_t
            plot_wthinb += tree.wthinb
            plot_wl += tree.wl
            # plot_wtbl += tree.wtbl
            # plot_wbl0_7 += tree.wbl0_7
            plot_wr += tree.wr
            plot_wt += tree.wt

        # plot.add_value('WSW', plot_wsw/1000)  # Wsw  # wsw = stem wood (Tn)
        plot.add_value('WSB', plot_wsb/1000)  # Wsb  # wsb = stem bark (Tn)
        # plot.add_value('W_CORK', plot_w_cork/1000)  # W Fresh Cork  # w_cork = fresh cork biomass (Tn)
        # plot.add_value('WTHICKB', plot_wthickb/1000)  # Wthickb  # wthickb = Thick branches > 7 cm (Tn)
        plot.add_value('WSTB', plot_wstb/1000)  # Wstb  # wstb = wsw + wthickb, stem + branches >7 cm (Tn)
        plot.add_value('WB2_7', plot_wb2_7/1000)  # Wb2_7  # wb2_7 = branches (2-7 cm) (Tn)
        # plot.add_value('WB2_T', plot_wb2_t/1000)  # Wb2_t  # wb2_t = wb2_7 + wthickb; branches >2 cm (Tn)
        plot.add_value('WTHINB', plot_wthinb/1000)  # Wthinb  # wthinb = Thin branches (2-0.5 cm) (Tn)
        plot.add_value('WB05', plot_wb05)  # wb05 = thinniest branches (<0.5 cm) (Kg)
        plot.add_value('WL', plot_wl/1000)  # Wl  # wl = leaves (Tn)
        # plot.add_value('WTBL', plot_wtbl/1000)  # Wtbl  # wtbl = wthinb + wl; branches <2 cm and leaves (Tn)
        # plot.add_value('WBL0_7', plot_wbl0_7/1000)  # Wbl0_7  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Tn)
        plot.add_value('WR', plot_wr/1000)  # Wr  # wr = roots (Tn)
        plot.add_value('WT', plot_wt/1000)  # Wt  # wt = biomasa total (Tn)


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
        #PLOT_VARIABLE_NAMES.remove('BA_MAX')  # BA Max  # (m2)
        #PLOT_VARIABLE_NAMES.remove('BA_MIN')  # BA Min  # (m2)
        #PLOT_VARIABLE_NAMES.remove('MEAN_BA')  # Mean BA  # (m2)
        
        # Basic plot variables calculated - diameter
        #PLOT_VARIABLE_NAMES.remove('DBH_MAX')  # D Max  # (cm)
        #PLOT_VARIABLE_NAMES.remove('DBH_MIN')  # D Min  # (cm)
        #PLOT_VARIABLE_NAMES.remove('MEAN_DBH')  # Mean dbh  # (cm)
        #PLOT_VARIABLE_NAMES.remove('QM_DBH')  # Quadratic mean dbh  # (m2)
        #PLOT_VARIABLE_NAMES.remove('DOMINANT_DBH')  # Dominant dbh  # (cm)

        # Basic plot variables calculated - height
        #PLOT_VARIABLE_NAMES.remove('H_MAX')  # H Max  # (m)
        #PLOT_VARIABLE_NAMES.remove('H_MIN')  # H Min  # (m)
        #PLOT_VARIABLE_NAMES.remove('MEAN_H')  # Mean height  # (m)
        #PLOT_VARIABLE_NAMES.remove('DOMINANT_H')  # Dominant height  # (m)

        # Basic plot variables calculated - crown
        #PLOT_VARIABLE_NAMES.remove('CROWN_MEAN_D')  # Mean crown diameter  # (m)
        #PLOT_VARIABLE_NAMES.remove('CROWN_DOM_D')  # Dominant crown diameter  # (m)
        #PLOT_VARIABLE_NAMES.remove('CANOPY_COVER')  # Canopy cover  # (%)

        # Basic plot variables calculated - plot
        #PLOT_VARIABLE_NAMES.remove('REINEKE')  # Reineke Index  # Stand Density Index - SDI
        #PLOT_VARIABLE_NAMES.remove('HART')  # Hart-Becking Index  # Hart-Becking Index - S
        #PLOT_VARIABLE_NAMES.remove('SI')  # Site Index  # (m)
        PLOT_VARIABLE_NAMES.remove('QI')  # Quality Index

        # Basic plot variables calculated - volume
        #PLOT_VARIABLE_NAMES.remove('VOL')  # Volume  # (m3)
        PLOT_VARIABLE_NAMES.remove('BOLE_VOL')  # Bole Volume  # (m3)
        PLOT_VARIABLE_NAMES.remove('BARK_VOL')  # Bark Volumen  # (m3)

        # Plot variables calculated - biomass
        PLOT_VARIABLE_NAMES.remove('WSW')  # Wsw  # wsw = stem wood (Kg)
        # PLOT_VARIABLE_NAMES.remove('WSB')  # Wsb  # wsb = stem bark (Kg)
        PLOT_VARIABLE_NAMES.remove('W_CORK')  # W Fresh Cork  # w_cork = fresh cork biomass (Kg)
        PLOT_VARIABLE_NAMES.remove('WTHICKB')  # Wthickb  # wthickb = Thick branches > 7 cm (Kg)
        # PLOT_VARIABLE_NAMES.remove('WSTB')  # Wstb  # wstb = wsw + wthickb, stem + branches >7 cm (Kg)
        # PLOT_VARIABLE_NAMES.remove('WB2_7')  # Wb2_7  # wb2_7 = branches (2-7 cm) (Kg)
        PLOT_VARIABLE_NAMES.remove('WB2_T')  # Wb2_t  # wb2_t = wb2_7 + wthickb; branches >2 cm (Kg)
        # PLOT_VARIABLE_NAMES.remove('WTHINB')  # Wthinb  # wthinb = Thin branches (2-0.5 cm) (Kg)
        #PLOT_VARIABLE_NAMES.remove('WB05')  # wb05 = thinniest branches (<0.5 cm) (Kg)
        # PLOT_VARIABLE_NAMES.remove('WL')  # Wl  # wl = leaves (Kg)
        PLOT_VARIABLE_NAMES.remove('WTBL')  # Wtbl  # wtbl = wthinb + wl; branches <2 cm and leaves (Kg)
        PLOT_VARIABLE_NAMES.remove('WBL0_7')  # Wbl0_7  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Kg)
        # PLOT_VARIABLE_NAMES.remove('WR')  # Wr  # wr = roots (Kg)
        # PLOT_VARIABLE_NAMES.remove('WT')  # Wt  # wt = biomasa total (Kg) 

        # Plot variables calculated - wood uses
        PLOT_VARIABLE_NAMES.remove('UNWINDING')  # Unwinding  # unwinding = useful volume for unwinding destiny (m3)
        PLOT_VARIABLE_NAMES.remove('VENEER')  # Veneer  # veneer = useful volume for veneer destiny (m3)
        #PLOT_VARIABLE_NAMES.remove('SAW_BIG')  # Saw big  # saw_big = useful volume for big saw destiny (m3)
        #PLOT_VARIABLE_NAMES.remove('SAW_SMALL')  # Saw small  # saw_small = useful volume for small saw destiny (m3)
        #PLOT_VARIABLE_NAMES.remove('SAW_CANTER')  # Saw canter  # saw_canter = useful volume for canter saw destiny (m3)
        PLOT_VARIABLE_NAMES.remove('POST')  # Post  # post = useful volume for post destiny (m3)
        PLOT_VARIABLE_NAMES.remove('STAKE')  # Stake  # stake = useful volume for stake destiny (m3)
        #PLOT_VARIABLE_NAMES.remove('CHIPS')  # Chips  # chips = useful volume for chips destiny (m3)

#########################################################################################################################
############################################  TREE variables ############################################################
#########################################################################################################################

#------------------------------------------- REMOVE -------------------------------------------------------#

        # Tree general information
        #VARIABLE_NAMES.remove('number_of_trees')  #  number of trees
        #VARIABLE_NAMES.remove('specie')  #  specie
        #VARIABLE_NAMES.remove('quality')  #  quality
        #VARIABLE_NAMES.remove('shape')  #  shape
        #VARIABLE_NAMES.remove('special_param')  #  parameter esp
        #VARIABLE_NAMES.remove('remarks')  #  remarks
        #VARIABLE_NAMES.remove('age_130')  #  normal age  # (years)
        #VARIABLE_NAMES.remove('social_class')  #  social class
        #VARIABLE_NAMES.remove('tree_age')  #  tree age  # (years)
        #VARIABLE_NAMES.remove('coord_x')  #  coord X
        #VARIABLE_NAMES.remove('coord_y')  #  coord Y

        # Basic variables measured
        VARIABLE_NAMES.remove('dbh_1')  #  dbh 1  # diameter mesasurement 1 (cm)
        VARIABLE_NAMES.remove('dbh_2')  #  dbh 2  # diameter mesasurement 1 (cm)
        #VARIABLE_NAMES.remove('stump_h')  #  stump height  # (m)
        VARIABLE_NAMES.remove('bark_1')  #  bark thickness 1  # bark thickness mesasurement 1 (mm)
        VARIABLE_NAMES.remove('bark_2')  #  bark thickness 2  # bark thickness mesasurement 2 (mm)
        VARIABLE_NAMES.remove('bark')  #  bark thickness  # mean bark thickness (mm)

        # Basic variables calculated
        #VARIABLE_NAMES.remove('normal_circumference')  #  normal circumference  # circumference at breast height (cm)
        #VARIABLE_NAMES.remove('hd_ratio')  #  slentherness  # (%)
        #VARIABLE_NAMES.remove('basal_area')  #  basal area  #  (m2)
        #VARIABLE_NAMES.remove('bal')  #  basal area acumulated  # (m2)
        #VARIABLE_NAMES.remove('ba_ha')  #  basal area per ha  # (m2/ha)    

        # Crown variables
        #VARIABLE_NAMES.remove('cr')  #  crown ratio  # (%)
        #VARIABLE_NAMES.remove('lcw')  #  lcw  #  largest crown width (m)
        #VARIABLE_NAMES.remove('hcb')  #  hcb  # height crown base (m)
        #VARIABLE_NAMES.remove('hlcw')  #  hlcw  # height of largest crown width (m)

        # Volume variables
        #VARIABLE_NAMES.remove('vol')  #  volume  # volume with bark (dm3)
        #VARIABLE_NAMES.remove('bole_vol')  #  bole volume  # volume without bark (dm3)
        VARIABLE_NAMES.remove('bark_vol')  #  bark vol  # volume of bark (dm3)
        VARIABLE_NAMES.remove('firewood_vol')  #  fuelwood volume  # (dm3)
        #VARIABLE_NAMES.remove('vol_ha')  #  volume per ha  # volume with bark per hectare (m3/ha)

        # Biomass variables
        VARIABLE_NAMES.remove('wsw')  #  wsw  # wsw = stem wood (Kg)
        #VARIABLE_NAMES.remove('wsb')  #  wsb # wsb = stem bark (Kg)
        VARIABLE_NAMES.remove('w_cork')  #  w fresh cork  # w_cork = fresh cork biomass (Kg)
        VARIABLE_NAMES.remove('wthickb')  #  wthickb  # wthickb = Thick branches > 7 cm (Kg)
        #VARIABLE_NAMES.remove('wstb')  #  wstb  # wstb = wsw + wthickb, stem + branches >7 cm (Kg)
        #VARIABLE_NAMES.remove('wb2_7')  #  wb2_7  # wb2_7 = branches (2-7 cm) (Kg)
        VARIABLE_NAMES.remove('wb2_t')  #  wb2_t  # wb2_t = wb2_7 + wthickb; branches >2 cm (Kg)
        #VARIABLE_NAMES.remove('wthinb')  #  wthinb  # wthinb = Thin branches (2-0.5 cm) (Kg)
        #VARIABLE_NAMES.remove('wb05')  # wb05 = thinniest branches (<0.5 cm) (Kg)
        #VARIABLE_NAMES.remove('wl')  #  wl  # wl = leaves (Kg)
        VARIABLE_NAMES.remove('wtbl')  #  wtbl  # wtbl = wthinb + wl; branches <2 cm and leaves (Kg)
        VARIABLE_NAMES.remove('wbl0_7')  #  wbl0_7  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Kg)
        #VARIABLE_NAMES.remove('wr')  #  wr  # wr = roots (Kg)
        #VARIABLE_NAMES.remove('wt')  #  wt  # wt = biomasa total (Kg)

        # Wood uses variables
        VARIABLE_NAMES.remove('unwinding')  #  unwinding  # unwinding = useful volume for unwinding destiny (dm3)
        VARIABLE_NAMES.remove('veneer')  #  veneer  # veneer = useful volume for veneer destiny (dm3)
        #VARIABLE_NAMES.remove('saw_big')  #  saw big  # saw_big = useful volume for big saw destiny (dm3)
        #VARIABLE_NAMES.remove('saw_small')  #  saw small  # saw_small = useful volume for small saw destiny (dm3)
        #VARIABLE_NAMES.remove('saw_canter')  #  saw canter  # saw_canter = useful volume for canter saw destiny (dm3)
        VARIABLE_NAMES.remove('post')  #  post  # post = useful volume for post destiny (dm3)
        VARIABLE_NAMES.remove('stake')  #  stake  # stake = useful volume for stake destiny (dm3)
        #VARIABLE_NAMES.remove('chips')  #  chips  # chips = useful volume for chips destiny (dm3)
        
        # Quercus suber special variables
        VARIABLE_NAMES.remove('dbh_oc')  #  dbh over cork  # dbh over cork (cm) - Quercus suber
        VARIABLE_NAMES.remove('h_uncork')  #  uncork height  # uncork height on main stem (m) - Quercus suber
        VARIABLE_NAMES.remove('nb')  #  uncork boughs  # number of main bough stripped - Quercus suber
        VARIABLE_NAMES.remove('cork_cycle')  #  cork cycle  # moment to obtain cork data; 0 to the moment just immediately before the stripping process,
    # or 1 to the moment after the stripping process or at an intermediate age of the cork cycle production - Quercus suber

PinusRadiataGalicia.vars()