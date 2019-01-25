from pyecharts import Kline
import tushare as ts
import pandas as pd
ts.set_token('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
pro = ts.pro_api()
df1 = pro.daily(ts_code='000938.SZ', start_date='20150401', end_date='20180930')
df=df1.sort_values(by=['trade_date'])
df.reset_index(level=0,inplace=True)
df.drop(['index'],axis=1,inplace=True)
print(df)
df.to_csv("aaa.csv")
date=df.trade_date.tolist()
data=[]
for idx in df.index :
     row=[df.iloc[idx]['open'],df.iloc[idx]['close'],df.iloc[idx]['low'],df.iloc[idx]['high']]
     data.append(row)
kline = Kline("K 线图示例")
kline.add(
    "日K",
    date,
    data,
    mark_point=["max"],
    is_datazoom_show=True,
)
kline.render()
