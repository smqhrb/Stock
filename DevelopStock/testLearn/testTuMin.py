import tushare as ts

df = ts.get_tick_data('000651',date='2018-12-08',src='tt')
print(df.head(10))