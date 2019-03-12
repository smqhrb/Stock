import urllib.request
import re
import datetime
import time

def getHtml(url):
    while True:
        try:
            html = urllib.request.urlopen(url, timeout=5).read()
            break
        except:
            print("超时重试")
    html = html.decode('gbk')
    return html


def getTable(html):
    s = r'(?<=<table class="datatbl" id="datatbl">)([\s\S]*?)(?=</table>)'
    pat = re.compile(s)
    code = pat.findall(html)
    return code


def getTitle(tableString):
    s = r'(?<=<thead)>.*?([\s\S]*?)(?=</thead>)'
    pat = re.compile(s)
    code = pat.findall(tableString)
    s2 = r'(?<=<tr).*?>([\s\S]*?)(?=</tr>)'
    pat2 = re.compile(s2)
    code2 = pat2.findall(code[0])
    s3 = r'(?<=<t[h,d]).*?>([\s\S]*?)(?=</t[h,d]>)'
    pat3 = re.compile(s3)
    code3 = pat3.findall(code2[0])
    return code3


def getBody(tableString):
    s = r'(?<=<tbody)>.*?([\s\S]*?)(?=</tbody>)'
    pat = re.compile(s)
    code = pat.findall(tableString)
    s2 = r'(?<=<tr).*?>([\s\S]*?)(?=</tr>)'
    pat2 = re.compile(s2)
    code2 = pat2.findall(code[0])
    s3 = r'(?<=<t[h,d]).*?>(?!<)([\s\S]*?)(?=</)[^>]*>'
    pat3 = re.compile(s3)
    code3 = []
    for tr in code2:
        code3.append(pat3.findall(tr))
    return code3


# 股票代码
symbol = 'sz000001'
# 日期
dateObj = datetime.datetime(2018, 6, 1)
date = dateObj.strftime("%Y-%m-%d")

# 页码，因为不止1页，从第一页开始爬取
page = 1

while True:
    Url = 'http://market.finance.sina.com.cn/transHis.php?symbol=' + symbol + '&date=' + date + '&page=' + str(page)
    print(Url)
    
    html = getHtml(Url)
    table = getTable(html)
    if len(table) != 0:
        tbody = getBody(table[0])
        if len(tbody) == 0:
            print("结束")
            break
        if page == 1:
            thead = getTitle(table[0])
            print(thead)
        for tr in tbody:
            print(tr)
    else:
        print("当日无数据")
        break
    time.sleep(3)
    page += 1


 
