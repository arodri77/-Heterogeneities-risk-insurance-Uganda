# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 11:18:55 2018

@author: Albert
"""

##### Panel data

import pandas as pd
import numpy as np
import os
import statsmodels.formula.api as sm
from statsmodels.iolib.summary2 import summary_col
pd.options.display.float_format = '{:,.2f}'.format

os.chdir('D:/Documents/Documents/IDEA/Master tesi/Data & Code (Uganda)')

#Import 2009
data09 = pd.read_csv('D:/Documents/Documents/IDEA/Master tesi/Data & Code (Uganda)/data09/data09.csv')
#Import 2010
data10 = pd.read_csv('D:/Documents/Documents/IDEA/Master tesi/Data & Code (Uganda)/data10/data10.csv')
#Import 2011
data11 = pd.read_csv('D:/Documents/Documents/IDEA/Master tesi/Data & Code (Uganda)/data11/data11.csv')
#Import 2013
data13 = pd.read_csv('D:/Documents/Documents/IDEA/Master tesi/Data & Code (Uganda)/data13/data13.csv')


# Create panel
panel = data09.append(data10)
panel = panel.append(data11)
panel = panel.append(data13)


# Create region, wave averages
regionmeans = panel.groupby(by=["wave","region"])[["lnc"]].mean()
regionmeans.reset_index(inplace=True)
regionmeans.rename(columns={"lnc":"avgc"}, inplace=True)
regionmeans.loc[regionmeans["avgc"]==-np.inf, "avgc"] = np.nan
regionmeans["avgc"].fillna(np.mean(regionmeans["avgc"]), inplace=True)
panel = panel.merge(regionmeans, on=["wave","region"], how="outer")



## Create balanced panel: Only those observed across 4 waves
counthh = panel.groupby(by="hh")[["hh"]].count()
counthh.columns = ["counthh"]
counthh.reset_index(inplace=True)
panel = panel.merge(counthh, on="hh", how="left")
#panel.dropna(inplace=True)
panel.to_stata("dataUGA.dta", write_index=False)

panel = pd.read_stata("dataUGA.dta")

## Generate temporary shocks
olsc = sm.ols(formula="lnc ~ age +age_sq +region2 +region3 +region4 +urban +female +worker +businessman  +bednet +illdays +classeduc ", data=panel).fit()
print(olsc.summary())

olsi = sm.ols(formula="lny ~ age +age_sq +region2 +region3 +region4 +urban +female +worker +businessman  +bednet +illdays +classeduc ", data=panel).fit()
print(olsi.summary())

panel["u_c"] = olsc.resid
panel["u_y"] = olsi.resid
panel["lnc_nogift"] = np.log(panel["ctotal"] - panel["ctotal_gift"].fillna(0))

panel.to_stata("dataUGA.dta", write_index=False)


# Panel
panel.sort_values(["hh","wave"])
panel.set_index(["hh","wave"],inplace=True)
paneldiff = panel.groupby(level=0)['d_shock','d_aggregate','d_idiosyn','d_climate','d_prices','d_health','d_job','d_pests','lnc','lny','avgc','lnctotal_gift', "lnc_nogift"].diff()
paneldiff.columns = ["Δshock","Δaggregate","Δidiosyn","Δclimate","Δprices","Δhealth","Δjob","Δpests",'Δc','Δy','Δavgc', 'Δc_gift', 'Δc_nogift']
paneldiff.reset_index(inplace=True)
paneldiff = paneldiff[paneldiff.wave != "2009-2010"]


data = paneldiff

#%% Consumption heterogeneities

# =============================================================================
# Do Shocks correlate with consumption?
# =============================================================================

ols3 = sm.ols(formula=" Δc ~ Δshock", data=data).fit()
ols3.summary()

#Does it depending on the type of shock?
ols31 = sm.ols(formula=" Δc ~ Δaggregate", data=data).fit()
ols31.summary()

ols32 = sm.ols(formula=" Δc ~ Δidiosyn", data=data).fit()
ols32.summary()

ols33 = sm.ols(formula=" Δc ~ Δclimate", data=data).fit()
ols33.summary()

ols34 = sm.ols(formula=" Δc ~ Δprices", data=data).fit()
ols34.summary()

ols35 = sm.ols(formula=" Δc ~ Δhealth", data=data).fit()
ols35.summary()

ols36 = sm.ols(formula=" Δc ~ Δjob", data=data).fit()
ols36.summary()

ols37 = sm.ols(formula=" Δc ~ Δpests", data=data).fit()
ols37.summary()

results = summary_col([ols3, ols31, ols32, ols33, ols34, ols35, ols36, ols37],stars=True)
print(results)


# =============================================================================
# Shocks and consumption through gifts??
# =============================================================================
data = paneldiff
ols5 = sm.ols(formula=" Δc_gift ~ Δshock", data=data).fit()
ols5.summary()
#Experiencing a shock negatively correlates with Consumption

#Does it depending on the type of shock?
ols51 = sm.ols(formula=" Δc_gift ~ Δaggregate", data=data).fit()
ols51.summary()

ols52 = sm.ols(formula=" Δc_gift ~ Δidiosyn", data=data).fit()
ols52.summary()

ols53 = sm.ols(formula=" Δc_gift ~ Δclimate", data=data).fit()
ols53.summary()

ols54 = sm.ols(formula=" Δc_gift ~ Δprices", data=data).fit()
ols54.summary()

ols55 = sm.ols(formula=" Δc_gift ~ Δhealth", data=data).fit()
ols55.summary()

ols56 = sm.ols(formula=" Δc_gift ~ Δjob", data=data).fit()
ols56.summary()

ols57 = sm.ols(formula=" Δc_gift ~ Δpests", data=data).fit()
ols57.summary()

results = summary_col([ols5, ols51, ols52, ols53, ols54, ols55, ols56, ols57],stars=True)
print(results)



#%% Income correlation
# =============================================================================
# Do Shocks correlate with income?
# =============================================================================

ols4 = sm.ols(formula="Δy ~ Δshock", data=data).fit()
ols4.summary()

ols41 = sm.ols(formula=" Δy ~ Δaggregate", data=data).fit()
ols41.summary()

ols42 = sm.ols(formula=" Δy ~ Δidiosyn", data=data).fit()
ols42.summary()

ols43 = sm.ols(formula=" Δy ~ Δclimate", data=data).fit()
ols43.summary()

ols44 = sm.ols(formula=" Δy ~ Δprices", data=data).fit()
ols44.summary()

ols45 = sm.ols(formula=" Δy ~ Δhealth", data=data).fit()
ols45.summary()

ols46 = sm.ols(formula=" Δy ~ Δjob", data=data).fit()
ols46.summary()

ols47 = sm.ols(formula=" Δy ~ Δpests", data=data).fit()
ols47.summary()

results = summary_col([ols4, ols41, ols42, ols43, ols44, ols45, ols46, ols47],stars=True)
print(results)



# =============================================================================
#%% Townsend Test
# =============================================================================
test1 = sm.ols("Δc ~ Δavgc + Δy ", data=data).fit()
print(test1.summary())


test2 = sm.ols("Δc ~ Δavgc + Δy+Δy*Δshock +Δshock ", data=data).fit()
print(test2.summary())


test3 = sm.ols("Δc ~ Δavgc + Δy +Δy*Δaggregate +Δaggregate", data=data).fit()
print(test3.summary())

test4 = sm.ols("Δc ~ Δavgc + Δy +Δy*Δidiosyn +Δidiosyn ", data=data).fit()
print(test4.summary())

test5 = sm.ols("Δc ~ Δavgc + Δy +Δy*Δclimate +Δclimate ", data=data).fit()
print(test5.summary())

test6 = sm.ols("Δc ~ Δavgc + Δy +Δy*Δprices +Δprices ", data=data).fit()
print(test6.summary())

test7 = sm.ols("Δc ~ Δavgc + Δy +Δy*Δhealth +Δhealth ", data=data).fit()
print(test7.summary())

test8 = sm.ols("Δc ~ Δavgc + Δy +Δy*Δjob +Δjob ", data=data).fit()
print(test8.summary())

test9 = sm.ols("Δc ~ Δavgc+ Δy +Δy*Δpests +Δpests ", data=data).fit()
print(test9.summary())

results = summary_col([ test2, test3, test4, test5, test6, test7, test8, test9], stars=True)
print(results)


