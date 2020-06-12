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

# Quercus suber model (Cataluña, Spain), version 01
# Written by iuFOR
# Sustainable Forest Management Research Institute UVa-INIA, iuFOR (University of Valladolid-INIA)
# Higher Technical School of Agricultural Engineering, University of Valladolid - Avd. Madrid s/n, 34004 Palencia (Spain)
# http://sostenible.palencia.uva.es/

class QuercusSuberCataluña(TreeModel):


    def __init__(self, configuration=None):
        super().__init__(name="Quercus suber - Cataluña", version=1)


    def catch_model_exception(self):  # that function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)


    def initialize(self, plot: Plot):
        """
        Function that update the gaps on the information with the inventory data
        Height/Diameter equation:
            Doc.: Sánchez-González M, Cañellas I, Montero G (2007). Generalized height-diameter and crown diameter prediction models for cork oak forests in Spain. Forest Systems, 16(1), 76-88
            Ref.: Sánchez-González et al, 2007
            Doc.: Sánchez-González M, Calama R, Cañellas I, Montero G (2007). Management oriented growth models for multifunctional Mediterranean Forests: the case of Cork Oak (Quercus suber L.). In EFI proceedings (Vol. 56, pp. 71-84)
            Ref.: Sánchez-González et al, 2007
        SI equation:
            Doc.: Sánchez-González M, Tomé M, Montero G (2005). Modelling height and diameter growth of dominant cork oak trees in Spain. Annals of Forest Science, 62(7), 633-643
            Ref.: Sánchez-González et al, 2005
            Doc.: Sánchez-González M, Calama R, Cañellas I, Montero G (2007). Management oriented growth models for multifunctional Mediterranean Forests: the case of Cork Oak (Quercus suber L.). In EFI proceedings (Vol. 56, pp. 71-84)
            Ref.: Sánchez-González et al, 2007
        Dominant diameter equation:
            Doc.: Sánchez-González M, Tomé M, Montero G (2005). Modelling height and diameter growth of dominant cork oak trees in Spain. Annals of Forest Science, 62(7), 633-643
            Ref.: Sánchez-González et al, 2005
            Doc.: Sánchez-González M, Calama R, Cañellas I, Montero G (2007). Management oriented growth models for multifunctional Mediterranean Forests: the case of Cork Oak (Quercus suber L.). In EFI proceedings (Vol. 56, pp. 71-84)
            Ref.: Sánchez-González et al, 2007
        """

        print('#----------------------------------------------------------------------------#')
        print('                  Quercus suber model (Cataluña) is running                   ')
        print('#----------------------------------------------------------------------------#')

        try:  # errors inside that construction will be announced
            
            #-----------------------------------SI-----------------------------------------#

            # site index is defined as top height at a base age of 80 years
            t2 = 80  # age to estimate the SI and Dominant_diamter (years)
            SI = 20.7216 / ((1 - (1 - 20.7216/plot.dominant_h)*(plot.age/t2)) ** 1.4486)
            plot.add_value('SI', SI)  # Site Index (m) calculation

            # a1 = math.log(1 - math.exp(-0.0063*plot.age))
            # a2 = math.log(1 - math.exp(-0.0063*t2))
            # dbh must be diameter under bark (cm)
            # DD = ((83.20 + 5.28*plot.si - 1.53*plot.dominant_h*100/plot.dominant_dbh)**(1 - a2/a1)) * (plot.dominant_dbh**(a2/a1))
            # plot.add_value('DOMINANT_DBH', DD )

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # stablish an order to calculate tree variables
            bal: float = 0

            for tree in plot_trees:  # for each tree...

                #-----------------------------------DBH CALCULATION-----------------------------------------#

                if tree.dbh == 0:
                    tree.add_value('dbh', tree.dbh_oc - tree.bark/10)  # dbh under cork calculated if it is not at the initial inventory (cm)
                
                if tree.dbh_oc != 0 and tree.bark == 0:
                    tree.add_value('bark', (tree.dbh_oc - tree.dbh)*10)  # cork calculated using dbh outside and inside cork (mm)

                if tree.dbh_oc == 0:
                    tree.add_value('dbh_oc', tree.dbh + tree.bark/10)  # diameter outside bark calculation (cm)

                #-----------------------------------BASAL AREA-----------------------------------------#

                tree.add_value('bal', bal)  # the first tree must receive 0 value (m2)
                tree.add_value('basal_area', math.pi * (tree.dbh / 2) ** 2)  # normal (at 1.30m) section (cm2) calculation
                tree.add_value('ba_ha', tree.basal_area * tree.expan / 10000)  # basimetric area per ha (m2/ha)
                bal += tree.basal_area * tree.expan / 10000  # then, that value is acumulated

                tree.add_value('hd_ratio', tree.height * 100 / tree.dbh)  # height/diameter ratio (%) calculation
                tree.add_value('normal_circumference', math.pi * tree.dbh)  # normal (at 1.30m) circumference (cm) calculation

                #-----------------------------------HEIGHT-----------------------------------------#

                if tree.height == 0:  # if the tree hasn't height (m) value, it is calculated
                    tree.add_value('height', 1.3 + (plot.dominant_h - 1.3)*((tree.dbh/plot.dominant_dbh)**0.4898))

                #-----------------------------------FUNCTIONS-----------------------------------------#

                self.crown(tree, plot, 'initialize')  # activate crown variables calculation

                self.vol(tree, plot)  # activate volume variables calculation
                
                # self.merch_classes(tree)  # activate wood uses variables calculation

                self.biomass(tree)  # activate biomass variables calculation

            # self.merch_classes_plot(plot)  # activate wood uses (plot) variables calculation

            self.biomass_plot(plot)  # activate biomass (plot) variables calculation   

        except Exception:
            self.catch_model_exception()


    def survives(self, time: int, plot: Plot, tree: Tree):
        """
        Survive function. The trees that are death appear on the output with "M" on the "State of the tree" column
        """
        return 1


    def grow(self, time: int, plot: Plot, old_tree: Tree, new_tree: Tree):
        """
        Function that run the diameter and height growing equations
        Source for diameter grow equation:
            Doc.: Sánchez-González M, del Río M, Cañellas I, Montero G (2006). Distance independent tree diameter growth model for cork oak stands. Forest Ecology and Management, 225(1-3), 262-270
            Ref.: Sánchez-González et al, 2006
            Doc.: Sánchez-González M, Calama R, Cañellas I, Montero G (2007). Management oriented growth models for multifunctional Mediterranean Forests: the case of Cork Oak (Quercus suber L.). In EFI proceedings (Vol. 56, pp. 71-84)
            Ref.: Sánchez-González et al, 2007
        Source for height/diameter equation:
            Doc.: Sánchez-González M, Cañellas I, Montero G (2007). Generalized height-diameter and crown diameter prediction models for cork oak forests in Spain. Forest Systems, 16(1), 76-88
            Ref.: Sánchez-González et al, 2007
            Doc.: Sánchez-González M, Calama R, Cañellas I, Montero G (2007). Management oriented growth models for multifunctional Mediterranean Forests: the case of Cork Oak (Quercus suber L.). In EFI proceedings (Vol. 56, pp. 71-84)
            Ref.: Sánchez-González et al, 2007
        Source for cork grow equation:
            Doc.: Sánchez-González M, Calama R, Cañellas I, Montero G (2007). Management oriented growth models for multifunctional Mediterranean Forests: the case of Cork Oak (Quercus suber L.). In EFI proceedings (Vol. 56, pp. 71-84)
            Ref.: Sánchez-González et al, 2007
        """

        idu = 0.18 + 7.89/plot.density - 1.02/plot.si + 2.45/old_tree.dbh
        new_tree.sum_value('dbh', idu)  # annual diameter increment under cork (cm)


        h2 = 1.3 + (plot.dominant_h - 1.3)*((new_tree.dbh/plot.dominant_dbh)**0.4898)
        new_tree.add_value('height', h2)  # height/diameter equation result (m)


        t = old_tree.tree_age + 1  # years
        Xo1 = 0.5*(math.log(old_tree.bark) - 0.57*math.log(1 - math.exp(-0.04*old_tree.tree_age)))
        # Xo2 = math.sqrt((math.log(old_tree.bark) - 0.57*math.log(1 - math.exp(-0.04*old_tree.tree_age))**2 - 4*1.86*math.log(1 - math.exp(-0.04*old_tree.tree_age))))
        Xo = Xo1 # +- Xo2

        cork_2 = old_tree.bark*(((1 - math.exp(-0.04*t)) / (1 - math.exp(-0.04*old_tree.tree_age)))**((0.57+1.86)/Xo))
        new_tree.sum_value('bark', cork_2)


    def add_tree(self, time: int, plot: Plot):
        """
        Ingrowth stand function.
        That function calculates the probability that trees are added to the plot, and if that probability is higher than a limit value, then basal area
        incorporated are calculated. The next function will order how to divide that basal area on the different diametric classes.
        """
        return 0


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
        print('                  Quercus suber model (Cataluña) is running                   ')
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
                    
                    # self.merch_classes(tree)  # activate wood uses variables calculation

                    self.biomass(tree)  # activate biomass variables calculation

            # self.merch_classes_plot(plot)  # activate wood uses (plot) variables calculation

            self.biomass_plot(plot)  # activate biomass (plot) variables calculation   

        except Exception:
            self.catch_model_exception()


    def taper_equation_with_bark(self, tree: Tree, hr: float):
        """
        Function that returns the taper equation to calculate the diameter (cm, over bark) at different height
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually
        """


    def taper_equation_without_bark(self, tree: Tree, hr: float):
        """
        Function that returns the taper equation to calculate the diameter (cm, without bark) at different height
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually
        """


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
        usage, merch_list = TreeModel.merch_calculation(tree, class_conditions, QuercusSuberCataluña)

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
        Mean crown diameter equation:
            Doc.: Sánchez-González M, Cañellas I, Montero G (2007). Generalized height-diameter and crown diameter prediction models for cork oak forests in Spain. Forest Systems, 16(1), 76-88
            Ref.: Sánchez-González et al, 2007
            Doc.: Sánchez-González M, Calama R, Cañellas I, Montero G (2007). Management oriented growth models for multifunctional Mediterranean Forests: the case of Cork Oak (Quercus suber L.). In EFI proceedings (Vol. 56, pp. 71-84)
            Ref.: Sánchez-González et al, 2007
        """

        if func == 'initialize':  # if that function is called from initilize, first we must check if that variables are available on the initial inventory
            if tree.lcw == 0:  # if the tree hasn't height maximum crown-width (m) value, it is calculated
                tree.add_value('lcw', (0.2416 + 0.0013*plot.qm_dbh)*tree.dbh - 0.0015*(tree.dbh**2))  # largest crown width (m)
        else:
            tree.add_value('lcw', (0.2416 + 0.0013*plot.qm_dbh)*tree.dbh - 0.0015*(tree.dbh**2))  # largest crown width (m)


    def vol(self, tree: Tree, plot: Plot):
        """
        Function to calculate volume variables for each tree.
        That function is run by initialize and process_plot functions.
        Volume under bark equation:
            Doc.: Amaral J, Tomé M (2006). Equações para estimação do volume e biomassa de duas espécies de carvalhos: Quercus suber e Quercus ilex. Publicações do GIMREF, 1-21
            Ref.: Amaral and Tomé (2006)
        """

        # hr = np.arange(0, 1, 0.001)  # that line stablish the integrate conditions for volume calculation
        # dob = self.taper_equation_with_bark(tree, hr)  # diameter over bark using taper equation (cm)
        # dub = self.taper_equation_without_bark(tree, hr)  # diameter under/without bark using taper equation (cm)
        # fwb = (dob / 20) ** 2  # radius^2 using dob (dm2)
        # fub = (dub / 20) ** 2  # radius^2 using dub (dm2)
        # tree.add_value('vol', math.pi * tree.height * 10 * integrate.simps(fwb, hr))  # volume over bark using simpson integration (dm3)
        # tree.add_value('bole_vol', math.pi * tree.height * 10 * integrate.simps(fub, hr))  # volume under bark using simpson integration (dm3)
        # tree.add_value('bark_vol', tree.vol - tree.bole_vol)  # bark volume (dm3)
        # tree.add_value('vol_ha', tree.vol * tree.expan / 1000)  # volume over bark per ha (m3/ha)
        tree.add_value('bole_vol', 0.000115*(tree.dbh**2.147335) * 1000)  # volume under bark (dm3)

        if isinstance(tree.bark, float) and isinstance(tree.h_uncork, float) and isinstance(tree.dbh_oc, float):
            tree.add_value('bark_vol', (tree.bark/100) * (tree.h_uncork*10) * ((tree.dbh + tree.dbh_oc) / 20))  # cork fresh volume (dm3)


    def biomass(self, tree: Tree):
        """
        Function to calculate volume variables for each tree.
        That function is run by initialize and process_plot functions.
        Biomass equations:
            Doc.: Ruiz-Peinado R, Montero G, del Río M (2012). Biomass models to estimate carbon stocks for hardwood tree species. Forest systems, 21(1), 42-52
            Ref.: Ruiz-Peinado et al, 2012
        Cork biomass equation:
            Doc.: Ribeiro F, Tomé M (2002). Cork weight prediction at tree level. Forest ecology and management, 171(3), 231-241
            Ref.: Ribeiro and Tomé (2002)
            Doc.: Montero G, López E (2008). Selvicultura de Quercus suber L. En: Compendio de Selvicultura Aplicada en España, Fundación Conde del Valle de Salazar. Madrid, Spain. pp, 779-829
            Ref.: Montero and López (2008)
        """

        wsw = 0.00525*(tree.dbh**2)*tree.height + 0.278*tree.dbh*tree.height
        wthickb = 0.0135*(tree.dbh**2)*tree.height
        wb2_7 = 0.127*tree.dbh*tree.height
        wtbl = 0.0463*tree.dbh*tree.height
        wr = 0.0829*(tree.dbh**2)
        wt = wsw + wb2_7 + wthickb + wtbl + wr

        tree.add_value('wsw', wsw)  # wsw = stem wood (Kg)
        # tree.add_value('wsb', wsb)  # wsb = stem bark (Kg)
        # tree.add_value('w_cork', w_cork)   # w_cork = fresh cork biomass (Kg)
        tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (Kg)
        # tree.add_value('wstb', wstb)  # wstb = wsw + wthickb, stem + branches >7 cm (Kg)
        tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (Kg)
        # tree.add_value('wb2_t', wb2_t)  # wb2_t = wb2_7 + wthickb; branches >2 cm (Kg)
        # tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (Kg)
        # tree.add_value('wb05', wb05)  # wb05 = thinniest branches (<0.5 cm) (Kg)
        # tree.add_value('wl', wl)  # wl = leaves (Kg)
        tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches <2 cm and leaves (Kg)
        # tree.add_value('wbl0_7', wbl0_7)  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Kg)
        tree.add_value('wr', wr)  # wr = roots (Kg)
        tree.add_value('wt', wt)  # wt = biomasa total (Kg)

        if isinstance(tree.h_uncork, float) and isinstance(tree.dbh_oc, float) and isinstance(tree.nb, float):

            pbhoc = (tree.dbh_oc*math.pi) / 100  # perimeter at breast height outside cork (m)
            pbhic = tree.normal_circumference / 100  # perimeter at breast height inside cork (m)
            shs = tree.h_uncork  # stripped height in the stem (m)
            nb = tree.nb + 1  # number of stripped main bough + 1

            if tree.cork_cycle == 0:  # To use inmediately before the stripping process
                if nb == 1:
                    tree.add_value('w_cork', math.exp(2.3665 + 2.2722*math.log(pbhoc) + 0.4473*math.log(shs)))
                else:
                    tree.add_value('w_cork', math.exp(2.1578 + 1.5817*math.log(pbhoc) + 0.5062*math.log(nb) + 0.6680*math.log(shs)))
            
            elif tree.cork_cycle == 1:  # To use after the stripping process or in a intermediate age of the cork cycle production
                if nb == 1:
                    tree.add_value('w_cork', math.exp(2.7506 + 1.9174*math.log(pbhic) + 0.4682*math.log(shs)))
                else:
                    tree.add_value('w_cork', math.exp(2.2137 + 0.9588*math.log(shs) + 0.6546*math.log(nb)))

        elif isinstance(tree.h_uncork, float) and isinstance(tree.dbh_oc, float) and not isinstance(tree.nb, float):

            pbhoc = (tree.dbh_oc*math.pi) / 100  # perimeter at breast height outside cork (m)
            pbhic = tree.normal_circumference / 100  # perimeter at breast height inside cork (m)
            shs = tree.h_uncork  # stripped height in the stem (m)
            nb = 1  # number of stripped main bough + 1

            if tree.cork_cycle == 0:  # To use inmediately before the stripping process
                tree.add_value('w_cork', math.exp(2.3665 + 2.2722*math.log(pbhoc) + 0.4473*math.log(shs)))
            
            elif tree.cork_cycle == 1:  # To use after the stripping process or in a intermediate age of the cork cycle production
                tree.add_value('w_cork', math.exp(2.7506 + 1.9174*math.log(pbhic) + 0.4682*math.log(shs)))
        else:
            
            tree.add_value('w_cork', 0)


    def biomass_plot(self, plot: Plot):
        """
        Function to calculate the wood uses values to the plot.
        That function is run by initialize and process_plot functions.
        """

        plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # stablish an order to calculate tree variables

        plot_wsw = plot_wsb = plot_w_cork = plot_wthickb = plot_wstb = plot_wb2_7 = plot_wb2_t = plot_wthinb = plot_wl = plot_wtbl = plot_wbl0_7 = plot_wr = plot_wt =  0

        for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

            plot_wsw += tree.wsw
            # plot_wsb += tree.wsb 
            plot_w_cork += tree.w_cork
            plot_wthickb += tree.wthickb
            # plot_wstb += tree.wstb
            plot_wb2_7 += tree.wb2_7
            # plot_wb2_t += tree.wb2_t
            # plot_wthinb += tree.wthinb
            # plot_wl += tree.wl
            plot_wtbl += tree.wtbl
            # plot_wbl0_7 += tree.wbl0_7
            plot_wr += tree.wr
            plot_wt += tree.wt

        plot.add_value('WSW', plot_wsw/1000)  # Wsw  # wsw = stem wood (Tn)
        # plot.add_value('WSB', plot_wsb/1000)  # Wsb  # wsb = stem bark (Tn)
        plot.add_value('W_CORK', plot_w_cork/1000)  # W Fresh Cork  # w_cork = fresh cork biomass (Tn)
        plot.add_value('WTHICKB', plot_wthickb/1000)  # Wthickb  # wthickb = Thick branches > 7 cm (Tn)
        # plot.add_value('WSTB', plot_wstb/1000)  # Wstb  # wstb = wsw + wthickb, stem + branches >7 cm (Tn)
        plot.add_value('WB2_7', plot_wb2_7/1000)  # Wb2_7  # wb2_7 = branches (2-7 cm) (Tn)
        # plot.add_value('WB2_T', plot_wb2_t/1000)  # Wb2_t  # wb2_t = wb2_7 + wthickb; branches >2 cm (Tn)
        # plot.add_value('WTHINB', plot_wthinb/1000)  # Wthinb  # wthinb = Thin branches (2-0.5 cm) (Tn)
        # plot.add_value('WB05', plot_wb05)  # wb05 = thinniest branches (<0.5 cm) (Kg)
        # plot.add_value('WL', plot_wl/1000)  # Wl  # wl = leaves (Tn)
        plot.add_value('WTBL', plot_wtbl/1000)  # Wtbl  # wtbl = wthinb + wl; branches <2 cm and leaves (Tn)
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
        PLOT_VARIABLE_NAMES.remove('CROWN_MEAN_D')  # Mean crown diameter  # (m)
        PLOT_VARIABLE_NAMES.remove('CROWN_DOM_D')  # Dominant crown diameter  # (m)
        PLOT_VARIABLE_NAMES.remove('CANOPY_COVER')  # Canopy cover  # (%)

        # Basic plot variables calculated - plot
        #PLOT_VARIABLE_NAMES.remove('REINEKE')  # Reineke Index  # Stand Density Index - SDI
        #PLOT_VARIABLE_NAMES.remove('HART')  # Hart-Becking Index  # Hart-Becking Index - S
        #PLOT_VARIABLE_NAMES.remove('SI')  # Site Index  # (m)
        PLOT_VARIABLE_NAMES.remove('QI')  # Quality Index

        # Basic plot variables calculated - volume
        PLOT_VARIABLE_NAMES.remove('VOL')  # Volume  # (m3)
        #PLOT_VARIABLE_NAMES.remove('BOLE_VOL')  # Bole Volume  # (m3)
        #PLOT_VARIABLE_NAMES.remove('BARK_VOL')  # Bark Volumen  # (m3)

        # Plot variables calculated - biomass
        #PLOT_VARIABLE_NAMES.remove('WSW')  # Wsw  # wsw = stem wood (Kg)
        PLOT_VARIABLE_NAMES.remove('WSB')  # Wsb  # wsb = stem bark (Kg)
        #PLOT_VARIABLE_NAMES.remove('W_CORK')  # W Fresh Cork  # w_cork = fresh cork biomass (Kg)
        #PLOT_VARIABLE_NAMES.remove('WTHICKB')  # Wthickb  # wthickb = Thick branches > 7 cm (Kg)
        PLOT_VARIABLE_NAMES.remove('WSTB')  # Wstb  # wstb = wsw + wthickb, stem + branches >7 cm (Kg)
        #PLOT_VARIABLE_NAMES.remove('WB2_7')  # Wb2_7  # wb2_7 = branches (2-7 cm) (Kg)
        PLOT_VARIABLE_NAMES.remove('WB2_T')  # Wb2_t  # wb2_t = wb2_7 + wthickb; branches >2 cm (Kg)
        PLOT_VARIABLE_NAMES.remove('WTHINB')  # Wthinb  # wthinb = Thin branches (2-0.5 cm) (Kg)
        PLOT_VARIABLE_NAMES.remove('WB05')  # wb05 = thinniest branches (<0.5 cm) (Kg)
        PLOT_VARIABLE_NAMES.remove('WL')  # Wl  # wl = leaves (Kg)
        #PLOT_VARIABLE_NAMES.remove('WTBL')  # Wtbl  # wtbl = wthinb + wl; branches <2 cm and leaves (Kg)
        PLOT_VARIABLE_NAMES.remove('WBL0_7')  # Wbl0_7  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Kg)
        #PLOT_VARIABLE_NAMES.remove('WR')  # Wr  # wr = roots (Kg)
        #PLOT_VARIABLE_NAMES.remove('WT')  # Wt  # wt = biomasa total (Kg) 

        # Plot variables calculated - wood uses
        PLOT_VARIABLE_NAMES.remove('UNWINDING')  # Unwinding  # unwinding = useful volume for unwinding destiny (m3)
        PLOT_VARIABLE_NAMES.remove('VENEER')  # Veneer  # veneer = useful volume for veneer destiny (m3)
        PLOT_VARIABLE_NAMES.remove('SAW_BIG')  # Saw big  # saw_big = useful volume for big saw destiny (m3)
        PLOT_VARIABLE_NAMES.remove('SAW_SMALL')  # Saw small  # saw_small = useful volume for small saw destiny (m3)
        PLOT_VARIABLE_NAMES.remove('SAW_CANTER')  # Saw canter  # saw_canter = useful volume for canter saw destiny (m3)
        PLOT_VARIABLE_NAMES.remove('POST')  # Post  # post = useful volume for post destiny (m3)
        PLOT_VARIABLE_NAMES.remove('STAKE')  # Stake  # stake = useful volume for stake destiny (m3)
        PLOT_VARIABLE_NAMES.remove('CHIPS')  # Chips  # chips = useful volume for chips destiny (m3)   


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
        #VARIABLE_NAMES.remove('bark')  #  bark thickness  # mean bark thickness (mm)

        # Basic variables calculated
        #VARIABLE_NAMES.remove('normal_circumference')  #  normal circumference  # circumference at breast height (cm)
        #VARIABLE_NAMES.remove('hd_ratio')  #  slentherness  # (%)
        #VARIABLE_NAMES.remove('basal_area')  #  basal area  #  (m2)
        #VARIABLE_NAMES.remove('bal')  #  basal area acumulated  # (m2)
        #VARIABLE_NAMES.remove('ba_ha')  #  basal area per ha  # (m2/ha)    

        # Crown variables
        VARIABLE_NAMES.remove('cr')  #  crown ratio  # (%)
        #VARIABLE_NAMES.remove('lcw')  #  lcw  #  largest crown width (m)
        VARIABLE_NAMES.remove('hcb')  #  hcb  # height crown base (m)
        VARIABLE_NAMES.remove('hlcw')  #  hlcw  # height of largest crown width (m)

        # Volume variables
        #VARIABLE_NAMES.remove('vol')  #  volume  # volume with bark (dm3)
        #VARIABLE_NAMES.remove('bole_vol')  #  bole volume  # volume without bark (dm3)
        #VARIABLE_NAMES.remove('bark_vol')  #  bark vol  # volume of bark (dm3)
        VARIABLE_NAMES.remove('firewood_vol')  #  fuelwood volume  # (dm3)
        VARIABLE_NAMES.remove('vol_ha')  #  volume per ha  # volume with bark per hectare (m3/ha)

        # Biomass variables
        #VARIABLE_NAMES.remove('wsw')  #  wsw  # wsw = stem wood (Kg)
        VARIABLE_NAMES.remove('wsb')  #  wsb # wsb = stem bark (Kg)
        #VARIABLE_NAMES.remove('w_cork')  #  w fresh cork  # w_cork = fresh cork biomass (Kg)
        #VARIABLE_NAMES.remove('wthickb')  #  wthickb  # wthickb = Thick branches > 7 cm (Kg)
        VARIABLE_NAMES.remove('wstb')  #  wstb  # wstb = wsw + wthickb, stem + branches >7 cm (Kg)
        #VARIABLE_NAMES.remove('wb2_7')  #  wb2_7  # wb2_7 = branches (2-7 cm) (Kg)
        VARIABLE_NAMES.remove('wb2_t')  #  wb2_t  # wb2_t = wb2_7 + wthickb; branches >2 cm (Kg)
        VARIABLE_NAMES.remove('wthinb')  #  wthinb  # wthinb = Thin branches (2-0.5 cm) (Kg)
        VARIABLE_NAMES.remove('wb05')  # wb05 = thinniest branches (<0.5 cm) (Kg)
        VARIABLE_NAMES.remove('wl')  #  wl  # wl = leaves (Kg)
        #VARIABLE_NAMES.remove('wtbl')  #  wtbl  # wtbl = wthinb + wl; branches <2 cm and leaves (Kg)
        VARIABLE_NAMES.remove('wbl0_7')  #  wbl0_7  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Kg)
        #VARIABLE_NAMES.remove('wr')  #  wr  # wr = roots (Kg)
        #VARIABLE_NAMES.remove('wt')  #  wt  # wt = biomasa total (Kg)

        # Wood uses variables
        VARIABLE_NAMES.remove('unwinding')  #  unwinding  # unwinding = useful volume for unwinding destiny (dm3)
        VARIABLE_NAMES.remove('veneer')  #  veneer  # veneer = useful volume for veneer destiny (dm3)
        VARIABLE_NAMES.remove('saw_big')  #  saw big  # saw_big = useful volume for big saw destiny (dm3)
        VARIABLE_NAMES.remove('saw_small')  #  saw small  # saw_small = useful volume for small saw destiny (dm3)
        VARIABLE_NAMES.remove('saw_canter')  #  saw canter  # saw_canter = useful volume for canter saw destiny (dm3)
        VARIABLE_NAMES.remove('post')  #  post  # post = useful volume for post destiny (dm3)
        VARIABLE_NAMES.remove('stake')  #  stake  # stake = useful volume for stake destiny (dm3)
        VARIABLE_NAMES.remove('chips')  #  chips  # chips = useful volume for chips destiny (dm3)
        
        # Quercus suber special variables
        #VARIABLE_NAMES.remove('dbh_oc')  #  dbh over cork  # dbh over cork (cm) - Quercus suber
        #VARIABLE_NAMES.remove('h_uncork')  #  uncork height  # uncork height on main stem (m) - Quercus suber
        #VARIABLE_NAMES.remove('nb')  #  uncork boughs  # number of main bough stripped - Quercus suber
        #VARIABLE_NAMES.remove('cork_cycle')  #  cork cycle  # moment to obtain cork data; 0 to the moment just immediately before the stripping process,
    # or 1 to the moment after the stripping process or at an intermediate age of the cork cycle production - Quercus suber

QuercusSuberCataluña.vars()