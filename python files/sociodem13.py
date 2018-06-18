# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 17:30:29 2018

@author: Albert
"""

import pandas as pd
import numpy as np
import os


pd.options.display.float_format = '{:,.2f}'.format
os.chdir('D:/Documents/Documents/IDEA/Research/Data/UGANDA/data13')

# =============================================================================
#  Merging Sociodemographic characteristics
# =============================================================================

#Age
age = pd.read_csv('gsec2.csv')
age = age[["PID","h2q3","h2q4","h2q8"]]
age.columns = ["pid","sex","hh_member", "age"]


## Health
health = pd.read_csv('gsec5.csv')
health = health[["PID","h5q5"]]
health.columns = [["pid","illdays"]]


#Background and bednets
bck = pd.read_csv('gsec3.csv')
bck = bck[["PID","h3q3","h3q4", "h3q9","h3q10"]]
bck.columns = ["pid","father_educ", "father_ocup","ethnic","bednet"]
bck.father_educ = bck.father_educ.replace(99,np.nan)
#Group bednet answer as yes I have, no 
bck.bednet = bck.bednet.replace([2 , 3, 9],[1 , 0, np.nan])


#Education
educ = pd.read_stata('GSEC4.dta', convert_categoricals=False)
educ = educ[["HHID","PID","h4q4", "h4q7"]]
educ.columns = ["hh","pid","writeread","classeduc"]
educ.loc[educ["classeduc"]==99, "classeduc"] = np.nan
educ.writeread = educ.writeread.replace([2, 4, 5],0)
#1 if able to read and write. 0 if unable both, unable writing, uses braille


#Sociodemographic dataset
socio = pd.merge(age, bck, on="pid", how="outer")
socio = pd.merge(socio, educ, on="pid", how="outer")
socio = pd.merge(socio, health, on="pid", how="outer")
socio = socio.loc[(socio.hh_member==1)]
socio.drop(["hh_member", "pid"], axis=1, inplace=True)
#socio.drop(socio.columns[0], axis=1, inplace=True)


socio.to_csv("sociodem13.csv")