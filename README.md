# Heterogeneities in Risk and insurance Uganda: An Empirical Exploration

Here I upload the code (in Python) and  datasets used in my thesis, Heterogeneities in Risk and insurance Uganda: An Empirical Exploration. 
To run the code one must first download the data from the World Bank website (http://surveys.worldbank.org/lsms/integrated-surveys-agriculture-ISA/uganda). For the 2013-14 wave I use the files in csv. For the rest of waves I use the dta files. The data in the World Bank have free access but one must register first.

- In the files cons09-cons13, I create the consumption datasets per each wave.

- In the files agric09-10, I obtain the agricultural and livestock hh income datasets per wave.

- In the files labor_bs09-13, I obtain the labor and business hh income datasets per wave.

- In the files shocks09-13 I create the reported shocks datasets per wave.

- In the files sociodem09-13 I obtain the household sociodemographic characteristics datasets per wave.

- In file ownagrc I recover the household crops and livestock consumption from own sources to measure it as income that has been own conumed.

- With these datasets (which I already upload but one can also obtain running the previous files), in files data09-13 I construct the datasets per wave and I summaryze the main variables.

- In file regressions_panel I join the 4 waves datasets (and export the join data as dataUGA.dta), I create a nonbalanced panel, I run regressions of changes in log consumption-income on changes in reported shocks and I perform insurance tests under different shocks.

- In file regressions_panelbal, using the file dataUGA.dta, I construct the balanced panel, I obtain the means of reported shocks under household heterogeneities, I run consumption-income vs shocks correlations, I perform insurance tests for shocks heterogeneities and I perform insurance tests for household heterogeneities. The main tables and results from thesis are obtained using this file.
