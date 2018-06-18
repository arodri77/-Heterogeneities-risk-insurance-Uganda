# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 12:06:36 2018

@author: Albert
"""
import pandas as pd
import numpy as np
import os

os.chdir('D:/Documents/Documents/IDEA/Master tesi/Data & Code (Uganda)/data11')
pd.options.display.float_format = '{:,.2f}'.format

# =============================================================================
# Import data
# =============================================================================
shocks = pd.read_stata('GSEC16.dta', convert_categoricals=False)
shocks.columns = ["hh", "shock_code", "shock_d", "shock_month", "shock_long", "income1","income2","income3","income4","cope1","cope2","cope3", "result"]       
shocks['shock_d'] =(shocks['shock_d']==1)*1
shocks = shocks[["hh","shock_d","shock_code"]]


# =============================================================================
# Generate shocks labels
# =============================================================================

d={101:'Drought', 103:'Landslides-Erosion', 102:"floods", 104:"crop pest", 105: "livestock pest", 106:'↑P inp', 107:'↓P outp',  108:'↓wage', 109:'Unemp', 110:'Illness_inc',
         111:'Illness_oth', 112:'Death_inc', 113:'Death_oth', 114:'Theft', 115:'Theft agr', 116:'violence', 117:'Fire', 118:'Other'}

shocks["label"]=shocks.shock_code
shocks["label"] = shocks.label.apply(lambda x:d[x])

del d

# =============================================================================
# Generate shocks variables
# =============================================================================

shocks["climate"] = np.nan
shocks["prices"] = np.nan
shocks["job"] = np.nan
shocks["health"] = np.nan
shocks["aggregate"] = np.nan
shocks["idiosyn"] = np.nan
shocks["pests"] = np.nan


#Generate 
for i in range(0,len(shocks)):
    #climate shock
    shocks.iloc[i,4] = ((shocks.iloc[i,1] == 1) &((shocks.iloc[i,3] == 'Drought')  | (shocks.iloc[i,3] == 'Landslides-Erosion')   | (shocks.iloc[i,3] == 'floods')))*1
    #prices shock
    shocks.iloc[i,5] = ((shocks.iloc[i,1] == 1) &((shocks.iloc[i,3] == '↑P inp' )  | (shocks.iloc[i,3] == '↓P outp')))*1
    #income source shock
    shocks.iloc[i,6] = ((shocks.iloc[i,1] == 1) &((shocks.iloc[i,3] == '↓wage')| (shocks.iloc[i,3] == 'Unemp')))*1
    #health
    shocks.iloc[i,7] = ((shocks.iloc[i,1] == 1) &((shocks.iloc[i,3] == 'Illness_inc')  | (shocks.iloc[i,3] == 'Illness_oth')| (shocks.iloc[i,3] == 'Death_inc')| (shocks.iloc[i,3] == 'Death_oth')))*1
    #aggregate shock
    shocks.iloc[i,8] =  ((shocks.iloc[i,1] == 1) &((shocks.iloc[i,3] == 'Drought')  | (shocks.iloc[i,3] == 'Landslides-Erosion') | (shocks.iloc[i,3] == 'floods')  | (shocks.iloc[i,3] == '↑P inp')  | (shocks.iloc[i,3] == '↓P outp')))*1
    #idiosyncratic shocks
    shocks.iloc[i,9] =  ((shocks.iloc[i,1] == 1) &((shocks.iloc[i,3] == 'crop pest')  | (shocks.iloc[i,3] == 'Livestock pest')| (shocks.iloc[i,3] == '↓wage')| (shocks.iloc[i,3] == 'Unemp')
    | (shocks.iloc[i,3] == 'Illness_inc')  | (shocks.iloc[i,3] == 'Illness_oth')| (shocks.iloc[i,3] == 'Death_inc')| (shocks.iloc[i,3] == 'Death_oth') 
    | (shocks.iloc[i,3] == 'Theft') | (shocks.iloc[i,3] == 'Theft agr')| (shocks.iloc[i,3] ==  'violence') | (shocks.iloc[i,3] ==  'Fire')))*1
    #pests shocks
    shocks.iloc[i,10] = ((shocks.iloc[i,1] == 1) & ((shocks.iloc[i,3] == 'crop pest')  | (shocks.iloc[i,3] == 'Livestock pest')))*1




# %% Generate households shocks dataset 

shockshh = shocks.groupby(by="hh")[["shock_d","climate","prices","job","health","aggregate","idiosyn", "pests"]].sum()
shockshh.rename(columns={"shock_d":"shock"}, inplace=True)

# Generate shocks in dummies
for item in shockshh.columns.tolist():
    shockshh["d_"+str(item)] = (shockshh[str(item)]!=0)*1
    del item

#Describe Dataset
sumshocks= shockshh.describe()

sumshocks= shockshh.iloc[:,8:16].describe()
print(sumshocks.to_latex())


#Export dataset
shockshh["hh"] = shockshh.index.values
shockshh.to_csv("shocks11.csv", index=False)






