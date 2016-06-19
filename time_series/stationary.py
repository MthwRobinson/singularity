# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 14:45:15 2016

@author: Matt Robinson
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
import statsmodels.formula.api as sm
import seaborn
import quandl

interactive(True)

# Read the data and generate the appropriate columns
data = quandl.get('FRED/EXMXUS', collapse = 'monthly')
data.columns=['ex_rate']

# Exchange Rate Plot
data['ex_rate'].plot()
plt.title('US / Mexico Exchange Rate')
plt.xlabel('Date')
plt.ylabel('Exchange Rate (MXN/USD)')

# De-trended Exchange Rate Plot
data['day'] = [x for x in range(data.shape[0])]
fit = sm.ols(formula = 'ex_rate ~ day', data = data).fit()
trend = fit.predict(data)
data['trend'] = trend

plt.figure()
data['ex_rate'].plot()
data['trend'].plot()
plt.title('US / Mexico Exchange Rate')
plt.xlabel('Date')
plt.ylabel('Exchange Rate (MXN/USD)')

data['detrend_ex_rate'] = data['ex_rate'] - data['trend']
data['detrend_mean'] = data['detrend_ex_rate'].mean()

plt.figure()
data['detrend_ex_rate'].plot()
data['detrend_mean'].plot()
plt.title('US / Mexico Exchange Rate, Relative to Trend')
plt.xlabel('Date')
plt.ylabel('Relative Exchange Rate (MXN/USD)')

# Differenced Exchange Rate Plot
plt.figure()
data['ex_rate_diff'] = data['ex_rate'].diff(periods = 12)
data['diff_mean'] = data['ex_rate_diff'].mean()
data['ex_rate_diff'].plot()
data['diff_mean'].plot()
plt.title('US / Mexico Exchange Rate, 12-mo Diff')
plt.xlabel('Date')
plt.ylabel('Exchange Rate Change (MXN/USD)')

# Percent Change Exchange Rate
data['ex_rate_pct'] = (data['ex_rate_diff'] / 
                      data['ex_rate'].shift(periods = 12))
data['pct_diff_mean'] = data['ex_rate_pct'].mean()
plt.figure()
data['ex_rate_pct'].plot()
data['pct_diff_mean'].plot()
plt.title('US / Mexico Exchange Rate, 12-mo Pct Diff')
plt.xlabel('Date')
plt.ylabel('Exchange Rate Pct Change (MXN/USD)')

# ADF Tests
from statsmodels.tsa.stattools import adfuller
adfuller(data['ex_rate'], autolag = 'AIC')
adfuller(data['detrend_ex_rate'], autolag = 'AIC')
adfuller(data['ex_rate_pct'][12:], autolag = 'AIC')


