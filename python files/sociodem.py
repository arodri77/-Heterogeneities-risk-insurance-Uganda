# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 16:05:08 2018

@author: Albert
"""

import pandas as pd
import numpy as np
import os


os.chdir('D:/Documents/Documents/IDEA/Research/Data/UGANDA/data13')
pd.options.display.float_format = '{:,.2f}'.format

#%% Import 2013 Data
cwi13 = pd.read_csv('uga_cwi.csv')
socio13 = pd.read_csv("sociodem13.csv")