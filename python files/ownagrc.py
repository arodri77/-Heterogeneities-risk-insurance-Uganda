# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 11:59:02 2018

@author: Albert
"""


###  UGA_C2: food consumption during the last 7 days


import pandas as pd
import numpy as np
import os

#%%IMPORT DATA
os.chdir('D:/Documents/Documents/IDEA/Research/Data/UGANDA/UGA_2013_UNPS_v01_M_CSV')
c2 = pd.read_csv('gsec15b.csv', header=0, na_values='NA')
c2.columns = ["hh","code","food_group","cons_7d","cons_days","unit","purch_home_quant","purch_home_value","purch_away_quant","purch_away_value","own_quant","own_value","gift_quant","gift_value","total_quant","total_value", "m_p", "gate_p","wgt_X"]
c2 = c2[["hh","code","own_quant","own_value"]]

crops = np.concatenate((range(101,117), range(130,151)))
animal = range(117,126)


crops_c = c2[c2['code'].isin(crops)]
animal_c = c2[c2['code'].isin(animal)]

crops_c = crops_c.groupby(by="hh")[["own_quant","own_value"]].sum()
crops_c[["own_quant","own_value"]] = crops_c[["own_quant","own_value"]]*52
sumcrop = crops_c.describe()/2500

animal_c = animal_c.groupby(by="hh")[["own_quant","own_value"]].sum()
animal_c[["own_quant","own_value"]] = animal_c[["own_quant","own_value"]]*52
sumcan = animal_c.describe()/2500


crops_c.to_csv("crops_c.csv")
animal_c.to_csv("animal_c.csv")



#%%IMPORT DATA
os.chdir('D:/Documents/Documents/IDEA/Research/Data/UGANDA/UGA_2011_UNPS_v01_M_Stata8')
c2 = pd.read_stata('GSEC15B.dta', convert_categoricals=False)
c2 = c2[["HHID","itmcd","h15bq9"]]
c2.columns = ["hh","code","own_value"]

crops = np.concatenate((range(101,117), range(130,151)))
animal = range(117,126)


crops_c = c2[c2['code'].isin(crops)]
animal_c = c2[c2['code'].isin(animal)]

crops_c = crops_c.groupby(by="hh")[["own_value"]].sum()
crops_c[["own_value"]] = crops_c[["own_value"]]*52
sumcrop = crops_c.describe()/2500

animal_c = animal_c.groupby(by="hh")[["own_value"]].sum()
animal_c[["own_value"]] = animal_c[["own_value"]]*52
sumcan = animal_c.describe()/2500


crops_c.to_csv("crops_c11.csv")
animal_c.to_csv("animal_c11.csv")