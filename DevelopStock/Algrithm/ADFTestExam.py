import numpy as np 
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt
def hurst(ts):
    lags =range(2,120)

    tau =[np.sqrt(np.std(np.subtract(ts[lag:],ts[:-lag]))) for lag in lags]

    poly =np.polyfit(np.log(lags),np.log(tau),1)

    return poly[0]*2.0

import tushare as tsh
tsh.set_token('582c8c9ab1bd9e3e14d5d60527d63affb8c310fba3fb9f5d7853bf9c')
pro = tsh.pro_api()
stocklist = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data = pro.daily(ts_code='000651.SZ', start_date='20170701', end_date='20180718')
#Create a Gometric Brownian Motion,Mean-Reverting and Trending Series
gbm =np.log(np.cumsum(np.random.randn(100000))+1000)
gbm_result =ts.adfuller(gbm,1)
mr =np.log(np.random.randn(100000)+1000)
mr_result =ts.adfuller(mr,1)
tr =np.log(np.cumsum(np.random.randn(100000)+1)+1000)
tr_result =ts.adfuller(tr,1)

print("Hurst(GBM): %s"%hurst(gbm))#Hurst Exponent
print("ADF(GBM): ",gbm_result)
print("Hurst(MR): %s"%hurst(mr))
print("ADF(MR): ",mr_result)
print("Hurst(TR): %s"%hurst(tr))
print("ADF(TR): ",tr_result)
print("Hurst(GLDQ): %s"%hurst(data['close']))
Gldq_result =ts.adfuller(data['close'],1)
print("ADF(GLDQ): ",Gldq_result)

fig, ax = plt.subplots()
ax.scatter(np.arange(0,100000), gbm,s=30,c='red')
ax.scatter(np.arange(0,100000), mr,s=30,c='yellow')
ax.scatter(np.arange(0,100000), tr)
plt.show()