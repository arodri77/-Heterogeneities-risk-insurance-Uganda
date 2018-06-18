# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 12:44:33 2018

@author: Albert
"""

import pandas as pd
import numpy as np
import os


os.chdir('D:/Documents/Documents/IDEA/Research/Data/UGANDA/data13')
pd.options.display.float_format = '{:,.2f}'.format

dollars = 2586.89

#%%Income 

lab9 = pd.read_stata("GSEC8_1.dta")
#lab9 = lab9[["HHID","PID","h8q30a","h8q30b", "h8q31a","h8q31b","h8q31c","h8q44","h8q44b","h8q45a","h8q45b","h8q45c", "h8q47"]]     
lab9 = lab9[["HHID","PID","h8q52","h8q52_1","h8q52_2","h8q53a","h8q53b","h8q53c","h8q57","h8q57_1","h8q57_2","h8q58a","h8q58b","h8q58c"]]

lab9.columns = [["hh","pid","months1","weeks1","hours1", "cash1","inkind1", "time1", "months2","weeks2","hours2", "cash2","inkind2", "time2"]]




pd.value_counts(lab9.time1).reset_index()
pd.value_counts(lab9.time2).reset_index()

#Compute means to use in 2011-2012
avg_months = lab9.months1.mean()
avg_weeks = lab9.weeks1.mean()

lab9["pay1"] = lab9.loc[:,["cash1","inkind1"]].sum(axis=1)
lab9["pay2"] = lab9.loc[:,["cash2","inkind2"]].sum(axis=1)
del lab9["cash1"], lab9["inkind1"], lab9["cash2"], lab9["inkind2"]


#Creating week wages
#I assume that on average people work 5 days (they don't ask how many days)


lab9.loc[lab9.time1 == "Month", 'pay1'] = lab9.loc[lab9.time1 == "Month", 'pay1']*lab9.loc[lab9.time1 == "Month", 'months1']
lab9.loc[lab9.time1 == "Week", 'pay1'] = lab9.loc[lab9.time1 == "Hour", 'pay1']*lab9.loc[lab9.time1 == "Month", 'months1']*lab9.loc[lab9.time1 == "Month", 'weeks1']
lab9.loc[lab9.time1 == "Day", 'pay1'] = lab9.loc[lab9.time1 == "Hour", 'pay1']*lab9.loc[lab9.time1 == "Month", 'months1']*lab9.loc[lab9.time1 == "Month", 'weeks1']*5

lab9.loc[lab9.time2 == "Month", 'pay2'] = lab9.loc[lab9.time2 == "Month", 'pay2']*lab9.loc[lab9.time2 == "Month", 'months2']
lab9.loc[lab9.time2 == "Week", 'pay2'] = lab9.loc[lab9.time2 == "Hour", 'pay2']*lab9.loc[lab9.time2 == "Month", 'months2']*lab9.loc[lab9.time2 == "Month", 'weeks1']
lab9.loc[lab9.time2 == "Day", 'pay2'] = lab9.loc[lab9.time2 == "Hour", 'pay2']*lab9.loc[lab9.time2 == "Month", 'months2']*lab9.loc[lab9.time2 == "Month", 'weeks1']*5






lab99 = lab9.groupby(by="hh")[["pay1","pay2"]].sum()
lab99.columns = ["wage1","wage2"]
lab99["wage_total"] = lab99.loc[:,["wage1","wage2"]].sum(axis=1)
lab99 = lab99.replace(0, np.nan)

lab99 = lab99/dollars
lab99["hh"] = np.array(lab99.index.values)
summaryw = lab99.describe()
print(summaryw.to_latex())

del lab9

#%% business

bus12 = pd.read_stata('gsec12.dta')
bus12 = bus12[["hhid","h12q12", "h12q13","h12q15","h12q16","h12q17"]]
bus12.rename(columns={'hhid':'hh'}, inplace=True)
bus12.rename(columns={'h12q13':'revenue'}, inplace=True)
bus12["cost"] = -bus12.loc[:,["h12q15","h12q16","h12q17"]].sum(axis=1)
bus12["bs_profit"] = bus12.loc[:,["revenue","cost"]].sum(axis=1)
bus12["bs_profit"] = bus12["bs_profit"].replace(0,np.nan)
bus12 = bus12[["hh","bs_profit"]]
bus12 = bus12.groupby(by="hh").sum()
bus12 = bus12/dollars
bus12["hh"] = np.array(bus12.index.values)

summarybus = bus12.describe()

print(summarybus.to_latex())

#%% Other income

other = pd.read_stata('GSEC11A.dta')
other = other[["HHID","h11q5","h11q6"]]
other.rename(columns={'HHID':'hh'}, inplace=True)
other["other_inc"] = other.loc[:,["h11q5","h11q6"]].sum(axis=1)
other = other[["hh","other_inc"]]
other = other.groupby(by="hh").sum()
other = other/dollars
other["hh"] = np.array(other.index.values)
summaryo = other.describe()
print(summaryo.to_latex())


# extra-expenditures ---------------------------------------
c5 = pd.read_csv('gsec15e.csv', header=0, na_values='NA')
c5.columns = ["id","code","purchase_d","value","wgt_X"]
c5 = c5.groupby(by="id")[["value"]].sum()
c5 = -c5/dollars
c5["hh"] = np.array(c5.index.values)


# Merge ----------------------------
extra = pd.merge(other, c5, on="hh", how="outer")

extra["other_net"] = extra["other_inc"].fillna(0) +extra["value"].fillna(0)
extra= extra[["hh","other_net"]]
extra["other_net"] = extra["other_net"].replace(0,np.nan)
summaryo = extra.describe()


print(summaryo.to_latex())


#%% Merge datasets
income_gsec = pd.merge(lab99, bus12, on="hh", how="outer")
income_gsec = pd.merge(income_gsec, extra, on="hh", how="outer")
del income_gsec["wage1"], income_gsec["wage2"], bus12, c5, extra,  dollars, other, lab99, summarybus, summaryo, summaryw

income_gsec.to_csv('income_hhsec.csv')