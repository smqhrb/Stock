        ####################
import pandas as pd
import lxml.html
from lxml import etree
import numpy as np
from pandas.io.html import read_html
from pandas.compat import StringIO
try:    
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
import time
import sys#地址模板
# FINIANCE_SINA_URL = 'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/%s/ctrl/%s/displaytype/4.phtml';
# FINIANCE_SINA_URL = 'http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/%s/ctrl/%s/displaytype/4.phtml'
# zcfzb id="BalanceSheetNewTable0" 
# FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/%s/ctrl/%s/displaytype/4.phtml'
# lrb id="ProfitStatementNewTable0"
# FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/%s/ctrl/%s/displaytype/4.phtml'
# llb id="ProfitStatementNewTable0"
FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/%s/ctrl/%s/displaytype/4.phtml'
def read_html_sina_finiance1(code):
    has_data = True
    #获取当前年份
    today = pd.to_datetime(time.strftime("%x"))
    year = today.year    #数据用pandas的dataframe储存
    dataArr = pd.DataFrame()   
    while has_data:        #新浪财经网页数据
        furl = FINIANCE_SINA_URL%(code,year)        #获取数据，标准处理方法
        request = Request(furl)
        text = urlopen(request, timeout=5).read()
        text = text.decode('gbk')
        html = lxml.html.parse(StringIO(text))        #分离目标数据
        # res = html.xpath("//table[@id=\"BalanceSheetNewTable0\"]")#ProfitStatementNewTable0
        res = html.xpath("//table[@id=\"ProfitStatementNewTable0\"]")
        sarr = [etree.tostring(node).decode('gbk') for node in res]        #存储文件
        sarr = ''.join(sarr)
        sarr = '<table>%s</table>'%sarr        #向前滚动一年
        year-=1
        #对最后一页进行判断，依据是数据是否有
        try:            #将数据读入到dataframe数据个数中；并进行连接；
            df = read_html(sarr)[0]
            df.columns=range(0,df.shape[1])
            df = df.set_index(df.columns[0])
            dataArr = [dataArr, df]
            # dataArr = pd.concat(dataArr, axis=1, join='inner')
            dataArr = pd.concat(dataArr, axis=1)
        except:
            if (year+1)==today.year:
                has_data=True
            else:
                has_data=False
    dataArr = dataArr.T
    dataArr =dataArr.dropna(axis=0,thresh=10) 
    dataArr =dataArr.dropna(axis=1,thresh=10) 
    try:
        dataArr = dataArr.set_index(dataArr.columns[0])
    except:
        dataArr=dataArr
    return dataArr
test = read_html_sina_finiance1('000001')
print(test)
###################