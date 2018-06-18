# -*- coding: utf-8 -*-
"""
Created on Wed May 23 15:20:42 2018

@author: Albert
"""

# =============================================================================
# Consumption aggregation 2013
# =============================================================================


import pandas as pd
import numpy as np
import os
dollars = 2586.89

os.chdir('D:/Documents/Documents/IDEA/Research/Data/UGANDA/data13')

#%% FOOD CONSUMPTION

c2 = pd.read_csv('gsec15b.csv', header=0, na_values='NA')
c2.columns = ["hh","code","food_group","cons_7d","cons_days","unit","purch_home_quant","purch_home_value","purch_away_quant","purch_away_value","own_quant","own_value","gift_quant","gift_value","total_quant","total_value", "m_p", "gate_p","wgt_X"]
pricescons = c2.groupby(by="code")[["m_p", "gate_p"]].median()
pricescons.to_csv("pricesfood13.csv")


livestock = c2.loc[c2["code"].isin([117,118,119,120,121,122,123,124,125]),["hh","own_value"]]
livestock = livestock.groupby(by="hh").sum()*52

livestock.to_csv("c_animal13.csv")
suml = livestock.describe()/dollars

#Aggregate across items
c2 = c2.groupby(by="hh")[["purch_home_quant","purch_home_value","purch_away_quant","purch_away_value","own_quant","own_value","gift_quant","gift_value","total_quant","total_value"]].sum()
c2 = c2[["purch_home_value", "purch_away_value", "own_value","gift_value","total_value"]]
c2.rename(columns={'total_value':'cfood'}, inplace=True)
c2.rename(columns={'gift_value':'cfood_gift'}, inplace=True)
c2.rename(columns={'own_value':'cfood_own'}, inplace=True)

c2["cfood_purch"] = c2.loc[:,["purch_home_value","purch_away_value"]].sum(axis=1)
c2["cfood_nogift"] = c2.loc[:,["cfood_purch","own_value"]].sum(axis=1)

# Food consumption at year level
c2 = c2[["cfood", "cfood_nogift", "cfood_own", "cfood_purch", "cfood_gift"]]*52
# Cfood is total value. cfood_nogift is total value minus gifts.
c2.reset_index(inplace=True)

data = c2



#%% NONFOOD NONDURABLE CONSUMPTION

c3 = pd.read_csv('gsec15c.csv', header=0, na_values='NA')
c3.columns = ["hh","code","cons_30d","unit","purch_quant","purch_value","own_quant","own_value","gift_quant","gift_value", "m_p", "wgt_X"]



#Aggregate across items
c3 = c3.groupby(by="hh")[["purch_quant","purch_value","own_quant","own_value","gift_quant","gift_value"]].sum()

c3['cnodur'] = c3.fillna(0)["purch_value"] + c3.fillna(0)["own_value"] + c3.fillna(0)["gift_value"]
c3["cnodur_nogift"] = c3.loc[:,["purch_value","own_value"]].sum(axis=1)
c3.rename(columns={'gift_value':'cnodur_gift'}, inplace=True)
c3.rename(columns={'own_value':'cnodur_own'}, inplace=True)
c3.rename(columns={'purch_value':'cnodur_purch'}, inplace=True)

# non food non durable consumption at year level
c3 = c3[["cnodur", "cnodur_nogift", "cnodur_own", "cnodur_purch", "cnodur_gift"]]*12
c3.reset_index(inplace=True)

data = data.merge(c3, on="hh", how="outer")


#%% DURABLE CONSUMPTION
c4 = pd.read_csv('gsec15d.csv', header=0, na_values='NA')
c4.columns = ["hh","code","cons_y","purch_value","own_value","gift_value", "wgt_X"]

c4 = c4.groupby(by="hh")[["purch_value","own_value","gift_value"]].sum()

c4['cdur'] = c4.fillna(0)["purch_value"] + c4.fillna(0)["own_value"] + c4.fillna(0)["gift_value"]
c4["cdur_nogift"] = c4.loc[:,["purch_value","own_value"]].sum(axis=1)
c4.rename(columns={'gift_value':'cdur_gift'}, inplace=True)
c4.rename(columns={'own_value':'cdur_own'}, inplace=True)
c4.rename(columns={'purch_value':'cdur_purch'}, inplace=True)

#  durable consumption at year level
c4 = c4[["cdur", "cdur_nogift", "cdur_own", "cdur_purch", "cdur_gift"]]
c4.reset_index(inplace=True)

data = data.merge(c4, on="hh", how="outer")



#%% Create join variables
data["ctotal"] = data.loc[:,["cfood","cnodur"]].sum(axis=1)
data["ctotal_dur"] = data.loc[:,["cfood","cnodur","cdur"]].sum(axis=1)

data["ctotal_gift"] = data.loc[:,["cfood_gift","cnodur_gift"]].sum(axis=1)
data["ctotal_dur_gift"] = data.loc[:,["ctotal_gift","cdur_gift"]].sum(axis=1)

data["ctotal_nogift"] = data.loc[:,["cfood_nogift","cnodur_nogift"]].sum(axis=1)
data["ctotal_dur_nogift"] = data.loc[:,["cfood_nogift","cnodur_nogift"]].sum(axis=1)

data["ctotal_own"] = data.loc[:,["cfood_own","cnodur_own"]].sum(axis=1)
data["ctotal_dur_own"] = data.loc[:,["ctotal_own","cdur_own"]].sum(axis=1)


cdata_short = data[["hh","ctotal","ctotal_dur","ctotal_gift","ctotal_dur_gift","ctotal_nogift","ctotal_dur_nogift","ctotal_own","ctotal_dur_own","cfood","cnodur","cdur"]]
sumc = cdata_short.describe()/dollars
cdata_short.to_csv("cons13.csv", index=False)





