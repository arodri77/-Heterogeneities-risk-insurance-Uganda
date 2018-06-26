# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 16:34:53 2018

@author: Albert
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 09:31:22 2018

@author: Albert
"""

# =============================================================================
# Heterogeneities Townsend: Balanced Panel Data Urban Households
# =============================================================================


import pandas as pd
import numpy as np
import os
import statsmodels.formula.api as sm
from statsmodels.iolib.summary2 import summary_col

pd.options.display.float_format = '{:,.2f}'.format

os.chdir('D:/Documents/Documents/IDEA/Master tesi/Data & Code (Uganda)')


panel = pd.read_stata("dataUGA.dta")


#Balanced panel
panelbal = panel.loc[panel["counthh"]==4,]
panelbal = panelbal.loc[panelbal["urban"]==1,]

counthh = panelbal.groupby(by="hh")[["hh"]].count()

control = panelbal.groupby(by="hh")[["lnc","lny",]].mean()
control.reset_index(inplace=True)
control['crich'] = pd.qcut(control["lnc"], 2, labels=False)
control['c_quin'] = pd.qcut(control["lnc"], 5, labels=False)
control['yrich'] = pd.qcut(control["lny"], 2, labels=False)
control['y_quin'] = pd.qcut(control["lny"], 5, labels=False)


#Create HH characteristics controls
dummies = pd.get_dummies(control["c_quin"])
dummies.drop([0.0], axis=1, inplace=True)
dummies.columns = [["c2","c3","c4","c5"]]

control = control.join(dummies)

dummiesy = pd.get_dummies(control["y_quin"])
dummiesy.drop([0.0], axis=1, inplace=True)
dummiesy.columns = [["y2","y3","y4","y5"]]
control = control.join(dummiesy)


control13 = panelbal.loc[panelbal.wave=="2013-2014",["hh","sex","region"]]
control13["female"] = (control13.sex==2)*1
control = control.merge(control13, on="hh",how="inner")

dummiesr = pd.get_dummies(control["region"])
dummiesr.drop([1.0], axis=1, inplace=True)
dummiesr.columns = [["region2","region3","region4"]]
control = control.join(dummiesr)
control.drop(["lny","lnc","sex"],axis=1, inplace=True)


panelbal.drop(["female","region","region2","region3","region4"],axis=1, inplace=True)
panelbal.sort_values(["hh","wave"])
panelbal.set_index(["hh","wave"],inplace=True)

panelbaldiff = panelbal.groupby(level=0)['d_shock','d_aggregate','d_idiosyn','d_climate','d_prices','d_health','d_job','d_pests','lnc','lny','avgc','lnctotal_gift', "lnc_nogift"].diff()
panelbaldiff.columns = ["Δshock","Δaggregate","Δidiosyn","Δclimate","Δprices","Δhealth","Δjob","Δpests",'Δc','Δy','Δavgc','Δc_gift', 'Δc_nogift']
panelbaldiff.reset_index(inplace=True)
panelbaldiff = panelbaldiff[panelbaldiff.wave != "2009-2010"]



### Balanced panel with hh controls
panelbal.reset_index(inplace=True)
panelcontrol = panelbal.merge(control, on="hh", how='left')
panelcontrol.set_index(["hh","wave"],inplace=True)

panelcontroldiff = panelbaldiff.merge(control, on="hh", how='left')
panelcontroldiff.set_index(["hh","wave"],inplace=True)


#panelcontroldiff.to_stata("panelbalcontrol.dta")

## Cochrane set-up
panelbal.sort_values(["hh","wave"])
panelbal.set_index(["hh","wave"],inplace=True)

cochranediff = panelbal.groupby(level=0)['lnc','lny','lnctotal_gift', "lnc_nogift", 'avgc'].diff(periods=3,axis=0)
cochranediff.columns = ['Δc','Δy','Δc_gift', 'Δc_nogift', 'Δavgc']
cochranediff.reset_index(inplace=True)
cochranediff = cochranediff[cochranediff.wave== "2013-2014"]

cochraneshocks = panelbal.groupby(by="hh")['shock','_aggregate','idiosyn','climate','prices','health','job','pests'].sum()
cochraneshocks.columns = ["Δshock","Δaggregate","Δidiosyn","Δclimate","Δprices","Δhealth","Δjob","Δpests"]
cochraneshocks.reset_index(inplace=True)

cochrane = pd.merge(cochranediff, cochraneshocks, on="hh", how="left")
#%% Proportion of Shocks household report
data = panelcontrol
sumshocks = data[["d_shock","d_aggregate","d_idiosyn","d_climate","d_prices","d_job","d_health","d_pests"]].mean()*100


#Proportion of shocks by Region
sumshocks_reg = data.groupby(by="region")[["d_shock","d_aggregate","d_idiosyn","d_climate","d_prices","d_job","d_health","d_pests"]].mean()*100
nreg = data.groupby(by="region")[["d_shock"]].count()
print(sumshocks_reg.to_latex())

#Proportion of shocks by Sex
sumshocks_sex = data.groupby(by="female")[["d_shock","d_aggregate","d_idiosyn","d_climate","d_prices","d_job","d_health","d_pests"]].mean()*100
nsex = data.groupby(by="female")[["d_shock"]].count()
print(sumshocks_sex.to_latex())

#Proportion of shocks by Quintiles
sumshocks_quin = data.groupby(by="c_quin")[["d_shock","d_aggregate","d_idiosyn","d_climate","d_prices","d_job","d_health","d_pests"]].mean()*100
nquin = data.groupby(by="c_quin")[["d_shock"]].count()
print(sumshocks_quin.to_latex())




#Proportion of shocks by 50%rich
sumshocks_rich = data.groupby(by="crich")[["d_shock","d_aggregate","d_idiosyn","d_climate","d_prices","d_job","d_health","d_pests"]].mean()*100
nrich = data.groupby(by="crich")[["d_shock"]].count()
print(sumshocks_rich.to_latex())


#Proportion of shocks by Ocupation
sumshocks_ocupation = data.groupby(by="ocupation")[["d_shock","d_aggregate","d_idiosyn","d_climate","d_prices","d_job","d_health","d_pests"]].mean()*100
nocup = data.groupby(by="ocupation")[["d_shock"]].count()
print(sumshocks_ocupation.to_latex())


#Proportion of shocks by Wave
sumshocks_wave = data.groupby(by="wave")[["d_shock","d_aggregate","d_idiosyn","d_climate","d_prices","d_job","d_health","d_pests"]].mean()*100
nwave = data.groupby(by="wave")[["d_shock"]].count()
print(sumshocks_wave.to_latex())

#%% Consumption heterogeneities


# =============================================================================
# Do Shocks correlate with consumption?
# =============================================================================

data=cochrane
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
print(results.as_latex())

ols3.bse
store_c = pd.DataFrame(np.array([ols3.params, ols3.bse, ols31.params,ols31.bse, ols32.params, ols32.bse, ols33.params, ols33.bse, ols34.params, ols34.bse, ols35.params, ols35.bse, ols36.params, ols36.bse, ols37.params, ols37.bse]))
print(store_c.to_latex())
# =============================================================================
# Shocks and consumption through gifts??
# =============================================================================

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

resultsgift = summary_col([ols5, ols51, ols52, ols53, ols54, ols55, ols56, ols57],stars=True)
print(resultsgift)

store_gift = pd.DataFrame(np.array([ols5.params, ols5.bse, ols51.params,ols51.bse, ols52.params, ols52.bse, ols53.params, ols53.bse, ols54.params, ols54.bse, ols55.params, ols55.bse, ols56.params, ols56.bse, ols57.params, ols57.bse]))


#%% Income correlation
# =============================================================================
# Do Shocks correlate with income?
# =============================================================================
data = cochrane

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

store_inc = pd.DataFrame(np.array([ols4.params, ols4.bse, ols41.params,ols41.bse, ols42.params, ols42.bse, ols43.params, ols43.bse, ols44.params, ols44.bse, ols45.params, ols45.bse, ols46.params, ols46.bse, ols47.params, ols47.bse]))


pd.options.display.float_format = '{:,.4f}'.format
shockscorr = pd.concat([store_c, store_gift, store_inc], axis=1)
print(shockscorr.to_latex())

pd.options.display.float_format = '{:,.2f}'.format
# =============================================================================
#%% Townsend Test
# =============================================================================
data = panelcontroldiff

test1 = sm.ols("Δc ~ Δavgc + Δy ", data=data).fit()
print(test1.summary())


test2 = sm.ols("Δc ~ Δavgc +Δy*female +female ", data=data).fit()
print(test2.summary())



test4 = sm.ols("Δc ~ Δavgc +Δy*crich +crich ", data=data).fit()
print(test4.summary())

test5 = sm.ols("Δc ~ Δavgc +Δy*c2 +c2 +Δy*c3 +c3 +Δy*c4 +c4 +Δy*c5 +c5 ", data=data).fit()
print(test5.summary())

#Ftest sum of coefficients: Insurance per quintiles
ftestc2 = test5.f_test("Δy+Δy:c2 = 0")
ftestc3 = test5.f_test("Δy+Δy:c3 = 0")
ftestc4 = test5.f_test("Δy+Δy:c4 = 0")
ftestc5 = test5.f_test("Δy+Δy:c5 = 0")
print(ftestc2, ftestc3, ftestc4, ftestc5)


test8 = sm.ols("Δc ~ Δavgc +Δy*c2 +c2 +Δy*c3 +c3 +Δy*c4 +c4 +Δy*c5 +c5 +region2 +region3 +region4 +Δy*region2 +Δy*region3 +Δy*region4 ", data=data).fit()
print(test5.summary())
test6 = sm.ols("Δc ~ Δavgc +Δy*female +female  +Δy*c2 +c2 +Δy*c3 +c3 +Δy*c4 +c4 +Δy*c5 +c5 +region2 +region3 +region4 +Δy*region2 +Δy*region3 +Δy*region4 ", data=data).fit()
print(test6.summary())

test7 = sm.ols("Δc ~ Δavgc +Δy*female +female  +Δy*crich +crich", data=data).fit()
print(test7.summary())


results = summary_col([test1,  test5],stars=True)
print(results)
print(results.as_latex())

pd.options.display.float_format = '{:,.4f}'.format
ftests= pd.DataFrame(np.array([ftestc2.fvalue[0,0], ftestc2.pvalue, ftestc3.fvalue[0,0], ftestc3.pvalue, ftestc4.fvalue[0,0], ftestc4.pvalue, ftestc5.fvalue[0,0], ftestc5.pvalue]))
print(ftests.to_latex())


# =============================================================================
#%% Townsend Test
# =============================================================================
data = cochrane

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

pd.options.display.float_format = '{:,.4f}'.format
results = pd.DataFrame(np.array([ test2.params, test2.bse, test3.params, test3.bse, test4.params, test4.bse, test5.params, test5.bse, test6.params, test6.bse, test7.params, test7.bse, test8.params, test8.bse, test9.params, test9.bse]))
print(results.to_latex())







