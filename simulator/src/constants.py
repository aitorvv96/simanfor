#!/usr/bin/env python
#
# Copyright (c) $today.year Spiros Michalakopoulos (Sngular). All Rights Reserved.
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

OUTPUT_FILE_BASE = 'Output_Plot_'
OUTPUT_EXTENSION = ['xlsx', 'json']

OUTPUT_NAMES = [
    'Id',
    'Age',
    'Min age',
    'Max age',
    'Action',
    'Years',
    'Harvest by',
    'Value',
    'By means of'
]

PLOT_VARIABLE_NAMES = [

    # IDs
    'INVENTORY_ID',
    'PLOT_ID',

    # Plot general information
    'PLOT_TYPE',
    'PLOT_AREA',
    'PROVINCE',
    'STUDY_AREA',
    'MUNICIPALITY',
    'FOREST',
    'MAIN_SPECIE',
    'SPECIE_IFN_ID',
    'SLOPE',  # Slope  # (%)
    'ASPECT',  # Aspect  # (rad)
    'CONTINENTALITY',  # Continentality  # (linear distance to the Mediterranean sea, Km)
    'LONGITUDE',
    'LATITUDE',
    'ALTITUDE',

    # Basic plot variables measured
    "EXPAN",  # Expan  # expansion factor
    "AGE",  # Age  # (years)
    "DENSITY",  # Density  # (nº trees/ha)

    # Basic plot variables calculated - basal area
    "BASAL_AREA",  # Basal area  # (m2/ha)
    "BA_MAX",  # BA Max  # (m2)
    "BA_MIN",  # BA Min  # (m2)
    "MEAN_BA",  # Mean BA  # (m2)

    # Basic plot variables calculated - diameter
    "DBH_MAX",  # D Max  # (cm)
    "DBH_MIN",  # D Min  # (cm)
    "MEAN_DBH",  # Mean dbh  # (cm)
    "QM_DBH",  # Quadratic mean dbh  # (m2)
    "DOMINANT_DBH",  # Dominant dbh  # (cm)

    # Basic plot variables calculated - height
    "H_MAX",  # H Max  # (m)
    "H_MIN",  # H Min  # (m)
    "MEAN_H",  # Mean height  # (m)
    "DOMINANT_H",  # Dominant height  # (m)

    # Basic plot variables calculated - crown
    "CROWN_MEAN_D",  # Mean crown diameter  # (m)
    "CROWN_DOM_D",  # Dominant crown diameter  # (m)
    "CANOPY_COVER",  # Canopy cover  # (%)

    # Basic plot variables calculated - plot
    "REINEKE",  # Reineke Index  # Stand Density Index - SDI
    "HART",  # Hart-Becking Index  # Hart-Becking Index - S
    "SI",  # Site index  # (m)
    "QI",  # Quality Index

     # Plot variables calculated - volume and biomass
    "VOL",  # Volume  # (m3)
    "BOLE_VOL",  # Bole Volume  # (m3)
    "BARK_VOL",  # Bark Volumen  # (m3) 

    # Plot variables calculated - biomass
    "WSW",  # Wsw  # wsw = stem wood (Tn)
    "WSB",  # Wsb  # wsb = stem bark (Tn)
    "W_CORK",  # W Fresh Cork  # w_cork = fresh cork biomass (Tn)
    "WTHICKB",  # Wthickb  # wthickb = Thick branches > 7 cm (Tn)
    "WSTB",  # Wstb  # wstb = wsw + wthickb, stem + branches >7 cm (Tn)
    "WB2_7",  # Wb2_7  # wb2_7 = branches (2-7 cm) (Tn)
    "WB2_T",  # Wb2_t  # wb2_t = wb2_7 + wthickb; branches >2 cm (Tn)
    "WTHINB",  # Wthinb  # wthinb = Thin branches (2-0.5 cm) (Tn)
    "WB05",  # Wb0.5  # wb05 = thinniest branches (<0.5 cm) (Kg)
    "WL",  # Wl  # wl = leaves (Tn)
    "WTBL",  # Wtbl  # wtbl = wthinb + wl; branches <2 cm and leaves (Tn)
    "WBL0_7",  # Wbl0_7  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Tn)
    "WR",  # Wr  # wr = roots (Tn)
    "WT",  # Wt  # wt = biomasa total (Tn)

    # Plot variables calculated - wood uses
    "UNWINDING",  # Unwinding  # unwinding = useful volume for unwinding destiny (m3)
    "VENEER",  # Veneer  # veneer = useful volume for veneer destiny (m3)
    "SAW_BIG",  # Saw big  # saw_big = useful volume for big saw destiny (m3)
    "SAW_SMALL",  # Saw small  # saw_small = useful volume for small saw destiny (m3)
    "SAW_CANTER",  # Saw canter  # saw_canter = useful volume for canter saw destiny (m3)
    "POST",  # Post  # post = useful volume for post destiny (m3)
    "STAKE",  # Stake  # stake = useful volume for stake destiny (m3)
    "CHIPS"  # Chips  # chips = useful volume for chips destiny (m3)
    
]

CUTTYPES_LIST = [
    ('PERCENTOFTREES', 'PercentOfTrees'), 
    ('VOLUME', 'Volume'), 
    ('AREA', 'Area')
]

CUTTYPES_DICT = {
    'PERCENTOFTREES': 'Percent of trees',
    'VOLUME': 'Volumen',
    'AREA': 'Area'
}

# TRIM_TYPE_ENUM = enumerate(['ByTallest', 'BySmallest', 'Systematic'])
