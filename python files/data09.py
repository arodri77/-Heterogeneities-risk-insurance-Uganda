# -*- coding: utf-8 -*-
"""
Created on Thu May 31 15:09:46 2018

@author: Albert
"""

import pandas as pd
import numpy as np
import os
import statsmodels.formula.api as sm
os.chdir('D:/Documents/Documents/IDEA/Research/python Albert')
from data_functions_albert import remove_outliers
from statsmodels.iolib.summary2 import summary_col
pd.options.display.float_format = '{:,.2f}'.format

dollars = 2586.89    #https://data.worldbank.org/indicator/PA.NUS.FCRF

#%%IMPORT DATA
os.chdir('D:/Documents/Documents/IDEA/Master tesi/Data & Code (Uganda)/data09')

basic = pd.read_stata('GSEC1.dta', convert_categoricals=False )
basic = basic[["HHID","urban","h1bq2c", "h1bq2b"]] 
basic.columns = ["hh","urban","year", "month"]
basic["hh"] = pd.to_numeric(basic["hh"])
basic["urban"] = pd.to_numeric(basic["urban"])
basic["year"] = pd.to_numeric(basic["year"])
basic["month"] = pd.to_numeric(basic["month"])


pd.value_counts(basic["year"])
pd.value_counts(basic["month"])
basic = basic.dropna(subset = ['year'])
basic["index"] = range(0,len(basic))
basic.set_index(basic["index"], inplace=True)

#Generate inflation variable (per individual)
inflation = pd.read_excel("inflation_UGA_09_14.xlsx")
lulu = []
for i in range(0,len(basic)):
    a = inflation.loc[basic.loc[i,"year"], basic.loc[i,"month"]]
    lulu.append(a)    
basic["inflation"] = pd.Series(lulu)

del inflation, i, lulu, a


#%% Consumption
cons = pd.read_csv("cons09.csv")
cons = cons[["hh","ctotal","ctotal_dur","ctotal_gift","cfood","cnodur"]]
# ctotal: food + nofood
# ctotal dur: food + nofood + durables
# ctotal gift: food + nofood of gifts
data = pd.merge(basic, cons, on="hh", how="left")




#%% +Wealth

"""
wealth = pd.read_stata('totalWEALTH.dta')
wealth = wealth[["HHID","totW"]]
wealth.rename(columns={'HHID':'hh'}, inplace=True)

data = pd.merge(data, wealth, on='hh', how='inner')
"""



#%% Income: 
#labor & business income: in US dollars
lab_inc = pd.read_csv('income_hhsec_2009.csv', header=0, na_values='nan')
lab_inc[["wage_total","bs_profit", "other_inc"]] = remove_outliers(lab_inc[["wage_total","bs_profit", "other_inc"]], lq=0.001, hq=0.999)
#Agricultural income: in UG Shillings
ag_inc = pd.read_csv('income_agsec_09.csv', header=0, na_values='nan')
#ag_inc["hh"] = ag_inc["hh"].astype(int)

inc = pd.merge(lab_inc, ag_inc, on="hh", how="outer")
inc = inc.drop(inc.columns[[0,5]], axis=1)

inc = remove_outliers(inc, lq=0.001, hq=0.999)

inc["inctotal"] = inc.loc[:,["wage_total","bs_profit","total_agrls"]].sum(axis=1)
inc["inctotal_trans"] = inc.loc[:,["wage_total","bs_profit","other","total_agrls"]].sum(axis=1)
inc["inctotal"] = inc["inctotal"].replace(0,np.nan)

suminc1 = inc.describe()


#Create income share

inc["w_share"] = inc[["wage_total"]].divide(inc.inctotal, axis=0)
inc["worker"] = (inc.w_share>=0.329)*1
inc["agr_share"] = inc[["total_agrls"]].divide(inc.inctotal, axis=0)
inc["farmer"] =  (inc.agr_share>=0.329)*1
inc["bus_share"] = inc[["bs_profit"]].divide(inc.inctotal, axis=0)
inc["businessman"] = (inc.bus_share>=0.329)*1

inc["ocupation"] = "nothing"
inc.loc[inc["worker"]==1, "ocupation"] = "worker"
inc.loc[inc["farmer"]==1, "ocupation"] = "farmer"
inc.loc[inc["businessman"]==1, "ocupation"] = "businessman"
inc["hh"] = pd.to_numeric(inc["hh"])

data = data.merge( inc, on='hh', how='left')



#%% Desinflate and convert to 2013 US$

# Substract for inflation and convert to US dollars
data[["ctotal","ctotal_dur","ctotal_gift","cfood","cnodur", "wage_total", "bs_profit", "profit_agr","profit_ls", "total_agrls", "inctotal", "inctotal_trans"]]= data[["ctotal","ctotal_dur","ctotal_gift","cfood","cnodur", "wage_total", "bs_profit", "profit_agr","profit_ls", "total_agrls", "inctotal", "inctotal_trans"]].div(data.inflation, axis=0)/dollars
#data[["ctotal","ctotal_dur","ctotal_gift","cfood","cnodur","totW", "profit_agr","profit_ls", "total_agrls"]] = data[["ctotal","ctotal_dur","ctotal_gift","cfood","cnodur","totW", "profit_agr","profit_ls", "total_agrls"]]/dollars
data.to_csv("cwi_ciextended09.csv")


