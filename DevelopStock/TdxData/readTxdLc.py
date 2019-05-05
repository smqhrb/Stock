'''
https://blog.csdn.net/liuyukuan/article/details/53560278
读取通达信的LC文件
可是通达信 的日线数据如下：
    日线数据在 通达信的安装目录： vipdoc\sh\lday  下面
（在调用这个py文件前， 先在通达信的 软件 菜单里面 ，把通达信的 历史日K线数据都下载到本地，
  一次即可下载整个市场所有股票品种的数据。。）
'''
from struct import *
import numpy as np
import pandas as pd
#!/usr/bin/python  
def exactStock(fileName, code):
    ofile = open(fileName,'rb')
    buf=ofile.read()
    ofile.close()
    num=len(buf)
    no=num/32
    b=0
    e=32
    items = list() 
    for i in range(int(no)):
        a=unpack('IIIIIfII',buf[b:e])
        year = int(a[0]/10000);
        m = int((a[0]%10000)/100);
        month = str(m);
        if m <10 :
            month = "0" + month;
        d = (a[0]%10000)%100;
        day=str(d);
        if d< 10 :
            day = "0" + str(d);
        dd = str(year)+"-"+month+"-"+day
        openPrice = a[1]/100.0
        high = a[2]/100.0
        low =  a[3]/100.0
        close = a[4]/100.0
        amount = a[5]/10.0
        vol = a[6]
        unused = a[7]
        if i == 0 :
            preClose = close
        ratio = round((close - preClose)/preClose*100, 2)
        preClose = close
        item=[code, dd, str(openPrice), str(high), str(low), str(close), str(ratio), str(amount), str(vol)]
        items.append(item)
        b=b+32
        e=e+32
        
    return items
# write = pd.ExcelWriter("LC(000001).xls")
# dl =exactStock('sz000001.day',"000001")
# df = pd.DataFrame(dl,['code','date','open','high','low','close','ratio','amount','volume'])#ratio涨跌幅,amount总额,volume(万手)
# df.to_excel(write,sheet_name='000001',index=True)
# write.save()
# exactStock('E:\\new_tdx\\vipdoc\\sh\\lday\\sh000001.day',"000001")
'''
通达信5分钟线*.lc5文件和*.lc1文件
    文件名即股票代码
    每32个字节为一个5分钟数据，每字段内低字节在前
    00 ~ 01 字节：日期，整型，设其值为num，则日期计算方法为：
                  year=floor(num/2048)+2004;
                  month=floor(mod(num,2048)/100);
                  day=mod(mod(num,2048),100);
    02 ~ 03 字节： 从0点开始至目前的分钟数，整型
    04 ~ 07 字节：开盘价，float型
    08 ~ 11 字节：最高价，float型
    12 ~ 15 字节：最低价，float型
    16 ~ 19 字节：收盘价，float型
    20 ~ 23 字节：成交额，float型
    24 ~ 27 字节：成交量（股），整型
    28 ~ 31 字节：（保留）
'''

ofile=open('sh000001.lc5','rb')
buf=ofile.read()
ofile.close()
 
num=len(buf)
no=num/32
b=0
e=32
dl = []
for i in range(int(no)):
   a=unpack('hhfffffii',buf[b:e])
   dl.append([str(int(a[0]/2048)+2004)+'-'+str(int(a[0]%2048/100)).zfill(2)+'-'+str((a[0]%2048)%100).zfill(2),str(int(a[1]/60)).zfill(2)+':'+str(a[1]%60).zfill(2)+':00',a[2],a[3],a[4],a[5],a[6],a[7]])
   b=b+32
   e=e+32
write = pd.ExcelWriter("LC5(000001).xls")
df = pd.DataFrame(dl, columns=['date','time','open','high','low','close','amount','volume'])
df.to_excel(write,sheet_name='000001',index=True)
write.save()