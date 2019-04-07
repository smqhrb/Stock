#
#Pytdx - Python tdx数据接口
#Pytdx 是一款纯Python语言开发的类似TradeX的行情数据接口的实现

#交易相关 (使用TdxTradeServer(wrapper of trade.dll))
#https://rainx.gitbooks.io/pytdx/content/pytdx_trade.html 

# 威廉指标
def williams(df, n, column='williams'):
# 100*(10日内最高价的最高值-收盘价)/(10日内最高价的最高值-10日内最低价的最低值)
for i in range(len(df)):
if i < n-1: continue
df.ix[i, column] = 100 * (df.high.values[i-n+1:i+1].max()-df.close.values[i])/(
df.high.values[i-n+1:i+1].max()-df.low.values[i-n+1:i+1].min())
return df

# 布林指标
def bollinger(df,n):
for i in range(len(df)):
if i < n-1: continue
df.ix[i, 'BOLL'] = df.close.values[i-n+1:i+1].mean()
df.ix[i, 'UB'] = df.ix[i, 'BOLL'] + 2 * numpy.std(df.close.values[i-n+1:i+1], ddof=1)
df.ix[i, 'LB'] = df.ix[i, 'BOLL'] - 2 * numpy.std(df.close.values[i-n+1:i+1], ddof=1)
return df

# 轨道线
def ene(df,n,m1,m2):
for i in range(len(df)):
if i < n-1: continue
df.ix[i, 'UPPER'] = (1+m1/100)*df.close.values[i-n+1:i+1].mean()
df.ix[i, 'LOWER'] = (1-m2/100)*df.close.values[i-n+1:i+1].mean()
df.ix[i, 'ENE'] = (df.ix[i, 'UPPER'] + df.ix[i, 'LOWER'])/2
return df

def kdj(df,n,m1,m2):
for i in range(len(df)):
if i < n-1: continue
df.ix[i, 'rsv'] = (df.close.values[i]-df.low.values[i-n+1:i+1].min()) / (df.high.values[i-n+1:i+1].max()-df.low.values[i-n+1:i+1].min())*100
df = getSMA(df,m1,1,'rsv','K')
df = getSMA(df,m2,1,'K','D')
for i in range(len(df)):
df.ix[i, 'J'] = 3*df.K.values[i] - 2*df.D.values[i]
return df