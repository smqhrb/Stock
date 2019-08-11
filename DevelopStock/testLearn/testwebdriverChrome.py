#coding=utf-8
from selenium import webdriver
import time
import re
from pyquery import PyQuery as pq

def openurl(url,num):
    options=webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    browser=webdriver.Chrome(chrome_options=options)
    # browser= webdriver.Chrome()    #打开浏览器
    browser.get(url)                 #进入相关网站
    html=browser.page_source #获取网站源码
    data=str(pq(html)) #str() 函数将对象转化为适于人阅读的形式。

    dic={}
    re_rule=r'<div class="news-item-container">(.*?)<div data-v-00b2e9bc=""/>'
    datalist=re.findall(re_rule,data,re.S)
    for i in range(0,len(datalist)):
        rule1=r'<img src="/img/icon-lihao.png" data-v-6c26747a=""/>(.*?)<!----></span>'
        bullish = re.findall(rule1,datalist[i],re.S)
        if len(bullish)==0:
            rule1=r'<img src="/img/icon-likong.png" data-v-6c26747a=""/>(.*?)</span>'
            bullish = re.findall(rule1,datalist[i],re.S)

            rule2=r'<span class="stock-group-item-name" data-v-f97d9694="">(.*?)</span>'
            stock_name=re.findall(rule2,datalist[i], re.S)

            if len(stock_name) > 0 and len( bullish) > 0:
                for c in range(0,len(stock_name)):
                    dic[stock_name[c]]= bullish[0]
                    # print("正在爬取第",len(dic)+1,".....") 
                    print("正在爬取第",len(dic)+1,"....")

    c=len(datalist)
    if len(dic) < num:
        while(1):
            browser.find_element_by_class_name("home-news-footer").click()
            time.sleep(1)
            html=browser.page_source
            data=str(pq(html))
            datalist=re.findall(re_rule,data,re.S)
            for i in range(c,len(datalist)):
                rule3=r'<img data-v-6c26747a="" src="/img/icon-lihao.png"/>(.*?)<!----></span>'
                bullish = re.findall(rule3,datalist[i],re.S)
                if len(bullish)==0:
                    rule5=r'<img data-v-6c26747a="" src="/img/icon-likong.png"/>(.*?)</span>'
                    bullish = re.findall(rule5,datalist[i],re.S)
                rule4=r'<span data-v-f97d9694="" class="stock-group-item-name">(.*?)</span>'
                stock_name=re.findall(rule4,datalist[i], re.S)

                if len(stock_name) > 0 and len( bullish) > 0:
                    for c in range(0,len(stock_name)):
                        dic[stock_name[c]]= bullish[0]

            c=len(datalist)
            if len(dic) > num :
                browser.quit()
                print("爬取完毕！！")
                break

    else:
        browser.quit()
        print("爬取完毕！！")

        return dic

url='https://www.xuangubao.cn/'
dict=openurl(url,3)

print(dict)
#f=open("F:\\text.txt","a")
#for key,values in  dict.items():
#f.write((key+"\t"))
#print(key,values)
#f.close() 
