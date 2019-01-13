import numpy as np 
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt
def hurst(ts):
    lags =range(2,120)

    tau =[np.sqrt(np.std(np.subtract(ts[lag:],ts[:-lag]))) for lag in lags]

    poly =np.polyfit(np.log(lags),np.log(tau),1)

    return poly[0]*2.0

# x = np.array([1, 2, 3, 4, 5, 4, 3,2,1,0,-1,-2,-3,-2,-1,0,1,2,3,4])
# print(x[2:])
# print(x[:-2])
# result = ts.adfuller(x, 1)
# print( result)
# # (-2.6825663173365015, 0.077103947319183241, 0, 7, {'5%': -3.4775828571428571, '1%': -4.9386902332361515, '10%': -2.8438679591836733}, 15.971188911270618)
# print(hurst(x))
# ###random walk condition

import tushare as tsh
tsh.set_token('582c8c9ab1bd9e3e14d5d60527d63affb8c310fba3fb9f5d7853bf9c')
pro = tsh.pro_api()
stocklist = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# data = pro.daily(ts_code='000651.SZ', start_date='20170701', end_date='20180718')

# i=0
# j=0
# aa={'1':0}
# bb={'1':0}
# for tscode in stocklist['ts_code']:
#     data = pro.daily(ts_code=tscode, start_date='20170701', end_date='20180718')
#     # print(data)
#     # data =tsh.get_hist_data('000651',start='2015-01-05',end='2016-01-09')
#     if(len(data)<=200):
#         continue
#     result =ts.adfuller(data['close'],1)
#     hurst_ret =hurst(data['close'])
#     if(hurst_ret<0.3):
#         aa[tscode]=hurst_ret
#         i =i+1
#     if(hurst_ret>0.7):
#         bb[tscode]=hurst_ret  
        
#     print('tscode =',tscode+'|'+str(result))
#     print('tscode1 =',tscode+'|'+str(hurst_ret))

# print('aa=',aa)
# print('bb=',bb)


# kk =['000651.SZ','002280.SZ','601608.SH']
# for tscode in kk:
#     data = pro.daily(ts_code=tscode, start_date='20170701', end_date='20180718')
#     # print(data)
#     # data =tsh.get_hist_data('000651',start='2015-01-05',end='2016-01-09')
#     if(len(data)<=200):
#         continue
#     result =ts.adfuller(data['close'],1)
#     hurst_ret =hurst(data['close'])
#     # if(hurst_ret<0.3):
#     #     aa[tscode]=hurst_ret
#     #     i =i+1
#     # if(hurst_ret>0.7):
#     #     bb[tscode]=hurst_ret  
        
#     print('tscode =',tscode+'|'+str(result))
#     print('tscode1 =',tscode+'|'+str(hurst_ret))
# 
# data = pro.daily(ts_code='000651.SZ', start_date='20170701', end_date='20180718')
# data1 = pro.daily(ts_code='002280.SZ', start_date='20170701', end_date='20180718')
# npD = np.array(data['close'])
# npD1 =np.array(data1['close'])
# diff_data =npD[0:255] -npD1[0:255]

# print(diff_data.shape)
# print(diff_data)

# # from sklearn.impute import SimpleImputer
# # imp = SimpleImputer(missing_values=np.nan, strategy='mean')
# # diff_data.reshape(1,-1)
# # im1 = imp.fit(diff_data)
# # X2 =imp.transform(diff_data)
# # print(X2)
# result =ts.adfuller(diff_data,1)
# hurst_ret =hurst(diff_data)
# print(hurst_ret)
# print (result)

# data = pro.daily(ts_code='002617.SZ', start_date='20111201', end_date='20180718')
# result =ts.adfuller(data['close'],1)
# hurst_ret =hurst(data['close'])
# print(hurst_ret)
# print (result)

dataGL = pro.daily(ts_code='000651.SZ', start_date='20131001', end_date='20181218')
dataMD = pro.daily(ts_code='000333.SZ', start_date='20131001', end_date='20181218')
print(dataGL.head())
npDX = np.array(dataGL['close'])
npDX_tradeDate =np.array(dataGL['trade_date'])
# npDX =np.diff(npDX)
sizX =np.size(npDX)
npDY =np.array(dataMD['close'])
npDY_tradeDate =np.array(dataMD['trade_date'])
sizY =np.size(npDY)
if sizX>sizY:
    siz =sizY
else:
    siz =sizX

# npDY =np.diff(npDY)
print(npDX.shape)
print(npDY.shape)

##div trainData,TestData,ValidataData
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(npDX[0:siz].reshape(-1,1), npDY[0:siz].reshape(-1,1), random_state=1)

###start traina
from sklearn.linear_model import LinearRegression
linregModel = LinearRegression()
linregModel.fit(X_train, y_train)

       
err =npDY[0:siz]
result =ts.adfuller(err,1)
print(result)
hurst_ret =hurst(err)
print(hurst_ret)
##test on X_test
y_pred = linregModel.predict(X_test)
print('Variance score: %.2f' % linregModel.score(X_test, y_test))
print(linregModel.coef_)      #如果y=0.1x+0.3   则此行输出的结果为0.1
print(linregModel.intercept_)             #此行输出的结果为0.3


fig, ax = plt.subplots()
ax.scatter(npDX[0:siz], npDY[0:siz],s=30,c='red')
ax.plot(npDY_tradeDate[0:siz], npDY[0:siz],'g')
ax.plot(npDX_tradeDate[0:siz], npDX[0:siz],'y')
# ax.plot(np.arange(0,255,1), 1.117*npDX[0:255]+0.179,'k')
# ax.plot(np.arange(0,255,1), npDY[0:255] - (1.117*npDX[0:255]+0.179),'k')
plt.show()