#Summary
sum_c = data[["ctotal","ctotal_dur","ctotal_gift","cfood","cnodur"]].describe()
sum_inc = data[["wage_total","bs_profit","profit_agr","profit_ls","inctotal"]].describe()


#Store data
data_cwi = data[["hh", "ctotal", "inctotal"]]


# Trimming 0.1% and 0.1% each tail
"""
for serie in ["ctotal", "totW", "inctotal"]:
    data['percentiles'] = pd.qcut(data[serie], [0.001,0.999], labels = False)
    data.dropna(axis=0, subset=['percentiles'], inplace=True)
    data.drop('percentiles', axis=1, inplace=True)

"""
sumdata = data[["urban", "ctotal", "inctotal"]].describe()



data_cwi.to_csv('uga_cwi09.csv')  

#%% Seasonalize data
#data = data.merge(basic, on="id", how="right")
"""
data["season"] = ((data.month>=7) & (data.month<=12))*1 +1
data["season2"] =  ((data.month>=4) & (data.month<=6))*1 +1 +((data.month>=7) & (data.month<=9))*2 +((data.month>=10) & (data.month<=12))*3

## Regressions not signficant. Also then problems of negative numbers
#Deseasonalization regressions

for var in ["ctotal", "totW", "inctotal"]:
     ols1 = sm.ols(formula= var + " ~ season2", data=data).fit()
     data[var] = ols1.resid + np.min(ols1.resid)    

print(data[["ctotal","totW","inctotal"]])
  
sumcwi = data[["ctotal","totW","inctotal"]].describe() 
"""


#%% Import sociodemographic charact
socio10 = pd.read_csv("sociodem09.csv")
socio10.drop(socio10.columns[0], axis=1, inplace= True)
#socio11.drop_duplicates(subset=['hh'], keep=False)
data = pd.merge(data, socio10, on="hh", how="left")
data = data.drop_duplicates(subset=['hh'], keep=False)
repeated = pd.DataFrame(pd.value_counts(data.hh))
data["wave"] = "2009-2010"
data["age_sq"] = data.age**2

data.loc[data["region"]==0, "region"] = 1

# Import shocks
shocks = pd.read_csv('shocks09.csv')
data = pd.merge(data, shocks, on="hh", how="left")

#Obtain hh size
health = pd.read_stata('GSEC5.dta', convert_categoricals=False)
health = health[["HHID","PID","h5q4","h5q5","h5q10","h5q11","h5q12"]]
familysize =  pd.DataFrame(pd.value_counts(health.HHID))
familysize.columns= ["familysize"]
familysize["hh"] = pd.to_numeric(np.array(familysize.index.values))
data = data.merge(familysize, on="hh", how="left")

#Create dummies
dummies = pd.get_dummies(data['region'])
dummies.columns = ["region1","region2","region3","region4"]
dummies.drop(["region1"], axis=1, inplace=True)
# 1:central, 2:Eastern, 3:Northern, 4:Western
data = data.join(dummies)
dummies = pd.get_dummies(data['sex'])
dummies.columns = ["male","female"]
dummies.drop(["male"], axis=1, inplace=True)
data = data.join(dummies)



#Generate logs
for item in ['ctotal', 'ctotal_dur', 'ctotal_gift', 'cfood', 'cnodur', 'wage_total', 'bs_profit', 'profit_agr', 'profit_ls', 'total_agrls', 'inctotal','inctotal_trans']:
    data["ln"+item] = np.log(data[item]+np.abs(np.min(data[item])))
    #data["ln"+item] = np.log(data[item])
    
data.rename(columns={"lnctotal":"lnc"}, inplace=True)
data.rename(columns={"lninctotal":"lny"}, inplace=True)


#Obtain income and consumption residuals
#problems of multicollinearity at adding familysize
olsc = sm.ols(formula="lnc ~ age +age_sq +region2 +region3 +region4 +female   +bednet +illdays  ", data=data, ).fit()
print(olsc.summary())

olsi = sm.ols(formula="lny ~ age +age_sq +region2 +region3 +region4 +female   +bednet  +illdays", data=data,).fit()
print(olsi.summary())


data["u_c"] = olsc.resid
data["u_y"] = olsi.resid
data = data.drop_duplicates(subset=['hh'], keep=False)


sum_c = data[["ctotal","ctotal_dur","ctotal_gift","cfood","cnodur"]].describe()
sum_inc = data[["inctotal","wage_total","bs_profit","profit_agr","profit_ls"]].describe()
sum_lab = data[["farmer","worker","businessman","agr_share","w_share","bus_share"]].describe()
sum_sociodem = data[["age", "illdays", "urban","female","familysize","bednet", "writeread"]].describe()

print(sum_c.to_latex())
print(sum_inc.to_latex())
print(sum_lab.to_latex())
print(sum_sociodem.to_latex())

a = data[["ctotal","lnc", "inctotal","lny"]]



#data.to_csv("data09.csv", index=False)